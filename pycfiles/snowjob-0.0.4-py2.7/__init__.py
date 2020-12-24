# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snowjob/__init__.py
# Compiled at: 2013-12-26 00:24:57
import os, sys, random, time, platform
snowflakes = {}
try:
    from colorama import init
    init()
except ImportError:
    pass

def get_terminal_size():

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return

        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        try:
            cr = (
             os.environ['LINES'], os.environ['COLUMNS'])
        except:
            cr = (25, 80)

    return (
     int(cr[1]), int(cr[0]))


columns, rows = get_terminal_size()

def clear_screen(numlines=100):
    """Clear the console.

    numlines is an optional argument used only as a fall-back.
    """
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        os.system('cls')
    else:
        print '\n' * rows


def get_random_flake():
    if not platform.system() == 'Windows':
        try:
            try:
                cmd = unichr
            except NameError:
                cmd = chr

            flake = cmd(random.choice(range(10048, 10057)))
            return flake
        except:
            pass

    return ' *'


current_rows = {}

def move_flake(col, stack):
    if stack:
        if col not in current_rows:
            current_rows[col] = rows
        current_row = current_rows[col]
        if current_row == 1:
            current_row = rows
            current_rows[col] = current_row
    else:
        current_row = rows
    if snowflakes[col][0] + 1 == current_row:
        snowflakes[col] = [
         1, get_random_flake()]
        if stack:
            current_rows[col] -= 1
    else:
        print '\x1b[%s;%sH  ' % (snowflakes[col][0], col)
        snowflakes[col][0] += 1
        print '\x1b[%s;%sH%s' % (snowflakes[col][0], col, snowflakes[col][1])
        print '\x1b[1;1H'


def main():
    if len(sys.argv) > 1:
        stack = sys.argv[1] == '--stack'
    else:
        stack = False
    clear_screen()
    while True:
        col = random.choice(range(1, int(columns)))
        if col % 2 == 0:
            continue
        if col in snowflakes.keys():
            move_flake(col, stack)
        else:
            flake = get_random_flake()
            snowflakes[col] = [1, flake]
            print '\x1b[%s;%sH%s' % (snowflakes[col][0], col,
             snowflakes[col][1])
        for flake in snowflakes.keys():
            move_flake(flake, stack)

        time.sleep(0.1)


if __name__ == '__main__':
    main()