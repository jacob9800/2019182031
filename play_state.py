from pico2d import *
import game_framework
import pause_state
import game_over_state
import random
from GameMap import Map
import time
from zombieclass import NormalZombie
from bulletclass import Tennis, Cola
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
    game_world.add_collision_pairs(player, n_zombie, 'player:zombie')
    game_world.add_collision_pairs(n_zombie, tennisball, 'zombie:tennis')
    game_world.add_collision_pairs(n_zombie, cola, 'zombie:cola')

    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie, tennisball, cola
    del player, gamemap, n_zombie, tennisball, cola

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a,b):
            #print('COLLISION', group)
            a.handle_collision(b, group) # 어떤 놈(b)이 와서 나한테 꼬라박았나?
            b.handle_collision(a, group) # 어떤 놈(a)이 와서 나한테 꼬라박았나?
        else:
            for zombie in n_zombie:
                if zombie.dead == 0:
                    zombie.attack = 0
                    zombie.idle = 1

    for zombie in n_zombie:
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

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True