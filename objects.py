import pygame


class PointCoins(pygame.sprite.Sprite):
    def __init__(self, filename, x_c, y_c, *size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x_c, y_c))
