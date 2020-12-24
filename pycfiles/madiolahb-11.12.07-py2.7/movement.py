# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madiolahb/movement.py
# Compiled at: 2011-12-07 23:24:36


def nextpos(hexmap, x, y, n, dir):
    if hexmap:
        if dir == 'n':
            if n % 2 != 0:
                return (None, None)
            else:
                return (
                 x, y + n)

        else:
            if dir == 'ne':
                return (x + n % 2, y + n)
            if dir == 'e':
                return (x + n, y)
            if dir == 'se':
                return (x + n % 2, y - n)
            if dir == 's':
                if n % 2 != 0:
                    return (None, None)
                else:
                    return (
                     x, y - n)

            else:
                if dir == 'sw':
                    return (x - n % 2, y - n)
                if dir == 'w':
                    return (x - n, y)
                if dir == 'nw':
                    return (x - n % 2, y + n)
                raise ValueError, '%s is not a direction' % dir
    else:
        if dir == 'n':
            return (x, y + n)
        if dir == 'ne':
            return (x + n, y + n)
        if dir == 'e':
            return (x + n, y)
        if dir == 'se':
            return (x + n, y - n)
        if dir == 's':
            return (x, y - n)
        if dir == 'sw':
            return (x - n, y - n)
        if dir == 'w':
            return (x - n, y)
        if dir == 'nw':
            return (x - n, y + n)
        raise ValueError, '%s is not a direction' % dir
    return


def at(lifewheel, x=0, y=0, **kwargs):
    """
    Place the lifewheel's pawn at the given coordinates.
    """
    lifewheel['x'] = x
    lifewheel['y'] = y


def _register_at(subp):
    parser = subp.add_parser('at')
    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.set_defaults(func=at)


def move(lifewheel, count=0, direction=None, is_on_hexmap=True, **kwargs):
    is_on_hexmap = lifewheel['is_on_hexmap'] if 'is_on_hexmap' in lifewheel else is_on_hexmap
    if is_on_hexmap and direction in ('n', 's') and count % 2 != 0:
        lifewheel['errors'].append('%s is not a multiple of two for N/S on a hex map' % count)
        return
    lifewheel['x'], lifewheel['y'] = nextpos(is_on_hexmap, lifewheel['x'], lifewheel['y'], count, direction)


def _register_move(subp):
    parser = subp.add_parser('move')
    parser.add_argument('count', type=int)
    parser.add_argument('direction', choices=('n', 'ne', 'e', 'se', 's', 'sw', 'w',
                                              'nw'))
    parser.add_argument('--is-on-hexmap', type=bool)
    parser.set_defaults(func=move)


def register_commands(subp):
    _register_at(subp)
    _register_move(subp)