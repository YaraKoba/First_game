import pygame
import random
import math
from objects import PointCoins, Groups


class MoveStars:
    def __init__(self, w, h, sur):
        self.k = 0
        self.stars = 10
        self.surface = sur
        self.x_speed = 0
        self.y_speed = 0
        self.all_speed = 30
        self.max_speed = 40
        self.WITHE = (255, 255, 255)
        self.W = w
        self.H = h
        self.star_pos = {num: [random.randint(1, w), random.randint(1, h)] for num in range(self.stars)}

        self.pi = math.pi * 2

    def physics_fly(self, mouse_y):
        x_plain = self.all_speed ** 2 * 0.000009

        if self.all_speed < 6:
            if self.y_speed < -5:
                rot_speed = 0.01
                self.pi -= rot_speed * math.pi
                self.y_speed = -5
                self.x_speed = math.cos(self.pi)
                if int(math.degrees(self.pi)) < -40:
                    self.pi = math.radians(320)
                    self.all_speed = abs(self.y_speed) + 1
            else:
                self.y_speed -= 0.07

        else:
            if mouse_y > self.H // 2:  # Мышка в НИЖНЕЙ половине экрана
                rot_speed = self.all_speed * (mouse_y - self.H / 2) / (self.H / 2) * 0.0004
                self.pi += rot_speed * math.pi
                self.y_speed = self.all_speed * math.sin(self.pi)
                self.x_speed = self.all_speed * math.cos(self.pi)
            if mouse_y < self.H // 2:  # Мышка в ВЕРХНЕЙ половине экрана
                rot_speed = self.all_speed * (((self.H / 2) - mouse_y) / (self.H / 2)) * 0.0002
                self.pi -= rot_speed * math.pi
                self.y_speed = self.all_speed * math.sin(self.pi)
                self.x_speed = self.all_speed * math.cos(self.pi)
            if 0 <= math.degrees(self.pi) <= 180:
                degree = math.degrees(self.pi)
                corn = degree / 90 if degree <= 90 else (180 - degree) / 90
                self.all_speed -= corn * 0.1 + x_plain
            if 180 < math.degrees(self.pi) <= 360:
                degree = math.degrees(self.pi)
                corn = degree / 270 if degree <= 270 else (360 - degree) / 270
                self.all_speed += corn * 0.1 - x_plain
            if self.pi <= 0:
                self.pi = math.pi * 2
            elif self.pi >= math.pi * 2:
                self.pi = 0

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
            if y > self.H:
                self.star_pos[star][0] = random.randint(0, self.W)
                self.star_pos[star][1] = 2
            self.star_pos[star][0] -= self.x_speed
            self.star_pos[star][1] += self.y_speed
            pygame.draw.rect(self.surface, self.WITHE, (x, y, 3, 3))


