import pygame, requests


def speed_in_kph(speed_in_mps):
    return int(speed_in_mps * 3.6)

def print_gear(gear):
    if gear == 0:
        return 'N'
    elif gear == -1:
        return 'R'
    else:
        return str(gear)

def main():
    # Constants
    DISPLAY_RESOLUTIONS = (800, 480)
    WINDOW_TITLE = "Kuat Hadianto's pyracedash"
    FRAMES_PER_SECOND = 60
    IP_ADDRESS = '192.168.0.67'
    CREST_PORT = '8080'
    NEEDED_MODULES = ['carState', 'timings']  # TODO: Disamakan berdasarkan HUD class?

    # Initialization
    pygame.init()
    clock = pygame.time.Clock()

    # Set game display
    screen = pygame.display.set_mode(DISPLAY_RESOLUTIONS)

    # Set window caption
    pygame.display.set_caption(WINDOW_TITLE)

    # Create request url
    url = 'http://' + IP_ADDRESS + ':' + CREST_PORT + '/crest'
    if CREST_PORT == '8180':
        url += '2'
    url += '/v1/api'
    if len(NEEDED_MODULES) > 0:
        url += '?'
        for module in NEEDED_MODULES:
            url += module + '=true&'

    # Variables for drawing
    BACKGROUND_COLOR = (0, 0, 0)
    ELEMENT_ALL_ANTI_ALIASING = True

    # Gear
    ELEMENT_GEAR_FONT = pygame.font.SysFont(None, 380)
    ELEMENT_GEAR_COLOR = ((255, 204, 0))

    # RPM
    ELEMENT_FONT_RPM = pygame.font.SysFont(None, 60)
    ELEMENT_RPM_COLOR = (255, 255, 255)

    # Speed
    ELEMENT_SPEED_FONT = pygame.font.SysFont(None, 180)
    ELEMENT_SPEED_COLOR = (255, 255, 255)

    # Game loop
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        # Get game data
        try:
            r = requests.get(url, timeout=0.1).json()
        except requests.exceptions.ConnectionError: # Cannot connect to host TODO: Percantik
            screen.fill((255, 0, 0))
            pygame.display.update()
            continue

        screen.fill(BACKGROUND_COLOR)

        # Gear
        ELEMENT_GEAR = ELEMENT_GEAR_FONT.render(print_gear(r['carState']['mGear']), ELEMENT_ALL_ANTI_ALIASING, ELEMENT_GEAR_COLOR)
        ELEMENT_GEAR_POS_X = DISPLAY_RESOLUTIONS[0]/2 - ELEMENT_GEAR.get_rect().width/2
        ELEMENT_GEAR_POS_Y = DISPLAY_RESOLUTIONS[1]/2 - ELEMENT_GEAR.get_rect().height/2
        screen.blit(ELEMENT_GEAR, (ELEMENT_GEAR_POS_X, ELEMENT_GEAR_POS_Y))

        # RPM
        ELEMENT_RPM = ELEMENT_FONT_RPM.render(str(int(r['carState']['mRpm'])), ELEMENT_ALL_ANTI_ALIASING, ELEMENT_RPM_COLOR)
        ELEMENT_RPM_HEIGHT_OFFSET = -140
        ELEMENT_RPM_POS_X = DISPLAY_RESOLUTIONS[0]/2 - ELEMENT_RPM.get_rect().width/2
        ELEMENT_RPM_POS_Y = DISPLAY_RESOLUTIONS[1]/2 - ELEMENT_RPM.get_rect().height/2 + ELEMENT_RPM_HEIGHT_OFFSET
        screen.blit(ELEMENT_RPM, (ELEMENT_RPM_POS_X, ELEMENT_RPM_POS_Y))

        # Speed
        ELEMENT_SPEED = ELEMENT_SPEED_FONT.render(str(speed_in_kph(r['carState']['mSpeed'])), ELEMENT_ALL_ANTI_ALIASING, ELEMENT_SPEED_COLOR)
        ELEMENT_SPEED_WIDTH_OFFSET = 380
        ELEMENT_SPEED_HEIGHT_OFFSET = -50
        ELEMENT_SPEED_POS_X = DISPLAY_RESOLUTIONS[0]/2 - ELEMENT_SPEED.get_rect().width + ELEMENT_SPEED_WIDTH_OFFSET
        ELEMENT_SPEED_POS_Y = DISPLAY_RESOLUTIONS[1]/2 - ELEMENT_SPEED.get_rect().height/2 + ELEMENT_SPEED_HEIGHT_OFFSET
        screen.blit(ELEMENT_SPEED, (ELEMENT_SPEED_POS_X, ELEMENT_SPEED_POS_Y))

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)


if __name__ == '__main__':
    main()
