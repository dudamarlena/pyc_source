# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.3.0-Power_Macintosh/egg/simple_json/scanner.py
# Compiled at: 2005-12-25 18:07:59
import sre_parse, sre_compile, sre_constants
from sre_constants import BRANCH, SUBPATTERN
from sre import VERBOSE, MULTILINE, DOTALL
import re
__all__ = ['Scanner', 'pattern']
FLAGS = VERBOSE | MULTILINE | DOTALL

class Scanner(object):
    __module__ = __name__

    def __init__(self, lexicon, flags=FLAGS):
        self.actions = [None]
        s = sre_parse.Pattern()
        s.flags = flags
        p = []
        for (idx, token) in enumerate(lexicon):
            phrase = token.pattern
            try:
                subpattern = sre_parse.SubPattern(s, [
                 (
                  SUBPATTERN, (idx + 1, sre_parse.parse(phrase, flags)))])
            except sre_constants.error:
                print "Can't parse %s" % (token.__name__,)
                raise

            p.append(subpattern)
            self.actions.append(token)

        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile.compile(p)
        return

    def iterscan(self, string, dead=None, idx=0, context=None):
        """
        Yield match, end_idx for each match
        """
        match = self.scanner.scanner(string, idx).search
        actions = self.actions
        (i, j, k) = (0, 0, 0)
        end = len(string)
        while True:
            m = match()
            if m is None:
                break
            (k, j) = m.span()
            if i == j:
                break
            if k != i and dead is not None:
                rval = dead(string, i, k)
                if rval is not None:
                    yield (
                     rval, j)
            action = actions[m.lastindex]
            if action is not None:
                (rval, next_pos) = action(m, context)
                if next_pos is not None and next_pos != j:
                    j = next_pos
                    match = self.scanner.scanner(string, j).search
                yield (
                 rval, j)
            i = j

        if i != end and dead is not None:
            rval = dead(string, i, end)
            yield (rval, j)
        return


def pattern(pattern, flags=FLAGS):

    def decorator(fn):
        fn.pattern = pattern
        fn.regex = re.compile(pattern, flags)
        return fn

    return decorator


def InsignificantWhitespace(match, context):
    return (
     None, None)
    return


pattern('\\s+')(InsignificantWhitespace)