# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/theme.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 24033 bytes
"""
Module that contains theme implementation
"""
from __future__ import print_function, division, absolute_import
import os
from Qt.QtCore import *
from Qt.QtGui import *
from six import string_types
import tpDcc
from tpDcc.libs import qt
from tpDcc.libs.python import yamlio, color, python
from tpDcc.libs.qt.core import style, qtutils, cache, color as qt_color

class Theme(QObject, object):

    class Sizes(object):
        TINY = 18
        SMALL = 24
        MEDIUM = 32
        LARGE = 40
        HUGE = 48

    class Colors(object):
        BLUE = '#1890FF'
        PURPLE = '#722ED1'
        CYAN = '#13C2C2'
        GREEN = '#52C41A'
        MAGENTA = '#EB2F96'
        PINK = '#EF5B97'
        RED = '#F5222D'
        ORANGE = '#FA8C16'
        YELLOW = '#FADB14'
        VOLCANO = '#FA541C'
        GEEK_BLUE = '#2F54EB'
        LIME = '#A0D911'
        GOLD = '#FAAD14'

    updated = Signal()
    EXTENSION = 'yml'
    DEFAULT_ACCENT_COLOR = QColor(0, 175, 255)
    DEFAULT_SIZE = Sizes.SMALL

    def __init__(self, theme_file=None, accent_color=None, dark_mode=True):
        super(Theme, self).__init__()
        self._name = 'Default'
        self._style = 'default'
        self._file = theme_file
        self._dpi = 1
        self._background_color = None
        self._overrides = list()
        self._init_colors()
        self._init_sizes()
        self._init_font()
        accent_color = accent_color or self.Colors.BLUE
        if dark_mode:
            self.set_dark(accent_color)
        else:
            self.set_light(accent_color)
        self._init_icons()
        self.unit = 'px'
        self.default_size = self.small
        self.text_color_inverse = '#FFF'
        self._load_theme_data_from_file(theme_file)

    def __getattr__(self, item):
        options = self.options(skip_instance_attrs=True)
        if not options or item not in options:
            return super(Theme, self).__getattribute__(item)
        else:
            option_value = options[item]
            if isinstance(option_value, string_types):
                if option_value.startswith('^'):
                    return qtutils.dpi_scale(int(option_value[1:]))
                if color.string_is_hex(option_value):
                    return color.hex_to_rgb(option_value)
            else:
                return option_value

    def _load_theme_data_from_file(self, theme_file):
        """
        Internal function that laods file data from given file
        :param theme_file: str
        :return: dict
        """
        if not theme_file or not os.path.isfile(theme_file):
            return
        try:
            theme_data = yamlio.read_file(theme_file)
        except Exception:
            qt.logger.warning('Impossible to load theme data from file: "{}"!'.format(theme_file))
            return
        else:
            theme_name = theme_data.get('name', None)
            if not theme_name:
                qt.logger.warning('Impossible to retrieve them name from theme file: "{}"!'.format(theme_file))
                return
            accent_color = theme_data.get('accent_color', None)
            if not accent_color:
                qt.logger.warning('No theme color definitions found in theme file: "{}"'.format(theme_file))
                return
            self._style = theme_data.get('style', 'default.css')
            self._overrides = theme_data.get('overrides', list())
            self.set_name(theme_name)
            self.set_accent_color(accent_color)

    def name(self):
        """
        Returns the name for this theme
        :return: str
        """
        return self._name

    def set_name(self, name):
        """
        Sets the name for this theme
        :param name: str
        """
        self._name = name

    def dpi(self):
        """
        Returns zoom amount for this theme
        :return: float
        """
        return self._dpi

    def set_dpi(self, dpi):
        """
        Sets the zoom amount for this theme
        :param dpi: float
        """
        self._dpi = dpi

    def set_accent_color(self, accent_color):
        """
        Sets the main/accent color of the theme
        :param accent_color:
        """
        self._update_accent_color(accent_color)
        self.updated.emit()

    def is_dark(self):
        """
        Returns whether the current theme is dark or not
        :return: bool
        """
        bg_color = qt_color.Color(self.background_color)
        red = bg_color.redF() * 0.299
        green = bg_color.greenF() * 0.587
        blue = bg_color.blueF() * 0.114
        darkness = red + green + blue
        if darkness < 0.6:
            return True
        else:
            return False

    def set_dark(self, accent_color):
        """
        Sets the current theme to the default dark color
        """
        self.background_color = '#323232'
        self.background_selected_color = '#292929'
        self.background_in_color = '#3A3A3A'
        self.background_out_color = '#494949'
        self.mask_color = self._fade_color(self.background_color, '90%')
        self.toast_color = '#555555'
        self.title_color = '#FFFFFF'
        self.primary_text_color = '#D9D9D9'
        self.secondary_text_color = '#A6A6A6'
        self.disable_color = '#737373'
        self.border_color = '#1E1E1E'
        self.divider_color = '#262626'
        self.header_color = '#0A0A0A'
        self.icon_color = '#A6A6A6'
        self.window_dragger_color = '#232323'
        self.window_dragger_label_color = '#D9D9D9'
        self.set_accent_color(accent_color)

    def set_light(self, accent_color):
        """
        Sets the current theme to the default light color
        """
        self.background_color = '#F8F8F9'
        self.background_selected_color = '#BFBFBF'
        self.background_in_color = '#FFFFFF'
        self.background_out_color = '#EEEEEE'
        self.mask_color = self._fade_color(self.background_color, '90%')
        self.toast_color = '#333333'
        self.title_color = '#262626'
        self.primary_text_color = '#595959'
        self.secondary_text_color = '#8C8C8C'
        self.disable_color = '#E5E5E5'
        self.border_color = '#D9D9D9'
        self.divider_color = '#E8E8E8'
        self.header_color = '#FAFAFA'
        self.icon_color = '#8C8C8C'
        self.window_dragger_color = '#f2f2fd'
        self.window_dragger_label_color = '#262626'
        self.set_accent_color(accent_color)

    def _init_colors(self):
        """
        Internal function that initializes all theme colors
        """
        self.info_color = self.Colors.BLUE
        self.success_color = self.Colors.GREEN
        self.processing_color = self.Colors.BLUE
        self.error_color = self.Colors.RED
        self.warning_color = self.Colors.GOLD
        self.info_1 = self._fade_color(self.info_color, '15%')
        self.info_2 = qt_color.generate_color(self.info_color, 2)
        self.info_3 = self._fade_color(self.info_color, '35%')
        self.info_4 = qt_color.generate_color(self.info_color, 4)
        self.info_5 = qt_color.generate_color(self.info_color, 5)
        self.info_6 = qt_color.generate_color(self.info_color, 6)
        self.info_7 = qt_color.generate_color(self.info_color, 7)
        self.info_8 = qt_color.generate_color(self.info_color, 8)
        self.info_9 = qt_color.generate_color(self.info_color, 9)
        self.info_10 = qt_color.generate_color(self.info_color, 10)
        self.success_1 = self._fade_color(self.success_color, '15%')
        self.success_2 = qt_color.generate_color(self.success_color, 2)
        self.success_3 = self._fade_color(self.success_color, '35%')
        self.success_4 = qt_color.generate_color(self.success_color, 4)
        self.success_5 = qt_color.generate_color(self.success_color, 5)
        self.success_6 = qt_color.generate_color(self.success_color, 6)
        self.success_7 = qt_color.generate_color(self.success_color, 7)
        self.success_8 = qt_color.generate_color(self.success_color, 8)
        self.success_9 = qt_color.generate_color(self.success_color, 9)
        self.success_10 = qt_color.generate_color(self.success_color, 10)
        self.warning_1 = self._fade_color(self.warning_color, '15%')
        self.warning_2 = qt_color.generate_color(self.warning_color, 2)
        self.warning_3 = self._fade_color(self.warning_color, '35%')
        self.warning_4 = qt_color.generate_color(self.warning_color, 4)
        self.warning_5 = qt_color.generate_color(self.warning_color, 5)
        self.warning_6 = qt_color.generate_color(self.warning_color, 6)
        self.warning_7 = qt_color.generate_color(self.warning_color, 7)
        self.warning_8 = qt_color.generate_color(self.warning_color, 8)
        self.warning_9 = qt_color.generate_color(self.warning_color, 9)
        self.warning_10 = qt_color.generate_color(self.warning_color, 10)
        self.error_1 = self._fade_color(self.error_color, '15%')
        self.error_2 = qt_color.generate_color(self.error_color, 2)
        self.error_3 = self._fade_color(self.error_color, '35%')
        self.error_4 = qt_color.generate_color(self.error_color, 4)
        self.error_5 = qt_color.generate_color(self.error_color, 5)
        self.error_6 = qt_color.generate_color(self.error_color, 6)
        self.error_7 = qt_color.generate_color(self.error_color, 7)
        self.error_8 = qt_color.generate_color(self.error_color, 8)
        self.error_9 = qt_color.generate_color(self.error_color, 9)
        self.error_10 = qt_color.generate_color(self.error_color, 10)

    def _init_sizes(self):
        """
        Internal function that initializes all themes sizes
        """
        self.border_radius_large = 8
        self.border_radius_base = 4
        self.border_radius_small = 2
        self.tiny = self.Sizes.TINY
        self.small = self.Sizes.SMALL
        self.medium = self.Sizes.MEDIUM
        self.large = self.Sizes.LARGE
        self.huge = self.Sizes.HUGE
        self.tiny_icon = self.tiny - 8
        self.small_icon = self.small - 10
        self.medium_icon = self.medium - 12
        self.large_icon = self.large - 16
        self.huge_icon = self.huge - 20
        self.window_dragger_rounded_corners = 5
        self.window_dragger_font_size = 12
        self.window_rounded_corners = 5
        self.button_padding = 4

    def _init_font(self):
        """
        Internal function that initializes all theme fonts
        """
        self.font_family = 'BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",Helvetica,Arial,sans-serif'
        self.font_size_base = 14
        self.font_size_large = self.font_size_base + 2
        self.font_size_small = self.font_size_base - 2
        self.h1_size = int(self.font_size_base * 2.71)
        self.h2_size = int(self.font_size_base * 2.12)
        self.h3_size = int(self.font_size_base * 1.71)
        self.h4_size = int(self.font_size_base * 1.41)

    def _init_icons(self):
        """
        Internal function that initializes all theme icons
        """
        self.radio_checked_icon = 'radio_button_checked.png'
        self.radio_unchecked_icon = 'radio_button_unchecked.png'
        self.up_icon = 'collapse.png'
        self.down_icon = 'expand.png'
        self.up_arrow_icon = 'up_arrow.png'
        self.down_arrow_icon = 'down_arrow.png'
        self.left_icon = 'back.png'
        self.right_icon = 'next.png'
        self.calendar_icon = 'calendar.png'
        self.check_icon = 'check.png'
        self.uncheck_icon = 'uncheck.png'
        self.circle_icon = 'circle.png'
        self.splitter_icon = 'splitter.png'

    def _update_accent_color(self, accent_color):
        accent_color = qt_color.convert_2_hex(accent_color)
        self.accent_color = accent_color
        self.accent_color_1 = qt_color.generate_color(accent_color, 1)
        self.accent_color_2 = qt_color.generate_color(accent_color, 2)
        self.accent_color_3 = qt_color.generate_color(accent_color, 3)
        self.accent_color_4 = qt_color.generate_color(accent_color, 4)
        self.accent_color_5 = qt_color.generate_color(accent_color, 5)
        self.accent_color_6 = qt_color.generate_color(accent_color, 6)
        self.accent_color_7 = qt_color.generate_color(accent_color, 7)
        self.accent_color_8 = qt_color.generate_color(accent_color, 8)
        self.accent_color_9 = qt_color.generate_color(accent_color, 9)
        self.accent_color_10 = qt_color.generate_color(accent_color, 10)
        self.item_hover_background_color = self.accent_color_1

    def _get_color(self, color_value, alpha=None):
        """
        Internal function that returns a color value in proper format to be handled by theme
        :param color_value: variant, str or QColor or color.Color
        """
        if isinstance(color_value, (str, unicode)):
            color_value = qt_color.Color.from_string(color_value)
        else:
            if isinstance(color_value, QColor):
                color_value = qt_color.Color.from_color(color_value)
            else:
                if isinstance(color_value, (list, tuple)):
                    color_value = (qt_color.Color)(*color_value)
        return color_value

    def _fade_color(self, color, alpha):
        """
        Internal function that fades given color
        :param color: QColor
        :param alpha: float
        :return:
        """
        qt_color = QColor(color)
        return 'rgba({}, {}, {}, {})'.format(qt_color.red(), qt_color.green(), qt_color.blue(), alpha)

    def foreground_color(self):
        """
        Returns the foreground color for this theme
        :return: color.Color
        """
        if self.is_dark():
            return qt_color.Color(250, 250, 250, 255)
        else:
            return qt_color.Color(0, 40, 80, 180)

    def set_settings(self, settings):
        """
        Sets a dictionary of settings for the current theme
        :param settings: dict
        """
        for theme_sett_name, theme_sett_value in settings.items():
            if hasattr(self, theme_sett_name):
                setattr(self, theme_sett_name, theme_sett_value)

    def get_theme_option(self, option_name, default_value=None):
        """
        Returns option of the style
        :return: object
        """
        theme_options = self.options()
        if not theme_options:
            return default_value
        else:
            if option_name in theme_options:
                return theme_options[option_name]
            return default_value

    def options(self, skip_instance_attrs=False):
        """
        Returns the variables used to customize the style sheet
        :return: dict
        """
        if self.is_dark():
            darkness = 'white'
        else:
            darkness = 'black'
        theme_resources_dir = ''
        if self._file:
            if os.path.isfile(self._file):
                theme_dir = os.path.dirname(self._file)
                theme_name = os.path.splitext(os.path.basename(self._file))[0]
                theme_resources_dir = os.path.join(theme_dir, 'resources', theme_name)
        style_resources_dir = ''
        style_path = self.stylesheet_file()
        if style_path:
            if os.path.isfile(style_path):
                style_dir = os.path.dirname(style_path)
                style_name = os.path.splitext(os.path.basename(style_path))[0]
                style_resources_dir = os.path.join(style_dir, 'resources', style_name)
        options = {'darkness':darkness,  'theme_resources':theme_resources_dir, 
         'style_resources':style_resources_dir}
        if not skip_instance_attrs:
            inst_attrs = python.get_instance_user_attributes(self)
            for attr in inst_attrs:
                if isinstance(attr[1], QColor):
                    options[attr[0]] = qt_color.Color(attr[1]).to_string()
                else:
                    options[attr[0]] = str(attr[1])

        overrides = self._overrides or dict()
        options.update(overrides)
        return options

    def stylesheet_file(self):
        """
        Returns path where theme stylesheet is located
        :return: str
        """
        style_name = self._style or 'default'
        style_extension = style.StyleSheet.EXTENSION
        if not style_extension.startswith('.'):
            style_extension = '.{}'.format(style_extension)
        style_file_name = '{}{}'.format(style_name, style_extension)
        style_path = tpDcc.ResourcesMgr().get('styles', style_file_name)
        return style_path

    def stylesheet(self):
        """
        Returns the style sheet for this theme
        :return: str
        """
        style_path = self.stylesheet_file()
        options = self.options()
        stylesheet = style.StyleSheet.from_path(style_path, options=options, theme_name=(self._name), dpi=(self.dpi()))
        return stylesheet.data()


ThemeCache = cache.CacheResource(Theme)