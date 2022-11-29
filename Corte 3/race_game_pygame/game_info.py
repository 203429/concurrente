import time, sys, random, paths
from player_car import PlayerCar
from computer_car import ComputerCar
from settings import *
from utils import blit_text_center

class GameInfo:
    LEVELS = 3
    
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

        self.player_car = PlayerCar(CAR1, CAR1_POS, 6,4)

        type_path = random.randint(0,3)
        self.computer_car = ComputerCar(self, CAR2, CAR2_POS, 2, 4, paths.PATHS_LV1[type_path])
        self.computer_car.start()

        type_path = random.randint(0,3)
        self.computer_car2 = ComputerCar(self, CAR3, CAR3_POS, 2, 4, paths.PATHS_LV1[type_path])
        self.computer_car2.start()

        type_path = random.randint(0,3)
        self.computer_car3 = ComputerCar(self, CAR4, CAR4_POS, 2, 4, paths.PATHS_LV1[type_path])
        self.computer_car3.start()

    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)
    
    def draw_player(self):
        level_text = INFO_FONT.render(f"Level {self.level}", 1, (122, 17, 17))
        WIN.blit(level_text, (5, 5))

        time_text = INFO_FONT.render(f"Time: {self.get_level_time()}s", 1, (122, 17, 17))
        WIN.blit(time_text, (5, 40))

        vel_text = INFO_FONT.render(f"Vel: {round(self.player_car.vel)}px/s", 1, (122, 17, 17))
        WIN.blit(vel_text, (5, 75))

        self.player_car.draw(WIN)
        self.computer_car.draw(WIN)
        self.computer_car2.draw(WIN)
        self.computer_car3.draw(WIN)
        pygame.display.update()

    def move_player(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            self.player_car.rotate(left=True)
        if keys[pygame.K_d]:
            self.player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            self.player_car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            self.player_car.move_backward()

        if not moved:
            self.player_car.reduce_speed()

    def handle_collision(self):
        if self.player_car.collide(TRACK_BORDER_MASK) != None:
            self.player_car.bounce()

        player_finish_poi_collide = self.player_car.collide(FINISH_MASK, *FINISH_POS)
        if player_finish_poi_collide != None:
            if player_finish_poi_collide[1] == 0:
                self.player_car.bounce()
            else:
                self.next_level()
                self.player_car.reset(CAR1_POS)
                self.computer_car.next_level(self.level, CAR2_POS)
                self.computer_car2.next_level(self.level, CAR3_POS)
                self.computer_car3.next_level(self.level, CAR4_POS)

    def computer_wins(self, computer_car, start_pos):
        computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POS)
        if computer_finish_poi_collide != None:
            blit_text_center(WIN, MAIN_FONT, "You lost!")
            pygame.display.update()
            pygame.time.wait(5000)
            self.reset()
            self.player_car.reset(CAR1_POS)
            computer_car.reset(start_pos)

    def run(self):
        self.draw_player()
        self.move_player()
        self.computer_car.move()
        self.computer_car2.move()
        self.computer_car3.move()
        self.handle_collision()

        if self.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()