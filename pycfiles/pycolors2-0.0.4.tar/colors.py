# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/colors.py
# Compiled at: 2009-11-13 18:50:20
__doc__ = "\n    Module colors\n    ~~~~~~~~~~~~~~\n    \n    Python module to ease the use of colors on programs that run on CLI.\n    Works fine on Linux and any Operating System running BaSH or compatibles.\n    If the shell's not color compatible, he'll get the raw string.\n    The module have predefined some basic colors, but you can use any color,\n    if you know the color code.\n\n\n    Usage example\n    -------------\n\n        >>> from colors import Color\n        >>> yellow = Color('1;33')\n        >>> print yellow('Hello World')\n        Hello World\n        \n        >>> from colors import red\n        >>> print red('Ola Mundo')\n\n\n    Working with this module as an optional dependency\n    --------------------------------------------------\n\n    If you don't want to force the users to have PyColors installed\n    you can make the use of the colors module optional. For example: ::\n    \n        # trying to use colors\n        try:\n            from colors import light_blue, light_red, red, white\n        except:\n            light_blue = light_red = red = white = lambda(x): str(x)\n    \n    With this, if the user don't have the colors module, he'll get the\n    raw strings normally.\n    \n    :copyright: 2009 Rafael Goncalves Martins.\n    :license: BSD, see LICENSE for more details.\n\n"
__all__ = [
 'Color', 'disable_colors',
 'black', 'blue', 'green', 'cyan', 'red', 'purple', 'brown',
 'light_gray', 'dark_gray', 'light_blue', 'light_green', 'light_cyan',
 'light_red', 'light_purple', 'yellow', 'white']
__author__ = 'Rafael Goncalves Martins'
__email__ = 'rafael@rafaelmartins.eng.br'
__description__ = 'Python module to ease the use of colors on programs that run on CLI'
__url__ = 'http://packages.python.org/pycolors/'
__copyright__ = '(c) 2009 %s' % __author__
__license__ = 'BSD'
__version__ = '0.1.2'
from os import environ
from subprocess import Popen, PIPE

def __has_colors():
    """Checks if the current shell supports colors
    
    """
    p = Popen('tput colors', stdout=PIPE, stderr=PIPE, shell=True)
    try:
        num_colors = int(p.stdout.read())
    except:
        num_colors = 1

    if num_colors > 1:
        environ['HASCOLORS'] = '1'


def disable_colors():
    """This function forces the non-usage of colors. You can also disable
    colors setting the environment variable DISABLE_COLORS with any value.
    
    """
    environ['DISABLE_COLORS'] = '1'


class Color(object):
    """PyColors main class
    
    """

    def __init__(self, color_code):
        """Initialize the color object

        """
        self.color_code = color_code

    def __call__(self, string):
        """Callable object, used to return the string with color markup
        or the raw string if colors aren't available on the current
        shell or are disabled by user.
        
        """
        string = str(string)
        if 'HASCOLORS' in environ and 'DISABLE_COLORS' not in environ:
            return '\x1b[%sm%s\x1b[1;0m' % (self.color_code, string)
        else:
            return string


__has_colors()
black = Color('0;30')
blue = Color('0;34')
green = Color('0;32')
cyan = Color('0;36')
red = Color('0;31')
purple = Color('0;35')
brown = Color('0;33')
light_gray = Color('0;37')
dark_gray = Color('1;30')
light_blue = Color('1;34')
light_green = Color('1;32')
light_cyan = Color('1;36')
light_red = Color('1;31')
light_purple = Color('1;35')
yellow = Color('1;33')
white = Color('1;37')