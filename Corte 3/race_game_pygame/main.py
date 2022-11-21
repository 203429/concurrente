import pygame, time, math, sys
from utils import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.png"), 6)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 1.6)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 1.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")

CAR1 = scale_image(pygame.image.load("imgs/car1.png"), 0.8)

WIDTH, HEIGHT = GRASS.get_width(), GRASS.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula UP")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.3

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=-30, y=120):
        car_mark = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mark, offset)
        return poi

class PlayerCar(AbstractCar):
    IMG = CAR1
    START_POS = (1000, 430)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

def draw(win, images, player_car):
    for img,pos in images:
        win.blit(img,pos)

    player_car.draw(win)
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

clock = pygame.time.Clock()
images = [(GRASS, (0,0)),(TRACK, (-30,120))]
player_car = PlayerCar(7,3)

while True:
    clock.tick(FPS)

    draw(WIN, images, player_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()