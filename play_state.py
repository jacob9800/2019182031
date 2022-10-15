from pico2d import *
import game_framework
import random
import GameMap

class Player:
    def __init__(self):
        self.x, self.y = 800, 90 # 플레이어 좌표
        self.moving_frame = 0 # 이동 시 프레임
        self.idle_frame = 0 # 정지 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 0 # 0: 정지 상태, 1: 이동 상태
        self.hp = 100 # 플레이어 HP, 0이 될 경우 패배창 출력
        self.right_image = load_image('player_sheet.png')
        self.left_image = load_image('player_sheet_2.png')

    def update(self):
        self.moving_frame = (self.moving_frame + 1) % 6
        self.idle_frame = (self.idle_frame + 1) % 1

        if self.idle == 1:
            self.x += self.dir

        if self.x > gamemap.mapsize:
            self.x = gamemap.mapsize
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
                self.right_image.clip_draw(self.idle_frame*167, 546, 166, 190, self.x, self.y)
            else:
                self.left_image.clip_draw((self.idle_frame+7)*167, 546, 166, 190, self.x, self.y)

class NormalZombie:
    def __init__(self):
        self.zx, self.zy = 0, 40  # 좀비 좌표
        self.zmoving_frame = 0  # 이동 시 프레임
        self.zdir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 2
        self.hp = 50  # 좀비 HP, 0이 될 경우 사망 애니메이션 출력
        self.right_image = load_image('zombie_sheet.png')
        self.left_image = load_image('zombie_sheet_2.png')

    def update(self):
        self.zmoving_frame = (self.zmoving_frame + 1) % 6

        print(self.zx)

        if self.zx > gamemap.mapsize:
            self.zx = gamemap.mapsize
            self.zdir = -1
        elif self.zx < 0:
            self.zx = 0
            self.zdir = 1
        else:

                self.zx += self.zdir / 2  # 플레이어의 x 좌표에 따라서 이동 방향 변경

    def draw(self):
        if self.zdir == 1:
            self.right_image.clip_draw(self.zmoving_frame * 177, 0, 167, 220, self.zx, self.zy)
        elif self.zdir == -1:
            self.left_image.clip_draw((self.zmoving_frame+6) * 190, 0, 167, 220, self.zx, self.zy)

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
            elif event.key == SDLK_LEFT:
                player.idle = 0


player = None
gamemap = None
running = True
n_zombie = None

def enter():
    global player, gamemap, n_zombie, running
    gamemap = GameMap.Map()
    player = Player()
    n_zombie = NormalZombie()

    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie
    del player, gamemap, n_zombie

def update():
    player.update()
    n_zombie.update()
    dirchange()

def dirchange():
    if player.x > n_zombie.zx:
        n_zombie.zdir = 1
        print("Yes")
    elif player.x < n_zombie.zx:
        n_zombie.zdir = -1
        print("no")


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    gamemap.draw()
    player.draw()
    n_zombie.draw()

def pause():
    pass

def resume():
    pass