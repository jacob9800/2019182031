from pico2d import *
import play_state
from bulletclass import Tennis
from bulletclass import Cola
import time
import game_over_state
import game_framework
import game_world

# 이벤트 정리
RD, LD, RU, LU, SHOOTIN, SHOOTOUT, MELEEOUT, MELEEIN = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT) : RD,
    (SDL_KEYDOWN, SDLK_LEFT) : LD,
    (SDL_KEYUP, SDLK_RIGHT) : RU,
    (SDL_KEYUP, SDLK_LEFT) : LU,
    (SDL_KEYDOWN, SDLK_c) : SHOOTIN,
    (SDL_KEYUP, SDLK_c) : SHOOTOUT,
    (SDL_KEYDOWN, SDLK_SPACE) : MELEEIN,
    (SDL_KEYUP, SDLK_SPACE) : MELEEOUT
}

# 스테이트를 구현(class를 이용해서)
class IDLE:
    @staticmethod
    def enter(self, event):
        print("ENTER IDLE")
        self.dir = 0
        pass

    @staticmethod
    def exit(self, event):
        print("EXIT IDLE")
        if event == MELEEIN:
            self.attack = 1
        elif event == MELEEOUT:
            self.attack = 0
        if event == SHOOTIN:
            self.shoot = 1
            self.shoot_bullet()
        elif event == SHOOTOUT:
            self.shoot = 0
        pass

    @staticmethod
    def do(self):
        self.idle_frame = (self.idle_frame + 1) % 10
        self.shoot_frame = (self.shoot_frame + 1) % 5
        self.current_time = get_time()

        self.x = clamp(0, self.x, 1000) # x 가동 범위 0 ~ 1000

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0



    @staticmethod
    def draw(self):
        if self.attack == 0: # 대기 중인 경우
            if self.shoot == 0:
                if self.face_dir == 1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.ridle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.ridle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.face_dir == -1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.lidle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.lidle_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
            elif self.shoot == 1:
                if self.face_dir == 1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.face_dir == -1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
        elif self.attack == 1: # 근접 공격 중인 경우
            if self.shoot == 0:  # 사격 이벤트 미발생 시 근접 공격 스프라이트 출력
                if self.face_dir == 1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.rmelee_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.rmelee_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.face_dir == -1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.lmelee_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.lmelee_image.clip_draw(self.idle_frame * 123, 0, 123, 160, self.x, self.y)
            elif self.shoot == 1:  # 사격 이벤트 발생 시 총기 발사 스프라이트 출력
                if self.face_dir == 1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.rshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                elif self.face_dir == -1:
                    if self.invincible == 1 and self.moving_frame % 4 == 1:
                        self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)
                    elif self.invincible == 0:
                        self.lshoot_image.clip_draw(self.shoot_frame * 123, 0, 123, 160, self.x, self.y)

class RUN:
    @staticmethod
    def enter(self, event):
        print("ENTER RUN")

        # 어떤 이벤트 때문에, RUN으로 들어왔는지 확인하고, 그 이벤트에 따라서 실제 방향을 결정
        if event == RD:
            self.dir = 1
        elif event == LD:
            self.dir = -1
        elif event == RU:
            self.dir = 0
        elif event == LU:
            self.dir = 0
        pass

    @staticmethod
    def exit(self, event):
        print("EXIT RUN")
        self.face_dir = self.dir
        pass

    @staticmethod
    def do(self):
        self.moving_frame = (self.moving_frame + 1) % 8
        self.shoot_frame = (self.shoot_frame + 1) % 5
        self.x += self.dir * 13
        self.current_time = get_time()

        self.x = clamp(0, self.x, 1000) # x 가동 범위 0 ~ 1000

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0

        if self.shoot == 1:
            if self.bulletmod == 0 and self.current_time - self.shoot_time <= 0.01:  # 탄환 종류 선택
                if play_state.tennis_mag > 0:
                    play_state.tennisball.append(Tennis())  # 테니스공 1발 생성
                    play_state.tennis_mag -= 1  # 보유 탄환 1 감소
                else:
                    print("총알 없음!")
            elif self.bulletmod == 1 and self.current_time - self.shoot_time <= 0.01:
                if play_state.cola_mag > 0:
                    play_state.cola.append(Cola())  # 콜라 1발 생성
                    play_state.cola_mag -= 1
                else:
                    print("총알 없음!")
        pass

    @staticmethod
    def draw(self):
        if self.dir == 1:
            if self.invincible == 1 and self.moving_frame % 4 == 1:
                self.right_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)
            elif self.invincible == 0:
                self.right_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)
        elif self.dir == -1:
            if self.invincible == 1 and self.moving_frame % 4 == 1:
                self.left_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)
            elif self.invincible == 0:
                self.left_image.clip_draw(self.moving_frame * 123, 0, 123, 160, self.x, self.y)


# 상태 변환

next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, MELEEIN: IDLE, SHOOTIN: IDLE, SHOOTOUT: IDLE},
    RUN: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, MELEEIN: IDLE, MELEEOUT: RUN, SHOOTIN: RUN, SHOOTOUT: RUN },
}

class Player:
    def __init__(self):
        self.x, self.y = 500, 90  # 플레이어 좌표
        self.shoot_time = 0.0
        self.hit_time = 0.0  # 피격당한 시간
        self.current_time = 0.0  # 실시간 캐릭터 시간
        self.bulletmod = 0 # 탄환 종류
        self.moving_frame = 0  # 이동 시 프레임
        self.idle_frame = 0  # 정지 시 프레임
        self.shoot_frame = 0  # 사격 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.face_dir = 1 # 1: 오른쪽, -1: 왼쪽
        self.idle = 0  # 0: 정지 상태, 1: 이동 상태
        self.attack = 0  # 0: 대기 상태, 1: 근공 실행
        self.shoot = 0  # 0: 무기 없음, 1: 발사
        self.hp = 100  # 플레이어 HP, 0이 될 경우 패배창 출력
        self.invincible = 0  # 0일시 피격 가능, 1일시 무적 상태
        self.right_image = load_image('Sprites/Player/player_right_run.png')
        self.left_image = load_image('Sprites/Player/player_left_run.png')
        self.ridle_image = load_image('Sprites/Player/player_right_idle.png')
        self.lidle_image = load_image('Sprites/Player/player_left_idle.png')
        self.rmelee_image = load_image('Sprites/Player/player_right_melee.png')
        self.lmelee_image = load_image('Sprites/Player/player_left_melee.png')
        self.lshoot_image = load_image('Sprites/Player/player_left_shoot.png')
        self.rshoot_image = load_image('Sprites/Player/player_right_shoot.png')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):  # 키 입력 이벤트
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

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

    def shoot_bullet(self):
        if self.bulletmod == 0 :  # 탄환 종류 선택

            if play_state.tennis_mag > 0:
                tennisball = Tennis(self.x, self.y, self.dir)
                game_world.add_object(tennisball, 2)
                play_state.tennis_mag -= 1  # 보유 탄환 1 감소
            else:
                print("총알 없음!")
        elif self.bulletmod == 1 :
            if play_state.cola_mag > 0:
                play_state.cola.append(Cola())  # 콜라 1발 생성
                play_state.cola_mag -= 1
            else:
                print("총알 없음!")
