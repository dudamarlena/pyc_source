# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/color.py
# Compiled at: 2019-02-14 00:35:17
"""
Sets up the terminal color scheme.
"""
import os, sys
from django.utils import lru_cache, termcolors

def supports_color():
    """
    Returns True if the running system's terminal supports color,
    and False otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


class Style(object):
    pass


def make_style(config_string=''):
    """
    Create a Style object from the given config_string.

    If config_string is empty django.utils.termcolors.DEFAULT_PALETTE is used.
    """
    style = Style()
    color_settings = termcolors.parse_color_setting(config_string)
    for role in termcolors.PALETTES[termcolors.NOCOLOR_PALETTE]:
        if color_settings:
            format = color_settings.get(role, {})
            style_func = termcolors.make_style(**format)
        else:

            def style_func(x):
                return x

        setattr(style, role, style_func)

    style.ERROR_OUTPUT = style.ERROR
    return style


@lru_cache.lru_cache(maxsize=None)
def no_style():
    """
    Returns a Style object with no color scheme.
    """
    return make_style('nocolor')


def color_style():
    """
    Returns a Style object from the Django color scheme.
    """
    if not supports_color():
        return no_style()
    return make_style(os.environ.get('DJANGO_COLORS', ''))