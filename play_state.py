from pico2d import *
import game_framework
import pause_state
import game_over_state
import random
import GameMap
import time
from playerclass import Player
from zombieclass import NormalZombie
from bulletclass import Tennis
from bulletclass import Cola
import game_world


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
                game_framework.push_state(pause_state)
            if event.key == SDLK_c:
                player.shoot = 1
                player.shoot_time = get_time()

            if event.key == SDLK_1:
                player.bulletmod = 0
                print("테니스공")

            if event.key == SDLK_2:
                player.bulletmod = 1
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
                player.shoot = 0
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        #     game_framework.quit()
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
        #     game_framework.push_state(pause_state)
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
        #     player.bulletmod = 0
        #     print("테니스공")
        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
        #     player.bulletmod = 1
        #     print("콜라")
        # else:
        #     player.handle_event(event)


player = None
gamemap = None
running = True
n_zombie = None
tennisball = None
cola = None
tennis_mag = 30
cola_mag = 7
killcount = 0

def enter():
    global player, gamemap, n_zombie, running, tennisball, cola
    gamemap = GameMap.Map()
    player = Player()
    n_zombie = []

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
        zombie.update()
        zombie.dirchange(player)
        zombie.collide(player)
        player.melee_attack(zombie)
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
    delay(0.03)
    for ball in tennisball:
        ball.draw()
    for bottle in cola:
        bottle.draw()

def pause():
    pass

def resume():
    pass