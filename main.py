import sys
import sqlite3
import os
import pygame


def start_game():
    font = pygame.font.Font(None, 25)
    input_box = pygame.Rect(25, 175, 250, 27)
    color_inactive = (100, 67, 0)
    color_active = pygame.Color(150, 100, 0)
    color = color_inactive
    active = False
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text:
                            return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) <= 12:
                            text += event.unicode

        screen.fill((125, 84, 0))
        pygame.draw.rect(screen, color, input_box, 0)
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        pygame.display.flip()
        clock.tick(fps)


def start_menu():
    x, y = 0, 0
    screen.blit(menu, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 90 <= x <= 210:
                        if 195 <= y <= 258:
                            play()
                        if 261 <= y <= 324:
                            stat()
                        if 327 <= y <= 390:
                            exit_game()
        clock.tick(fps)
        pygame.display.flip()


def good_ending():
    font = pygame.font.Font(None, 60)
    txt = font.render(str(mushroom_counter), True, (255, 255, 255))
    result = cur.execute(f"SELECT mushrooms FROM Statistics WHERE name = '{name}'").fetchone()
    if mushroom_counter > result[0]:
        cur.execute(f"UPDATE Statistics SET mushrooms = {mushroom_counter} WHERE name = '{name}'")
    x, y = 0, 0
    screen.blit(good_end, (0, 0))
    screen.blit(txt, (70, 80))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            start_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def bad_ending():
    font = pygame.font.Font(None, 60)
    txt = font.render(str(mushroom_counter), True, (255, 255, 255))
    x, y = 0, 0
    screen.blit(bad_end, (0, 0))
    screen.blit(txt, (70, 80))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            start_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def death():
    font = pygame.font.Font(None, 60)
    txt = font.render(str(mushroom_counter), True, (255, 255, 255))
    x, y = 0, 0
    screen.blit(death_end, (0, 0))
    screen.blit(txt, (70, 80))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            start_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def play():
    pass


def stat():
    pass


def exit_game():
    pygame.quit()
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
    menu = load_image('Menuuuuu.jpg', -1)
    good_end = load_image('Good ending.jpg', -1)
    bad_end = load_image('Bad ending.jpg', -1)
    death_end = load_image('Death.jpg', -1)
    clock = pygame.time.Clock()
    fps = 60
    mushroom_counter = 0
    name = start_game()
    res = cur.execute("SELECT name FROM Statistics").fetchall()
    if name not in res:
        cur.execute(f"INSERT INTO Statistics(name,mushrooms) VALUES('{name}',0)")
    start_menu()
cur.execute("DELETE FROM Statistics")
con.close()