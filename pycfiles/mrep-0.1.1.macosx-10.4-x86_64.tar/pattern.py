# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/unno/.pyenv/versions/2.7.8/lib/python2.7/site-packages/mrep/pattern.py
# Compiled at: 2014-10-10 01:33:07


def find(s, m):

    class Collector(object):

        def __init__(self):
            self.pos = None
            return

        def collect(self, s, pos):
            if self.pos is None:
                self.pos = pos
                return True
            else:
                return

    result = []
    i = 0
    while i < len(s):
        collector = Collector()
        m.match(s[i:], 0, collector.collect)
        if collector.pos is not None:
            result.append({'match': s[i:i + collector.pos], 
               'begin': i, 
               'end': i + collector.pos})
            i += collector.pos
        else:
            i += 1

    return result


class Repeat(object):

    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, s, pos, after):

        def check_after(s, nxt):
            if nxt != pos:
                ret = self.match(s, nxt, after)
                if ret is not None:
                    return ret
                return after(s, nxt)
            else:
                return

        return self.matcher.match(s, pos, check_after)

    def __repr__(self):
        return '(* ' + repr(self.matcher) + ')'


class Condition(object):

    def __init__(self, func):
        self.func = func

    def match(self, s, pos, after):
        if pos < len(s) and self.func(s[pos]):
            return after(s, pos + 1)

    def __repr__(self):
        return '.'


class Select(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def match(self, s, pos, after):
        ret = self.left.match(s, pos, after)
        if ret is not None:
            return ret
        else:
            return self.right.match(s, pos, after)

    def __repr__(self):
        return '(OR ' + repr(self.left) + ' ' + repr(self.right) + ')'


class Sequence(object):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def match(self, s, pos, after):

        def apply_next(s, nxt):
            return self.second.match(s, nxt, after)

        return self.first.match(s, pos, apply_next)

    def __repr__(self):
        return repr(self.first) + ':' + repr(self.second)