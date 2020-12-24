# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: arsenal/terminal/colors.py
# Compiled at: 2016-10-28 12:22:32
import colored
normal = '\x1b[0m%s\x1b[0m'
bold = '\x1b[1m%s\x1b[0m'
black, red, green, yellow, blue, magenta, cyan, white = map(('\x1b[3%sm%%s\x1b[0m').__mod__, range(8))
light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = map(('\x1b[1;3%sm%%s\x1b[0m').__mod__, range(8))
bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = map(('\x1b[4%sm%%s\x1b[0m').__mod__, range(8))

def padr(w):
    """get format to pad right elements"""
    return '%%%ss' % w


pad = padr

def padl(w):
    """get format to pad left elements"""
    return '%%-%ss' % w


def getwidth(a):
    """Find maximum width of the string representations of the elements of ``a``."""
    return max(len(str(z)) for z in a)


def check(x, t='pass', f='fail'):
    if x:
        return green % t
    return red % f


underline = '\x1b[4m%s\x1b[0m'

def test():
    for c in ('black, red, green, yellow, blue, magenta, cyan, white').split(', '):
        print globals()[c] % c
        print globals()[('light_' + c)] % ('light_' + c)

    for c in ('black, red, green, yellow, blue, magenta, cyan, white').split(', '):
        print globals()[('bg_' + c)] % c

    print underline % 'underline'


def color01(x, fmt='%.10f', min_color=235, max_color=255):
    """Colorize numbers in [0,1] based on value; darker means smaller value."""
    if not 0 <= x <= 1.0000000001:
        return red % fmt % x
    width = max_color - min_color
    color = min_color + int(round(x * width))
    return '%s%s%s' % (colored.fg(color), fmt % x, colored.attr('reset'))


if __name__ == '__main__':
    test()