# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_progress.py
# Compiled at: 2011-01-06 01:19:27
import math

def find_terminal_size():

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
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
             env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)

    return (
     int(cr[1]), int(cr[0]))


def find_terminal_width():
    return find_terminal_size()[0]


def find_terminal_height():
    return find_terminal_size()[1]


def build_progress(numerator, denominator, width=None):
    if width == None:
        width = find_terminal_width()
    width = width - 12
    if width <= 1:
        return '%7s' % ('%%%.2f' % (100.0 * percent))
    else:
        percent = float(numerator) / float(denominator)
        complete = int(math.floor(percent * width))
        return '[ ' + '#' * complete + '.' * (width - complete) + ' ] %7s' % ('%%%.2f' % (100.0 * percent))


if __name__ == '__main__':
    print build_progress(26, 100) + '\r',
    print build_progress(99, 100) + '\r',
    print build_progress(100, 100) + '\r',
    print ''