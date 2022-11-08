from pico2d import *
import play_state
from zombieclass import NormalZombie
import game_framework

class Map:
    def __init__(self):
        self.background = load_image('Sprites/Map/background.png')
        self.tile = load_image('Sprites/Map/tile.png')
        self.background_city = load_image('Sprites/Map/city.png')
        self.mapsize = 1000
        self.counter = 0 # 좀비 수 제한 두기
    def draw(self):
        self.background.draw(self.mapsize/2,300)
        self.background_city.draw(self.mapsize/2, 120)
        self.tile.draw(self.mapsize/2, 220)

    def stage(self):
        if play_state.killcount <= 100:
            if len(play_state.n_zombie) < 5:
                play_state.n_zombie.append(NormalZombie())
                pass


