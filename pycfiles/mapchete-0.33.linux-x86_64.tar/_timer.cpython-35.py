# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/_timer.py
# Compiled at: 2019-06-18 09:13:29
# Size of source mod 2**32: 1956 bytes
import time

class Timer:
    __doc__ = '\n    Context manager to facilitate timing code.\n\n    Examples\n    --------\n    >>> with Timer() as t:\n            ...  # some longer running code\n    >>> print(t)  # prints elapsed time\n\n    based on http://preshing.com/20110924/timing-your-code-using-pythons-with-statement/\n    '

    def __init__(self, elapsed=0.0, str_round=3):
        self._elapsed = elapsed
        self._str_round = str_round
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self._elapsed = self.end - self.start

    def __lt__(self, other):
        return self._elapsed < other._elapsed

    def __le__(self, other):
        return self._elapsed <= other._elapsed

    def __eq__(self, other):
        return self._elapsed == other._elapsed

    def __ne__(self, other):
        return self._elapsed != other._elapsed

    def __ge__(self, other):
        return self._elapsed >= other._elapsed

    def __gt__(self, other):
        return self._elapsed > other._elapsed

    def __add__(self, other):
        return Timer(elapsed=self._elapsed + other._elapsed)

    def __sub__(self, other):
        return Timer(elapsed=self._elapsed - other._elapsed)

    def __repr__(self):
        return 'Timer(start=%s, end=%s, elapsed=%s)' % (
         self.start, self.end, self.__str__())

    def __str__(self):
        minutes, seconds = divmod(self.elapsed, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return '%sh %sm %ss' % (int(hours), int(minutes), int(seconds))
        else:
            if minutes:
                return '%sm %ss' % (int(minutes), int(seconds))
            return '%ss' % round(seconds, self._str_round)

    @property
    def elapsed(self):
        if self.start and not self.end:
            return time.time() - self.start
        return self._elapsed