#!/usr/bin/env python3
import pygame
import random
import math
import score
import components as com
from objects import Groups
from datetime import date
from messages import FormText
from database import DataBaseClient, PlayerRecord


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

    def change_color(self, color, dist):
        r, g, b = color[0], color[1], color[2]
        speed = 0.04
        if int(dist//1000) + 1 <= 2:
            if r < 240: r += speed
            if g < 140: g += speed
            if b > 55: b -= speed * 0.8
        elif int(dist//1000) + 1 < 5:
            if r > 0: r -= speed * 2
            if g > 0: g -= speed * 2
            if b > 65: b -= speed
        elif int(dist//1000) + 1 < 7:
            if r < 230: r += speed
            if g < 130: g += speed * 0.9
            if b > 55: b -= speed
        elif int(dist//1000) + 1 < 10:
            if r > 77: r -= speed
            if g < 105: g += speed
            if b < 250: b += speed
        return r, g, b


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

    def show_planer(self, pi):
        corner = 90
        if self.n % 2 == 0:
            corner = math.degrees(pi)
        turn_planer = pygame.transform.rotate(self.planer_img, corner)
        self.sc.blit(turn_planer, self.rect)


class GameWindow:
    def __init__(self):
        pygame.init()
        self.W = 1500
        self.H = 750
        self.k = 0
        self.mod = 'easy'
        self.status = 'Input'
        self.name_player = ''
        self.surface = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Fly GAME')
        pygame.time.set_timer(pygame.USEREVENT, random.randint(10, 2000))
        db = DataBaseClient(com.DATABASE_PLAYERS)
        self.db_players = PlayerRecord(db)
        self.db_players.setup()
        self.text = FormText(self.surface, self.H, self.W)
        self.planer = Planer(self.W, self.H, self.surface)
        self.map = Map(self.W, self.H, self.surface)
        self.group = Groups(self.H, self.W)
        self.clock = pygame.time.Clock()
        self.mess = ''

    def main_lop(self, sco: score.Score):
        while True:
            self.k += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    sco.update_mouse_y(event.pos[1])
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, random.randint(1, 1500))
                    self.group.create_point(sco.dist)
                    self.group.create_fox(sco.dist)
                if event.type == pygame.USEREVENT+1:
                    if event.message == 'point':
                        sco.update_point()
                    elif event.message == 'accel':
                        sco.xy_speed += 10
                    elif event.message == 'stop':
                        sco.xy_speed -= 10
                    elif event.message == 'fox':
                        self.surface.fill(sco.color_bg)
                        self.status = 'Game_over'
                        return sco.level, sco.dist, sco.point, sco.color_bg

            if self.k % 10 == 0:
                sco.update_dist()
                sco.update_speed_planer()
                sco.update_height()
                self.k = 0
            self.group.create_stars(sco.y_speed)

            sco.color_bg = self.map.change_color(sco.color_bg, sco.dist)
            self.surface.fill(sco.color_bg)
            if self.mod == 'easy':
                sco.update_xy_speed_easy(self.H)
            else:
                sco.update_xy_speed_real(self.H)
            self.group.point_group.update(self.surface, sco.x_speed, sco.y_speed, H=self.H, W=self.W)
            self.group.stars_group.update(self.surface, sco.x_speed, sco.y_speed)
            self.planer.show_planer(sco.pi)
            if self.map.draw_ground(sco.height_now, sco.x_speed):
                self.surface.fill(sco.color_bg)
                self.status = 'Game_over'
                return sco.level, sco.dist, sco.point, sco.color_bg
            self.text.join_main(sco.level, sco.dist, sco.speed_planer, sco.height_now, sco.point)

            pygame.display.update()
            self.clock.tick(60)


class Menu(GameWindow):
    def menu_lop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if self.status == 'Normal':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.surface.fill(com.BLUE)
                        pos_btn = self.text.join_menu(self.mod)
                        pos_start = pos_btn[0]
                        pos_results = pos_btn[3]
                        pos_real = pos_btn[2]
                        pos_easy = pos_btn[1]
                        p_r = event.pos
                        if pos_easy[0] - p_r[0] < pos_easy[2] and 0 < p_r[1] - pos_easy[1] < pos_easy[3]:
                            self.mod = 'easy'
                        if pos_real[0] - p_r[0] < pos_real[2] and 0 < p_r[1] - pos_real[1] < pos_real[3]:
                            self.mod = 'real'
                        elif pos_results[0] - p_r[0] < pos_results[2] and 0 < p_r[1] - pos_results[1] < pos_results[3]:
                            self.status = 'Results'
                        elif pos_start[0] - p_r[0] < pos_start[2] and 0 < p_r[1] - pos_start[1] < pos_start[3]:
                            self.mess = self.main_lop(score.Score())
                    self.surface.fill(com.BLUE)
                    self.text.join_menu(self.mod)
                elif self.status == 'Game_over':
                    lev, dist, point, color = self.mess
                    self.surface.fill(color)
                    self.text.join_game_over(lev, dist, point)
                    self.db_players.save_result((self.text.name, str(int(point * dist * 0.5)), date.today()), self.mod)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.status = 'Normal'
                elif self.status == 'Input':
                    self.surface.fill(com.BLUE)
                    self.text.join_input()
                    if event.type == pygame.KEYDOWN:
                        self.text.join_input(event.unicode)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.text.join_input('_backspace_')
                        elif event.button == 3:
                            self.status = 'Normal'
                elif self.status == 'Results':
                    self.surface.fill(com.BLUE)
                    db_easy = self.db_players.get_players('easy')
                    db_real = self.db_players.get_players('real')
                    self.text.join_results(db_easy, db_real)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.status = 'Normal'
            pygame.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    x = Menu()
    x.menu_lop()
