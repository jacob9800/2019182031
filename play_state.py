from pico2d import *
import game_framework
import pause_state
import game_over_state
import random
from GameMap import Map
import time
from zombieclass import NormalZombie
from bulletclass import Tennis
from bulletclass import Cola
from player_class import Player
import game_world


def handle_events():
    global running, tennis_mag, cola_mag, bulletmod
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            game_framework.push_state(pause_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            player.bulletmod = 0
            print("테니스공")
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            player.bulletmod = 1
            print("콜라")
        else:
            player.handle_event(event)


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
    gamemap = Map()
    player = Player()
    n_zombie = []
    tennisball = []
    cola = []
    game_world.add_object(gamemap, 0)
    game_world.add_object(player, 1)

    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie, tennisball, cola
    del player, gamemap, n_zombie, tennisball, cola

def update():
    for game_object in game_world.all_objects():
        game_object.update()


    for zombie in n_zombie:
        zombie.dirchange(player)
        zombie.collide(player)
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
    for game_object in game_world.all_objects():
        game_object.draw()
    delay(0.03)

def pause():
    pass

def resume():
    pass