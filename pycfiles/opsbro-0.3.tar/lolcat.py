# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/opsbro-oss/opsbro/misc/lolcat.py
# Compiled at: 2017-09-04 08:43:57
import atexit, math, os, random, re, sys, time
PY3 = sys.version_info >= (3, )
STRIP_ANSI = re.compile('\\x1b\\[(\\d+)(;\\d+)?(;\\d+)?[m|K]')
COLOR_ANSI = (
 (0, 0, 0), (205, 0, 0),
 (0, 205, 0), (205, 205, 0),
 (0, 0, 238), (205, 0, 205),
 (0, 205, 205), (229, 229, 229),
 (127, 127, 127), (255, 0, 0),
 (0, 255, 0), (255, 255, 0),
 (92, 92, 255), (255, 0, 255),
 (0, 255, 255), (255, 255, 255))

class LolCat(object):

    def __init__(self, mode=256, output=sys.stdout):
        self.mode = mode
        self.output = output

    def _distance(self, rgb1, rgb2):
        return sum(map(lambda c: (c[0] - c[1]) ** 2, zip(rgb1, rgb2)))

    def ansi(self, rgb):
        r, g, b = rgb
        if self.mode in (8, 16):
            colors = COLOR_ANSI[:self.mode]
            matches = [ (self._distance(c, map(int, rgb)), i) for i, c in enumerate(colors) ]
            matches.sort()
            color = matches[0][1]
            return '3%d' % (color,)
        else:
            gray_possible = True
            sep = 2.5
            while gray_possible:
                if r < sep or g < sep or b < sep:
                    gray = r < sep and g < sep and b < sep
                    gray_possible = False
                sep += 42.5

            if gray:
                color = 232 + int(float(sum(rgb) / 33.0))
            else:
                color = sum([16] + [ int(6 * float(val) / 256) * mod for val, mod in zip(rgb, [36, 6, 1])
                                   ])
            return '38;5;%d' % (color,)

    def wrap(self, *codes):
        return '\x1b[%sm' % (('').join(codes),)

    def rainbow(self, freq, i):
        r = math.sin(freq * i) * 127 + 128
        g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
        b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
        return [r, g, b]

    def cat(self, fd, options):
        if options.animate:
            self.output.write('\x1b[?25l')
        for line in fd:
            options.os += 1
            self.println(line, options)

        if options.animate:
            self.output.write('\x1b[?25h')

    def get_line(self, s, offset):
        s = s.rstrip()
        s = STRIP_ANSI.sub('', s)
        r = ''
        if isinstance(s, str):
            s = s.decode('utf-8', 'replace')
        for i, c in enumerate(s):
            rgb = self.rainbow(0.1, offset + i / 3.0)
            if isinstance(c, str):
                c = c.encode('utf-8', 'replace')
            r += ('').join([self.wrap(self.ansi(rgb)), c if PY3 else c])

        return r

    def println(self, s, options):
        s = s.rstrip()
        if options.force or self.output.isatty():
            s = STRIP_ANSI.sub('', s)
        if options.animate:
            self.println_ani(s, options)
        else:
            self.println_plain(s, options)
        self.output.write('\n')
        self.output.flush()

    def println_ani(self, s, options):
        if not s:
            return
        for i in range(1, options.duration):
            self.output.write('\x1b[%dD' % (len(s),))
            self.output.flush()
            options.os += options.spread
            self.println_plain(s, options)
            time.sleep(1.0 / options.speed)

    def println_plain(self, s, options):
        for i, c in enumerate(s if PY3 else s.decode(options.charset_py2, 'replace')):
            rgb = self.rainbow(options.freq, options.os + i / 3.0)
            self.output.write(('').join([
             self.wrap(self.ansi(rgb)),
             c if PY3 else c.encode(options.charset_py2, 'replace')]))


def detect_mode(term_hint='xterm-256color'):
    """
    Poor-mans color mode detection.
    """
    if 'ANSICON' in os.environ:
        return 16
    else:
        if os.environ.get('ConEmuANSI', 'OFF') == 'ON':
            return 256
        term = os.environ.get('TERM', term_hint)
        if term.endswith('-256color') or term in ('xterm', 'screen'):
            return 256
        if term.endswith('-color') or term in ('rxvt', ):
            return 16
        return 256


def run():
    """Main entry point."""
    import optparse

    def reset():
        sys.stdout.write('\x1b[0m')
        sys.stdout.flush()

    atexit.register(reset)
    parser = optparse.OptionParser(usage='%prog [<options>] [file ...]')
    parser.add_option('-p', '--spread', type='float', default=3.0, help='Rainbow spread')
    parser.add_option('-F', '--freq', type='float', default=0.1, help='Rainbow frequency')
    parser.add_option('-S', '--seed', type='int', default=0, help='Rainbow seed')
    parser.add_option('-a', '--animate', action='store_true', default=False, help='Enable psychedelics')
    parser.add_option('-d', '--duration', type='int', default=12, help='Animation duration')
    parser.add_option('-s', '--speed', type='float', default=20.0, help='Animation speed')
    parser.add_option('-f', '--force', action='store_true', default=False, help='Force colour even when stdout is not a tty')
    parser.add_option('-3', action='store_const', dest='mode', const=8, help='Force 3 bit colour mode')
    parser.add_option('-4', action='store_const', dest='mode', const=16, help='Force 4 bit colour mode')
    parser.add_option('-8', action='store_const', dest='mode', const=256, help='Force 8 bit colour mode')
    parser.add_option('-c', '--charset-py2', default='utf-8', help='Manually set a charset to convert from, for python 2.7')
    options, args = parser.parse_args()
    options.os = random.randint(0, 256) if options.seed == 0 else options.seed
    options.mode = options.mode or detect_mode()
    lolcat = LolCat(mode=options.mode)
    if not args:
        args = [
         '-']
    for filename in args:
        if filename == '-':
            lolcat.cat(sys.stdin, options)
        else:
            try:
                with open(filename, 'r') as (handle):
                    lolcat.cat(handle, options)
            except IOError as error:
                sys.stderr.write(str(error) + '\n')


lolcat = LolCat(mode=detect_mode())
if __name__ == '__main__':
    sys.exit(run())