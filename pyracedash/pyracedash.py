import configparser
import os
import pygame
import requests
import sys
import json
from themes.fallback import Fallback


def main():
    # Get configurations
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/../conf.ini')

    # Initialization
    pygame.init()
    clock = pygame.time.Clock()

    # Set game display
    screen = pygame.display.set_mode((int(config.get('global', 'X_RES')), int(config.get('global', 'Y_RES'))))

    # Set window caption
    pygame.display.set_caption(config.get('global', 'TITLE'))

    # Get theme
    theme = Fallback(pygame, screen, (int(config.get('global', 'X_RES')), int(config.get('global', 'Y_RES'))))

    # Create request url
    url = 'http://' + config.get('host', 'IP_ADDRESS') + ':' + config.get('host', 'PORT') + '/crest'
    if config.get('host', 'PORT') == '8180':
        url += '2'
    url += '/v1/api'
    if len(theme.needed_modules) > 0:
        url += '?'
        for module in theme.needed_modules:
            url += module + '=true&'

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Get game data
        try:
            # If debug mode, use sample JSON
            if len(sys.argv) > 1 and sys.argv[1] == 'debug':
                with open(os.path.dirname(os.path.realpath(__file__)) + '/crest2.json') as json_data:
                    theme.refresh(json.load(json_data))
            else:
                theme.refresh(requests.get(url, timeout=0.1).json())
        except requests.exceptions.ConnectionError: # Cannot connect to host TODO: Percantik
            screen.fill((255, 0, 0))
        except requests.exceptions.ReadTimeout:
            screen.fill((0, 255, 0))
        except KeyError:
            screen.fill((255, 255, 255))

        pygame.display.update()
        clock.tick(int(config.get('global', 'FPS')))


if __name__ == '__main__':
    main()

