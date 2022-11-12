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
event_name = ['RD', 'LD', 'RU', 'LU', 'SHOOTIN', 'SHOOTOUT', 'MELEEOUT', 'MELEEIN']

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

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8 # 이동 시 프레임
FRAMES_PER_IDLE = 10 # 대기 시 프레임
FRAMES_PER_MELEE = 10
FRAMES_PER_SHOOT = 5 # 사격 시 프레임
FRAMES_PER_FIRE = 5

# 스테이트를 구현(class를 이용해서)
class IDLE:
    @staticmethod
    def enter(self, event):
        #print("ENTER IDLE")
        self.dir = 0
        pass


    @staticmethod
    def exit(self, event):
        #print("EXIT IDLE")
        pass

    @staticmethod
    def do(self):
        self.idle_frame = (self.idle_frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 10
        self.current_time = get_time()

        self.x = clamp(0, self.x, 1000) # x 가동 범위 0 ~ 1000

        if self.current_time - self.hit_time >= 2 and self.invincible == 1: # 피격시 2초가량 무적 제공
            self.invincible = 0

    @staticmethod
    def draw(self):
        if self.invincible == 0:
            if self.face_dir == 1:
                self.ridle_image.clip_draw(int(self.idle_frame) * 123, 0, 123, 160, self.x, self.y)
            elif self.face_dir == -1:
                self.lidle_image.clip_draw(int(self.idle_frame) * 123, 0, 123, 160, self.x, self.y)
        elif self.invincible == 1:
            if self.face_dir == 1:
                if int(self.idle_frame) % 2 != 0:
                    self.ridle_image.clip_draw(int(self.idle_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.idle_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)
            elif self.face_dir == -1:
                if int(self.idle_frame) % 2 != 0:
                    self.lidle_image.clip_draw(int(self.idle_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.idle_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)

class SHOOT:
    @staticmethod
    def enter(self, event):
        #print("ENTER SHOOT")
        self.fire = True
        self.dir = 0

    @staticmethod
    def exit(self, event):
        #print("EXIT SHOOT")
        self.shoot_bullet()
        pass

    @staticmethod
    def do(self):
        self.shoot_frame = (self.shoot_frame + FRAMES_PER_SHOOT * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.fire_frame = (self.shoot_frame + FRAMES_PER_FIRE * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.current_time - self.hit_time >= 2 and self.invincible == 1: # 피격시 2초가량 무적 제공
            self.invincible = 0

        if int(self.fire_frame) >= 3:
            self.fire = False

    @staticmethod
    def draw(self):

        if self.invincible == 0:
            if self.face_dir == 1:
                self.rshoot_image.clip_draw(int(self.shoot_frame) * 123, 0, 123, 160, self.x, self.y)
            elif self.face_dir == -1:
                self.lshoot_image.clip_draw(int(self.shoot_frame) * 123, 0, 123, 160, self.x, self.y)
        elif self.invincible == 1:
            if self.face_dir == 1:
                if int(self.shoot_frame) % 2 != 0:
                    self.rshoot_image.clip_draw(int(self.shoot_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.shoot_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)
            elif self.face_dir == -1:
                if int(self.shoot_frame) % 2 != 0:
                    self.lshoot_image.clip_draw(int(self.shoot_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.shoot_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)

        if self.fire == True:
            if self.face_dir == 1:
                self.rfire_image.clip_draw(int(self.fire_frame) * 40, 0, 40, 40, self.x + 70, self.y)
            elif self.face_dir == -1:
                self.lfire_image.clip_draw(int(self.fire_frame) * 40, 0, 40, 40, self.x - 70, self.y)

class RUN:
    @staticmethod
    def enter(self, event):
        #print("ENTER RUN")

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
        #print("EXIT RUN")
        if self.dir != 0:
            self.face_dir = self.dir
        if event == SHOOTIN:
            self.shoot_bullet()
        pass

    @staticmethod
    def do(self):
        self.moving_frame = (self.moving_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.current_time = get_time()
        self.x = clamp(0, self.x, 1000) # x 가동 범위 0 ~ 1000

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0

        pass

    @staticmethod
    def draw(self):
        if self.invincible == 0:
            if self.dir == 1:
                self.right_image.clip_draw(int(self.moving_frame) * 123, 0, 123, 160, self.x, self.y)
            elif self.dir == -1:
                self.left_image.clip_draw(int(self.moving_frame) * 123, 0, 123, 160, self.x, self.y)
        elif self.invincible == 1:
            if self.dir == 1:
                if int(self.moving_frame) % 2 != 0:
                    self.right_image.clip_draw(int(self.moving_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.moving_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)
            elif self.dir == -1:
                if int(self.moving_frame) % 2 != 0:
                    self.left_image.clip_draw(int(self.moving_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.moving_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)

class MELEE:
    @staticmethod
    def enter(self, event):
        #print("ENTER MELEE")
        self.attack = 1
        self.dir = 0

    @staticmethod
    def exit(self, event):
        #print("EXIT MELEE")
        self.attack = 0
        pass

    @staticmethod
    def do(self):
        #print(self.attack)
        self.melee_frame = (self.melee_frame + FRAMES_PER_MELEE * ACTION_PER_TIME * game_framework.frame_time) % 10

        if int(self.melee_frame) == 0:
            self.atkchance = True

        if self.current_time - self.hit_time >= 2 and self.invincible == 1:
            self.invincible = 0

    @staticmethod
    def draw(self):
        if self.invincible == 0:
            if self.face_dir == 1:
                self.rmelee_image.clip_draw(int(self.melee_frame) * 123, 0, 123, 160, self.x, self.y)
                if int(self.melee_frame) >= 4:
                    self.rslash_image.draw(self.x + 40, self.y)
            elif self.face_dir == -1:
                self.lmelee_image.clip_draw(int(self.melee_frame) * 123, 0, 123, 160, self.x, self.y)
                if int(self.melee_frame) >= 4:
                    self.lslash_image.draw(self.x - 40, self.y)
        elif self.invincible == 1:
            if self.face_dir == 1:
                if int(self.melee_frame) % 2 != 0:
                    self.rmelee_image.clip_draw(int(self.melee_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.melee_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)

                if int(self.melee_frame) >= 4:
                    self.rslash_image.draw(self.x + 40, self.y)
            elif self.face_dir == -1:
                if int(self.melee_frame) % 2 != 0:
                    self.lmelee_image.clip_draw(int(self.melee_frame) * 123, 0, 123, 160, self.x, self.y)
                elif int(self.melee_frame) % 2 == 0:
                    self.invis_image.draw(self.x, self.y)

                if int(self.melee_frame) >= 4:
                    self.lslash_image.draw(self.x - 40, self.y)


# 상태 변환

next_state = {
    IDLE: {RU: IDLE, LU: IDLE, RD: RUN, LD: RUN, MELEEIN: MELEE, MELEEOUT: IDLE, SHOOTIN: SHOOT, SHOOTOUT: IDLE},
    RUN: {RU: IDLE, LU: IDLE, LD: RUN, RD: RUN, MELEEIN: MELEE, MELEEOUT: RUN, SHOOTIN: RUN, SHOOTOUT: RUN},
    SHOOT: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, MELEEIN: MELEE, MELEEOUT: SHOOT, SHOOTIN: SHOOT, SHOOTOUT: IDLE},
    MELEE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, MELEEIN: MELEE, MELEEOUT: IDLE, SHOOTIN: SHOOT, SHOOTOUT: MELEE}
}

class Player:
    def __init__(self):
        self.x, self.y = 500, 90  # 플레이어 좌표
        self.atkchance = False
        self.shoot_time = 0.0
        self.hit_time = 0.0  # 피격당한 시간
        self.current_time = 0.0  # 실시간 캐릭터 시간
        self.bulletmod = 0 # 탄환 종류
        self.moving_frame = 0  # 이동 시 프레임
        self.idle_frame = 0  # 정지 시 프레임
        self.shoot_frame = 0  # 사격 시 프레임
        self.melee_frame = 0
        self.fire_frame = 0
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.face_dir = 1 # 1: 오른쪽, -1: 왼쪽
        self.idle = 0  # 0: 정지 상태, 1: 이동 상태
        self.attack = 0  # 0: 대기 상태, 1: 근공 실행
        self.shoot = 0  # 0: 무기 없음, 1: 발사
        self.hp = 100  # 플레이어 HP, 0이 될 경우 패배창 출력
        self.invincible = 0  # 0일시 피격 가능, 1일시 무적 상태
        self.gettime = 0 # 아이템 습득 시간
        self.boxtype = 0 # 습득 박스 종류
        self.fire = False # 사격 시 불꽃 출력
        self.right_image = load_image('Sprites/Player/player_right_run.png')
        self.left_image = load_image('Sprites/Player/player_left_run.png')
        self.ridle_image = load_image('Sprites/Player/player_right_idle.png')
        self.lidle_image = load_image('Sprites/Player/player_left_idle.png')
        self.rmelee_image = load_image('Sprites/Player/player_right_melee.png')
        self.lmelee_image = load_image('Sprites/Player/player_left_melee.png')
        self.lshoot_image = load_image('Sprites/Player/player_left_shoot.png')
        self.rshoot_image = load_image('Sprites/Player/player_right_shoot.png')
        self.rslash_image = load_image('Sprites/Effect/slasheffect_right.png')
        self.lslash_image = load_image('Sprites/Effect/slasheffect_left.png')
        self.invis_image = load_image('Sprites/Player/invisible.png')
        self.rfire_image = load_image('Sprites/Effect/fire_right.png')
        self.lfire_image = load_image('Sprites/Effect/fire_left.png')
        self.font = load_font('Fonts/154_Impact.ttf')
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
                print(f'ERROR: State {self.cur_state.__name__}, Event {event_name[event]}')
            self.cur_state.enter(self, event)


    def draw(self):
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())

        if self.current_time - self.gettime <= 1:
            if self.boxtype == 5:
                if self.hp < 50:
                    self.font.draw(play_state.player.x - 70, play_state.player.y + 120, f'(HP +50)', (0, 255, 0))
                else :
                    self.font.draw(play_state.player.x - 70, play_state.player.y + 120, f'(HP FULLY CHARGED!)', (0, 255, 0))
            elif self.boxtype == 0:
                self.font.draw(play_state.player.x - 70, play_state.player.y + 120, f'(TENNISBALL RECHARGED!)', (255, 255, 255))
            elif self.boxtype == 1:
                self.font.draw(play_state.player.x - 70, play_state.player.y + 120, f'(COLA RECHARGED!)', (255, 255, 255))




    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):  # 키 입력 이벤트
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def shoot_bullet(self):
        if self.bulletmod == 0 :  # 탄환 종류 선택
            if play_state.tennis_mag > 0:
                ball = Tennis(self.x + 50 * self.face_dir, self.y, self.face_dir)
                game_world.add_object(ball, 3) # 게임 월드에 탄환 추가
                game_world.add_collision_pairs(game_world.objects[3][-1], None, 'zombie:tennis')
                play_state.tennis_mag -= 1  # 보유 탄환 1 감소
            else:
                print("총알 없음!")
        elif self.bulletmod == 1 :
            if play_state.cola_mag > 0:
                bottle = Cola(self.x + 70 * self.face_dir, self.y, self.face_dir)
                game_world.add_object(bottle, 3) # 게임 월드에 탄환 추가
                game_world.add_collision_pairs(game_world.objects[3][-1], None, 'zombie:cola')
                play_state.cola_mag -= 1
            else:
                print("총알 없음!")

    def get_bb(self):
        if self.attack == 0:
            return self.x - 50, self.y - 80, self.x + 50, self.y + 80
        elif self.attack == 1:
            return self.x - 70, self.y - 80, self.x + 70, self.y + 80

    def handle_collision(self, other, group):
        pass