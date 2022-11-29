import pygame, sys
from settings import *
from game_info import GameInfo
from utils import blit_text_center

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Formula UP")
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.game_info = GameInfo()

    def run(self):
        while True:
            self.clock.tick(FPS)

            for img,pos in images:
                self.win.blit(img,pos)

            while not self.game_info.started:
                blit_text_center(self.win, MAIN_FONT, f"Press W key to start level {self.game_info.level}!")
                pygame.display.update()
                self.game_info.draw_player()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w]:
                        self.game_info.start_level()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.game_info.run()

if __name__ == '__main__':
    game = Game()
    game.run()