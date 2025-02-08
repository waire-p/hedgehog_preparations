import sys
import sqlite3
import os
import pygame
import random


def start_game():
    # Создание поля для ввода имени
    font = pygame.font.Font(None, 25)
    input_box = pygame.Rect(25, 175, 250, 27)
    enter_box = pygame.Rect(50, 225, 200, 27)
    color_inactive = (100, 67, 0)
    color_active = pygame.Color(150, 100, 0)
    color = color_inactive
    enter_color = color_inactive
    active = False
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            # Нажатие кнопки
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif enter_box.collidepoint(event.pos):
                    if text:
                        return text
                else:
                    active = False
                color = color_active if active else color_inactive  # изменение цвета при нажатии на поле ввода
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) <= 9:
                            text += event.unicode
            if event.type == pygame.MOUSEMOTION:
                if enter_box.collidepoint(event.pos):
                    enter_color = color_active
                else:
                    enter_color = color_inactive
        # Отрисовка
        screen.fill((125, 84, 0))
        pygame.draw.rect(screen, color, input_box, 0)
        pygame.draw.rect(screen, enter_color, enter_box, 0)
        enter_text = font.render('Начать', True, (0, 0, 0))
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(enter_text, (120, 230))

        pygame.display.flip()
        clock.tick(fps)


