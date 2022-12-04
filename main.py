import pygame
import random


class MoveStars:
    def __init__(self, w, h, sur):
        self.stars = 10
        self.surface = sur
        self.x_speed = 0
        self.y_speed = 0
        self.all_speed = 50
        self.max_speed = 40
        self.WITHE = (255, 255, 255)
        self.W = w
        self.H = h
        self.star_pos = {num: [random.randint(1, w), random.randint(1, h)] for num in range(self.stars)}

    def physics_fly(self, mouse_y):
        x_plain = self.all_speed ** 2 * 0.00004
        all_speed_top = (mouse_y - self.H / 2) / (self.H / 2) * 0.07
        all_speed_down = (((self.H / 2) - mouse_y) / (self.H / 2)) * 0.07
        y_speed_top = (mouse_y - self.H / 2) / (self.H / 2) * self.all_speed
        y_speed_down = -((((self.H / 2) - mouse_y) / (self.H / 2)) * self.all_speed)
        x_speed = (1 - abs(self.y_speed) / self.all_speed) * self.all_speed
        d_turb = 0.01 * self.all_speed
        c_turb = 0.01 * self.all_speed
        # print(f'speed = {int(self.all_speed)}, x = {int(self.x_speed)}, y = {int(self.y_speed)}')
        # print(d_turb, c_turb)
        if self.all_speed <= 10:
            if self.y_speed < -10 and mouse_y < self.H / 2:
                self.all_speed = abs(self.y_speed)
            elif self.y_speed > -10:
                self.y_speed -= 0.07
                self.x_speed += 0.001
        else:
            if mouse_y > self.H / 2:  # Угол атаки +

                if self.y_speed < 0:  # Когда самолет литит вниз
                    if 0 < self.all_speed: self.all_speed += all_speed_top - x_plain

                if self.y_speed >= 0:  # Когда самолет летит вверх
                    self.all_speed -= all_speed_top + x_plain

                if y_speed_top > self.y_speed: self.y_speed += d_turb
                elif y_speed_top <= self.y_speed: self.y_speed -= d_turb
                self.x_speed = x_speed

            if mouse_y <= self.H / 2:  # Угол атаки -

                if self.y_speed <= 0:  # Когда самолет литит вниз
                    if 0 < self.all_speed: self.all_speed += all_speed_down - x_plain

                if self.y_speed > 0:  # Когда самолет летит вверх
                    if self.all_speed > 3: self.all_speed -= all_speed_down + x_plain

                if y_speed_down < self.y_speed: self.y_speed -= c_turb
                elif y_speed_down > self.y_speed: self.y_speed += c_turb
                self.x_speed = x_speed

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
    def __init__(self, w, h, sur):
        self.sc = sur
        self.w = w
        self.h = h
        self.gr_height = 0

    def draw_ground(self, h_planer, speed):
        if h_planer < 0:
            return True
        elif h_planer < 30:
            gr = pygame.Surface((self.w, (30 / 0.046) - (h_planer / 0.046)))
            line = pygame.Surface((50, (30 / 0.046) - (h_planer / 0.046) - 0.1))
            line.fill((255, 255, 255))
            rect_speed = gr.get_rect(centerx=self.w, centery=self.h)
            rect_gr = gr.get_rect(centerx=(self.w/2), centery=self.h)
            self.sc.blit(gr, rect_gr)
            self.sc.blit(line, rect_speed)


class Planer:
    def __init__(self, width, height, sc):
        green = (210, 10, 120)
        self.corner = 0
        self.n = 0
        self.width = width
        self.planer_img = pygame.image.load('plain.png').convert_alpha()
        self.planer_img = pygame.transform.scale(self.planer_img, (150, 75))
        self.planer_img = pygame.transform.rotate(self.planer_img, -90)
        self.height = height
        self.sc = sc
        self.rect = self.planer_img.get_rect(center=(width / 2, height / 2))

    def show_planer(self, mouse_pos, mov: MoveStars):
        if self.n % 2 == 0 and (mouse_pos / self.height * 180) - self.corner > 1:
            self.corner += mov.all_speed * 0.052
        elif self.n % 2 == 0 and self.corner - (mouse_pos / self.height * 180) > 1:
            self.corner -= mov.all_speed * 0.052
        x = pygame.transform.rotate(self.planer_img, self.corner)
        self.sc.blit(x, self.rect)


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
        pos_text = sc_text.get_rect(center=(self.w * 0.01, self.h * 0.03))
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
        self.top_height = 100
        self.color_bg = (120, 100, 190)
        self.mouse_y = self.H / 2
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Fly GAME')
        self.text = Text(self.W, self.H, self.top_height)
        self.planer = Planer(self.W, self.H, self.surface)
        self.stars = MoveStars(self.W, self.H, self.surface)
        self.ground = Map(self.W, self.H, self.surface)
        self.clock = pygame.time.Clock()

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
            if self.ground.draw_ground(self.text.top_height_plain, self.text.speed):
                print('game_over')
                self.surface.fill(self.color_bg)
                return False
            self.text.header_text(self.surface)
            self.text.fly_params(self.stars.y_speed, self.stars.x_speed, self.surface)
            pygame.display.update()

            self.clock.tick(60)


class Menu(GameWindow):
    def menu_lop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.surface.fill(self.color_bg)
                    pos = self.text.play_button(self.surface)
                    p_r = event.pos
                    if pos[0] - p_r[0] < pos[2] and 0 < p_r[1] - pos[1] < pos[3]:
                        self.text.top_height_plain = 100
                        if not self.main_lop():
                            self.text.game_over(self.surface)

            pygame.display.update()

            self.clock.tick(30)


if __name__ == "__main__":
    x = Menu()
    x.menu_lop()
