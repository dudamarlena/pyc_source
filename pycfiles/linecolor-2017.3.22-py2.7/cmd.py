# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/linecolor/cmd.py
# Compiled at: 2017-03-21 23:46:47
import sys
reload(sys)
sys.setdefaultencoding('utf8')
STYLE = {'fore': {'black': 30, 
            'red': 31, 
            'green': 32, 
            'yellow': 33, 
            'blue': 34, 
            'purple': 35, 
            'cyan': 36, 
            'white': 37}, 
   'back': {'black': 40, 
            'red': 41, 
            'green': 42, 
            'yellow': 43, 
            'blue': 44, 
            'purple': 45, 
            'cyan': 46, 
            'white': 47}, 
   'mode': {'mormal': 0, 
            'bold': 1, 
            'underline': 4, 
            'blink': 5, 
            'invert': 7, 
            'hide': 8}, 
   'default': {'end': 0}}

def color_str(string, mode='', fore='', back=''):
    mode = '%s' % STYLE['mode'][mode] if STYLE['mode'].has_key(mode) else ''
    fore = '%s' % STYLE['fore'][fore] if STYLE['fore'].has_key(fore) else ''
    back = '%s' % STYLE['back'][back] if STYLE['back'].has_key(back) else ''
    style = (';').join([ s for s in [mode, fore, back] if s ])
    style = '\x1b[%sm' % style if style else ''
    end = '\x1b[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def main():
    args = sys.argv[1:]
    pattern_color = {}
    if args:
        pattern_color = dict((x[0], x[1]) for x in map(lambda x: x.split('|'), args))
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        color = None
        for pattern, c in pattern_color.items():
            if pattern in line:
                color = c

        if color:
            print color_str(line.rstrip(), fore=color)
        else:
            print line.rstrip()

    return


if __name__ == '__main__':
    main()