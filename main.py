import pygame
import random
import os
from Sprites_class import Background2, Background1, Mushroom, Barrier1, Barrier2, Barrier3


# Игровой процесс
# Функция загрузки изображений
def load_image(name, colorkey=-1):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    running = True
    V = 20
    clock = pygame.time.Clock()
    # Персонаж
    unit_pos = 1  # индекс дорожки
    unit_scale = 50  # размер
    # Препятствия

    backgrounds_sprites = pygame.sprite.Group()
    background1 = Background1(backgrounds_sprites)
    background2 = Background2(backgrounds_sprites)
    backgrounds_sprites.add(background1)
    backgrounds_sprites.add(background2)

    mushroom_sprites = pygame.sprite.Group()
    barrier_sprites = pygame.sprite.Group()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if unit_pos + 1 < 3:
                        unit_pos += 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if unit_pos - 1 > -1:
                        unit_pos -= 1

        screen.fill((0, 0, 0))

        backgrounds_sprites.draw(screen)
        backgrounds_sprites.update()
        # Отрисовка персонажа
        pygame.draw.rect(screen, 'red', (unit_pos * 100 + unit_scale // 2 , height - unit_scale,
                                         unit_scale, unit_scale), 0)
        # Отрисовка препятствий
        barrier_type = random.randint(0, 2)  # заготовка под типы спрайтов
        barrier_road = (random.randint(1, 3) * 100 - 75)
        can_draw_barrier = random.randint(1, 100) # Шанс на отрисовку
        barriers = [Barrier1(road=barrier_road), Barrier2(road=barrier_road), Barrier3(road=barrier_road)]
        if can_draw_barrier > 97:
            new_barrier = barriers[barrier_type]
            barrier_sprites.add(new_barrier)
        for el in barrier_sprites:
            el.update()
            if el.rect.y >= height:
                 barrier_sprites.remove(el)
        # Отрисовка грибов
        mush_road = (random.randint(1, 3) * 100 - 75)
        can_draw_mush = random.randint(1, 100)  # Шанс на отрисовку
        if can_draw_mush > 95 and can_draw_barrier < 40:
            new_mushroom = Mushroom(road=mush_road)
            mushroom_sprites.add(new_mushroom)
        for el in mushroom_sprites:
            el.update()
            if el.rect.y >= height:
                mushroom_sprites.remove(el)
        mushroom_sprites.draw(screen)
        barrier_sprites.draw(screen)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
