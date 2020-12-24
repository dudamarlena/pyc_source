# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google_input_parser/InputParser.py
# Compiled at: 2012-05-05 08:53:30


class Parser(object):

    def __init__(self, filename):
        """Splits the input into T chunks.
        T is the number in the first line."""
        lines = [ l.strip() for l in open(filename).readlines() ]
        num_chunks = int(lines[0])
        chunk_size = (len(lines) - 1) / num_chunks
        self.chunks = [ lines[1:][chunk_size * i:chunk_size * (i + 1)] for i in range(num_chunks)
                      ]
        self.chunks = [ [ self.numerize_line(line) for line in chunk ] for chunk in self.chunks
                      ]

    @staticmethod
    def numerize(item):
        """Converts an item to a numeric value. Falls back to strings.
        
        >>> Parser.numerize(3)
        3
        >>> Parser.numerize("  3   ")
        3
        >>> Parser.numerize("55.57")
        55.57
        >>> Parser.numerize("Million")
        'Million'
        """
        try:
            return int(item)
        except ValueError:
            try:
                return float(item)
            except ValueError:
                return item

    @staticmethod
    def numerize_line(line):
        """Converts a line to a tuple of numerize() items.
        
        >>> Parser.numerize_line( '1.0 2 BLAH' )
        (1.0, 2, 'BLAH')"""
        return tuple([ Parser.numerize(item) for item in line.split() ])

    def get_chunks(self):
        return self.chunks


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False)