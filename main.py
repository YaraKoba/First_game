import pygame
import random


class MoveStars:
    def __init__(self, w, h, sur):
        self.surface = sur
        self.x_speed = 4
        self.y_speed = 0
        self.WITHE = (255, 255, 255)
        self.BLUE = (120, 100, 190)
        self.W = w
        self.H = h
        self.star_pos = {num: [random.randint(1, w), random.randint(1, h)] for num in range(100)}

    def physics_fly(self, mouse_y):
        if mouse_y > self.H / 2:  # Самолетик летит ВВЕРХ!
            if self.y_speed < 10:
                self.y_speed += mouse_y / (self.H / 2) * 0.02
            if self.x_speed > 0:
                self.x_speed -= mouse_y / (self.H / 2) * 0.02
        if mouse_y < self.H / 2:  # Самолетик летит ВНИЗ!
            if self.y_speed > -10 and mouse_y != 0:
                self.y_speed -= (self.H / 2) / mouse_y * 0.02
            if self.x_speed < 30 and mouse_y != 0:
                self.x_speed += (self.H / 2) / mouse_y * 0.02


    def draw_stars(self):
        self.surface.fill(self.BLUE)
        for star in range(100):
            x = self.star_pos[star][0]
            y = self.star_pos[star][1]
            if x < 2:
                self.star_pos[star][0] = self.W
                self.star_pos[star][1] = random.randint(0, self.H)
            if y < 2:
                self.star_pos[star][0] = random.randint(0, self.W)
                self.star_pos[star][1] = self.H - 2
            if y > 598:
                self.star_pos[star][0] = random.randint(0, self.W)
                self.star_pos[star][1] = 2
            self.star_pos[star][0] -= self.x_speed
            self.star_pos[star][1] += self.y_speed
            pygame.draw.rect(self.surface, self.WITHE, (x, y, 3, 3))
        pygame.display.update()

class Map:
    pass


class Planer:
    def __init__(self, width, height):
        pass


class GameWindow:
    def __init__(self):
        pygame.init()
        self.W = 1500
        self.H = 600
        self.mouse_y = self.H / 2
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Fly GAME')
        self.stars = MoveStars(self.W, self.H, self.surface)
        self.cloock = pygame.time.Clock()

    def main_lop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_y = event.pos[1]
            self.stars.physics_fly(self.mouse_y)
            self.stars.draw_stars()
            self.cloock.tick(60)


if __name__ == "__main__":
    x = GameWindow()
    x.main_lop()


