from pico2d import *
import play_state
import time
import game_framework

class Tennis:
    tennis_image = None

    def __init__(self):

        if Tennis.tennis_image == None:
            Tennis.tennis_image = load_image('Sprites/Bullet/tennisball.png')

        self.speed = 30
        self.x = play_state.player.x
        self.y = play_state.player.y
        self.dir = play_state.player.dir

    def update(self):
        self.x += self.dir * self.speed

    def draw(self):
        self.tennis_image.draw(self.x, self.y)

    def collide(self, zombie):
        if zombie.zx - 20 <= self.x + 20 and self.x - 20 <= zombie.zx + 20 and play_state.tennis_mag >= 0 and zombie.dead == 0:
            play_state.tennisball.remove(self)
            del self
            zombie.hp -= 20
            zombie.hit = 1
            zombie.hit_time = get_time()
            print("좀비 체력 : ", zombie.hp)
            if zombie.zdir == 1:
                zombie.zx -= 20
            elif zombie.zdir == -1:
                zombie.zx += 20



class Cola:
    coke_l_image = None
    coke_r_image = None

    def __init__(self):
        if Cola.coke_l_image == None:
            Cola.coke_l_image = load_image('Sprites/Bullet/cola_left.png')
        if Cola.coke_r_image == None:
            Cola.coke_r_image = load_image('Sprites/Bullet/cola_right.png')

        self.speed = 15
        self.count = 0
        self.x = play_state.player.x
        self.y = play_state.player.y
        self.dir = play_state.player.dir

    def update(self):
        self.x += self.dir * self.speed

    def draw(self):
        if self.dir == -1:
            self.coke_l_image.draw(self.x, self.y)
        elif self.dir == 1:
            self.coke_r_image.draw(self.x, self.y)

    def collide(self, zombie):
        if zombie.zx - 40 <= self.x <= zombie.zx + 40 and play_state.cola_mag >= 0 and zombie.dead == 0:
            self.count += 1
            zombie.hp -= 5
            zombie.hit = 1
            zombie.hit_time = get_time()
            if zombie.speed > 1:
                zombie.speed /= 2
            print("좀비 체력 : ", zombie.hp)
            if zombie.zdir == 1:
                zombie.zx -= 5
            elif zombie.zdir == -1:
                zombie.zx += 5

            if self.count == 5:
                play_state.cola.remove(self)
                del self

