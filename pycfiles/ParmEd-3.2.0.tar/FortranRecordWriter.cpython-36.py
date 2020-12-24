# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/FortranRecordWriter.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 1680 bytes
from ._output import output as _output
from ._lexer import lexer as _lexer
from ._parser import parser as _parser

class FortranRecordWriter(object):
    __doc__ = "\n    Generate a writer object for FORTRAN format strings\n\n    Typical use case ...\n\n    >>> header_line = FortranRecordWriter('(A15, A15, A15)')\n    >>> header_line.write(['x', 'y', 'z'])\n    '              x              y              z'\n    >>> line = FortranRecordWriter('(3F15.3)')\n    >>> line.write([1.0, 0.0, 0.5])\n    '          1.000          0.000          0.500'\n    >>> line.write([1.1, 0.1, 0.6])\n    '          1.100          0.100          0.600'\n\n    Note: it is best to create a new object for each format, changing the format\n    causes the parser to reevalute the format string which is costly in terms of\n    performance\n    "

    def __init__(self, format):
        self._eds = []
        self._rev_eds = []
        self.format = format

    def __eq__(self, other):
        if isinstance(other, FortranRecordWriter):
            return self.format == other.format
        else:
            return object.__eq__(self, other)

    def write(self, values):
        """
        Pass a list of values correspoding to the FORTRAN format specified
        to generate a string
        """
        return _output(self._eds, self._rev_eds, values)

    def get_format(self):
        return self._format

    def set_format(self, format):
        self._format = format
        self._parse_format()

    format = property(get_format, set_format)

    def _parse_format(self):
        self._eds, self._rev_eds = _parser(_lexer(self.format))


if __name__ == '__main__':
    import doctest
    doctest.testmod()