def main_menu():
    x, y = 0, 0
    font = pygame.font.Font(None, 45)
    menu_text_outline = font.render('Ежиные заготовки', True, (40, 28, 16))
    menu_text = font.render('Ежиные заготовки', True, (248, 200, 145))
    screen.blit(menu, (0, 0))
    # Обводка текста названия игры
    screen.blit(menu_text_outline, (width // 2 - menu_text.get_width() // 2 - 2, 55 + 2))
    screen.blit(menu_text_outline, (width // 2 - menu_text.get_width() // 2 + 2, 55 - 2))
    screen.blit(menu_text_outline, (width // 2 - menu_text.get_width() // 2 + 2, 55 + 2))
    screen.blit(menu_text_outline, (width // 2 - menu_text.get_width() // 2 - 2, 55 - 2))
    screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, 55))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Пересечение курсора для нажатия кнопок
                if pygame.mouse.get_pressed()[0]:
                    if 90 <= x <= 210:
                        if 195 <= y <= 258:
                            play()
                        if 261 <= y <= 324:
                            statistics()
                        if 327 <= y <= 390:
                            exit_game()
        clock.tick(fps)
        pygame.display.flip()


def good_ending():
    # Размещение необходимого текста
    font = pygame.font.Font(None, 60)
    message =  font.render('You win!', True, (248, 200, 145))
    txt = font.render('0' * (6 - len(str(mushroom_count))) + str(mushroom_count),
                                   True, (248, 200, 145))
    # Запись результатов в базу данных
    result = cur.execute(f"SELECT mushrooms FROM Statistics WHERE name = '{name}'").fetchone()
    if mushroom_count > result[0]:
        cur.execute(f"UPDATE Statistics SET mushrooms = {mushroom_count} WHERE name = '{name}'")
    x, y = 0, 0
    # Отрисовка текста
    screen.blit(good_end, (0, 0))
    screen.blit(message, (width // 2 - txt.get_width() // 2 - 10, 90))
    screen.blit(txt, (width // 2 - txt.get_width() // 2, 210))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Реакция на нажатие кнопок
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            main_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def bad_ending():
    # Размещение необходимого текста
    font = pygame.font.Font(None, 60)
    message = font.render('You lost', True, (248, 200, 145))
    txt = font.render('0' * (6 - len(str(mushroom_count))) + str(mushroom_count),
                      True, (248, 200, 145))
    x, y = 0, 0
    # Отрисовка текста
    screen.blit(good_end, (0, 0))
    screen.blit(message, (width // 2 - txt.get_width() // 2 - 10, 90))
    screen.blit(txt, (width // 2 - txt.get_width() // 2, 210))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Реакция на нажатие кнопок
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            main_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def death():
    font = pygame.font.Font(None, 60)
    message = font.render('You dead', True, (248, 200, 145))
    txt = font.render('0' * (6 - len(str(mushroom_count))) + str(mushroom_count),
                      True, (248, 200, 145))
    x, y = 0, 0
    # Отрисовка текста
    screen.blit(good_end, (0, 0))
    screen.blit(message, (width // 2 - txt.get_width() // 2 - 10, 90))
    screen.blit(txt, (width // 2 - txt.get_width() // 2, 210))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Реакция на нажатие кнопок
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            main_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def play():
    global game_speed
    global lives, mushroom_count
    running = True
    mushroom_count = 0  # Собранные грибы
    character_road = 1  # индекс дорожки персонажа
    barrier_chance = 98  # шанс на появление препятствия
    game_speed = 10 # Сброс скорости игры
    clock = pygame.time.Clock()
    # Событие генерации норы
    GENERATEHOLE = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERATEHOLE, 30000)  # 30000мс / 30 секунд
    # Событие увеличения скорости персонажа
    ADDGAMESPEED = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDGAMESPEED, 20000)  # 20000мс / 20 секунд
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
            # Увеличение скорости игры
            if event.type == ADDGAMESPEED:
                if game_speed < 30:
                    game_speed += 0.5
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
        can_draw_barrier = random.randint(1, 100)  # Шанс на отрисовку
        barriers = [Barrier1(road=barrier_road), Barrier2(road=barrier_road), Barrier3(road=barrier_road)]
        barrier_type = random.randint(0, len(barriers) - 1)  # Определение типа спрайта
        if game_speed > 25:  # изменение шанса на отрисовку препятствий при скорости > 25 пикс/сек
            barrier_chance = 96
        if can_draw_barrier > barrier_chance:
            new_barrier = barriers[barrier_type]
            barrier_sprites.add(new_barrier)
        # Проверка выхода объекта за пределы экрана
        for el in barrier_sprites:
            el.update()
            if el.rect.y >= height:
                el.kill()
        # Генерация грибов и их перемещение
        mush_road = (random.randint(1, 3) * 100 - 75)
        can_draw_mush = random.randint(1, 100)  # Шанс на отрисовку
        if can_draw_mush > barrier_chance and can_draw_barrier > 40:
            new_mushroom = Mushroom(road=mush_road)
            mushroom_sprites.add(new_mushroom)
        for el in mushroom_sprites:
            el.update()
            if el.rect.y >= height:
                el.kill()
        # Проверка выхода объекта за пределы экрана
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
        lives_ani_sprite.draw(screen)
        screen.blit(counter_text, (width // 2 - counter_text.get_width() // 2, 3))

        clock.tick(30)
        pygame.display.flip()


def statistics():
    main_font = pygame.font.Font(None, 40)
    font = pygame.font.Font(None, 30)
    result = cur.execute("SELECT name, mushrooms FROM Statistics ORDER BY mushrooms").fetchmany(10)
    # Запрос на рекорд игрока
    pl = cur.execute(f"SELECT mushrooms FROM Statistics WHERE name = '{name}'").fetchone()
    result.reverse()
    screen.blit(statistics_image, (0, 0))
    table_text = main_font.render('Таблица лидеров', True, (57, 32, 14))
    player_text = f'{name}    {str(pl[0])}'
    player_stat = font.render(player_text, True, (57, 32, 14))
    # Отрисовка рекордов первых 10 игроков в бд по грибам
    for i in range(10 * (len(result) >= 10) + len(result) * (len(result) < 10)):
        txt = str(i + 1) + '    ' * (i + 1 < 10) + '  ' * (i + 1 == 10) + result[i][0]
        string = font.render(txt, True, (57, 32, 14))
        mush = font.render(str(result[i][1]), True, (57, 32, 14))
        screen.blit(string, (30, 120 + 27 * i))
        screen.blit(mush, (230, 120 + 27 * i))
    screen.blit(table_text, (30, 30))
    screen.blit(player_stat, (120, 445))
    pygame.display.flip()
    x, y = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Реакция на нажатие кнопок
                if pygame.mouse.get_pressed()[0]:
                    if 410 <= y <= 490:
                        if 10 <= x <= 90:
                            main_menu()
        clock.tick(fps)
        pygame.display.flip()


def exit_game():
    pygame.quit()
    con.commit()
    con.close()
    sys.exit()


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
            self.rect = self.rect.move(0, game_speed)


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
            self.rect = self.rect.move(0, game_speed)

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
        self.rect = self.rect.move(0, game_speed)
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
        global lives
        self.rect = self.rect.move(0, game_speed)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            lives -= 1
            lives_ani_sprite.update()
            if lives == 0:
                lives = 3
                mushroom_sprites.empty()
                barrier_sprites.empty()
                hole_sprites.empty()
                particles_sprites.empty()
                death()
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()


class Barrier2(pygame.sprite.Sprite):
    image = load_image('barrier2.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier2.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global lives
        self.rect = self.rect.move(0, game_speed)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            lives -= 1
            lives_ani_sprite.update()
            if lives == 0:
                lives = 3
                mushroom_sprites.empty()
                barrier_sprites.empty()
                hole_sprites.empty()
                particles_sprites.empty()
                death()
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()


class Barrier3(pygame.sprite.Sprite):
    image = load_image('barrier3.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier3.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road  # Перемещение на дорогу
        self.rect.y = 0

    def update(self, *args):
        global lives
        self.rect = self.rect.move(0, game_speed)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            lives -= 1
            lives_ani_sprite.update()
            if lives == 0:
                lives = 3
                mushroom_sprites.empty()
                barrier_sprites.empty()
                hole_sprites.empty()
                particles_sprites.empty()
                death()
            create_hit_particles((self.rect.x, self.rect.y))  # Создание частиц удара
            self.kill()

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

# Спрайт жизней персонажа
class Lives(pygame.sprite.Sprite):
    def __init__(self, *group, sheet, cols, rows):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(5, 10)
        self.tick = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if lives == 0:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        else:
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
        global lives
        self.rect = self.rect.move(0, game_speed)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            self.kill()
            lives = 3
            mushroom_sprites.empty()
            barrier_sprites.empty()
            hole_sprites.empty()
            particles_sprites.empty()
            good_ending()


class FakeHole(pygame.sprite.Sprite):
    image = load_image('fake_hole.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = FakeHole.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        global lives
        self.rect = self.rect.move(0, game_speed)
        if pygame.sprite.spritecollideany(self, character_ani_sprite):
            self.kill()
            lives = 3
            mushroom_sprites.empty()
            barrier_sprites.empty()
            hole_sprites.empty()
            particles_sprites.empty()
            bad_ending()

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


con = sqlite3.connect("Hedgehog.sqlite")
cur = con.cursor()

if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    # Загрузка задних фонов меню
    menu = load_image('Main_menu.jpg', -1)
    good_end = load_image('Good_end.jpg', -1)
    bad_end = load_image('Bad_end.jpg', -1)
    death_end = load_image('Death.jpg', -1)
    statistics_image = load_image('Statistics.jpg', -1)
    game_speed = 10
    GRAVITY = -1
    lives = 3  # возможности сколкновения с препятствиями (жизни)
    mushroom_count = 0  # Собранные грибы
    screen_rect = (0, 0, width, height)  # "Рамка" при прикосновении к которой частицы исчезают
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
    character_ani_sprite.add(Hedgehog(character_ani_sprite, sheet=load_image("hedgehog.png"), cols=2, rows=2))
    lives_ani_sprite = pygame.sprite.Group()
    lives_ani_sprite.add(Lives(lives_ani_sprite, sheet=load_image('hearts.png'), cols=1, rows=4))
    clock = pygame.time.Clock()
    fps = 30
    mushroom_count = 0
    name = start_game()
    res = cur.execute("SELECT name FROM Statistics").fetchall()
    nick = True
    for el in res:
        if name in el:
            nick = False
    if nick:
        cur.execute(f"INSERT INTO Statistics(name,mushrooms) VALUES('{name}',0)")
    main_menu()