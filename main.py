import pygame
import os
from utils.config import WIDTH, HEIGHT, WINDOW_TITLE
from controllers.game_controller import GameController

def main():
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Create and run the game controller
    game = GameController(screen)
    game.run()

if __name__ == "__main__":
    main()