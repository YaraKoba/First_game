import pygame
import random

pygame.init()

WITHE = (255, 255, 255)
BLUE = (120, 100, 190)

W, H = 1500, 600
surface = pygame.display.set_mode((W, H))
pygame.display.set_caption('Fly GAME')
cloock = pygame.time.Clock()
star_pos = {num: [random.randint(1, W), random.randint(1, H)] for num in range(100)}
pygame.mouse.set_visible(False)
x_speed = 4
y_speed = 2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # if event.type == pygame.MOUSEMOTION:

    surface.fill(BLUE)

    for star in range(100):
        x = star_pos[star][0]
        y = star_pos[star][1]
        if x < 2:
            star_pos[star][0] = W
            star_pos[star][1] = random.randint(0, H)
        if y < 2:
            star_pos[star][0] = random.randint(0, W)
            star_pos[star][1] = H - 2
        if y > 598:
            star_pos[star][0] = random.randint(0, W)
            star_pos[star][1] = 2
        star_pos[star][0] -= x_speed
        star_pos[star][1] += y_speed
        pygame.draw.rect(surface, WITHE, (x, y, 3, 3))
    # pygame.draw.rect(surface, WITHE, (0, 0, 10, 10))
    pygame.display.update()

    cloock.tick(60)


