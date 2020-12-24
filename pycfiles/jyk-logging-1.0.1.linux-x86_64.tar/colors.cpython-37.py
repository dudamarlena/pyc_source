# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyongkang/anaconda3/lib/python3.7/site-packages/jyk/logging/colors.py
# Compiled at: 2020-04-01 00:12:12
# Size of source mod 2**32: 1889 bytes
"""jyk color"""
import os, sys

def color(text: str, color_code: int) -> str:
    """Colorize text.
    Args:
        text: text.
        color_code: color.
    Returns:
        colorized text.
    """
    if sys.platform == 'win32':
        if os.getenv('TERM') != 'xterm':
            return text
    return '\x1b[%dm%s\x1b[0m' % (color_code, text)


def black(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        black text.
    """
    return color(text, 30)


def red(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        red text.
    """
    return color(text, 31)


def green(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Return:
        green text.
    """
    return color(text, 32)


def yellow(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Return:
        yellow text.
    """
    return color(text, 33)


def blue(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        blue text.
    """
    return color(text, 34)


def magenta(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        magenta text.
    """
    return color(text, 35)


def cyan(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        cyan text.
    """
    return color(text, 36)


def white(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        white text.
    """
    return color(text, 37)


def bold(text: str) -> str:
    """Colorize text.
    Args:
        text: text.
    Returns:
        bold text.
    """
    return color(text, 1)