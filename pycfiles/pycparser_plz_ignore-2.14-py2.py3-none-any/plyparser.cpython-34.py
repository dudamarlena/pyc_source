# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../pycparser/plyparser.py
# Compiled at: 2015-10-01 19:10:08
# Size of source mod 2**32: 1594 bytes


class Coord(object):
    __doc__ = ' Coordinates of a syntactic element. Consists of:\n            - File name\n            - Line number\n            - (optional) column number, for the Lexer\n    '
    __slots__ = ('file', 'line', 'column', '__weakref__')

    def __init__(self, file, line, column=None):
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        str = '%s:%s' % (self.file, self.line)
        if self.column:
            str += ':%s' % self.column
        return str


class ParseError(Exception):
    pass


class PLYParser(object):

    def _create_opt_rule(self, rulename):
        """ Given a rule name, creates an optional ply.yacc rule
            for it. The name of the optional rule is
            <rulename>_opt
        """
        optname = rulename + '_opt'

        def optrule(self, p):
            p[0] = p[1]

        optrule.__doc__ = '%s : empty\n| %s' % (optname, rulename)
        optrule.__name__ = 'p_%s' % optname
        setattr(self.__class__, optrule.__name__, optrule)

    def _coord(self, lineno, column=None):
        return Coord(file=self.clex.filename, line=lineno, column=column)

    def _parse_error(self, msg, coord):
        raise ParseError('%s: %s' % (coord, msg))