from pico2d import *
import play_state
import time
import game_over_state
import game_framework

class Player:
    def __init__(self):
        self.x, self.y = 500, 90 # 플레이어 좌표
        self.hit_time = 0 # 피격당한 시간
        self.current_time = 0 # 실시간 캐릭터 시간
        self.moving_frame = 0 # 이동 시 프레임
        self.idle_frame = 0 # 정지 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 0 # 0: 정지 상태, 1: 이동 상태
        self.attack = 0 # 0: 대기 상태, 1: 근공 실행
        self.shoot = 0 # 0: 무기 없음, 1: 발사
        self.hp = 100 # 플레이어 HP, 0이 될 경우 패배창 출력
        self.invincible = 0 # 0일시 피격 가능, 1일시 무적 상태
        self.right_image = load_image('player_right_run.png')
        self.left_image = load_image('player_left_run.png')
        self.ridle_image = load_image('player_right_idle.png')
        self.lidle_image = load_image('player_left_idle.png')
        self.rmelee_image = load_image('player_right_melee.png')
        self.lmelee_image = load_image('player_left_melee.png')

    def update(self):
        self.moving_frame = (self.moving_frame + 1) % 8
        self.idle_frame = (self.idle_frame + 1) % 10
        self.current_time = get_time()

        if self.idle == 1:
            self.x += self.dir * 13
        else:
            pass

        if self.x > play_state.gamemap.mapsize:
            self.x = play_state.gamemap.mapsize
        elif self.x < 0:
            self.x = 0

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0

    def draw(self):
        if self.idle == 1:
            if self.dir == 1:
                self.right_image.clip_draw(self.moving_frame*123, 0, 123, 160, self.x, self.y)
            elif self.dir == -1:
                self.left_image.clip_draw(self.moving_frame*123, 0, 123, 160, self.x, self.y)
        elif self.idle == 0:
            if self.attack == 0:
                if self.dir == 1:
                    self.ridle_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                else:
                    self.lidle_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
            elif self.attack == 1:
                if self.dir == 1:
                    self.rmelee_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                else:
                    self.lmelee_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)

    def melee_attack(self, zombie):
        if self.x <= zombie.zx + 100 and zombie.zx - 100 <= self.x and self.attack == 1:
            if self.idle_frame == 2:
                 zombie.hp -= 15
                 zombie.hit = 1
                 if self.dir == 1:
                     zombie.zx += 90
                 elif self.dir == -1:
                     zombie.zx -= 90
                 print(zombie.hp)

