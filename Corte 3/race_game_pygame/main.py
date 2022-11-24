import pygame, time, math, sys, random
from utils import scale_image, blit_rotate_center, blit_text_center
import paths
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

class GameInfo:
    LEVELS = 3
    
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

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

class AbstractCar:
    def __init__(self, img, start_pos, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        # self.img = self.IMG
        # self.x, self.y = self.START_POS
        self.img = img
        self.x, self.y = start_pos
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

    def reset(self, start_pos):
        self.x, self.y = start_pos
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class ComputerCar(AbstractCar):
    def __init__(self, img, start_pos, max_vel, rotation_vel, path=[]):
        super().__init__(img, start_pos, max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        
        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level, start_pos):
        self.reset(start_pos)
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

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
                    # print(computer_car.path)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print(computer_car.path)
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
            game_info.reset()
            player_car.reset(CAR1_POS)
            computer_car.reset(CAR2_POS)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    images = [(GRASS, (0,0)),(TRACK, (-30,120)),(FINISH, FINISH_POS)]

    player_car = PlayerCar(CAR1, CAR1_POS, 5,4)

    type_path = random.randint(0,4)
    computer_car = ComputerCar(CAR2, CAR2_POS, 2, 4, paths.PATHS_LV1[type_path])
    # computer_car2 = ComputerCar(CAR3, CAR3_POS, 2, 4, PATH1)
    game_info = GameInfo()
    CARS_POS = []
    main(clock, images, player_car, computer_car, game_info)