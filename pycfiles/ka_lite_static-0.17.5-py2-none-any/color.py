# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/color.py
# Compiled at: 2018-07-11 18:15:30
"""
Sets up the terminal color scheme.
"""
import os, sys
from django.utils import termcolors

def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    unsupported_platform = sys.platform in ('win32', 'Pocket PC')
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if unsupported_platform or not is_a_tty:
        return False
    return True


def color_style():
    """Returns a Style object with the Django color scheme."""
    if not supports_color():
        style = no_style()
    else:
        DJANGO_COLORS = os.environ.get('DJANGO_COLORS', '')
        color_settings = termcolors.parse_color_setting(DJANGO_COLORS)
        if color_settings:

            class dummy:
                pass

            style = dummy()
            for role in termcolors.PALETTES[termcolors.NOCOLOR_PALETTE]:
                format = color_settings.get(role, {})
                setattr(style, role, termcolors.make_style(**format))

            style.ERROR_OUTPUT = style.ERROR
        else:
            style = no_style()
    return style


def no_style():
    """Returns a Style object that has no colors."""

    class dummy:

        def __getattr__(self, attr):
            return lambda x: x

    return dummy()