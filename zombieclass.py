from pico2d import *
import play_state
import time
import game_framework
import random
import game_world

ZPIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
ZRUN_SPEED_KMPH = 10.0  # Km / Hour
ZRUN_SPEED_MPM = (ZRUN_SPEED_KMPH * 1000.0 / 60.0)
ZRUN_SPEED_MPS = (ZRUN_SPEED_MPM / 60.0)
ZRUN_SPEED_PPS = (ZRUN_SPEED_MPS * ZPIXEL_PER_METER)

ZTIME_PER_ACTION = 0.9
ZACTION_PER_TIME = 1.0 / ZTIME_PER_ACTION
ZFRAMES_PER_ACTION = 8 # 공격, 출혈 시 프레임
ZFRAMES_PER_MOVING = 10 # 이동 시 프레임

class NormalZombie:
    right_image = None
    left_image = None
    rattack_image = None
    lattack_image = None
    rdead_image = None
    ldead_image = None
    blood_image = None
    def __init__(self):
        self.zx, self.zy = 0.0, 100.0  # 좀비 좌표
        self.atkchance = False
        self.dead_time = 0 # 사망 시간
        self.hit_time = 0 # 피격 시간
        self.current_time = 0 # 좀비 현재 시간
        self.counter = 0 # 프레임 카운터
        self.zmoving_frame = 0  # 이동, 사망 시 프레임
        self.zattack_frame = 0  # 공격 시 프레임
        self.blood_frame = 0 # 피격 시 프레임
        self.hit = 0 # 0 : 미피격 상태, 1 : 피격 상태
        self.zdir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 1  # 1: 이동, 0: 정지
        self.attack = 0  # 0: 무반응, 1: 공격
        self.dead = 0 # 0: 생존, 1: 사망, 2: 사망(삭제 필요)
        self.speed = random.randint(100,200) / 100
        self.hp = 50  # 좀비 HP, 0이 될 경우 사망 애니메이션 출력
        if NormalZombie.right_image == None:
            NormalZombie.right_image = load_image('Sprites/Zombie_male/zombie_right_walk.png')
        if NormalZombie.left_image == None:
            NormalZombie.left_image = load_image('Sprites/Zombie_male/zombie_left_walk.png')
        if NormalZombie.rattack_image == None:
            NormalZombie.rattack_image = load_image('Sprites/Zombie_male/zombie_right_attack.png')
        if NormalZombie.lattack_image == None:
            NormalZombie.lattack_image = load_image('Sprites/Zombie_male/zombie_left_attack.png')
        if NormalZombie.rdead_image == None:
            NormalZombie.rdead_image = load_image('Sprites/Zombie_male/zombie_right_dead.png')
        if NormalZombie.ldead_image == None:
            NormalZombie.ldead_image = load_image('Sprites/Zombie_male/zombie_left_dead.png')
        if NormalZombie.blood_image == None:
            NormalZombie.blood_image = load_image('Sprites/Effect/Bloodeffect.png')

    def update(self):
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.zmoving_frame = (self.zmoving_frame + ZFRAMES_PER_MOVING * ZACTION_PER_TIME * game_framework.frame_time) % 10
        self.zattack_frame = (self.zattack_frame + ZFRAMES_PER_ACTION * ZACTION_PER_TIME * game_framework.frame_time) % 8
        self.blood_frame = (self.blood_frame + ZFRAMES_PER_ACTION * ZACTION_PER_TIME * game_framework.frame_time) % 8
        self.current_time = get_time()

        if play_state.player.x > self.zx and self.dead == 0: # 플레이어 x좌표 기준 방향 전환
            self.zdir = 1
        elif play_state.player.x < self.zx and self.dead == 0:
            self.zdir = -1

        if self.zx > play_state.gamemap.mapsize:
            self.zx = play_state.gamemap.mapsize
            self.zdir = -1
        elif self.zx < 0:
            self.zx = 0
            self.zdir = 1
        else:
            if self.idle == 1:
                self.zx += self.zdir * ZRUN_SPEED_PPS * game_framework.frame_time * self.speed # 플레이어의 x 좌표에 따라서 이동 방향 변경
            else:
                self.zx = self.zx

        if self.hp <= 0 and self.dead == 0: # 좀비 사망 감지 코드
            self.dead = 1
            self.idle = 0
            self.dead_time = get_time()
            play_state.killcount += 1

        if (self.current_time - self.dead_time >= 0.5) and self.dead == 1: # 사망 1초 경과시 화면에서 제거 후 삭제 대기 상태로 전환
            self.dead = 2
            print(play_state.killcount, "번 좀비 사망")

        if self.dead == 2: # 삭제 대기 중인 객체 확인 후 제거
            play_state.n_zombie.remove(self)
            game_world.remove_object(self)
            play_state.zombie_num -= 1

        if int(self.zattack_frame) == 0:
            self.atkchance = True

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.zdir == 1:
            if self.dead == 0:
                if self.attack == 0:
                    self.right_image.clip_draw(int(self.zmoving_frame) * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.rattack_image.clip_draw(int(self.zattack_frame) * 124, 0, 124, 150, self.zx, self.zy)
            elif self.dead == 1:
                if self.counter <= 9:
                    self.rdead_image.clip_draw(int(self.zmoving_frame) * 179, 0, 179, 150, self.zx, self.zy-20)
                    self.counter += 1
                else :
                    self.rdead_image.clip_draw(9 * 179, 0, 179, 150, self.zx, self.zy-20)

        elif self.zdir == -1:
            if self.dead == 0:
                if self.attack == 0:
                    self.left_image.clip_draw(int(self.zmoving_frame) * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.lattack_image.clip_draw(int(self.zattack_frame) * 124, 0, 124, 150, self.zx, self.zy)
            elif self.dead == 1:
                if self.counter <= 9:
                    self.ldead_image.clip_draw(int(self.zmoving_frame) * 179, 0, 179, 150, self.zx, self.zy-20)
                    self.counter += 1
                else:
                    self.ldead_image.clip_draw(9 * 179, 0, 179, 150, self.zx, self.zy-20)

        if self.hit == 1 and self.dead == 0:
            if self.current_time - self.hit_time <= 0.3:
                self.blood_image.clip_draw(int(self.blood_frame) * 137, 0, 137, 68, self.zx, self.zy)  # 피격시 출혈 효과 발생
            else:
                self.hit = 0

    def collision(self, player):
        if self.dead == 0:  # 죽은 좀비들은 피격판정 x
            if player.attack == 0:  # IDLE 상태의 플레이어에게 접촉 시
                self.idle = 0
                self.attack = 1
                if player.invincible == 0 and self.atkchance == True:
                    self.atkchance = False
                    player.hp -= 10  # 플레이어에게 데미지
                    player.hit_time = get_time()  # 피격 시간 기록
                    player.invincible = 1

                print(player.hp)
            else:
                pass

            if player.attack == 1:  # MELEE 상태의 플레이어에게 접촉 시
                # print('hit!')
                if player.melee_frame == 2:
                    if self.zdir == -1 and self.dead == 0 and player.face_dir == 1:
                        self.hit_time = get_time()  # 피격 시간 기록
                        self.hp -= 15  # 자기 자신에게 데미지
                        self.hit = 1
                        self.zx += 50
                    elif self.zdir == 1 and self.dead == 0 and player.face_dir == -1:
                        self.hit_time = get_time()  # 피격 시간 기록
                        self.hp -= 15  # 자기 자신에게 데미지
                        self.hit = 1
                        self.zx -= 50
                    print(self.hp)
                else:
                    pass

    def get_bb(self):
        return self.zx - 60, self.zy - 80, self.zx + 60, self.zy + 80
    #
    # def handle_collision(self, other, group):
    #     if group == 'player:zombie':
    #         if self.dead == 0: # 죽은 좀비들은 피격판정 x
    #             if other.attack == 0: # IDLE 상태의 플레이어에게 접촉 시
    #                 self.idle = 0
    #                 self.attack = 1
    #                 if other.invincible == 0 and self.zattack_frame == 7:
    #                     other.hp -= 10  # 플레이어에게 데미지
    #                     other.hit_time = get_time()  # 피격 시간 기록
    #                     other.invincible = 1
    #
    #                 #print(other.hp)
    #             else:
    #                 pass
    #
    #             if other.attack == 1:  # MELEE 상태의 플레이어에게 접촉 시
    #                 #print('hit!')
    #                 if other.melee_frame == 2:
    #                     if self.zdir == -1 and self.dead == 0 and other.face_dir == 1:
    #                         self.hit_time = get_time()  # 피격 시간 기록
    #                         self.hp -= 15  # 자기 자신에게 데미지
    #                         self.hit = 1
    #                         self.zx += 50
    #                     elif self.zdir == 1 and self.dead == 0 and other.face_dir == -1:
    #                         self.hit_time = get_time()  # 피격 시간 기록
    #                         self.hp -= 15  # 자기 자신에게 데미지
    #                         self.hit = 1
    #                         self.zx -= 50
    #                     print(self.hp)
    #                 else:
    #                     pass
    # 미사용 코드



