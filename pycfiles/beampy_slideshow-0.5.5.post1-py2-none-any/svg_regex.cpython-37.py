# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/scour/svg_regex.py
# Compiled at: 2018-07-04 13:16:55
# Size of source mod 2**32: 11300 bytes
""" Small hand-written recursive descent parser for SVG <path> data.

In [1]: from svg_regex import svg_parser

In [3]: svg_parser.parse('M 10,20 30,40V50 60 70')
Out[3]: [('M', [(10.0, 20.0), (30.0, 40.0)]), ('V', [50.0, 60.0, 70.0])]

In [4]: svg_parser.parse('M 0.6051.5')  # An edge case
Out[4]: [('M', [(0.60509999999999997, 0.5)])]

In [5]: svg_parser.parse('M 100-200')  # Another edge case
Out[5]: [('M', [(100.0, -200.0)])]
"""
from __future__ import absolute_import
import re
from decimal import Decimal, getcontext
from functools import partial

class _EOF(object):

    def __repr__(self):
        return 'EOF'


EOF = _EOF()
lexicon = [
 ('float', '[-+]?(?:(?:[0-9]*\\.[0-9]+)|(?:[0-9]+\\.?))(?:[Ee][-+]?[0-9]+)?'),
 ('int', '[-+]?[0-9]+'),
 ('command', '[AaCcHhLlMmQqSsTtVvZz]')]

class Lexer(object):
    __doc__ = " Break SVG path data into tokens.\n\n    The SVG spec requires that tokens are greedy. This lexer relies on Python's\n    regexes defaulting to greediness.\n\n    This style of implementation was inspired by this article:\n\n        http://www.gooli.org/blog/a-simple-lexer-in-python/\n    "

    def __init__(self, lexicon):
        self.lexicon = lexicon
        parts = []
        for name, regex in lexicon:
            parts.append('(?P<%s>%s)' % (name, regex))

        self.regex_string = '|'.join(parts)
        self.regex = re.compile(self.regex_string)

    def lex(self, text):
        """ Yield (token_type, str_data) tokens.

        The last token will be (EOF, None) where EOF is the singleton object
        defined in this module.
        """
        for match in self.regex.finditer(text):
            for name, _ in self.lexicon:
                m = match.group(name)
                if m is not None:
                    yield (
                     name, m)
                    break

        yield (
         EOF, None)


svg_lexer = Lexer(lexicon)

