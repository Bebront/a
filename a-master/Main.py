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


def tank_move(tank, movement, speed):
    x, y = tank.x, tank.y
    if movement == 0:
        if level_map[(y - speed) // 100 + 1][x // 100 + 1] == "." and\
                level_map[(y - speed) // 100 + 1][(x - 10) // 100 + 2] == "." and \
                (abs(Tank_1.y - speed - Tank_2.y) > 100 or abs(Tank_1.x - Tank_2.x) > 100):
            tank.rect = tank.rect.move(0, -speed)
            tank.y -= speed
    elif movement == 180:
        if level_map[y // 100 + 2][x // 100 + 1] == "." and\
                level_map[(y - speed)// 100 + 2][(x - 10) // 100 + 2] == "." and \
                (abs(Tank_1.y + speed - Tank_2.y) > 100 or abs(Tank_1.x - Tank_2.x) > 100):
            tank.rect = tank.rect.move(0, speed)
            tank.y += speed
    elif movement == 270:
        if level_map[y // 100 + 1][(x - speed) // 100 + 1] == "." and\
                level_map[(y - 10) // 100 + 2][(x - speed) // 100 + 1] == "." and\
                (abs(Tank_1.x + speed - Tank_2.x) > 100 or abs(Tank_1.y - Tank_2.y) > 100):
            tank.rect = tank.rect.move(-speed, 0)
            tank.x -= speed
    elif movement == 90:
        if level_map[y // 100 + 1][(x - speed) // 100 + 2] == "." and\
                level_map[(y - 10) // 100 + 2][x // 100 + 2] == "." and \
                (abs(Tank_1.x - speed - Tank_2.x) > 100 or abs(Tank_1.y - Tank_2.y) > 100):
            tank.rect = tank.rect.move(speed, 0)
            tank.x += speed


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    x, y, tank_1, tank_2 = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile(x, y)
            elif level[y][x] == '2':
                print(x, y)
                tank_2 = Tank(radius=45, x_tank=x * 100, y_tank=y * 100, rotate=270, keyboard='wasd', image='tank_2.png')
                level[y][x] = "."
            elif level[y][x] == '1':
                print(x, y)
                tank_1 = Tank(radius=45, x_tank=x * 100, y_tank=y * 100, rotate=90, keyboard='udlr', image='tank.png')
                level[y][x] = "."
    return tank_1, tank_2, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = load_image('wall.png')
        self.rect = self.image.get_rect().move(
            100 * (pos_x - 1), 100 * (pos_y - 1))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, direction, speed):
        super().__init__(shards)
        self.direction = direction
        self.speed = speed
        self.image = load_image(image, -1)
        self.rect = pygame.Rect(x, y, 30, 30)
        print(1)

    def update(self):
        if self.direction == 0:
            self.rect = self.rect.move(0, -self.speed)
            print(2)
        if self.direction == 180:
            self.rect = self.rect.move(0, self.speed)
        if self.direction == 90:
            self.rect = self.rect.move(self.speed, 0)
        if self.direction == 270:
            self.rect = self.rect.move(-self.speed, 0)
        #if pygame.sprite.spritecollideany(self, all_sprites):
            #self.kill()


class Tank(pygame.sprite.Sprite):
    def __init__(self, radius, x_tank, y_tank, rotate, keyboard, image):
        super().__init__(tanks)
        self.image = load_image(image, -1)
        self.rect = pygame.Rect(x_tank, y_tank, 2 * radius, 2 * radius)
        self.x, self.y = x_tank, y_tank
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
        tank_move(self, self.angles[direction], self.speed)
        print(self.y, self.x)
        self.direction = self.angles[direction]


all_sprites = pygame.sprite.Group()
tanks = pygame.sprite.Group()
shards = pygame.sprite.Group()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

size = width, height = 1900, 1000
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
flag_1 = False
flag_2 = False
event_key_2 = '78'
event_key_1 = '56'
level_map = load_level(random.choice(("tanks_map.map", "tank_map_1.map", "tank_map_2.map")))
Tank_1, Tank_2, max_x, max_y = generate_level(level_map)
running = True
while running:
    if flag_1 is True:
        tanks.update(event_key_1)
    if flag_2 is True:
        tanks.update(event_key_2)
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
            if event.key == pygame.K_e:
                if Tank_2.direction == 0:
                    Bullet(Tank_2.x + 30, Tank_2.y - 50, 'Cacodemon.png', 0, Tank_2.bullet_speed)
                if Tank_2.direction == 180:
                    Bullet(Tank_2.x + 30, Tank_2.y + 100, 'Cacodemon.png', 180, Tank_2.bullet_speed)
                if Tank_2.direction == 90:
                    Bullet(Tank_2.x + 100, Tank_2.y + 25, 'Cacodemon.png', 90, Tank_2.bullet_speed)
                if Tank_2.direction == 270:
                    Bullet(Tank_2.x - 30, Tank_2.y + 25, 'Cacodemon.png', 270, Tank_2.bullet_speed)
            tanks.update(event.key)
        elif event.type == pygame.KEYUP:
            if if_control_key(event.key) == 1:
                flag_1 = False
            elif if_control_key(event.key) == 2:
                flag_2 = False
        shards.update()
    fon = pygame.transform.scale(load_image('Fon.jpg'), size)
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    tanks.draw(screen)
    shards.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
