# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/ZestyParser/DebuggingParser.py
# Compiled at: 2007-04-30 17:11:14
"""
@version: 0.8.1
@author: Adam Atlas
@copyright: Copyright 2006-2007 Adam Atlas. Released under the MIT license (see LICENSE.txt).
@contact: adam@atlas.st
"""
import Parser, sys

class DebuggingParser(Parser.ZestyParser):
    """
    A L{Parser.ZestyParser} subclass which is useful for debugging parsers. It parses as usual, but it also prints a comprehensive trace to stderr.
    """
    __module__ = __name__
    depth = -1

    def __init__(self, *a, **k):
        self.dest = k.pop('dest', sys.stderr)
        Parser.ZestyParser.__init__(self, *a, **k)

    def scan(self, token):
        self.depth += 1
        ind = ' |  ' * self.depth
        self.dest.write('%sBeginning to scan for %r at position %i\n' % (ind, token, self.cursor))
        r = Parser.ZestyParser.scan(self, token)
        if self.last:
            self.dest.write('%sGot %r -- now at %i\n' % (ind, r, self.cursor))
        else:
            self.dest.write("%sDidn't match\n" % ind)
        self.depth -= 1
        return r

    def skip(self, token):
        self.depth += 1
        ind = ' |  ' * self.depth
        self.dest.write('%sBeginning to skip %r at position %i\n' % (ind, token, self.cursor))
        r = Parser.ZestyParser.skip(self, token)
        if r:
            self.dest.write('%sMatched -- now at %i\n' % (ind, self.cursor))
        else:
            self.dest.write("%sDidn't match\n" % ind)
        self.depth -= 1
        return r

    def iter(self, token, *args, **kwargs):
        self.depth += 1
        ind = ' |  ' * self.depth
        self.dest.write('%sBeginning to iterate %r at position %i\n' % (ind, token, self.cursor))
        i = Parser.ZestyParser.iter(self, token, *args, **kwargs)
        while 1:
            self.dest.write('%sIterating\n' % ind)
            yield i.next()

        self.dest.write('%sDone iterating -- now at %i\n' % (ind, self.cursor))
        self.depth -= 1