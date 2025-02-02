import sys
import sqlite3
import os
import pygame


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
    x, y = 0, 0
    screen.blit(good_end, (0, 0))
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
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            start_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def bad_ending():
    x, y = 0, 0
    screen.blit(bad_end, (0, 0))
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
                    if 300 <= y <= 380:
                        if 50 <= x <= 130:
                            start_menu()
                        if 170 <= x <= 250:
                            play()
        clock.tick(fps)
        pygame.display.flip()


def death():
    x, y = 0, 0
    screen.blit(death_end, (0, 0))
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
    size = width, height = 300,500
    screen = pygame.display.set_mode(size)
    menu = load_image('Menuuuuu.jpg', -1)
    good_end = load_image('Good ending.jpg', -1)
    bad_end = load_image('Bad ending.jpg', -1)
    death_end = load_image('Death.jpg', -1)
    clock = pygame.time.Clock()
    fps = 60
    start_menu()
con.close()