from pico2d import *
import play_state
from zombieclass import NormalZombie
import game_framework
import game_world

zombie = None
class Map:
    def __init__(self):
        self.background = load_image('Sprites/Map/background.png')
        self.tile = load_image('Sprites/Map/tile.png')
        self.background_city = load_image('Sprites/Map/city.png')
        self.mapsize = 1000
        self.counter = 0 # 좀비 수 제한 두기
        self.font = load_font('Fonts/154_Impact.ttf')
    def draw(self):
        self.background.draw(self.mapsize/2,300)
        self.background_city.draw(self.mapsize/2, 120)
        self.tile.draw(self.mapsize/2, 220)

        # UI 관련 코드들
        self.font.draw(10, 550, f'(HP: {play_state.player.hp})', (255, 255, 0))  # 플레이어 HP 출력
        self.font.draw(10, 500,  f'(KILLCOUNT: {play_state.killcount})', (255, 255, 0)) # 킬 점수 출력
        if play_state.player.bulletmod == 0:
            self.font.draw(10, 525, f'(TENNISBALL | {play_state.tennis_mag}/30)', (255, 255, 0))  # 테니스볼 개수 출력
        elif play_state.player.bulletmod == 1:
            self.font.draw(10, 525, f'(JOKA-COLA | {play_state.cola_mag}/7)', (255, 255, 0))  # 콜라병 개수 출력

    def update(self):
        pass






