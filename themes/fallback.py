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
    rpm_color = (102, 252, 255)
    rpm_font_name = global_font
    rpm_font_size = 60

    # Speed
    speed_color = (126, 41, 255)
    speed_font_name = global_font
    speed_font_size = 250

    # kmh Label
    kmh_label_color = (255, 255, 255)
    kmh_label_font_name = global_font
    kmh_label_font_size = 80

    # Delta time
    delta_front_color = (255, 0, 0)
    delta_back_color = (0, 240, 32)
    delta_font_name = global_font
    delta_font_size = 60

    # Delta time label
    delta_label_color = (255, 255, 255)
    delta_label_font_name = global_font
    delta_label_font_size = 25

    # Fuel
    fuel_font_name = global_font
    fuel_font_size = 230

    # Fuel label
    fuel_label_color = (255, 255, 255)
    fuel_label_font_name = global_font
    fuel_label_font_size = 80

    # Lap time
    lap_time_font_name = global_font
    lap_time_font_size = delta_font_size

    def __init__(self, pygame, screen, display_resolution):
        '''Init. Pass pygame, screen and display resolution as parameter.'''
        self.pygame = pygame
        self.display_resolution = display_resolution
        self.screen = screen

        # Fonts
        self.gear_font = pygame.font.SysFont(self.gear_font_name, self.gear_font_size)
        self.rpm_font = pygame.font.SysFont(self.rpm_font_name, self.rpm_font_size)
        self.speed_font = pygame.font.SysFont(self.speed_font_name, self.speed_font_size)
        self.kmh_label_font = pygame.font.SysFont(self.kmh_label_font_name, self.kmh_label_font_size)
        self.delta_font = pygame.font.SysFont(self.delta_font_name, self.delta_font_size)
        self.delta_label_font = pygame.font.SysFont(self.delta_label_font_name, self.delta_label_font_size)
        self.fuel_font = pygame.font.SysFont(self.fuel_font_name, self.fuel_font_size)
        self.fuel_label_font = pygame.font.SysFont(self.fuel_label_font_name, self.fuel_label_font_size)
        self.lap_time_font = pygame.font.SysFont(self.lap_time_font_name, self.lap_time_font_size)

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

    def print_split_time(self, time, pos='ahead'):
        '''Print split time. "-" if ahead, and "+" if behind.'''
        out = '-'
        if pos == 'behind':
            out = '+'

        if time == -1:
            return '-----'
        else:
            return out + str("%.3f" % time)

    def print_fuel(self, fuel_current, fuel_capacity):
        '''Return current fuel in liter and its color level.'''
        if fuel_current >= 0.5:
            color = (0, 0, 255)
        elif fuel_current >= 0.3:
            color = (0, 255, 0)
        elif fuel_current >= 0.15:
            color = (255, 255, 0)
        elif fuel_current >= 0.1:
            color = (255, 127, 0)
        else:
            color = (255, 0, 0)
        return (int(fuel_current * fuel_capacity), color)

    def print_lap_time(self, time_in_s):
        '''Return lap time in this format: Minute:Second:Milisecond'''
        if time_in_s == -1:
            return '--.--.---'
        else:
            min = str(int(time_in_s / 60))
            sec = str("%.3f" % (time_in_s % 60))

            if int(min) < 10:
                min = '0' + min
            if float(sec) < 10:
                sec = '0' + sec

            return min + '.' + sec

    def refresh(self, json_from_request):
        '''Refresh screen from every incoming request.'''
        self.screen.fill(self.background_color)

        # Gear
        gear = self.gear_font.render(self.print_gear(json_from_request['carState']['mGear']), self.anti_aliasing, self.gear_color)
        x_centered = self.display_resolution[0] / 2
        gear_pos_x = x_centered - gear.get_rect().width / 2
        y_centered = self.display_resolution[1]
        gear_pos_y = y_centered / 2 - gear.get_rect().height / 2
        self.screen.blit(gear, (gear_pos_x, gear_pos_y))

        # RPM
        rpm = self.rpm_font.render(str(int(json_from_request['carState']['mRpm'])), self.anti_aliasing, self.rpm_color)
        rpm_pos_x = x_centered - rpm.get_rect().width / 2
        rpm_pos_y = gear_pos_y - 30
        self.screen.blit(rpm, (rpm_pos_x, rpm_pos_y))

        # Speed
        speed = self.speed_font.render(str(self.speed_in_kph(json_from_request['carState']['mSpeed'])), self.anti_aliasing, self.speed_color)
        speed_pos_x = self.display_resolution[0] - 10 - speed.get_rect().width
        speed_pos_y = gear_pos_y
        self.screen.blit(speed, (speed_pos_x, speed_pos_y))

        # kmh Label
        kmh_label = self.kmh_label_font.render('km/h', self.anti_aliasing, self.kmh_label_color)
        kmh_label_pos_x = self.display_resolution[0] - 10 - kmh_label.get_rect().width
        kmh_label_pos_y = gear_pos_y + gear.get_rect().height - kmh_label.get_rect().height - 40
        self.screen.blit(kmh_label, (kmh_label_pos_x, kmh_label_pos_y))

        # Delta time
        delta_front = self.delta_font.render(self.print_split_time(json_from_request['timings']['mSplitTimeAhead']), self.anti_aliasing, self.delta_front_color)
        delta_front_pos_x = x_centered - delta_front.get_rect().width / 2
        delta_front_pos_y = kmh_label_pos_y + 85
        self.screen.blit(delta_front, (delta_front_pos_x, delta_front_pos_y))

        delta_back = self.delta_font.render(self.print_split_time(json_from_request['timings']['mSplitTimeBehind'], 'behind'), self.anti_aliasing, self.delta_back_color)
        delta_back_pos_x = x_centered - delta_back.get_rect().width / 2
        delta_back_pos_y = delta_front_pos_y + 70
        self.screen.blit(delta_back, (delta_back_pos_x, delta_back_pos_y))

        # Delta time label
        delta_front_label = self.delta_label_font.render('Split Time Ahead', self.anti_aliasing, self.delta_label_color)
        delta_front_label_pos_x = x_centered - delta_front_label.get_rect().width / 2
        delta_front_label_pos_y = delta_front_pos_y - 23
        self.screen.blit(delta_front_label, (delta_front_label_pos_x, delta_front_label_pos_y))

        delta_back_label = self.delta_label_font.render('Split Time Behind', self.anti_aliasing, self.delta_label_color)
        delta_back_label_pos_x = x_centered - delta_back_label.get_rect().width / 2
        delta_back_label_pos_y = delta_back_pos_y - 23
        self.screen.blit(delta_back_label, (delta_back_label_pos_x, delta_back_label_pos_y))

        # Fuel
        fuel_output = self.print_fuel(json_from_request['carState']['mFuelLevel'], json_from_request['carState']['mFuelCapacity'])
        fuel = self.fuel_font.render(str(fuel_output[0]), self.anti_aliasing, fuel_output[1])
        fuel_pos_x = 10
        fuel_pos_y = gear_pos_y
        self.screen.blit(fuel, (fuel_pos_x, fuel_pos_y))

        # Fuel label
        fuel_label = self.fuel_label_font.render('Fuel/kg', self.anti_aliasing, self.fuel_label_color)
        self.screen.blit(fuel_label, (fuel_pos_x, gear_pos_y + gear.get_rect().height - fuel_label.get_rect().height - 40))

        # Lap time
        lap_time = self.lap_time_font.render(self.print_lap_time(json_from_request['timings']['mCurrentTime']), self.anti_aliasing, (255, 255,255))
        self.screen.blit(lap_time, (fuel_pos_x, delta_front_pos_y))

        # Last lap
        last_lap_time = self.lap_time_font.render(self.print_lap_time(json_from_request['timings']['mLastLapTime']), self.anti_aliasing, (255, 255, 255))
        self.screen.blit(last_lap_time, (fuel_pos_x, delta_back_pos_y))

