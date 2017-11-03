class Fallback:
    '''Fallback template, if no matched template found.'''

    needed_modules = ['carState', 'timings']

    # Variables for drawing
    background_color = (0, 0, 0)
    anti_aliasing = True
    global_font = None

    # Gear
    gear_color = ((255, 204, 0))
    gear_font_name = global_font
    gear_font_size = 380

    # RPM
    rpm_color = (255, 255, 255)
    rpm_font_name = global_font
    rpm_font_size = 60

    # Speed
    speed_color = (255, 255, 255)
    speed_font_name = global_font
    speed_font_size = 180

    def __init__(self, pygame, screen, display_resolution):
        '''Init. Pass pygame, screen and display resolution as parameter.'''
        self.pygame = pygame
        self.display_resolution = display_resolution
        self.screen = screen

        # Fonts
        self.gear_font = pygame.font.SysFont(self.gear_font_name, self.gear_font_size)
        self.rpm_font = pygame.font.SysFont(self.rpm_font_name, self.rpm_font_size)
        self.speed_font = pygame.font.SysFont(self.speed_font_name, self.speed_font_size)

    def speed_in_kph(self, speed_in_mps):
        '''Convert speed from meter per second to kilometer per hour.'''
        return int(speed_in_mps * 3.6)

    def print_gear(self, gear):
        '''Print current gear.'''
        if gear == 0:
            return 'N'
        elif gear == -1:
            return 'R'
        else:
            return str(gear)

    def refresh(self, json_from_request):
        '''Refresh screen from every incoming request.'''
        self.screen.fill(self.background_color)

        # Gear
        gear = self.gear_font.render(self.print_gear(json_from_request['carState']['mGear']), self.anti_aliasing, self.gear_color)
        gear_pos_x = self.display_resolution[0] / 2 - gear.get_rect().width / 2
        gear_pos_y = self.display_resolution[1] / 2 - gear.get_rect().height / 2
        self.screen.blit(gear, (gear_pos_x, gear_pos_y))

        # RPM
        rpm = self.rpm_font.render(str(int(json_from_request['carState']['mRpm'])), self.anti_aliasing, self.rpm_color)
        rpm_pos_x = self.display_resolution[0] / 2 - rpm.get_rect().width / 2
        rpm_pos_y = gear_pos_y - 30
        self.screen.blit(rpm, (rpm_pos_x, rpm_pos_y))

        # Speed
        speed = self.speed_font.render(str(self.speed_in_kph(json_from_request['carState']['mSpeed'])), self.anti_aliasing, self.speed_color)
        speed_pos_x = self.display_resolution[0] - 30 - speed.get_rect().width
        speed_pos_y = gear_pos_y
        self.screen.blit(speed, (speed_pos_x, speed_pos_y))
