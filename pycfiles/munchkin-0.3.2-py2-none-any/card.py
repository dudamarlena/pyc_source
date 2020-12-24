# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/card.py
# Compiled at: 2016-05-02 03:44:35
import logging, sys, numpy as np, strategies
from passwordcard import passwordcard
from strategies.left_to_right import left_to_right
from strategies.right_to_left import right_to_left
from strategies.top_to_down import top_to_down
from strategies.bottom_to_top import bottom_to_top
from strategies.zig_zag import zig_zag
from strategies.zig_zag_reverse import zig_zag_reverse
from strategies.diagonal import diagonal
from strategies.angled import angled
from strategies.spiral import spiral
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

class Card:
    """ Represents a password card """

    def __init__(self, args):
        self._m = None
        self._args = vars(args)
        self._seed = self._args.get('seed')
        self._header = None
        return

    @staticmethod
    def _validate_matrix(m):
        """ Validates custom cards supplied by the user """
        try:
            matrix = np.matrix(m)
        except TypeError:
            logging.error('Invalid password card format, please try again')
            sys.exit(2)

        for i in range(0, len(m) - 1):
            if not len(m[i]) == len(m[(i + 1)]):
                logging.error('Invalid password card format, please try again')
                sys.exit(2)

        return matrix

    def _generate_data_streams(self):
        """ Adds appropriate character streams based on the selected card reading strategies """
        streams = {'default': []}
        if self._args.get('left_to_right'):
            results = left_to_right(self)
            streams['default'].append(results)
        if self._args.get('right_to_left'):
            results = right_to_left(self)
            streams['default'].append(results)
        if self._args.get('top_down'):
            results = top_to_down(self)
            streams['default'].append(results)
        if self._args.get('bottom_up'):
            results = bottom_to_top(self)
            streams['default'].append(results)
        if self._args.get('zig_zag'):
            results = zig_zag(self)
            streams['default'].append(results)
        if self._args.get('zig_zag_rev'):
            results = zig_zag_reverse(self)
            streams['default'].append(results)
        if self._args.get('diagonal'):
            results = diagonal(self)
            streams['default'].append(results)
        if self._args.get('angled'):
            data = angled(self)
            for i in range(0, len(data)):
                streams['default'].append(data[i])

        if self._args.get('spiral'):
            data = spiral(self)
            streams['spiral'] = []
            for i in range(0, len(data)):
                if len(data[i]) >= int(self._args.get('minlen')):
                    streams['spiral'].append(data[i])

        return streams

    @staticmethod
    def _passwords_generator(streams, pwlen):
        """ Generator that dumps the passwords for each card read strategy """
        for stream in streams['default']:
            counter = 0
            while counter + pwlen < len(stream) + 1:
                result = stream[counter:counter + pwlen]
                yield ('').join(result)
                counter += 1

        if streams.get('spiral'):
            for stream in streams['spiral']:
                if len(stream) >= pwlen:
                    result = stream[0:pwlen]
                    yield ('').join(result)

    def generate_password_card(self, digits=False, symbols=False):
        """ Generate password card as on http://passwordcard.org """
        m = []
        header, card = passwordcard.generate_card(self._seed, digits=digits, symbols=symbols)
        for row in card:
            m.append(list(row))

        self._m = self._validate_matrix(m)
        self._header = header
        return self._m

    def generate_custom_card(self, m):
        """ Generates custom password card """
        self._m = self._validate_matrix(m)
        return self._m

    @property
    def m(self):
        """ Return password card matrix """
        return self._m

    @property
    def rows(self):
        """ Get number of password card rows """
        return self._m.shape[0]

    @property
    def columns(self):
        """ Get number of password card columns """
        return self._m.shape[1]

    @property
    def print_card(self):
        """ Generates fancy password card box """
        output = []
        try:
            header = ' %s ' % self._seed
        except AttributeError:
            header = ' PASSWORD CARD '

        if len(header) + 2 > self.columns:
            top = '+-' + '-' * self.columns + '-+\r'
        else:
            top = '+-%s-+\r' % header.center(self.columns, '-')
        output.append(top)
        empty_line = '| ' + ' ' * self.columns + ' |'
        output.append(empty_line)
        if self._header:
            row = '| %s |' % self._header.center(self.columns)
            output.append(row)
            output.append(empty_line)
        for i in range(len(self._m)):
            row = ('').join(self._m.tolist()[i])
            row = '| %s |' % row.center(self.columns)
            output.append(row)

        output.append(empty_line)
        dimensions = ' %sx%s ' % (self.rows, self.columns)
        bottom = '+%s+\r' % dimensions.center(self.columns + 2, '-')
        output.append(bottom)
        output.append('\r')
        return ('\r\n').join(output)

    @property
    def passwords(self):
        """ Dumps passwords from the password card """
        streams = self._generate_data_streams()
        for pwlen in range(int(self._args.get('minlen')), int(self._args.get('maxlen')) + 1):
            for password in self._passwords_generator(streams, pwlen):
                yield password