class SVGPathParser(object):
    __doc__ = " Parse SVG <path> data into a list of commands.\n\n    Each distinct command will take the form of a tuple (command, data). The\n    `command` is just the character string that starts the command group in the\n    <path> data, so 'M' for absolute moveto, 'm' for relative moveto, 'Z' for\n    closepath, etc. The kind of data it carries with it depends on the command.\n    For 'Z' (closepath), it's just None. The others are lists of individual\n    argument groups. Multiple elements in these lists usually mean to repeat the\n    command. The notable exception is 'M' (moveto) where only the first element\n    is truly a moveto. The remainder are implicit linetos.\n\n    See the SVG documentation for the interpretation of the individual elements\n    for each command.\n\n    The main method is `parse(text)`. It can only consume actual strings, not\n    filelike objects or iterators.\n    "

    def __init__(self, lexer=svg_lexer):
        self.lexer = lexer
        self.command_dispatch = {'Z':self.rule_closepath, 
         'z':self.rule_closepath, 
         'M':self.rule_moveto_or_lineto, 
         'm':self.rule_moveto_or_lineto, 
         'L':self.rule_moveto_or_lineto, 
         'l':self.rule_moveto_or_lineto, 
         'H':self.rule_orthogonal_lineto, 
         'h':self.rule_orthogonal_lineto, 
         'V':self.rule_orthogonal_lineto, 
         'v':self.rule_orthogonal_lineto, 
         'C':self.rule_curveto3, 
         'c':self.rule_curveto3, 
         'S':self.rule_curveto2, 
         's':self.rule_curveto2, 
         'Q':self.rule_curveto2, 
         'q':self.rule_curveto2, 
         'T':self.rule_curveto1, 
         't':self.rule_curveto1, 
         'A':self.rule_elliptical_arc, 
         'a':self.rule_elliptical_arc}
        self.number_tokens = list(['int', 'float'])

    def parse(self, text):
        """ Parse a string of SVG <path> data.
        """
        gen = self.lexer.lex(text)
        next_val_fn = partial(next, *(gen,))
        token = next_val_fn()
        return self.rule_svg_path(next_val_fn, token)

    def rule_svg_path(self, next_val_fn, token):
        commands = []
        while token[0] is not EOF:
            if token[0] != 'command':
                raise SyntaxError('expecting a command; got %r' % (token,))
            rule = self.command_dispatch[token[1]]
            command_group, token = rule(next_val_fn, token)
            commands.append(command_group)

        return commands

    def rule_closepath(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        return ((command, []), token)

    def rule_moveto_or_lineto(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        coordinates = []
        while token[0] in self.number_tokens:
            pair, token = self.rule_coordinate_pair(next_val_fn, token)
            coordinates.extend(pair)

        return (
         (
          command, coordinates), token)

    def rule_orthogonal_lineto(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        coordinates = []
        while token[0] in self.number_tokens:
            coord, token = self.rule_coordinate(next_val_fn, token)
            coordinates.append(coord)

        return (
         (
          command, coordinates), token)

    def rule_curveto3(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        coordinates = []
        while token[0] in self.number_tokens:
            pair1, token = self.rule_coordinate_pair(next_val_fn, token)
            pair2, token = self.rule_coordinate_pair(next_val_fn, token)
            pair3, token = self.rule_coordinate_pair(next_val_fn, token)
            coordinates.extend(pair1)
            coordinates.extend(pair2)
            coordinates.extend(pair3)

        return (
         (
          command, coordinates), token)

    def rule_curveto2(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        coordinates = []
        while token[0] in self.number_tokens:
            pair1, token = self.rule_coordinate_pair(next_val_fn, token)
            pair2, token = self.rule_coordinate_pair(next_val_fn, token)
            coordinates.extend(pair1)
            coordinates.extend(pair2)

        return (
         (
          command, coordinates), token)

    def rule_curveto1(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        coordinates = []
        while token[0] in self.number_tokens:
            pair1, token = self.rule_coordinate_pair(next_val_fn, token)
            coordinates.extend(pair1)

        return (
         (
          command, coordinates), token)

    def rule_elliptical_arc(self, next_val_fn, token):
        command = token[1]
        token = next_val_fn()
        arguments = []
        while token[0] in self.number_tokens:
            rx = Decimal(token[1]) * 1
            if rx < Decimal('0.0'):
                raise SyntaxError('expecting a nonnegative number; got %r' % (token,))
            else:
                token = next_val_fn()
                if token[0] not in self.number_tokens:
                    raise SyntaxError('expecting a number; got %r' % (token,))
                else:
                    ry = Decimal(token[1]) * 1
                    if ry < Decimal('0.0'):
                        raise SyntaxError('expecting a nonnegative number; got %r' % (token,))
                    token = next_val_fn()
                    if token[0] not in self.number_tokens:
                        raise SyntaxError('expecting a number; got %r' % (token,))
                    axis_rotation = Decimal(token[1]) * 1
                    token = next_val_fn()
                    if token[1][0] not in ('0', '1'):
                        raise SyntaxError('expecting a boolean flag; got %r' % (token,))
                    large_arc_flag = Decimal(token[1][0]) * 1
                    if len(token[1]) > 1:
                        token = list(token)
                        token[1] = token[1][1:]
                    else:
                        token = next_val_fn()
                if token[1][0] not in ('0', '1'):
                    raise SyntaxError('expecting a boolean flag; got %r' % (token,))
                sweep_flag = Decimal(token[1][0]) * 1
                if len(token[1]) > 1:
                    token = list(token)
                    token[1] = token[1][1:]
                else:
                    token = next_val_fn()
            if token[0] not in self.number_tokens:
                raise SyntaxError('expecting a number; got %r' % (token,))
            x = Decimal(token[1]) * 1
            token = next_val_fn()
            if token[0] not in self.number_tokens:
                raise SyntaxError('expecting a number; got %r' % (token,))
            y = Decimal(token[1]) * 1
            token = next_val_fn()
            arguments.extend([rx, ry, axis_rotation, large_arc_flag, sweep_flag, x, y])

        return ((command, arguments), token)

    def rule_coordinate(self, next_val_fn, token):
        if token[0] not in self.number_tokens:
            raise SyntaxError('expecting a number; got %r' % (token,))
        x = getcontext().create_decimal(token[1])
        token = next_val_fn()
        return (x, token)

    def rule_coordinate_pair(self, next_val_fn, token):
        if token[0] not in self.number_tokens:
            raise SyntaxError('expecting a number; got %r' % (token,))
        x = getcontext().create_decimal(token[1])
        token = next_val_fn()
        if token[0] not in self.number_tokens:
            raise SyntaxError('expecting a number; got %r' % (token,))
        y = getcontext().create_decimal(token[1])
        token = next_val_fn()
        return ([x, y], token)


svg_parser = SVGPathParser()