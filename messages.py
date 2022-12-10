import pygame
import components as com


class Text:
    def __init__(self, font, size, surface):
        self.surface = surface
        self.font = pygame.font.Font(font, size)

    def crate_text(self, text, position, color_font=com.WHITE, color_bg=None):
        sc_text = self.font.render(text, True, color_font, color_bg)
        pos_text = sc_text.get_rect(center=position)
        self.surface.blit(sc_text, pos_text)
        return pos_text


class FormText:
    def __init__(self, surface, h, w):
        self.text_40 = Text(com.PIXEL, 40, surface)
        self.text_25 = Text(com.PIXEL, 25, surface)
        self.text_18 = Text(com.PIXEL, 18, surface)
        self.H = h
        self.W = w
        self.name = ''

    def join_main(self, level, dist, speed, height, point):
        self.text_40.crate_text(f'Level {level}', (self.W * 0.5, self.H * 0.9))
        self.text_40.crate_text(f'speed {int(speed)}', (self.W * 0.14, self.H * 0.1))
        self.text_25.crate_text(f'height {int(height)}', (self.W * 0.1, self.H * 0.2))
        self.text_25.crate_text(f'dist {int(dist)}', (self.W * 0.1, self.H * 0.3))
        self.text_25.crate_text(f'point {point}', (self.W * 0.9, self.H * 0.9))

    def join_game_over(self, level, dist, point):
        self.text_40.crate_text(f'Game over!', (self.W * 0.5, self.H * 0.3))
        self.text_25.crate_text(f'Level {level}', (self.W * 0.2, self.H * 0.5))
        self.text_25.crate_text(f'Dist {int(dist)}', (self.W * 0.5, self.H * 0.5))
        self.text_25.crate_text(f'Points {point}', (self.W * 0.8, self.H * 0.5))
        self.text_40.crate_text(f'TOTAL {int(point * dist * 0.5)}', (self.W * 0.5, self.H * 0.7))
        self.text_18.crate_text(f'Jast one click to back to the menu', (self.W * 0.5, self.H * 0.8))

    def join_menu(self, status):
        start = self.text_40.crate_text(f'START!', (self.W * 0.5, self.H * 0.3))
        result = self.text_25.crate_text(f'Results', (self.W * 0.5, self.H * 0.7))
        self.text_18.crate_text(f'Player - {self.name}', (self.W * 0.5, self.H * 0.4))
        if status == 'easy':
            easy = self.text_25.crate_text(f'Easy', (self.W * 0.3, self.H * 0.5), color_bg=com.ORANGE)
            real = self.text_25.crate_text(f'Real', (self.W * 0.7, self.H * 0.5))
        else:
            easy = self.text_25.crate_text(f'Easy', (self.W * 0.3, self.H * 0.5))
            real = self.text_25.crate_text(f'Real', (self.W * 0.7, self.H * 0.5), color_bg=com.ORANGE)
        return start, easy, real, result

    def join_input(self, key=''):
        self.text_40.crate_text('Hello! Hho are you?', (self.W * 0.5, self.H * 0.3))
        self.text_25.crate_text('Jast LEFT-click to DELETE ALL', (self.W * 0.5, self.H * 0.6))
        self.text_25.crate_text('Jast RIGHT-click to CONTINUE', (self.W * 0.5, self.H * 0.7))
        if len(self.name) < 8:
            self.name += key
        if key == '_backspace_':
            self.name = ''
        self.text_25.crate_text(self.name, (self.W * 0.5, self.H * 0.5))

    def join_results(self, db_easy, db_real):
        self.text_25.crate_text('Easy', (self.W * 0.2, self.H * 0.1))
        self.text_25.crate_text('Real', (self.W * 0.8, self.H * 0.1))
        for index, player in enumerate(db_easy):
            self.text_18.crate_text(f'{index + 1}. {player[0]}  {player[1]},  {player[2]}',
                                    (self.W * 0.2, self.H * ((index + 2) / 12)))
        for index, player in enumerate(db_real):
            self.text_18.crate_text(f'{index + 1} {player[0]}  {player[1]},  {player[2]}',
                                    (self.W * 0.8, self.H * ((index + 2) / 12)))


