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


class Tank(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.image = load_image('tank.png', -1)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x, self.y = x, y
        self.speed = random.choice([10, 20, 30])
        self.image = pygame.transform.rotate(self.image, -90)
        self.direction = 90
        if self.speed == 10:
            self.bullet_speed = 300
        elif self.speed == 20:
            self.bullet_speed = 200
        else:
            self.bullet_speed = 100

    def update(self, direction):
        angles = {
            pygame.K_UP: 0,
            pygame.K_DOWN: 180,
            pygame.K_RIGHT: 90,
            pygame.K_LEFT: 270
        }
        if not direction in angles:
            return
        self.image = pygame.transform.rotate(self.image, (self.direction - angles[direction]) % 360)
        if angles[direction] == 0:
            self.rect = self.rect.move(0, -self.speed)
        if angles[direction] == 180:
            self.rect = self.rect.move(0, self.speed)
        if angles[direction] == 90:
            self.rect = self.rect.move(self.speed, 0)
        if angles[direction] == 270:
            self.rect = self.rect.move(-self.speed, 0)
        print(self.y, self.x)
        self.direction = angles[direction]
        # if pygame.sprite.spritecollideany(self, horizontal_borders):
        #     self.vy = -self.vy
        # if pygame.sprite.spritecollideany(self, vertical_borders):
        #     self.vx = -self.vx


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

for i in range(1):
    Tank(20, 100, 100)

clock = pygame.time.Clock()
flag = False
event_key = '78'
running = True
while running:
    if flag is True:
        all_sprites.update(event_key)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            flag = True
            event_key = event.key
            all_sprites.update(event.key)
        elif event.type == pygame.KEYUP:
            flag = False
    fon = pygame.transform.scale(load_image('Fon.jpg'), size)
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
