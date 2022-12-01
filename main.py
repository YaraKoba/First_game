import pygame
import random


class MoveStars:
    def __init__(self, w, h, sur):
        self.surface = sur
        self.x_speed = 0
        self.y_speed = 0
        self.all_speed = 10
        self.max_speed = 40
        self.c_turb = 0.5
        self.WITHE = (255, 255, 255)
        self.BLUE = (120, 100, 190)
        self.speed_x_middle = 0
        self.tmp_mouse_pos = 0
        self.W = w
        self.H = h
        self.star_pos = {num: [random.randint(1, w), random.randint(1, h)] for num in range(100)}

    def physics_fly(self, mouse_y):
        # print(self.all_speed, str(self.x_speed)[:-12], str(self.y_speed)[:-12])
        if self.tmp_mouse_pos <= self.H / 2 < mouse_y:
            self.speed_x_middle = self.x_speed
        self.tmp_mouse_pos = mouse_y
        if mouse_y > self.H / 2:  # Угол атаки +
            if self.y_speed < 0:
                if 0 < self.all_speed < self.max_speed:
                    self.all_speed += ((mouse_y - self.H / 2) / (self.H / 2) * 0.09) - self.all_speed * 0.0009
                self.y_speed = (mouse_y - self.H / 2) / (self.H / 2) * self.all_speed
                self.x_speed = (1 - (mouse_y - self.H / 2) / (self.H / 2)) * self.all_speed
            if self.y_speed >= 0:
                if self.all_speed > 3:
                    self.all_speed -= ((mouse_y - self.H / 2) / (self.H / 2) * 0.12) + self.all_speed * 0.0009
                self.y_speed = (mouse_y - self.H / 2) / (self.H / 2) * self.all_speed
                self.x_speed = (1 - (mouse_y - self.H / 2) / (self.H / 2)) * self.all_speed
        if mouse_y <= self.H / 2:  # Угол атаки -
            if mouse_y == 0:
                mouse_y = 1
            if self.y_speed <= 0:
                if 0 < self.all_speed < self.max_speed:
                    self.all_speed += ((((self.H / 2) - mouse_y) / (self.H / 2)) * 0.09) - self.all_speed * 0.0009
                self.y_speed = -((((self.H / 2) - mouse_y) / (self.H / 2)) * self.all_speed)
                self.x_speed = (1 - (((self.H / 2) - mouse_y) / (self.H / 2))) * self.all_speed
            if self.y_speed > 0:
                if self.all_speed > 3:
                    self.all_speed -= ((((self.H / 2) - mouse_y) / (self.H / 2)) * 0.12) + self.all_speed * 0.0009
                self.y_speed = -((((self.H / 2) - mouse_y) / (self.H / 2)) * self.all_speed)
                self.x_speed = (1 - (((self.H / 2) - mouse_y) / (self.H / 2))) * self.all_speed

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
    def __init__(self, width, height, sc):
        green = (210, 10, 120)
        self.planer_img = pygame.image.load('plain.png')
        self.h = height
        self.planer.fill(green)
        self.sc = sc
        self.rect = self.planer_img.get_rect(center=(width / 2, height / 2))

    def show_planer(self, mouse_pos):
        # corner = self.h / mouse_pos * 180
        # new_img = pygame.transform.rotate(self.planer, corner)
        self.planer_img.set_colorkey((255, 255, 255))
        self.sc.blit(self.planer_img, self.rect)
        pygame.display.update()


class GameWindow:
    def __init__(self):
        pygame.init()
        self.W = 1500
        self.H = 600
        self.mouse_y = self.H / 2
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Fly GAME')
        self.planer = Planer(self.W, self.H, self.surface)
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
            self.planer.show_planer(self.mouse_y)

            self.cloock.tick(60)


if __name__ == "__main__":
    x = GameWindow()
    x.main_lop()


