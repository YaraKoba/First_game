import pygame
import random


class Groups:
    def __init__(self, h, w):
        self.W = w
        self.H = h
        self.point_img = ['pos1.png', 'stop.png', 'go.png']
        self.point_lst = [pygame.image.load(f'image/{img}').convert_alpha() for img in self.point_img]
        self.fox = pygame.image.load(f'image/fox.png').convert_alpha()
        self.point_group = pygame.sprite.Group()

    def create_point(self):
        size = (70, 70)
        indx = random.randint(0, 2)
        y_c = random.randint(0, self.H)
        PointCoins(self.point_img[indx], self.point_lst[indx], self.W, y_c, self.point_group, size)

    def create_fox(self, dist):
        sch = 1
        if 5 - int(dist // 1000) >= 1:
            sch = 5 - int(dist // 1000)
        if random.randint(0, sch) == 1:
            y_c = random.randint(0, self.H)
            PointCoins('fox.png', self.fox, self.W, y_c, self.point_group, (300, 300))


class PointCoins(pygame.sprite.Sprite):
    def __init__(self, img, sc, x_c, y_c, group, size):
        self.k = 0
        self.img = img
        pygame.sprite.Sprite.__init__(self)
        self.image = sc
        self.image = pygame.transform.scale(self.image, size)
        self.coin_img = ['pos1.png', 'pos2.png', 'pos3.png', 'pos4.png', 'pos5.png', 'pos6.png']
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
        if (w // 2) - 80 < self.rect.centerx < (w // 2) + 80 and (h // 2) - 80 < self.rect.centery < (h // 2) + 80:
            if self.img == 'pos1.png':
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='point'))
                self.kill()
            elif self.img == 'go.png':
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='go'))
                self.kill()
            elif self.img == 'stop.png':
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='stop'))
                self.kill()
            elif self.img == 'fox.png':
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, message='fox'))
                self.kill()
        if self.k % 10 == 0 and self.img == 'pos1.png':
            self.k = 0
            try:
                img = next(self.coin_iter)
            except StopIteration:
                self.coin_iter = self.create_coins()
                img = next(self.coin_iter)
            self.image = pygame.image.load(f'image/{img}').convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 70))
        surface.blit(self.image, self.rect)


