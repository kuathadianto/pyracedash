# TODO: Docstring every functions
class NewFallback:
    """
    Fallback theme, if no matched theme found.
    Or use this as template to make a new theme.
    The name of this class and this file should be the same and case sensitive.
    """

    # CREST Modules that this theme use
    needed_modules = ['carState', 'timings', 'eventInformation']

    # These attributes below are optional, and only meant to use for this theme only.
    # All with None value are reserved, and initialized on __init__
    theme_color = {
        'default_background': (0, 0, 0),
        'background_flash': (122, 0, 0),
        'gear': (255, 204, 0),
        'rpm_circle_low': (0, 0, 255),
        'rpm_circle_mid': (0, 255, 0),
        'rpm_circle_hi': (255, 0, 0),
    }
    font_size = {
        'gear': None
    }
    parameter_value = {
        'hi_rpm_percentage': 0.95,
        'rpm_percentage_list': [0.5, 0.6, 0.7, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.915, 0.93, 0.945],
        'rpm_circle_radius': None,
        'rpm_meter_range_per_circle': None
    }
    object_position = {
        'screen_center': None,
        'rpm_meter_y': None
    }
    flashing_object = {
        'background': {
            'visible': True,
            'counter': 0,
            'counter_max': 3
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
        if self.object_position['screen_center'] is None:
            self.object_position['screen_center'] = (display_resolution[0] / 2, display_resolution[1] / 2)
        if self.font_size['gear'] is None:
            self.font_size['gear'] = int(display_resolution[1] / 1.263157894736842)
        if self.parameter_value['rpm_circle_radius'] is None:
            self.parameter_value['rpm_circle_radius'] = int(display_resolution[1] / 17.78)
        if self.object_position['rpm_meter_y'] is None:
            self.object_position['rpm_meter_y'] = self.object_position['screen_center'][1] / 6
        if self.parameter_value['rpm_meter_range_per_circle'] is None:
            self.parameter_value['rpm_meter_range_per_circle'] = int(display_resolution[0] / 66)

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

        self.print_gear(game_data['carState']['mGear'],
                        self.font_size['gear'],
                        self.theme_color['gear'],
                        self.object_position['screen_center'])

        self.draw_rpm_meter(game_data['carState']['mRpm'] / game_data['carState']['mMaxRPM'],
                            self.parameter_value['rpm_percentage_list'],
                            self.parameter_value['rpm_circle_radius'],
                            self.object_position['rpm_meter_y'],
                            self.parameter_value['rpm_meter_range_per_circle'],
                            self.theme_color['rpm_circle_low'],
                            self.theme_color['rpm_circle_mid'],
                            self.theme_color['rpm_circle_hi'])

        # TODO: Finish
        font_size = 180
        color = (126, 41, 255)
        pos = (self.display_resolution[0] - 24, self.object_position['screen_center'][1])
        self.print_speed(game_data['carState']['mSpeed'],
                         font_size,
                         color,
                         pos,
                         'right',
                         'middle')

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
        self.print_text(text, font_size, color, position,
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

    def print_speed(self, speed_in_mps, font_size, color, position,
                   horizontal_align='left',
                   vertical_align='top',
                   font=None,
                   anti_aliasing=True,
                   screen=None):
        self.print_text(str(int(speed_in_mps * 3.6)), font_size, color, position,
                        horizontal_align,
                        vertical_align,
                        font,
                        anti_aliasing,
                        screen)
