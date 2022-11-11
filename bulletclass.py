from pico2d import *
import play_state
import time
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Tennis:
    tennis_image = None

    def __init__(self, x = 0, y = 0, dir = 1):

        if Tennis.tennis_image == None:
            Tennis.tennis_image = load_image('Sprites/Bullet/tennisball.png')

        self.speed = 50
        self.x = x
        self.y = y
        self.dir = dir
        self.count = 0

    def update(self):
        self.x += self.dir * RUN_SPEED_KMPH * game_framework.frame_time * self.speed

    def draw(self):
        self.tennis_image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        if self.x <= 20 or self.x >= 1000:
            game_world.remove_object(self) # 게임 월드에서 오브젝트 삭제
            play_state.tennisball.remove(self) # play_state 리스트에서 데이터 값 삭제
            del self # 메모리 삭제

    def collide(self, zombie):
        if zombie.zx - 20 <= self.x + 20 and self.x - 20 <= zombie.zx + 20 and play_state.tennis_mag >= 0 and zombie.dead == 0:
            game_world.remove_object(self)
            play_state.tennisball.remove(self)
            del self
            zombie.hp -= 20
            zombie.hit = 1
            zombie.hit_time = get_time()
            print("좀비 체력 : ", zombie.hp)
            if zombie.zdir == 1:
                zombie.zx -= 70
            elif zombie.zdir == -1:
                zombie.zx += 70

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    # def handle_collision(self, other, group):
    #     if group == 'zombie:tennis':
    #         game_world.remove_object(self)
    #         #play_state.tennisball.remove(self)
    #         if play_state.tennis_mag >= 0 and other.dead == 0:
    #             other.hp -= 20
    #             other.hit = 1
    #             other.hit_time = get_time()
    #             print("좀비 체력 : ", other.hp)
    #             if other.zdir == 1:
    #                 other.zx -= 100
    #             elif other.zdir == -1:
    #                 other.zx += 100








class Cola:
    coke_l_image = None
    coke_r_image = None

    def __init__(self, x = 500, y = 20, dir = 1):
        if Cola.coke_l_image == None:
            Cola.coke_l_image = load_image('Sprites/Bullet/cola_left.png')
        if Cola.coke_r_image == None:
            Cola.coke_r_image = load_image('Sprites/Bullet/cola_right.png')

        self.speed = 30
        self.count = 0
        self.x = x
        self.y = y
        self.dir = dir

    def update(self):
        self.x += self.dir * RUN_SPEED_KMPH * game_framework.frame_time * self.speed
        if self.x <= 0 or self.x >= 1000:
            game_world.remove_object(self)
            play_state.cola.remove(self)


    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.dir == -1:
            self.coke_l_image.draw(self.x, self.y)
        elif self.dir == 1:
            self.coke_r_image.draw(self.x, self.y)

    def collide(self, zombie):
        if zombie.zx - 40 <= self.x <= zombie.zx + 40 and play_state.cola_mag >= 0 and zombie.dead == 0:
            self.count += 1
            if self.count <= 1:
                zombie.hp -= 5
            zombie.hit = 1
            zombie.hit_time = get_time()
            if zombie.speed > 1:
                zombie.speed /= 2
            print("좀비 체력 : ", zombie.hp)
            if zombie.zdir == 1:
                zombie.zx -= 20
            elif zombie.zdir == -1:
                zombie.zx += 20

            if self.count == 5:
                if self.count == 5:  # 5명 이상의 좀비 타격 시
                    game_world.remove_object(self)
                    play_state.cola.remove(self)
                    del self
    def get_bb(self):
        return self.x - 20, self.y - 10, self.x + 45, self.y + 10

    # def handle_collision(self, other, group):
    #     if group == 'zombie:cola':
    #         if play_state.cola_mag >= 0 and other.dead == 0:
    #             self.count += 1
    #             other.hp -= 5
    #             other.hit = 1
    #             other.hit_time = get_time()
    #             if other.speed > 1:
    #                 other.speed /= 2
    #             print("좀비 체력 : ", other.hp)
    #             if other.zdir == 1:
    #                 other.zx -= 5
    #             elif other.zdir == -1:
    #                 other.zx += 5
    #
    #             if self.count == 5:  # 5명 이상의 좀비 타격 시
    #                 game_world.remove_object(self)
    #                 play_state.cola.remove(self)


