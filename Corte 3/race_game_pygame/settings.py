from utils import scale_image
import pygame

ICON = pygame.image.load("imgs/icon.png")

GRASS = scale_image(pygame.image.load("imgs/grass.png"), 6)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 1.6)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 1.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

WIDTH, HEIGHT = GRASS.get_width(), GRASS.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

FINISH = scale_image(pygame.image.load("imgs/finish.png"), 0.9)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (960,570)

images = [(GRASS, (0,0)),(TRACK, (-30,120)),(FINISH, FINISH_POS)]

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)
INFO_FONT = pygame.font.SysFont("standard-block",49)

CAR1 = scale_image(pygame.image.load("imgs/car1.png"), 0.8)
CAR1_POS = (1017, 510)
CAR2 = scale_image(pygame.image.load("imgs/car2.png"), 0.8)
CAR2_POS = (974, 510)
CAR3 = scale_image(pygame.image.load("imgs/car3.png"), 0.8)
CAR3_POS = (974, 448)
CAR4 = scale_image(pygame.image.load("imgs/car3.png"), 0.8)
CAR4_POS = (1017, 448)