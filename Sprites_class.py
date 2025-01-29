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


width, height = 300, 500
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
    def __init__(self, *group, road):
        super().__init__(*group)
        self.mushroom = Mushroom.image
        self.rect = self.mushroom.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)


class Barrier1(pygame.sprite.Sprite):
    image = load_image('barrier1.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier1.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)


class Barrier2(pygame.sprite.Sprite):
    image = load_image('barrier2.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier2.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)

class Barrier3(pygame.sprite.Sprite):
    image = load_image('barrier3.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = Barrier3.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)


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

class TrueHole(pygame.sprite.Sprite):
    image = load_image('true_hole.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = TrueHole.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)


class FakeHole(pygame.sprite.Sprite):
    image = load_image('fake_hole.png', -1)
    def __init__(self, *group, road):
        super().__init__(*group)
        self.barrier = FakeHole.image
        self.rect = self.barrier.get_rect()
        self.rect.x = road
        self.rect.y = 0

    def update(self, *args):
        self.rect = self.rect.move(0, V)