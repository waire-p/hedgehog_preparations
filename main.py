# Игровой процесс
import pygame
import random
from pygame import Rect
if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    running = True
    v = 10
    balls = []
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_d:
                pass
            if event.type == pygame.K_a:
                pass

        screen.fill((0, 0, 0))
        unit = Rect(width // 2 - 25, 0, 50, 50)
        unit = pygame.draw.rect(screen, 'red', (width // 2 - 25, 0, 50, 50), 0)
        unit.move(50, 50)
        rect_r = (random.randint(1, 3) * 100 - 75)
        can_draw = random.randint(1, 100)
        if can_draw > 97:
            balls.append([rect_r, 0])
        for el in balls:
            pygame.draw.rect(screen, 'white', [int(el[0]), int(el[1]), 50, 50], 0)
            el[1] += v
            if el[1] >= height:
                 balls.remove(el)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
