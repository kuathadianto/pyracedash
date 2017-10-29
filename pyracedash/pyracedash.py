import pygame
from templates import *


def main():
    # Constants
    DISPLAY_RESOLUTIONS = (800, 480)
    WINDOW_TITLE = "Kuat Hadianto's pyracedash"
    FRAMES_PER_SECOND = 60

    # Initialization
    pygame.init()
    clock = pygame.time.Clock()

    # Set game display
    pygame.display.set_mode(DISPLAY_RESOLUTIONS)

    # Set window caption
    pygame.display.set_caption(WINDOW_TITLE)

    # Game loop
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                game_exit = True

        clock.tick(FRAMES_PER_SECOND)


if __name__ == '__main__':
    main()
