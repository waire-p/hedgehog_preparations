import pygame
import random
import os


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

# Функция создания частиц удара
def create_hit_particles(position):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        HitParticle(position, random.choice(numbers), random.choice(numbers))


def create_collect_particles(position):
    CollectParticle(position, 1, 1)


# Спрайты заднего фона
class Background1(pygame.sprite.Sprite):
    image = load_image("background.png", None)
    def __init__(self, *group):
        super().__init__(*group)
        self.background = Background1.image
        self.rect = self.background.get_rect()
        self.rect.x = 0
        self.rect.y = -656

    def update(self, *args):
        if self.rect.y  >= height: # Если спрайт опускается вниз, то перемещаем наверх
            self.rect.y = -656
        else:
            self.rect = self.rect.move(0, V)


class Background2(pygame.sprite.Sprite):
    image = load_image("background.png", None)
    def __init__(self, *group):
        super().__init__(*group)
        self.background = Background2.image
        self.rect = self.background.get_rect()

    def update(self, *args):
        if self.rect.y >= height:  # Если спрайт опускается вниз, то перемещаем наверх
            self.rect.y = -656
        else:
            self.rect = self.rect.move(0, V)

# Спрайты грибов
class Mushroom(pygame.sprite.Sprite):
    image = load_image('mushroom.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.mushroom = Mushroom.image
        self.rect = self.mushroom.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global mushroom_count
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            create_collect_particles((self.rect.x, self.rect.y))  # Создание частиц сбопа грибов
            mushroom_count += 1  # Добавление к счетчику
            self.kill()

# Спрайты перпятствий
class Barrier1(pygame.sprite.Sprite):
    image = load_image('barrier1.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier1.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global running
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()
            running = False


class Barrier2(pygame.sprite.Sprite):
    image = load_image('barrier2.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier2.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global running
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()
            running = False


class Barrier3(pygame.sprite.Sprite):
    image = load_image('barrier3.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier3.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global running
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()
            running = False

# Спрайт персонажа
class Hedgehog(pygame.sprite.Sprite):
    def __init__(self, *group, sheet, cols, rows):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(0, height - 100)
        self.tick = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, unit_road):
        self.tick += 1
        self.rect.x = unit_road * 100
        if self.tick >= 5:
            self.tick = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

# Спрайт нор для сохранения результатов
class TrueHole(pygame.sprite.Sprite):
    image = load_image('true_hole.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = TrueHole.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        global running
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            self.kill()
            running = False


class FakeHole(pygame.sprite.Sprite):
    image = load_image('fake_hole.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = FakeHole.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        global running
        self.rect = self.rect.move(0, V)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            self.kill()
            running = False

# Спрайты частиц
class HitParticle(pygame.sprite.Sprite):
    fire = [load_image("hit.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particles_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class CollectParticle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(particles_sprites)
        self.image = pygame.transform.scale(load_image("collect.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    running = True
    V = 17
    GRAVITY = 0.3
    clock = pygame.time.Clock()
    # Событие генерации норы
    GENERATEHOLE = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERATEHOLE, 60000) # 60000мс / 1 минута
    screen_rect = (0, 0, width, height)
    character_road = 1  # индекс дорожки персонажа
    # Задний фон
    backgrounds_sprites = pygame.sprite.Group()
    backgrounds_sprites.add(Background1(backgrounds_sprites))
    backgrounds_sprites.add(Background2(backgrounds_sprites))
    # Группы спрайтов
    particles_sprites = pygame.sprite.Group()
    hole_sprites = pygame.sprite.Group()
    mushroom_sprites = pygame.sprite.Group()
    barrier_sprites = pygame.sprite.Group()
    character_ani_sprite = pygame.sprite.Group()
    character_ani_sprite.add(Hedgehog(character_ani_sprite, sheet=load_image("hedgehog.1.png"), cols=2, rows=2))
    mushroom_count = 0
    while running:
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
        # движение заднего фона и частиц
        backgrounds_sprites.update()
        particles_sprites.update()
        # Счетчик
        counter = load_image('counter.png', -1)
        font = pygame.font.SysFont('Arial', 30)
        counter_text = font.render('0' * (6 - len(str(mushroom_count))) + str(mushroom_count),
                                   True, (248, 200, 145))
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
                el.kill()
        # Генерация грибов и их перемещение
        mush_road = (random.randint(1, 3) * 100 - 75)
        can_draw_mush = random.randint(1, 100)  # Шанс на отрисовку
        if can_draw_mush > 95 and can_draw_barrier < 45:
            new_mushroom = Mushroom(road=mush_road)
            mushroom_sprites.add(new_mushroom)
        for el in mushroom_sprites:
            el.update()
            if el.rect.y >= height:
                 el.kill()

        for el in hole_sprites:
            el.update()
            if el.rect.y >= height:
                el.kill()
        # Отрисовка необходимых спрайтов
        backgrounds_sprites.draw(screen)
        particles_sprites.draw(screen)
        mushroom_sprites.draw(screen)
        barrier_sprites.draw(screen)
        hole_sprites.draw(screen)
        character_ani_sprite.draw(screen)
        screen.blit(counter, (0, 0))
        screen.blit(counter_text, (width // 2 - counter_text.get_width() // 2, 3))
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()
