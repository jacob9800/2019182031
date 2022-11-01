from pico2d import *
import game_framework
import pause_state
import random
import GameMap
from playerclass import Player
from zombieclass import NormalZombie
import game_over_state

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
            if event.key == SDLK_p:
                pass
                # game_framework.push_state(pause_state)
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
    n_zombie = [NormalZombie() for i in range (1)]

    running = True

# 게임 종료 함수
def exit():
    global player, gamemap, n_zombie
    del player, gamemap, n_zombie

def update():
    player.update()
    for zombie in n_zombie:
        player.melee_attack(zombie)
        zombie.update()
        zombie.dirchange(player)
        zombie.collide(player)
        zombie.deathcheck()
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

def pause():
    pass

def resume():
    pass