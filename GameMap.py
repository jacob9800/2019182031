from pico2d import *
import game_framework

class Map:
    def __init__(self):
        self.background = load_image('background.png')
        self.tile = load_image('tile.png')
        self.background_city = load_image('city.png')
        self.mapsize = 1000
    def draw(self):
        self.background.draw(self.mapsize/2,300)
        self.background_city.draw(self.mapsize/2, 120)
        self.tile.draw(self.mapsize/2, 220)
