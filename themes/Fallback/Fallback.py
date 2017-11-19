# TODO: Docstring every functions
class Fallback:
    """
    Fallback theme, if no matched theme found.
    Or use this as template to make a new theme.
    The name of this class and this file should be the same and case sensitive.
    """
    # CREST Modules that this theme use
    needed_modules = ['carState', 'timings', 'eventInformation', 'participants', 'gameStates']

    # These attributes below are optional, and only meant to use for this theme only.
    # All with None value and screen_center are reserved, and initialized on __init__
    config = None
    theme_color = {
        'label': (255, 255, 255),
        'default_background': (0, 0, 0),
        'background_flash': (122, 0, 0),
        'gear': (255, 204, 0),
        'rpm_circle_low': (0, 0, 255),
        'rpm_circle_mid': (0, 255, 0),
        'rpm_circle_hi': (255, 0, 0),
        'speed': (126, 41, 255),
        'fuel': [
            (0.5, (0, 0, 255)),
            (0.3, (0, 255, 0)),
            (0.15, (255, 255, 0)),
            (0.1, (255, 127, 0)),
            (0, (255, 0, 0))
        ],
        'fuel_last_lap': (26, 206, 137)
    }
    font_size = {
        'gear': None,
        'speed': None,
        'fuel': None,
        'label': None
    }
    parameter_value = {
        'hi_rpm_percentage': 0.95,
        'rpm_percentage_list': [0.5, 0.6, 0.7, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.915, 0.93, 0.945],
        'rpm_circle_radius': None,
        'rpm_meter_range_per_circle': None,
    }
    object_position = {
        'rpm_meter_y': None,
        'screen_center': (0, 0),
        'upper_label_y': None
    }
    flashing_object = {
        'background': {
            'visible': True,
            'counter': 0,
            'counter_max': 3
        },
        'fuel_warning': {
            'visible': True,
            'counter': 0,
            'counter_max': 30
        }
    }

    # These methods are needed and should be exist in every theme class:
    # __init__(self, pygame, screen, display_resolution)
    # refresh(self, json_from_request)
    def __init__(self, pygame, screen, display_resolution):
        # These 3 initialization are required
        self.pygame = pygame
        self.display_resolution = display_resolution
        self.screen = screen

        # From here is optional
        self.object_position['screen_center'] = (display_resolution[0] / 2, display_resolution[1] / 2)
        if self.font_size['gear'] is None:
            self.font_size['gear'] = int(display_resolution[1] / 1.263157894736842)
        if self.parameter_value['rpm_circle_radius'] is None:
            self.parameter_value['rpm_circle_radius'] = int(display_resolution[1] / 17.78)
        if self.object_position['rpm_meter_y'] is None:
            self.object_position['rpm_meter_y'] = self.object_position['screen_center'][1] / 6
        if self.parameter_value['rpm_meter_range_per_circle'] is None:
            self.parameter_value['rpm_meter_range_per_circle'] = int(display_resolution[0] / 66)
        if self.font_size['speed'] is None:
            self.font_size['speed'] = int(display_resolution[1] / 2.67)
        if self.font_size['fuel'] is None:
            self.font_size['fuel'] = int(display_resolution[1] / 3)
        if self.font_size['label'] is None:
            self.font_size['label'] = int(display_resolution[1] / 16)
        if self.object_position['upper_label_y'] is None:
            self.object_position['upper_label_y'] = int(display_resolution[1] / 48)

    def refresh(self, game_data):
        """
        Draw everything written here to the main screen. This method will be called every 1/FPS seconds.
        :param game_data: JSON from request. Dict type.
        :return: None (void)
        """
        self.draw_background(game_data['carState']['mRpm'],
                             game_data['carState']['mMaxRPM'],
                             self.parameter_value['hi_rpm_percentage'],
                             self.theme_color['default_background'],
                             self.theme_color['background_flash'])

        gear_surface_rect = self.print_gear(game_data['carState']['mGear'],
                                            self.font_size['gear'],
                                            self.theme_color['gear'],
                                            self.object_position['screen_center'])

        try:
            rpm = game_data['carState']['mRpm'] / game_data['carState']['mMaxRPM']
        except ZeroDivisionError:
            rpm = 0
        rpm_meter_surface_rect = self.draw_rpm_meter(rpm,
                                                     self.parameter_value['rpm_percentage_list'],
                                                     self.parameter_value['rpm_circle_radius'],
                                                     self.object_position['rpm_meter_y'],
                                                     self.parameter_value['rpm_meter_range_per_circle'],
                                                     self.theme_color['rpm_circle_low'],
                                                     self.theme_color['rpm_circle_mid'],
                                                     self.theme_color['rpm_circle_hi'])

        # x edge of RPM meter
        x_edge_rpm = int(self.display_resolution[0] - rpm_meter_surface_rect.width) / 2

        speed_surface_rect = self.print_speed(game_data['carState']['mSpeed'],
                                              self.font_size['speed'],
                                              self.theme_color['speed'],
                                              (self.display_resolution[0] - x_edge_rpm,
                                               self.object_position['screen_center'][1]),
                                              'right', 'middle')

        fuel_surface_rect = self.print_fuel(game_data['carState']['mFuelLevel'], game_data['carState']['mFuelCapacity'],
                                            self.font_size['fuel'],
                                            self.theme_color['fuel'],
                                            (x_edge_rpm, self.object_position['screen_center'][1]
                                             - (gear_surface_rect.height / 2)))

        # On game only calculations
        if game_data['participants']['mNumParticipants'] != -1:
            # Driver name
            self.print_text(game_data['participants']['mParticipantInfo'][0]['mName'],
                            self.font_size['label'], self.theme_color['label'],
                            (self.display_resolution[0] - x_edge_rpm, self.object_position['upper_label_y']),
                            horizontal_align='right', vertical_align='top')

            # Lap or remaining time
            if game_data['timings']['mEventTimeRemaining'] == -1:   # Indeed lap race
                lap = str(game_data['participants']['mParticipantInfo'][0]['mCurrentLap'])
                total_laps = str(game_data['eventInformation']['mLapsInEvent'])
                self.print_text('LAP: ' + lap + '/' + total_laps, self.font_size['label'],
                                self.theme_color['label'], (x_edge_rpm, self.object_position['upper_label_y']))
            else:   # Time race
                self.print_text('TIME: ' + self.float_to_time(game_data['timings']['mEventTimeRemaining']),
                                self.font_size['label'], self.theme_color['label'],
                                (x_edge_rpm, self.object_position['upper_label_y']))
            # Position
            self.print_text(' POS: ' + str(game_data['participants']['mParticipantInfo'][0]['mRacePosition']) + '/'
                            + str(game_data['participants']['mNumParticipants']),
                            self.font_size['label'], self.theme_color['label'],
                            (self.object_position['screen_center'][0], self.object_position['upper_label_y']),
                            horizontal_align='center')

            # Fuel last lap
            if game_data['timings']['mCurrentTime'] < 2 and game_data['timings']['mLastLapTime'] == -1:
                self.IN_GAME_CURRENT_FUEL = game_data['carState']['mFuelLevel']
                self.IN_GAME_LAST_LAP_TIME = game_data['timings']['mLastLapTime']
                self.IN_GAME_LAST_FUEL_USAGE = 0
                self.IN_GAME_FUEL_WARNING = False
            elif game_data['timings']['mLastLapTime'] != self.IN_GAME_LAST_LAP_TIME:
                self.IN_GAME_LAST_LAP_TIME = game_data['timings']['mLastLapTime']
                self.IN_GAME_LAST_FUEL_USAGE = self.IN_GAME_CURRENT_FUEL - game_data['carState']['mFuelLevel']
                self.IN_GAME_CURRENT_FUEL = game_data['carState']['mFuelLevel']
                # Not enough fuel warning
                if self.IN_GAME_LAST_FUEL_USAGE \
                        * (game_data['eventInformation']['mLapsInEvent']
                               - game_data['participants']['mParticipantInfo'][0]['mLapsCompleted']) \
                        > game_data['carState']['mFuelLevel']:
                    self.IN_GAME_FUEL_WARNING = True
                else:
                    self.IN_GAME_FUEL_WARNING = False

            self.print_fuel(self.IN_GAME_LAST_FUEL_USAGE, game_data['carState']['mFuelCapacity'],
                            self.font_size['fuel'],
                            [(0, self.theme_color['fuel_last_lap'])],
                            (x_edge_rpm, self.object_position['screen_center'][1]
                             + gear_surface_rect.width / 2),
                            'left', 'bottom')

            # Last lap fuel label
            self.print_text('Last Fuel Usage', self.font_size['label'], self.theme_color['label'],
                            (x_edge_rpm, self.object_position['screen_center'][1]
                             + (gear_surface_rect.height / 2) - self.font_size['fuel'] / 6),
                            'left', 'bottom')

            self.print_fuel_warning(self.IN_GAME_FUEL_WARNING and game_data['gameStates']['mSessionState'] == 5)

        # Fuel label
        self.print_text('Fuel', self.font_size['label'], self.theme_color['label'],
                        (x_edge_rpm, self.object_position['screen_center'][1]
                         - (gear_surface_rect.height / 2) + fuel_surface_rect.height - self.font_size['fuel'] / 10))

        # Speed label
        self.print_text('Speed', self.font_size['label'], self.theme_color['label'],
                        (self.display_resolution[0] - x_edge_rpm,
                         self.object_position['screen_center'][1] - speed_surface_rect.height / 2 +
                         self.font_size['speed'] / 18), 'right', 'bottom')

    # Methods below are optional. I made these only for this theme.
    def draw_flash(self, object_name, condition, function_if_cond_true, function_if_cond_false):
        if condition and self.flashing_object[object_name]['visible']:
            # Processing flashing effect
            self.flashing_object[object_name]['counter'] += 1
            if self.flashing_object[object_name]['counter'] >= self.flashing_object[object_name]['counter_max']:
                self.flashing_object[object_name]['counter'] = 0
                if self.flashing_object[object_name]['visible']:
                    self.flashing_object[object_name]['visible'] = False
                else:
                    self.flashing_object[object_name]['visible'] = True

            # Run function if condition true
            function_if_cond_true()
        else:
            # Run function if condition false
            function_if_cond_false()
            self.flashing_object[object_name]['counter'] = 0
            self.flashing_object[object_name]['visible'] = True

    def print_text(self, text, font_size, color, position,
                   horizontal_align='left',
                   vertical_align='top',
                   font=None,
                   anti_aliasing=True,
                   screen=None):
        if screen is None:
            screen = self.screen

        text_object = self.pygame.font.SysFont(font, font_size).render(text, anti_aliasing, color)

        if horizontal_align == 'center':
            x_offset = text_object.get_width() / 2
        elif horizontal_align == 'right':
            x_offset = text_object.get_width()
        else:
            x_offset = 0

        if vertical_align == 'middle':
            y_offset = text_object.get_height() / 2
        elif vertical_align == 'bottom':
            y_offset = text_object.get_height()
        else:
            y_offset = 0

        screen.blit(text_object, (position[0] - x_offset, position[1] - y_offset))
        return text_object.get_rect()

    def draw_background(self, rpm, max_rpm, hi_rpm_percentage, default_background_color, flash_background_color,
                        screen=None):
        if screen is None:
            screen = self.screen

        # Flashing condition
        def condition():
            try:
                return (rpm / max_rpm) >= hi_rpm_percentage
            except ZeroDivisionError:
                return False

        # Flash condition is met
        def function_if_cond_true():
            screen.fill(flash_background_color)

        # No flashing
        def function_if_cond_false():
            screen.fill(default_background_color)

        self.draw_flash('background', condition(), function_if_cond_true, function_if_cond_false)

    def print_fuel_warning(self, cond, screen=None):
        if screen is None:
            screen = self.screen

        # Flash condition is met
        def function_if_cond_true():
            self.print_text('FUEL', 80, (255, 255, 255), (0, self.display_resolution[1]), vertical_align='bottom')

        # No flashing
        def function_if_cond_false():
            pass

        self.draw_flash('fuel_warning', cond, function_if_cond_true, function_if_cond_false)

    def print_gear(self, gear, font_size, color, position,
                   horizontal_align='center',
                   vertical_align='middle',
                   font=None,
                   anti_aliasing=True,
                   screen=None):
        if gear == 0:
            text = 'N'
        elif gear == -1:
            text = 'R'
        else:
            text = str(gear)
        return self.print_text(text, font_size, color, position,
                               horizontal_align,
                               vertical_align,
                               font,
                               anti_aliasing,
                               screen)

    def draw_rpm_meter(self, rpm_percentage, rpm_percentage_list, radius, pos_y, range_per_circle,
                       low_rpm_color, med_rpm_color, hi_rpm_color,
                       screen=None):
        if screen is None:
            screen = self.screen

        sum_of_circles = len(rpm_percentage_list)
        diameter = radius * 2
        range_per_circle = diameter + range_per_circle
        rpm_surface_x_length = sum_of_circles * diameter + (sum_of_circles - 1) * (range_per_circle - diameter)
        rpm_surface = self.pygame.Surface((rpm_surface_x_length, diameter), self.pygame.SRCALPHA, 32)
        pos_x = radius

        for i in range(0, len(rpm_percentage_list)):
            if i < len(rpm_percentage_list) / 3:
                color = low_rpm_color
            elif i < len(rpm_percentage_list) * 2 / 3:
                color = med_rpm_color
            else:
                color = hi_rpm_color

            if rpm_percentage >= rpm_percentage_list[i]:
                self.pygame.draw.circle(rpm_surface, color, (pos_x, radius), radius)
                pos_x += range_per_circle
            else:
                break

        screen.blit(rpm_surface, (self.object_position['screen_center'][0] - rpm_surface.get_width() / 2, pos_y))
        return rpm_surface.get_rect()

    def print_speed(self, speed_in_mps, font_size, color, position,
                    horizontal_align='left',
                    vertical_align='top',
                    font=None,
                    anti_aliasing=True,
                    screen=None):
        return self.print_text(str(int(speed_in_mps * 3.6)), font_size, color, position,
                               horizontal_align,
                               vertical_align,
                               font,
                               anti_aliasing,
                               screen)

    def print_fuel(self, fuel_current, fuel_capacity, font_size, list_of_fuel_tuple_colors, position,
                   horizontal_align='left',
                   vertical_align='top',
                   font=None,
                   anti_aliasing=True,
                   screen=None):
        if screen is None:
            screen = self.screen

        c = None

        for i in range(0, len(list_of_fuel_tuple_colors)):
            if fuel_current >= list_of_fuel_tuple_colors[i][0]:
                c = list_of_fuel_tuple_colors[i][1]
                break

        if c is None:
            c = list_of_fuel_tuple_colors[-1][1]

        return self.print_text(str("%.1f" % (fuel_current * fuel_capacity)), font_size, c, position,
                               horizontal_align,
                               vertical_align,
                               font,
                               anti_aliasing,
                               screen)

    def float_to_time(self, time_in_float, sec_only=False):
        minutes, seconds = divmod(time_in_float, 60)
        if sec_only and seconds < 100:
            extra_zero = '00'
        elif seconds < 10:
            extra_zero = '0'
        else:
            extra_zero = ''
        if sec_only:
            return str(extra_zero + str("%.3f" % seconds))
        return str(int(minutes)) + ':' + extra_zero + str("%.3f" % seconds)
