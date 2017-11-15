#!/usr/bin/env python3
import configparser
import os
import pygame
import requests
import sys
import json
# TODO: Fix warnings and typos


def main(args):
    # Get configurations
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/conf.ini')

    # Initialization
    pygame.init()
    clock = pygame.time.Clock()

    # Set game display
    if config.get('global', 'FULLSCREEN') == '1':
        fullscreen = pygame.FULLSCREEN
    else:
        fullscreen = 0

    screen = pygame.display.set_mode((int(config.get('global', 'X_RES')), int(config.get('global', 'Y_RES'))), fullscreen)

    # Set window caption
    pygame.display.set_caption(config.get('global', 'TITLE'))

    # Get theme
    try:
        theme_name = config.get('global', 'THEME')
        theme_class = getattr(__import__('themes.' + theme_name, fromlist=[theme_name]), theme_name)
    except (ModuleNotFoundError, configparser.NoOptionError):
        theme_class = getattr(__import__('themes.Fallback', fromlist=['Fallback']), 'Fallback')

    theme = theme_class(pygame, screen, (int(config.get('global', 'X_RES')), int(config.get('global', 'Y_RES'))))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        # Get game data
        try:
            # If debug mode, use sample JSON
            if len(args) > 1 and 'debug' in args:
                with open(os.path.dirname(os.path.realpath(__file__)) + '/crest2.json') as json_data:
                    theme.refresh(json.load(json_data))
            else:
                theme.refresh(requests.get(url, timeout=0.1).json())
        except requests.exceptions.ConnectionError: # Cannot connect to host
            # TODO: Make it prettier, and use relative font size?
            screen.fill((0, 0, 0))
            screen.blit(pygame.font.SysFont(None, 32).render('Connection error! Is Host IP address correct? Is CREST running?', True, (255, 255, 255)), (10, 10))
        except requests.exceptions.ReadTimeout:
            pass
        except KeyError: # PCARS is not running or Shared Memory is disabled
            # TODO: Make it prettier, and use relative font size?
            screen.fill((0, 0, 0))
            screen.blit(pygame.font.SysFont(None, 28).render('Connection successful! Please run Project CARS with Shared Memory enabled.', True, (255, 255, 255)), (10, 10))

        pygame.display.update()
        clock.tick(int(config.get('global', 'FPS')))


if __name__ == '__main__':
    main(sys.argv)

