from pico2d import *
import play_state
import time
import game_framework

class NormalZombie:
    def __init__(self):
        self.zx, self.zy = 1000, 100  # 좀비 좌표
        self.dead_time = 0 # 사망 시간
        self.current_time = 0 # 좀비 현재 시간
        self.counter = 0 # 프레임 카운터
        self.zmoving_frame = 0  # 이동, 사망 시 프레임
        self.zattack_frame = 0  # 공격 시 프레임
        self.zdir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 1  # 1: 이동, 0: 정지
        self.attack = 0  # 0: 무반응, 1: 공격
        self.dead = 0 # 0: 생존, 1: 사망
        self.hp = 50  # 좀비 HP, 0이 될 경우 사망 애니메이션 출력
        self.right_image = load_image('zombie_right_walk.png')
        self.left_image = load_image('zombie_left_walk.png')
        self.rattack_image = load_image('zombie_right_attack.png')
        self.lattack_image = load_image('zombie_left_attack.png')
        self.rdead_image = load_image('zombie_right_dead.png')
        self.ldead_image = load_image('zombie_left_dead.png')

    def update(self):
        self.zmoving_frame = (self.zmoving_frame + 1) % 10
        self.zattack_frame = (self.zattack_frame + 1) % 8
        self.current_time = get_time()

        if self.zx > play_state.gamemap.mapsize:
            self.zx = play_state.gamemap.mapsize
            self.zdir = -1
        elif self.zx < 0:
            self.zx = 0
            self.zdir = 1
        else:
            if self.idle == 1:
                self.zx += self.zdir * 5 # 플레이어의 x 좌표에 따라서 이동 방향 변경
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


    def dirchange(self,player):
        if player.x > self.zx:
            self.zdir = 1
        elif player.x < self.zx:
            self.zdir = -1

    def collide(self, player):
        if self.dead == 0:
            if player.x - 70 <= self.zx <= player.x + 70:
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
        else:
            pass
