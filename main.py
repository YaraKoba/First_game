import pygame
import random


class MoveStars:
    def __init__(self, w, h, sur):
        self.stars = 10
        self.surface = sur
        self.x_speed = 0
        self.y_speed = 0
        self.all_speed = 10
        self.max_speed = 40
        self.WITHE = (255, 255, 255)
        self.W = w
        self.H = h
        self.star_pos = {num: [random.randint(1, w), random.randint(1, h)] for num in range(self.stars)}

    def physics_fly(self, mouse_y):
        x_plain = self.all_speed * 0.000009
        all_speed_top = (mouse_y - self.H / 2) / (self.H / 2) * 0.07
        all_speed_down = (((self.H / 2) - mouse_y) / (self.H / 2)) * 0.07
        y_speed_top = (mouse_y - self.H / 2) / (self.H / 2) * self.all_speed
        y_speed_down = -((((self.H / 2) - mouse_y) / (self.H / 2)) * self.all_speed)
        x_speed_top = (1 - y_speed_top) * self.all_speed
        x_speed_down = (1 - (((self.H / 2) - mouse_y) / (self.H / 2))) * self.all_speed
        d_turb = 0.01 * self.all_speed
        c_turb = 0.01 * self.all_speed
        print(f'speed = {int(self.all_speed)}, x = {int(self.x_speed)}, y = {int(self.y_speed)}')
        # print(d_turb, c_turb)

        if mouse_y > self.H / 2:  # Угол атаки +

            if self.y_speed < 0:  # Когда самолет литит вниз
                if 0 < self.all_speed < self.max_speed: self.all_speed += all_speed_top - x_plain

            if self.y_speed >= 0:  # Когда самолет летит вверх
                if self.all_speed > 3: self.all_speed -= all_speed_top + x_plain

            if y_speed_top > self.y_speed: self.y_speed += d_turb
            elif y_speed_top <= self.y_speed: self.y_speed -= d_turb

            if x_speed_top > self.x_speed: self.x_speed += d_turb
            elif x_speed_top <= self.x_speed: self.x_speed -= d_turb

        if mouse_y <= self.H / 2:  # Угол атаки -

            if self.y_speed <= 0:  # Когда самолет литит вниз
                if 0 < self.all_speed < self.max_speed: self.all_speed += all_speed_down - x_plain

            if self.y_speed > 0:  # Когда самолет летит вверх
                if self.all_speed > 3: self.all_speed -= all_speed_down + x_plain

            if y_speed_down < self.y_speed: self.y_speed -= c_turb
            elif y_speed_down > self.y_speed: self.y_speed += c_turb

            if x_speed_down > self.x_speed: self.x_speed += c_turb
            elif x_speed_down < self.x_speed: self.x_speed -= c_turb



    def draw_stars(self):
        for star in range(self.stars):
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



class Map:
    pass


class Planer:
    def __init__(self, width, height, sc):
        green = (210, 10, 120)
        self.planer_img = pygame.image.load('plain.png').convert_alpha()
        self.planer_img = pygame.transform.scale(self.planer_img, (200, 100))
        self.planer_img = pygame.transform.rotate(self.planer_img, -90)
        self.h = height
        self.sc = sc
        self.rect = self.planer_img.get_rect(center=(width / 2, height / 2))

    def show_planer(self, mouse_pos, mov: MoveStars):
        # print((mov.y_speed + 40) / (mov.all_speed + 40))
        corner = int((mov.y_speed + 40) / (mov.all_speed + 40) * 180)
        x = pygame.transform.rotate(self.planer_img, corner)
        self.sc.blit(x, self.rect)



class GameWindow:
    def __init__(self):
        pygame.init()
        self.W = 1500
        self.H = 600
        self.color_bg = (120, 100, 190)
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

            self.surface.fill(self.color_bg)
            self.stars.physics_fly(self.mouse_y)
            self.stars.draw_stars()
            self.planer.show_planer(self.mouse_y, self.stars)
            pygame.display.update()

            self.cloock.tick(60)


if __name__ == "__main__":
    x = GameWindow()
    x.main_lop()


