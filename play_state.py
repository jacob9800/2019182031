from pico2d import *
import game_framework
import random
import GameMap

class Player:
    def __init__(self):
        self.x, self.y = 500, 90 # 플레이어 좌표
        self.moving_frame = 0 # 이동 시 프레임
        self.idle_frame = 0 # 정지 시 프레임
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 0 # 0: 정지 상태, 1: 이동 상태
        self.attack = 0 # 0: 대기 상태, 1: 근공 실행
        self.hp = 100 # 플레이어 HP, 0이 될 경우 패배창 출력
        self.right_image = load_image('player_right_run.png')
        self.left_image = load_image('player_left_run.png')
        self.ridle_image = load_image('player_right_idle.png')
        self.lidle_image = load_image('player_left_idle.png')
        self.rmelee_image = load_image('player_right_melee.png')
        self.lmelee_image = load_image('player_left_melee.png')

    def update(self):
        self.moving_frame = (self.moving_frame + 1) % 8
        self.idle_frame = (self.idle_frame + 1) % 10

        if self.idle == 1:
            self.x += self.dir * 10
        else:
            pass

        if self.x > gamemap.mapsize:
            self.x = gamemap.mapsize
        elif self.x < 0:
            self.x = 0

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

class NormalZombie:
    def __init__(self):
        self.zx, self.zy = 1000, 100  # 좀비 좌표
        self.zmoving_frame = 0  # 이동, 사망 시 프레임
        self.zattack_frame = 0  # 공격 시 프레임
        self.zdir = 1  # 1: 오른쪽, -1: 왼쪽
        self.idle = 1  # 1: 이동, 0: 사망(정지)
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

        print(self.zx)

        if self.zx > gamemap.mapsize:
            self.zx = gamemap.mapsize
            self.zdir = -1
        elif self.zx < 0:
            self.zx = 0
            self.zdir = 1
        else:
            if self.idle == 1:
                self.zx += self.zdir * 7 # 플레이어의 x 좌표에 따라서 이동 방향 변경
            else:
                pass

    def draw(self):
        if self.zdir == 1:
            if self.dead == 0:
                if self.attack == 0:
                    self.right_image.clip_draw(self.zmoving_frame * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.rattack_image.clip_draw(self.zattack_frame * 124, 0, 124, 150, self.zx, self.zy)
            else:
                self.rdead_image.clip_draw(self.zmoving_frame * 179, 0, 179, 150, self.zx, self.zy)
        elif self.zdir == -1:
            if self.dead == 0:
                if self.attack == 0:
                    self.left_image.clip_draw(self.zmoving_frame * 124, 0, 124, 150, self.zx, self.zy)
                else:
                    self.lattack_image.clip_draw(self.zattack_frame * 124, 0, 124, 150, self.zx, self.zy)
            else:
                self.ldead_image.clip_draw(self.zmoving_frame * 179, 0, 179, 150, self.zx, self.zy)

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
            if event.key == SDLK_SPACE:
                player.idle = 0
                player.attack = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.idle = 0
            if event.key == SDLK_LEFT:
                player.idle = 0
            if event.key == SDLK_SPACE:
                player.idle = 0
                player.attack = 0


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
    collide()
    deathcheck()

def dirchange():
    if player.x > n_zombie.zx:
        n_zombie.zdir = 1
    elif player.x < n_zombie.zx:
        n_zombie.zdir = -1

def collide():
    if n_zombie.dead == 0:
        if player.x+60 >= n_zombie.zx and player.x-60 <= n_zombie.zx:
            n_zombie.idle = 0
            n_zombie.attack = 1
            if n_zombie.zattack_frame == 7:
                player.hp -= 10

            print(player.hp)
        else:
            n_zombie.idle = 1
            n_zombie.attack = 0
            atkcheck = 0
            print(player.hp)
    else:
        pass

def deathcheck():
    if n_zombie.hp == 0:
        n_zombie.idle = 0
        n_zombie.dead = 1
    else:
        n_zombie.dead = 0

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    gamemap.draw()
    player.draw()
    n_zombie.draw()
    delay(0.03)

def pause():
    pass

def resume():
    pass