from pico2d import *
import play_state
import time
import game_framework
import random

class NormalZombie:
    right_image = None
    left_image = None
    rattack_image = None
    lattack_image = None
    rdead_image = None
    ldead_image = None
    blood_image = None
    def __init__(self):
        self.zx, self.zy = 1000, 100  # 좀비 좌표
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
        self.dead = 0 # 0: 생존, 1: 사망
        self.speed = random.randint(300,500) / 100
        self.hp = 50  # 좀비 HP, 0이 될 경우 사망 애니메이션 출력
        if NormalZombie.right_image == None:
            NormalZombie.right_image = load_image('zombie_right_walk.png')
        if NormalZombie.left_image == None:
            NormalZombie.left_image = load_image('zombie_left_walk.png')
        if NormalZombie.rattack_image == None:
            NormalZombie.rattack_image = load_image('zombie_right_attack.png')
        if NormalZombie.lattack_image == None:
            NormalZombie.lattack_image = load_image('zombie_left_attack.png')
        if NormalZombie.rdead_image == None:
            NormalZombie.rdead_image = load_image('zombie_right_dead.png')
        if NormalZombie.ldead_image == None:
            NormalZombie.ldead_image = load_image('zombie_left_dead.png')
        if NormalZombie.blood_image == None:
            NormalZombie.blood_image = load_image('Bloodeffect.png')

    def update(self):
        self.zmoving_frame = (self.zmoving_frame + 1) % 10
        self.zattack_frame = (self.zattack_frame + 1) % 8
        self.blood_frame = (self.blood_frame + 1) % 8
        self.current_time = get_time()

        if self.zx > play_state.gamemap.mapsize:
            self.zx = play_state.gamemap.mapsize
            self.zdir = -1
        elif self.zx < 0:
            self.zx = 0
            self.zdir = 1
        else:
            if self.idle == 1:
                self.zx += self.zdir * self.speed # 플레이어의 x 좌표에 따라서 이동 방향 변경
            else:
                pass

    def draw(self):
        if self.zdir == 1:
            if self.dead == 0:
                if self.attack == 0:
                    self.right_image.clip_draw(self.zmoving_frame * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.rattack_image.clip_draw(self.zattack_frame * 124, 0, 124, 150, self.zx, self.zy)
            elif self.dead == 1:
                if self.counter <= 9:
                    self.rdead_image.clip_draw(self.zmoving_frame * 179, 0, 179, 150, self.zx, self.zy-20)
                    self.counter += 1
                else :
                    self.rdead_image.clip_draw(9 * 179, 0, 179, 150, self.zx, self.zy-20)
                if (self.current_time - self.dead_time >= 1):
                    play_state.n_zombie.pop(-1)
                    self.counter = 0
        elif self.zdir == -1:
            if self.dead == 0:
                if self.attack == 0:
                    self.left_image.clip_draw(self.zmoving_frame * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.lattack_image.clip_draw(self.zattack_frame * 124, 0, 124, 150, self.zx, self.zy)
            elif self.dead == 1:
                if self.counter <= 9:
                    self.ldead_image.clip_draw(self.zmoving_frame * 179, 0, 179, 150, self.zx, self.zy-20)
                    self.counter += 1
                else:
                    self.ldead_image.clip_draw(9 * 179, 0, 179, 150, self.zx, self.zy-20)
                if (self.current_time - self.dead_time >= 1):
                    play_state.n_zombie.pop(-1)
                    self.counter = 0

            if self.hit == 1 and self.dead == 0:
                if self.current_time - self.hit_time <= 0.3:
                    self.blood_image.clip_draw(self.blood_frame * 137,0,137,68,self.zx,self.zy) # 피격시 출혈 효과 발생
                else:
                    self.hit_time = 0
                    self.hit = 0


    def dirchange(self,player):
        if player.x > self.zx:
            self.zdir = 1
        elif player.x < self.zx:
            self.zdir = -1

    def collide(self, player):
        if self.dead == 0:
            if player.x - 50 <= self.zx <= player.x + 50:
                self.attack = 1
                self.idle = 0
                if player.invincible == 0 and self.zattack_frame == 7:
                    player.hp -= 10
                    player.hit_time = get_time()
                    player.invincible = 1

                print(player.hp)
            else:
                self.attack = 0
                self.idle = 1
        else:
            pass

    def deathcheck(self):
        if self.hp <= 0 and self.dead == 0:
            self.dead_time = get_time()
            self.idle = 0
            self.dead = 1
            play_state.killcount += 1
            print("킬 카운트 : ",play_state.killcount)
        else:
            pass