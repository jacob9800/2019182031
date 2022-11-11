from pico2d import *
import play_state
import bulletclass
import time
import game_over_state
import game_framework
import game_world



class Player:
    # Player Run Speed
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    # Player Action Speed
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    FRAMES_PER_IDLE = 10
    FRAMES_PER_SHOOT = 5
    def __init__(self):
        self.x, self.y = 500, 90 # 플레이어 좌표
        self.shoot_time = 0.0
        self.hit_time = 0.0 # 피격당한 시간
        self.current_time = 0.0 # 실시간 캐릭터 시간
        self.bulletmod = 0
        self.moving_frame = 0 # 이동 시 프레임
        self.idle_frame = 0 # 정지 시 프레임
        self.shoot_frame = 0 # 사격 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 0 # 0: 정지 상태, 1: 이동 상태
        self.attack = 0 # 0: 대기 상태, 1: 근공 실행
        self.shoot = 0 # 0: 무기 없음, 1: 발사
        self.hp = 100 # 플레이어 HP, 0이 될 경우 패배창 출력
        self.invincible = 0 # 0일시 피격 가능, 1일시 무적 상태
        self.right_image = load_image('Sprites/Player/player_right_run.png')
        self.left_image = load_image('Sprites/Player/player_left_run.png')
        self.ridle_image = load_image('Sprites/Player/player_right_idle.png')
        self.lidle_image = load_image('Sprites/Player/player_left_idle.png')
        self.rmelee_image = load_image('Sprites/Player/player_right_melee.png')
        self.lmelee_image = load_image('Sprites/Player/player_left_melee.png')
        self.lshoot_image = load_image('Sprites/Player/player_left_shoot.png')
        self.rshoot_image = load_image('Sprites/Player/player_right_shoot.png')

    def update(self):
        self.moving_frame = (self.moving_frame + 1) % 8
        self.idle_frame = (self.idle_frame + 1) % 10
        self.shoot_frame = (self.shoot_frame + 1) % 5
        self.current_time = get_time()

        if self.idle == 1:
            self.x += self.dir * 13

        self.x = clamp(0, self.x, 1000)

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0

        if self.shoot == 1:
            if self.bulletmod == 0 and self.current_time - self.shoot_time <= 0.01:  # 탄환 종류 선택
                if play_state.tennis_mag > 0:
                    play_state.tennisball.append(bulletclass.Tennis())  # 테니스공 1발 생성
                    play_state.tennis_mag -= 1  # 보유 탄환 1 감소
                else:
                    print("총알 없음!")
            elif self.bulletmod == 1 and self.current_time - self.shoot_time <= 0.01:
                if play_state.cola_mag > 0:
                    play_state.cola.append(bulletclass.Cola())  # 콜라 1발 생성
                    play_state.cola_mag -= 1
                else:
                    print("총알 없음!")


    def draw(self):
        if self.idle == 1:
            if self.dir == 1:
                if self.invincible == 1 and self.moving_frame % 4 == 1:
                    self.right_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.invincible == 0:
                    self.right_image.clip_draw(self.moving_frame*123, 0, 123, 160, self.x, self.y)
            elif self.dir == -1:
                if self.invincible == 1 and self.moving_frame % 4 == 1:
                    self.left_image.clip_draw(self.moving_frame*123, 0, 123, 160, self.x, self.y)
                elif self.invincible == 0:
                    self.left_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)
        elif self.idle == 0:
            if self.attack == 0:
                if self.shoot == 0:
                    if self.dir == 1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.ridle_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.ridle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.dir == -1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.lidle_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.lidle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.shoot == 1:
                    if self.dir == 1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.dir == -1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
            elif self.attack == 1:
                if self.shoot == 0: # 근접 공격 스프라이트 출력
                    if self.dir == 1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.rmelee_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.rmelee_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                    elif self.dir == -1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.lmelee_image.clip_draw(self.idle_frame*123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.lmelee_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.shoot == 1: # 총기 발사 스프라이트 출력
                    if self.dir == 1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.dir == -1:
                        if self.invincible == 1 and self.moving_frame % 4 == 1:
                            self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                        elif self.invincible == 0:
                            self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)


    def melee_attack(self, zombie):
        if (self.x + 100 >= zombie.zx >= self.x and self.dir == 1) or (self.dir == -1 and self.x - 100 <= zombie.zx <= self.x) and self.attack == 1:
            zombie.hit_time = get_time()
            if self.idle_frame == 2:
                 zombie.hp -= 15
                 if self.dir == 1 and zombie.dead == 0:
                     zombie.hit = 1
                     zombie.zx += 50
                 elif self.dir == -1 and zombie.dead == 0:
                     zombie.hit = 1
                     zombie.zx -= 50
                 print(zombie.hp)

