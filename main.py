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
    pass


def statistics():
    main_font = pygame.font.Font(None, 40)
    font = pygame.font.Font(None, 30)
    result = cur.execute("SELECT name, mushrooms FROM Statistics ORDER BY mushrooms").fetchmany(10)
    # Запрос на рекорд игрока
    pl = cur.execute(f"SELECT id, mushrooms FROM Statistics WHERE name = '{name}'").fetchone()
    result.reverse()
    screen.blit(statistics_image, (0, 0))
    table_text = main_font.render('Таблица лидеров', True, (57, 32, 14))
    player_text = f'{pl[0]}  {name}  {str(pl[1])}'
    player_stat = font.render(player_text, True, (57, 32, 14))
    # Отрисовка рекордов первых 10 игроков в бд по грибам
    for i in range(10 * (len(result) >= 10) + len(result) * (len(result) < 10)):
        txt = str(i + 1) + '    ' * (i + 1 < 10) + '  ' * (i + 1 == 10) + result[i][0]
        string = font.render(txt, True, (57, 32, 14))
        mush = font.render(str(result[i][1]), True, (57, 32, 14))
        screen.blit(string, (30, 120 + 27 * i))
        screen.blit(mush, (230, 120 + 27 * i))
    screen.blit(table_text, (30, 30))
    screen.blit(player_stat, (120, 440))
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