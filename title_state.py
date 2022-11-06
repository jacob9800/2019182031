# 게임 시작 대기 상태
from pico2d import *
import game_framework
import play_state
import logo_state


image = None

def enter():
    global image
    image = load_image('Sprites/etc/startpage.png')
    pass

def exit():
    global image
    del image
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_state(play_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
    pass

def draw():
    clear_canvas()
    image.draw(500,300)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass






