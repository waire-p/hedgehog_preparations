# Игровой процесс
import pygame
import random
import os


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


class Backround(pygame.sprite.Sprite):
    image = load_image("background1.jpg", None)
    def __init__(self, group):
        super().__init__(self, group)
        self.image = Backround.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, v)



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


    all_sprites = pygame.sprite.Group()
    background = Backround(all_sprites)
    all_sprites.add(background)
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
        # Отрисовка персонажа
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.draw.rect(screen, 'red', (unit_pos * 100 + unit_scale // 2 , height - unit_scale,
                                         unit_scale, unit_scale), 0)
        # Отрисовка препятствий
        #barrier_type = random.randint(1, 10) заготовка под типы спрайтов
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
