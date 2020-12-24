# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marx/venv3/lib/python3.6/site-packages/tsr/modules/colours.py
# Compiled at: 2018-05-13 09:02:24
# Size of source mod 2**32: 4602 bytes
from sys import platform as sys_platform
if sys_platform == 'linux':

    class cl:
        purple = '\x1b[0;0;95m'
        cyan = '\x1b[0;0;96m'
        dcyan = '\x1b[0;0;36m'
        green = '\x1b[0;0;92m'
        yellow = '\x1b[0;0;93m'
        red = '\x1b[0;0;91m'
        bold = '\x1b[0;0;1m'
        underlined = '\x1b[0;0;4m'
        end = '\x1b[0;0;0m'
        white = '\x1b[1;37m'
        blue = '\x1b[0;34m'
        lblue = '\x1b[1;34m'
        lgreen = '\x1b[1;32m'
        lcyan = '\x1b[1;36;40m'
        lred = '\x1b[1;31m'
        lpurple = '\x1b[1;35m'
        orange = '\x1b[0;33;40m'
        brown = '\x1b[0;0;33m'
        grey = '\x1b[0;0;37m'
        lgrey = '\x1b[0;0;37m'
        _black_white = '\x1b[0;30;47m'
        _blue_yellow = '\x1b[1;33;44m'
        _blue_white = '\x1b[1;37;46m'
        _blue_red = '\x1b[1;34;41m'
        _cyan_white = '\x1b[1;37;46m'
        _green_white = '\x1b[1;37;42m'
        _red_black = '\x1b[7;31;40m'
        _red_blue = '\x1b[7;31;44m'
        _purple_white = '\x1b[1;37;45m'
        _purple_black = '\x1b[6;30;45m'
        _purple_purple = '\x1b[7;35;44m'
        _black_red = '\x1b[7;30;41m'
        _orange_black = '\x1b[0;30;43m'
        _flash_orange_black = '\x1b[5;30;43m'


else:
    import colorama
    colorama.init()

    class cl:
        purple = colorama.Fore.MAGENTA
        cyan = colorama.Fore.CYAN
        dcyan = colorama.Fore.CYAN
        green = colorama.Fore.CYAN
        yellow = colorama.Fore.YELLOW
        red = colorama.Fore.RED
        bold = colorama.Fore.WHITE
        underlined = colorama.Fore.WHITE
        end = colorama.Fore.RESET
        white = colorama.Fore.WHITE
        blue = colorama.Fore.BLUE
        lblue = colorama.Fore.BLUE
        lgreen = colorama.Fore.GREEN
        COLOR_CYAN = colorama.Fore.CYAN
        lcyan = colorama.Fore.CYAN
        lred = colorama.Fore.RED
        lpurple = colorama.Fore.MAGENTA
        brown = colorama.Fore.YELLOW
        grey = colorama.Fore.RESET
        lgrey = colorama.Fore.WHITE
        _red_black = colorama.Back.RED + colorama.Fore.BLACK
        _black_red = colorama.Back.BLACK + colorama.Fore.RED
        _orange_black = colorama.Back.YELLOW + colorama.Fore.BLACK


colour = {x:vars(cl)[x] for x in dir(cl) if not x.startswith('__') if not x.startswith('__')}
cl_to_assign = [x for x in dir(cl) if not x.startswith('_')]
colours = [
 [
  cl.white, cl.end, cl.red, cl.purple],
 [
  cl.lcyan, cl.lblue, cl.brown, cl.blue]]

def cl_seq_to_str(sequence):
    for c in colour:
        if colour[c] == sequence:
            return c
        if c == sequence:
            return c

    raise Exception('Sequence:' + sequence + ' is not in colour dictionary')


def colour_alternating(*args):
    global colours
    tpl = []

    def aaa(*args):
        tpl_new = []
        for arg in args:
            if type(arg).__name__ in ('str', 'int', 'float', 'datetime.date'):
                tpl_new.append(str(arg))
            else:
                if type(arg).__name__ in ('list', 'tuple'):
                    for x in arg:
                        tpl_new += aaa([], x)

        return tpl_new

    tpl += aaa(args)
    to_print = ''
    for i in range(len(tpl)):
        try:
            to_print += colours[0][(i % len(colours[0]))] + tpl[i] + '  '
        except:
            print(tpl[i])

    colours[0], colours[1] = colours[1], colours[0]
    return to_print


def toprint_expanded(*args):
    to_print = ''
    for i in range(len(args)):
        try:
            to_print += args[i] + cl.end + '  '
        except TypeError:
            if int(float(args[i])) == float(int(args[i])):
                to_print += str(int(args[i])) + cl.end + '  '
            else:
                to_print += str(float(args[i])) + cl.end + '  '

    return to_print


def toprint_expanded_ls(*args):
    tpl = []

    def aaa(*args):
        tpl_new = []
        for arg in args:
            if type(arg).__name__ in ('str', 'int', 'float', 'datetime.date'):
                tpl_new.append(str(arg))
            else:
                if type(arg).__name__ in ('list', 'tuple'):
                    for x in arg:
                        tpl_new += aaa([], x)

        return tpl_new

    tpl += aaa(args)
    to_print = ''
    for i in range(len(tpl)):
        try:
            to_print += tpl[i] + cl.end + '  '
        except:
            pass

    return to_print