class Map:
    def __init__(self, w, h, sur):
        self.sc = sur
        self.w = w
        self.h = h
        self.gr_height = 0
        self.num_line = 3
        coord_gen = (x_coord for x_coord in range(0, self.w, self.w // self.num_line))
        x_coord = iter(coord_gen)
        self.line = {num + 1: next(x_coord) for num in range(self.num_line)}

    def draw_ground(self, h_planer, speed):
        if h_planer < 0:
            return True
        elif h_planer < 30:
            gr = pygame.Surface((self.w, (30 / 0.046) - (h_planer / 0.046)))
            line = pygame.Surface((50, (30 / 0.046) - (h_planer / 0.046) - 0.1))
            line.fill((255, 120, 0))
            rect_speed = gr.get_rect(centerx=self.w/2, centery=self.h)
            rect_gr = gr.get_rect(centerx=(self.w/2), centery=self.h)
            self.sc.blit(gr, rect_gr)
            for line_num in self.line:
                if self.line[line_num] < 0:
                    self.line[line_num] = self.w
                self.line[line_num] -= speed
                new = rect_speed.move(self.line[line_num], 0)
                self.sc.blit(line, new)


class Planer:
    def __init__(self, width, height, sc):
        green = (210, 10, 120)
        self.corner = 0
        self.n = 0
        self.width = width
        self.planer_img = pygame.image.load('image/plain.png').convert_alpha()
        self.planer_img = pygame.transform.scale(self.planer_img, (150, 75))
        self.planer_img = pygame.transform.rotate(self.planer_img, 0)
        self.height = height
        self.sc = sc
        self.rect = self.planer_img.get_rect(center=(width / 2, height / 2))

    def show_planer(self, mouse_pos, mov: MoveStars):
        corner = 90
        if self.n % 2 == 0:
            corner = math.degrees(mov.pi)
        turn_planer = pygame.transform.rotate(self.planer_img, corner)
        self.sc.blit(turn_planer, self.rect)


class Text:
    def __init__(self, w, h, top_height):
        self.w = w
        self.h = h
        self.k = 0
        self.speed = 0
        self.top_height_plain = top_height
        self.black = (0, 0, 0)
        self.white = (255, 215, 226)
        self.font_header = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
        self.font_params = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20)

    def header_text(self, sc):
        sc_text = self.font_header.render('2D FLY', True, self.white)
        pos_text = sc_text.get_rect(center=(self.w * 0.1, self.h * 0.1))
        sc.blit(sc_text, pos_text)

    def play_button(self, sc):
        sc_text = self.font_header.render('Start', True, self.white)
        pos_text = sc_text.get_rect(center=(self.w // 2, self.h // 2))
        sc.blit(sc_text, pos_text)
        return pos_text

    def fly_params(self, y_speed, x_speed, sc):
        self.k += 1
        if self.k % 2 == 0:
            self.top_height_plain += (y_speed * 0.06)
            self.speed = int((x_speed ** 2 + y_speed ** 2) ** 0.5 * 6.6)
        sc_speed = self.font_params.render(f'speed - {self.speed}', True, self.white)
        sc_height = self.font_params.render(f'height - {int(self.top_height_plain)}', True, self.white)
        pos_speed = sc_speed.get_rect(center=(self.w * 0.1, self.h * 0.8))
        pos_height = sc_height.get_rect(center=(self.w * 0.1, self.h * 0.9))
        sc.blit(sc_speed, pos_speed)
        sc.blit(sc_height, pos_height)

    def game_over(self, sc):
        sc_game_over = self.font_header.render('Game Over', True, self.white)
        sc_down_mouse = self.font_params.render('jast one clik', True, self.white)
        pos_game_over = sc_game_over.get_rect(center=(self.w // 2, self.h // 2))
        pos_down_mouse = sc_down_mouse.get_rect(center=(self.w // 2, self.h * 0.7))
        sc.blit(sc_game_over, pos_game_over)
        sc.blit(sc_down_mouse, pos_down_mouse)


class GameWindow:
    def __init__(self):
        pygame.init()
        self.W = 1500
        self.H = 600
        self.top_height = 1000
        self.color_bg = (120, 100, 190)
        self.mouse_y = self.H / 2
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Fly GAME')
        pygame.time.set_timer(pygame.USEREVENT, random.randint(10, 2000))
        self.text = Text(self.W, self.H, self.top_height)
        self.planer = Planer(self.W, self.H, self.surface)
        self.stars = MoveStars(self.W, self.H, self.surface)
        self.ground = Map(self.W, self.H, self.surface)
        self.group = Groups(self.H, self.W)
        self.clock = pygame.time.Clock()

    def main_lop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_y = event.pos[1]
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, random.randint(10, 2000))
                    self.group.create_point()

            self.surface.fill(self.color_bg)
            self.stars.physics_fly(self.mouse_y)
            self.stars.draw_stars()
            self.group.point_group.update(self.surface, self.stars.x_speed, self.stars.y_speed, H=self.H, W=self.W)
            # self.coins.update(self.surface, self.stars.x_speed, self.stars.y_speed, H=self.H, W=self.W)
            self.planer.show_planer(self.mouse_y, self.stars)
            if self.ground.draw_ground(self.text.top_height_plain, self.stars.x_speed):
                print('game_over')
                self.surface.fill(self.color_bg)
                return False
            self.text.header_text(self.surface)
            self.text.fly_params(self.stars.y_speed, self.stars.x_speed, self.surface)
            pygame.display.update()

            self.clock.tick(60)


class Menu(GameWindow):
    def menu_lop(self):
        self.surface.fill(self.color_bg)
        self.text.play_button(self.surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.surface.fill(self.color_bg)
                    pos = self.text.play_button(self.surface)
                    p_r = event.pos
                    if pos[0] - p_r[0] < pos[2] and 0 < p_r[1] - pos[1] < pos[3]:
                        self.text.top_height_plain = 1000
                        if not self.main_lop():
                            self.text.game_over(self.surface)

            pygame.display.update()

            self.clock.tick(30)


if __name__ == "__main__":
    x = Menu()
    x.menu_lop()
