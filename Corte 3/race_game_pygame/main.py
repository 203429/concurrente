import pygame, time, math, sys, random, threading, paths
from utils import scale_image, blit_rotate_center, blit_text_center

from game_info import GameInfo
from player_car import PlayerCar
from computer_car import ComputerCar

pygame.init()
pygame.font.init()

GRASS = scale_image(pygame.image.load("imgs/grass.png"), 6)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 1.6)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 1.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = scale_image(pygame.image.load("imgs/finish.png"), 0.9)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (960,570)

CAR1 = scale_image(pygame.image.load("imgs/car1.png"), 0.8)
CAR1_POS = (1015, 480)
CAR2 = scale_image(pygame.image.load("imgs/car2.png"), 0.8)
CAR2_POS = (980, 480)
CAR3 = scale_image(pygame.image.load("imgs/car3.png"), 0.8)
CAR3_POS = (980, 390)

WIDTH, HEIGHT = GRASS.get_width(), GRASS.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula UP")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)
INFO_FONT = pygame.font.SysFont("standard-block",49)

FPS = 60

def draw(win, images, player_car, computer_car, game_info):
    for img,pos in images:
        win.blit(img,pos)

    level_text = INFO_FONT.render(f"Level {game_info.level}", 1, (122, 17, 17))
    win.blit(level_text, (5, 5))

    time_text = INFO_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (122, 17, 17))
    win.blit(time_text, (5, 40))

    vel_text = INFO_FONT.render(f"Vel: {round(player_car.vel)}px/s", 1, (122, 17, 17))
    win.blit(vel_text, (5, 75))

    player_car.draw(win)
    computer_car.draw(win)
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

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POS)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset(CAR1_POS)
        computer_car.reset(CAR2_POS)

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset(CAR1_POS)
            computer_car.next_level(game_info.level, CAR2_POS)

def main(clock, images, player_car, computer_car, game_info):
    while True:
        clock.tick(FPS)

        draw(WIN, images, player_car, computer_car, game_info)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     computer_car.path.append(pos)

        move_player(player_car)
        computer_car.move()

        handle_collision(player_car, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    clock = pygame.time.Clock()
    images = [(GRASS, (0,0)),(TRACK, (-30,120)),(FINISH, FINISH_POS)]

    player_car = PlayerCar(CAR1, CAR1_POS, 6,4)

    type_path = random.randint(0,3)
    computer_car = ComputerCar(CAR2, CAR2_POS, 2, 4, paths.PATHS_LV1[type_path])

    game_info = GameInfo()
    CARS_POS = []
    main(clock, images, player_car, computer_car, game_info)