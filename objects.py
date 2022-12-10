import pygame
import random
import components as com


class Groups:
    def __init__(self, h, w):
        self.W = w
        self.H = h
        self.point_img = [com.COIN_lST[0], com.STOP, com.ACCEL]
        self.point_lst = [pygame.image.load(img).convert_alpha() for img in self.point_img]
        self.fox = pygame.image.load(com.FOX).convert_alpha()
        self.point_group = pygame.sprite.Group()
        self.stars_group = pygame.sprite.Group()

    def create_point(self, dist):
        size = (50, 50)
        for indx in range(len(self.point_img)):
            if self.point_img[indx] == com.ACCEL:
                y_c = random.randint(0, self.H)
                sch = 10
                if int(dist // 1000) <= 15:
                    sch = int(dist // 1000) + 1
                if random.randint(0, sch) == 1:
                    PointCoins(self.point_img[indx], self.point_lst[indx], self.W, y_c, self.point_group, size)
            if self.point_img[indx] == com.STOP:
                y_c = random.randint(0, self.H)
                sch = 1
                if 10 - int(dist // 1000) >= 1:
                    sch = 10 - int(dist // 1000)
                if random.randint(0, sch) == 1:
                    PointCoins(self.point_img[indx], self.point_lst[indx], self.W, y_c, self.point_group, size)
            if self.point_img[indx] == com.COIN_lST[0]:
                y_c = random.randint(0, self.H)
                if random.randint(0, 1) == 1:
                    PointCoins(self.point_img[indx], self.point_lst[indx], self.W, y_c, self.point_group, size)

    def create_fox(self, dist):
        sch = 1
        if 10 - int(dist // 1000) >= 3:
            sch = 10 - int(dist // 1000)
        if random.randint(0, sch) == 1:
            y_c = random.randint(0, self.H)
            PointCoins(com.FOX, self.fox, self.W, y_c, self.point_group, (250, 250))

    def create_stars(self, y_speed):
        sz = random.randint(5, 10)
        if y_speed > 0:
            y_c = random.randint(-self.H, self.H)
            if y_c < 0:
                x_c = random.randint(0, self.W * 2)
            else:
                x_c = random.randint(self.W, self.W * 2)
        else:
            y_c = random.randint(0, self.H * 2)
            if y_c > self.H:
                x_c = random.randint(0, self.W * 2)
            else:
                x_c = random.randint(self.W, self.W * 2)
        Stars(x_c, y_c, self.stars_group, (sz, sz), (self.W, self.H))


class Stars(pygame.sprite.Sprite):
    def __init__(self, x_c, y_c, group, size, size_window):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image = pygame.transform.scale(self.image, size)
        self.image.fill(com.WHITE)
        self.rect = self.image.get_rect(center=(x_c, y_c))
        self.size = size
        self.W, self.H = size_window
        self.add(group)

    def update(self, surface, x_speed, y_speed):
        if self.rect.x < - self.W:
            self.kill()
        if self.rect.x > self.W * 2:
            self.kill()
        if self.rect.y < - self.H:
            self.kill()
        if self.rect.y > self.H * 2:
            self.kill()
        self.rect.x -= x_speed
        self.rect.y += y_speed
        surface.blit(self.image, self.rect)


class PointCoins(pygame.sprite.Sprite):
    def __init__(self, img, sc, x_c, y_c, group, size):
        self.k = 0
        self.img = img
        pygame.sprite.Sprite.__init__(self)
        self.image = sc
        self.image = pygame.transform.scale(self.image, size)
        self.coin_img = com.COIN_lST
        self.coin_iter = self.create_coins()
        self.rect = self.image.get_rect(center=(x_c, y_c))
        self.add(group)

    def create_coins(self):
        coins = (img for img in self.coin_img)
        return iter(coins)

    def update(self, surface, x_speed, y_speed, **kwargs) -> None:
        self.k += 1
        w = kwargs['W']
        h = kwargs['H']
        if self.rect.x < - kwargs['W']:
            self.kill()
        if self.rect.x > kwargs['W']:
            self.kill()
        if self.rect.y < - kwargs['H']:
            self.kill()
        if self.rect.y > kwargs['H']:
            self.kill()
        self.rect.x -= x_speed * 0.4
        self.rect.y += y_speed
        if (w // 2) - 55 < self.rect.centerx < (w // 2) + 55 and (h // 2) - 55 < self.rect.centery < (h // 2) + 55:
            if self.img == com.COIN_lST[0]:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='point'))
                self.kill()
            elif self.img == com.ACCEL:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='accel'))
                self.kill()
            elif self.img == com.STOP:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='stop'))
                self.kill()
            elif self.img == com.FOX:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='fox'))
                self.kill()
        if self.k % 10 == 0 and self.img == com.COIN_lST[0]:
            self.k = 0
            try:
                img = next(self.coin_iter)
            except StopIteration:
                self.coin_iter = self.create_coins()
                img = next(self.coin_iter)
            self.image = pygame.image.load(img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 70))
        surface.blit(self.image, self.rect)



