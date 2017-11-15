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
    theme_color = {
        'default_background': (0, 0, 0),
        'background_flash': (122, 0, 0)
    }
    flashing_object = {
        'background': {
            'condition': False,
            'visible': True,
            'counter': 0,
            'counter_max': 3
        }
    }
    parameter_value = {
        'hi_rpm_percentage': 0.95
    }

    # These methods are needed and should be exist in every theme class:
    # __init__(self, pygame, screen, display_resolution)
    # refresh(self, json_from_request)
    def __init__(self, pygame, screen, display_resolution):
        self.pygame = pygame
        self.display_resolution = display_resolution
        self.screen = screen

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

    # Methods below are optional. I made these only for this theme.
    def flashing_effect(self, object_name):
        self.flashing_object[object_name]['counter'] += 1
        if self.flashing_object[object_name]['counter'] >= self.flashing_object[object_name]['counter_max']:
            self.flashing_object[object_name]['counter'] = 0
            if self.flashing_object[object_name]['visible']:
                self.flashing_object[object_name]['visible'] = False
            else:
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
            x_offset = text_object.get_rect().width / 2
        elif horizontal_align == 'right':
            x_offset = text_object.get_rect().width
        else:
            x_offset = 0

        if vertical_align == 'middle':
            y_offset = text_object.get_rect().height / 2
        elif vertical_align == 'bottom':
            y_offset = text.object.get_rect().height
        else:
            y_offset = 0

        screen.blit(text_object, (position[0] - x_offset, position[1] - y_offset))

    def draw_background(self, rpm, max_rpm, hi_rpm_percentage, default_background_color, flash_background_color,
                        screen=None):
        # TODO: Refactor this.
        if screen is None:
            screen = self.screen

        # Flashing condition
        try:
            self.flashing_object['background']['condition'] = (rpm / max_rpm) >= hi_rpm_percentage
        except ZeroDivisionError:
            self.flashing_object['background']['condition'] = False

        # Flash condition is met
        if self.flashing_object['background']['condition'] and self.flashing_object['background']['visible']:
            self.flashing_effect('background')  # Always called
            screen.fill(flash_background_color)

        # No flashing
        else:
            screen.fill(default_background_color)
            # Always called
            self.flashing_object['background']['counter'] = 0
            self.flashing_object['background']['visible'] = True
