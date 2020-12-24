# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/scanner/scanner.py
# Compiled at: 2014-04-19 23:21:48
# Size of source mod 2**32: 4015 bytes
__doc__ = "\nJava-like input scanner.\n\nThe scanner breaks the input into tokens, and then converts them to\ndifferent types when requested using various next methods.\n\nThe following example allows to read a float from stdin:\n    # Input:\n    # 3 0.5\n    sc = Scanner()\n    x = sc.next_int()\n    y = sc.next_float()\n    type(x) is int # True\n    type(y) is float # True\n    x + y # 3.5\n\nThe following code allows to read until EOF and obtain int types:\n    # Assume input is:\n    # 10 20 30\n    # 40 50 60\n    sc = Scanner()\n    sum = 0\n    while sc.has_next():\n        sum += sc.next_int()\n    sum # 210\n\nThe default input stream is sys.stdin. However, it is possible\nto read from a file or even a string:\n    sc = Scanner(file='data.txt')\n    # do stuff\n    sc.close()\n    # Or\n    sc = Scanner(source='some string to use as input')\n\nThe scanner can also use string delimeters other than whitespace.\n    sc = Scanner(delim=',')\n\nBy default, the scanner does a str split. If forced, a regex pattern can also\nbe used. As expected, the latter method is slower:\n    content = '1 fish  2.5 fish red fish  blue fish\n    sc = Scanner(source=content, delim='\\S*fish\\S*', force_regex=True)\n    sc.next_int() # 1\n    sc.has_next() # True\n    sc.next_float() # 2.5\n    sc.next() # red\n    sc.next() # blue\n    sc.has_next() # False\n"
import io, re, sys

class Scanner:

    def __init__(self, file=None, source=None, delim=None, force_regex=False):
        if file:
            file = open(file, 'r')
        else:
            if source:
                file = io.StringIO(source)
            else:
                file = sys.stdin
        if force_regex and not delim:
            raise ValueError('delim must be specified with force_regex')
        self._file = file
        self._delim = delim
        self._force_regex = force_regex
        self._token = None
        self._tokens = None
        return

    def has_next(self):
        """Returns true if there's another token in the input."""
        return self.peek() is not None

    def next(self):
        """Returns the next token in the input as a string."""
        return self.next_token()

    def next_line(self):
        """Returns the remaining of the current line as a string."""
        current = self.next_token()
        rest = self._delim.join(self._tokens)
        return current + rest

    def next_int(self):
        """Returns the next token in the input as an int."""
        return self.next_type(int)

    def next_float(self):
        """Returns the next token in the input as a float."""
        return self.next_type(float)

    def next_type(self, func):
        """Convert the next token in the input as a given type func."""
        return func(self.next_token())

    def next_token(self):
        """Scans and returns the next token that matches the delimeter."""
        next_token = self.peek()
        self._token = None
        return next_token

    def peek(self):
        """Internal method. Creates a tokens iterator from the current line,
        and assigns the next token. When the iterator is finished, repeats
        the same process for the next line."""
        if self._token:
            return self._token
        else:
            if not self._tokens:
                line = self._file.readline()
                if not line:
                    return
                if self._force_regex:
                    splits = re.split(self._delim, line)
                else:
                    splits = line.split(self._delim)
                self._tokens = iter(splits)
            try:
                self._token = next(self._tokens)
            except StopIteration:
                self._tokens = None

            return self.peek()

    def is_stdin(self):
        """Returns true if sys.stdin is being used as the input."""
        return self._file == sys.stdin

    def close(self):
        """Closes the scanner, including open files if any."""
        if not self.is_stdin():
            self._file.close()