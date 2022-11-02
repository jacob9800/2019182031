from pico2d import *
import game_framework
import pause_state
import random
import GameMap
import time
from playerclass import Player
from zombieclass import NormalZombie
from bulletclass import Tennis
from bulletclass import Cola
import game_over_state

def handle_events():
    global running, tennis_mag, cola_mag, bulletmod
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
            if event.key == SDLK_p:
                pass
                # game_framework.push_state(pause_state)
            if event.key == SDLK_c:
                player.shoot = 1
                if bulletmod == 0: # 탄환 종류 선택
                    if tennis_mag > 0:
                        tennisball.append(Tennis()) # 테니스공 1발 생성
                        tennis_mag -= 1 # 보유 탄환 1 감소
                    else :
                        print("총알 없음!")
                elif bulletmod == 1:
                    if cola_mag > 0 :
                        cola.append(Cola()) # 콜라 1발 생성
                        cola_mag -= 1
                    else :
                        print("총알 없음!")

            if event.key == SDLK_1:
                bulletmod = 0
                print("테니스공")

            if event.key == SDLK_2:
                bulletmod = 1
                print("콜라")

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.idle = 0
            if event.key == SDLK_LEFT:
                player.idle = 0
            if event.key == SDLK_SPACE:
                player.idle = 0
                player.attack = 0
            if event.key == SDLK_c:
                player.shoot = 0 # 플레이어 총탄 사격 취소


player = None
gamemap = None
running = True
n_zombie = None
tennisball = None
bulletmod = 0
cola = None
tennis_mag = 7
cola_mag = 7
killcount = 0

def enter():
    global player, gamemap, n_zombie, running, tennisball, cola
    gamemap = GameMap.Map()
    player = Player()
    n_zombie = [NormalZombie() for i in range (1)]
    tennisball = []
    cola = []

    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie, tennisball, cola
    del player, gamemap, n_zombie, tennisball, cola

def update():
    player.update()
    gamemap.stage()
    for ball in tennisball:
        ball.update()

    for bottle in cola:
        bottle.update()

    for zombie in n_zombie:
        player.melee_attack(zombie)
        zombie.update()
        zombie.dirchange(player)
        zombie.collide(player)
        zombie.deathcheck()
        for ball in tennisball:
            ball.collide(zombie)
        for bottle in cola:
            bottle.collide(zombie)
    if player.hp <= 0:
        game_framework.change_state(game_over_state)



def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    gamemap.draw()
    player.draw()
    for zombie in n_zombie:
        zombie.draw()
    for ball in tennisball:
        ball.draw()
    for bottle in cola:
        bottle.draw()
    delay(0.03)

def pause():
    pass

def resume():
    pass