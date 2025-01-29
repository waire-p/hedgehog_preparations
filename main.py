import pygame
import random
import os
from Sprites_class import Background2, Background1  # Задний фон
from Sprites_class import TrueHole, FakeHole  # Норы для концовок
from Sprites_class import Barrier1, Barrier2, Barrier3  # Виды барьеров
from Sprites_class import Mushroom, Hedgehog  # Грибы и персонаж


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
            colorkey = image.get_at((49, 49))
        image.set_colorkey(colorkey)
    return image


if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    running = True
    V = 20
    clock = pygame.time.Clock()
    # Событие генерации норы
    GENERATEHOLE = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERATEHOLE, 120000) # 120000мс / 2 минуты

    character_road = 1  # индекс дорожки персонажа
    # Задний фон
    backgrounds_sprites = pygame.sprite.Group()
    backgrounds_sprites.add(Background1(backgrounds_sprites))
    backgrounds_sprites.add(Background2(backgrounds_sprites))
    # Группы спрайтов грибов, препятствий, нор и персонажа
    hole_sprites = pygame.sprite.Group()
    mushroom_sprites = pygame.sprite.Group()
    barrier_sprites = pygame.sprite.Group()
    character_ani_sprite = pygame.sprite.Group()
    character_ani_sprite.add(Hedgehog(character_ani_sprite, sheet=load_image("hedgehog.1.png"), cols=2, rows=2))
    COUNT = 0
    while running:
        COUNT += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Управление персонажем
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if character_road + 1 < 3:
                        character_road += 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if character_road - 1 > -1:
                        character_road -= 1
            # Генерация новой дыры
            if event.type == GENERATEHOLE:
                hole_road = (random.randint(1, 3) * 100 - 75)
                holes = [TrueHole(road=hole_road), FakeHole(road=hole_road)]
                hole_type = random.randint(0, len(holes) - 1)
                new_hole = holes[hole_type]
                hole_sprites.add(new_hole)


        screen.fill((0, 0, 0))
        # Отрисовка и движение заднего фона
        backgrounds_sprites.draw(screen)
        backgrounds_sprites.update()

        # Счетчик
        counter = load_image('counter.png', -1)
        font = pygame.font.SysFont('Arial', 30)
        counter_text = font.render('0' * (6 - len(str(COUNT))) + str(COUNT), True, (248, 200, 145))


        # Обновление анимации персонажа
        character_ani_sprite.update(character_road)

        # Генерация препятствий и их перемещение
        barrier_road = (random.randint(1, 3) * 100 - 75)
        can_draw_barrier = random.randint(1, 100) # Шанс на отрисовку
        barriers = [Barrier1(road=barrier_road), Barrier2(road=barrier_road), Barrier3(road=barrier_road)]
        barrier_type = random.randint(0, len(barriers) - 1)  # Определение типа спрайта
        if can_draw_barrier > 97:
            new_barrier = barriers[barrier_type]
            barrier_sprites.add(new_barrier)
        for el in barrier_sprites:
            el.update()
            if el.rect.y >= height:
                 barrier_sprites.remove(el)

        # Генерация грибов и их перемещение
        mush_road = (random.randint(1, 3) * 100 - 75)
        can_draw_mush = random.randint(1, 100)  # Шанс на отрисовку
        if can_draw_mush > 95 and can_draw_barrier < 40:
            new_mushroom = Mushroom(road=mush_road)
            mushroom_sprites.add(new_mushroom)
        for el in mushroom_sprites:
            el.update()
            if el.rect.y >= height:
                mushroom_sprites.remove(el)

        for el in hole_sprites:
            el.update()
            if el.rect.y >= height:
                hole_sprites.remove(el)
        # Отрисовка необходимых спрайтов
        mushroom_sprites.draw(screen)
        barrier_sprites.draw(screen)
        hole_sprites.draw(screen)
        character_ani_sprite.draw(screen)
        screen.blit(counter, (0, 0))
        screen.blit(counter_text, (width // 2 - counter_text.get_width() // 2, 3))
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
