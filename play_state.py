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
from items_class import Itembox
import game_world
import schedule


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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_0):
            game_framework.change_state(game_over_state)
        else:
            player.handle_event(event)


player = None
gamemap = None
running = True
n_zombie = None
tennisball = None
cola = None
item = None
tennis_mag = 30
cola_mag = 7
bowling_mag = 5
killcount = 0

def enter():
    global player, gamemap, n_zombie, running, tennisball, cola, item
    gamemap = Map()
    player = Player()
    tennisball = []
    cola = []

    game_world.add_object(gamemap, 0)
    game_world.add_object(player, 1)

    game_world.add_collision_pairs(player, None, 'player:zombie')
    game_world.add_collision_pairs(player, None, 'player:item')
    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie, tennisball, cola, item
    del player, gamemap, n_zombie, tennisball, cola, item

def update():
    schedule.run_pending()
    for game_object in game_world.all_objects():
        game_object.update()

    if player.hp <= 0:
        game_framework.change_state(game_over_state)

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

    pass



def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()


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

def enemyspawn():
    for i in range(5):
        zombie = NormalZombie()
        game_world.add_object(zombie, 2)
        game_world.add_collision_pairs(None, game_world.objects[2][-1], 'player:zombie') # 플레이어 피격, 공격
        game_world.add_collision_pairs(None, game_world.objects[2][-1], 'zombie:tennis') # 테니스 피격
        game_world.add_collision_pairs(None, game_world.objects[2][-1], 'zombie:cola') # 콜라병 피격

def itemspawn():
    if len(game_world.objects[4]) <= 3: # 최대 4개까지 스폰
        box = Itembox()
        game_world.add_object(box, 4)
        game_world.add_collision_pairs(None, game_world.objects[4][-1], 'player:item')

zstart = schedule.every(7).seconds.do(enemyspawn) # 7초마다 5마리씩 스폰
istart = schedule.every(2).seconds.do(itemspawn) # 2초마다 보급 떨어짐, 최대 4개까지만 스폰




