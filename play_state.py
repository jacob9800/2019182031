from pico2d import *
import game_framework

class Player:
    def __init__(self):
        self.x, self.y = 400, 90 # 플레이어 좌표
        self.moving_frame = 0 # 이동 시 프레임
        self.idle_frame = 0 # 정지 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 0 # 0: 정지 상태, 1: 이동 상태
        self.right_image = load_image('player_sheet.png')
        self.left_image = load_image('player_sheet_2.png')
        self.speed = 2 # 캐릭터 이동 속도

    def update(self):
        self.moving_frame = (self.moving_frame + 1) % 6
        self.idle_frame = (self.idle_frame + 1) % 5

        if self.idle == 1:
            self.x += self.dir * 1
        elif self.idle == 0:
            pass
        if self.x > 800:
            self.x = 800
        elif self.x < 0:
            self.x = 0

    def draw(self):
        if self.idle == 1:
            if self.dir == 1:
                self.right_image.clip_draw(self.moving_frame*167, 0, 167, 190, self.x, self.y)
            elif self.dir == -1:
                self.left_image.clip_draw(self.moving_frame*167, 0, 167, 190, self.x, self.y)
        elif self.idle == 0:
            if self.dir == 1:
                self.right_image.clip_draw(self.idle_frame*167, 546, 167, 190, self.x, self.y)
                delay(0.1)
            else:
                self.left_image.clip_draw((self.idle_frame+7)*167, 546, 167, 190, self.x, self.y)
                delay(0.1)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_RIGHT:
                player.idle = 1
                player.dir = 1
            if event.key == SDLK_LEFT:
                player.idle = 1
                player.dir = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.idle = 0
                player.dir = 1
            elif event.key == SDLK_LEFT:
                player.idle = 0
                player.dir = -1




player = None
running = True

def enter():
    global player, running
    player = Player()
    running = True

# 게임 종료 함수
def exit():
    global player
    del player

def update():
    player.update()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    player.draw()


def pause():
    pass

def resume():
    pass