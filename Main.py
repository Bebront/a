import os
import random
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def if_control_key(key):
    if key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
        return 1
    elif key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
        return 2
    else:
        return 0


class Tank(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, rotate, keyboard):
        super().__init__(all_sprites)
        self.image = load_image('tank.png', -1)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x, self.y = x, y
        self.speed = random.choice([1, 2, 3])
        self.image = pygame.transform.rotate(self.image, -rotate)
        self.direction = rotate
        self.rotate = rotate
        self.keyboard = keyboard
        if self.keyboard == 'udlr':
            self.angles = {
                pygame.K_UP: 0,
                pygame.K_DOWN: 180,
                pygame.K_RIGHT: 90,
                pygame.K_LEFT: 270
            }
        else:
            self.angles = {
                pygame.K_w: 0,
                pygame.K_s: 180,
                pygame.K_d: 90,
                pygame.K_a: 270
            }
        if self.speed == 1:
            self.bullet_speed = 30
        elif self.speed == 2:
            self.bullet_speed = 20
        else:
            self.bullet_speed = 10

    def update(self, direction):
        if not direction in self.angles:
            return
        if self.rotate == 90:
            self.image = pygame.transform.rotate(self.image, (self.direction - self.angles[direction]) % 360)
        else:
            self.image = pygame.transform.rotate(self.image, (self.direction - self.angles[direction]) % 360)
        if self.angles[direction] == 0:
            self.rect = self.rect.move(0, -self.speed)
        if self.angles[direction] == 180:
            self.rect = self.rect.move(0, self.speed)
        if self.angles[direction] == 90:
            self.rect = self.rect.move(self.speed, 0)
        if self.angles[direction] == 270:
            self.rect = self.rect.move(-self.speed, 0)
        print(self.y, self.x)
        self.direction = self.angles[direction]


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


all_sprites = pygame.sprite.Group()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

size = width, height = 1920, 1030
screen = pygame.display.set_mode(size)

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

Tank_1 = Tank(10, 100, 100, 90, 'udlr')
Tank_2 = Tank(10, 600, 800, 270, 'wasd')

clock = pygame.time.Clock()
flag_1 = False
flag_2 = False
event_key_2 = '78'
event_key_1 = '56'
running = True
while running:
    if flag_1 is True:
        all_sprites.update(event_key_1)
    if flag_2 is True:
        all_sprites.update(event_key_2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if if_control_key(event.key) == 1:
                flag_1 = True
                event_key_1 = event.key
            elif if_control_key(event.key) == 2:
                flag_2 = True
                event_key_2 = event.key
            all_sprites.update(event.key)
        elif event.type == pygame.KEYUP:
            if if_control_key(event.key) == 1:
                flag_1 = False
            elif if_control_key(event.key) == 2:
                flag_2 = False
    fon = pygame.transform.scale(load_image('Fon.jpg'), size)
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
