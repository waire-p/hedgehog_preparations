import pygame
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


size = width, height = 300, 500
V = 20

class Background1(pygame.sprite.Sprite):
    image = load_image("background.png", None)
    def __init__(self, *group):
        super().__init__(*group)
        self.background = Background1.image
        self.rect = self.background.get_rect()
        self.rect.x = 0
        self.rect.y = - 656

    def update(self, *args):
        if self.rect.y  >= height:
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
        if self.rect.y >= height:
            self.rect.y = -656
        else:
            self.rect = self.rect.move(0, V)


class Mushroom(pygame.sprite.Sprite):
    image = load_image('mushroom.png', -1)
    def __init__(self, *group, road, y):
        super().__init__(*group)
        self.mushroom = Background2.image
        self.rect = self.mushroom.get_rect()
        self.rect.x = road
        self.rect.y = y

    def update(self, *args):
        self.rect = self.rect.move(0, V)