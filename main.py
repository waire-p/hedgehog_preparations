# Игровой процесс
import pygame
import random

if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    running = True
    v = 10
    clock = pygame.time.Clock()
    # Персонаж
    unit_pos = 1  # индекс дорожки
    unit_scale = 50  # размер
    # Препятствия
    barriers_scale = 50  # размер
    barriers = []  # координаты на экране
    # Грибы
    mushrooms_scale = 50  # размер
    mushrooms = []  # координаты на экране
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if unit_pos + 1 < 3:
                        unit_pos += 1
                if event.key == pygame.K_a:
                    if unit_pos - 1 > -1:
                        unit_pos -= 1

        screen.fill((0, 0, 0))
        # Отрисовка персонажа
        pygame.draw.rect(screen, 'red', (unit_pos * 100 + unit_scale // 2 , height - unit_scale,
                                         unit_scale, unit_scale), 0)
        # Отрисовка препятствий
        barrier_road = (random.randint(1, 3) * 100 - barriers_scale - barriers_scale / 2)
        can_draw_barrier = random.randint(1, 100) # Шанс на отрисовку
        if can_draw_barrier > 97:
            barriers.append([barrier_road, 0])
        for el in barriers:
            pygame.draw.rect(screen, 'white', [int(el[0]), int(el[1]), barriers_scale, barriers_scale], 0)
            el[1] += v
            if el[1] >= height:
                 barriers.remove(el)
        # Отрисовка грибов
        mush_road =  (random.randint(1, 3) * 100 - 75)
        can_draw_mush = random.randint(1, 100) # Шанс на отрисовку
        if can_draw_mush > 95 and can_draw_barrier < 40:
            mushrooms.append([mush_road, 0])
        for el in mushrooms:
            pygame.draw.rect(screen, 'green', [int(el[0]), int(el[1]), mushrooms_scale, mushrooms_scale], 0)
            el[1] += v
            if el[1] >= height:
                mushrooms.remove(el)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
