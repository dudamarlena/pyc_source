# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/podchecker/utils/print_with_color.py
# Compiled at: 2019-06-17 12:41:22
# Size of source mod 2**32: 6813 bytes
from __future__ import print_function
LTCSI = '\x1b['

def code_to_chars(code):
    return LTCSI + str(code) + 'm'


class LTCodes(object):

    def __init__(self):
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class LTFore(LTCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39


class LTBack(LTCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49


class LTStyle(LTCodes):
    HIGHLIGHTED = 1
    UNDERLINE = 4
    BLINK = 5
    INVISIBLE = 8
    RESET_ALL = 0


kFore = LTFore()
kBack = LTBack()
kStyle = LTStyle()

class PrintWithColor:
    """PrintWithColor"""

    @classmethod
    def __simple_print(cls, color, v, end):
        print((cls.simple_preferred_formatted_string(color, v)), end=end)
        return cls

    @classmethod
    def simple_preferred_formatted_string(cls, color, v):
        return f"{color}{v}{kFore.RESET}"

    @classmethod
    def black(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.BLACK, v, end)

    @classmethod
    def red(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.RED, v, end)

    @classmethod
    def green(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.GREEN, v, end)

    @classmethod
    def yellow(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.YELLOW, v, end)

    @classmethod
    def blue(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.BLUE, v, end)

    @classmethod
    def magenta(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.MAGENTA, v, end)

    @classmethod
    def cyan(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.CYAN, v, end)

    @classmethod
    def white(cls, v, end='\n'):
        return cls._PrintWithColor__simple_print(kFore.WHITE, v, end)

    _PrintWithColor__saved_chain = ''

    @classmethod
    def __advanced_chain(cls, node):
        cls._PrintWithColor__saved_chain += node
        return cls

    @classmethod
    def fore_black(cls):
        return cls._PrintWithColor__advanced_chain(kFore.BLACK)

    @classmethod
    def fore_red(cls):
        return cls._PrintWithColor__advanced_chain(kFore.RED)

    @classmethod
    def fore_green(cls):
        return cls._PrintWithColor__advanced_chain(kFore.GREEN)

    @classmethod
    def fore_yellow(cls):
        return cls._PrintWithColor__advanced_chain(kFore.YELLOW)

    @classmethod
    def fore_blue(cls):
        return cls._PrintWithColor__advanced_chain(kFore.BLUE)

    @classmethod
    def fore_magenta(cls):
        return cls._PrintWithColor__advanced_chain(kFore.MAGENTA)

    @classmethod
    def fore_cyan(cls):
        return cls._PrintWithColor__advanced_chain(kFore.CYAN)

    @classmethod
    def fore_white(cls):
        return cls._PrintWithColor__advanced_chain(kFore.WHITE)

    @classmethod
    def back_black(cls):
        return cls._PrintWithColor__advanced_chain(kBack.BLACK)

    @classmethod
    def back_red(cls):
        return cls._PrintWithColor__advanced_chain(kBack.RED)

    @classmethod
    def back_green(cls):
        return cls._PrintWithColor__advanced_chain(kBack.GREEN)

    @classmethod
    def back_yellow(cls):
        return cls._PrintWithColor__advanced_chain(kBack.YELLOW)

    @classmethod
    def back_blue(cls):
        return cls._PrintWithColor__advanced_chain(kBack.BLUE)

    @classmethod
    def back_magenta(cls):
        return cls._PrintWithColor__advanced_chain(kBack.MAGENTA)

    @classmethod
    def back_cyan(cls):
        return cls._PrintWithColor__advanced_chain(kBack.CYAN)

    @classmethod
    def back_white(cls):
        return cls._PrintWithColor__advanced_chain(kBack.WHITE)

    @classmethod
    def style_highlight(cls):
        return cls._PrintWithColor__advanced_chain(kStyle.HIGHLIGHTED)

    @classmethod
    def style_underline(cls):
        return cls._PrintWithColor__advanced_chain(kStyle.UNDERLINE)

    @classmethod
    def style_blink(cls):
        return cls._PrintWithColor__advanced_chain(kStyle.BLINK)

    @classmethod
    def style_invisible(cls):
        return cls._PrintWithColor__advanced_chain(kStyle.INVISIBLE)

    @classmethod
    def apply(cls, v, end='\n'):
        print(f"{cls._PrintWithColor__saved_chain}{v}{kFore.RESET}{kBack.RESET}{kStyle.RESET_ALL}", end=end)
        cls.clear()
        return cls

    @classmethod
    def clear(cls):
        cls._PrintWithColor__saved_chain = ''