# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: arsenal/alphabet.py
# Compiled at: 2016-10-11 13:19:10
import os
from numpy.random import randint

class Alphabet(object):
    """
    Bijective mapping from strings to integers.

    >>> a = Alphabet()
    >>> [a[x] for x in 'abcd']
    [0, 1, 2, 3]
    >>> map(a.lookup, range(4))
    ['a', 'b', 'c', 'd']

    >>> a.stop_growth()
    >>> a['e']

    >>> a.freeze()
    >>> a.add('z')
    Traceback (most recent call last):
      ...
    ValueError: Alphabet is frozen. Key "z" not found.

    >>> print a.plaintext()
    a
    b
    c
    d
    """

    def __init__(self, random_int=None):
        self._mapping = {}
        self._flip = {}
        self._i = 0
        self._frozen = False
        self._growing = True
        self._random_int = random_int

    def __repr__(self):
        return 'Alphabet(size=%s,frozen=%s)' % (len(self), self._frozen)

    def freeze(self):
        self._frozen = True

    def stop_growth(self):
        self._growing = False

    @classmethod
    def from_iterable(cls, s):
        """Assumes keys are strings."""
        inst = cls()
        for x in s:
            inst.add(x)

        return inst

    def keys(self):
        return self._mapping.iterkeys()

    def items(self):
        return self._mapping.iteritems()

    def imap(self, seq, emit_none=False):
        """
        Apply alphabet to sequence while filtering. By default, `None` is not
        emitted, so the Note that the output sequence may have fewer items.
        """
        if emit_none:
            for s in seq:
                yield self[s]

        else:
            for s in seq:
                x = self[s]
                if x is not None:
                    yield x

        return

    def map(self, seq, *args, **kwargs):
        return list(self.imap(seq, *args, **kwargs))

    def add_many(self, x):
        for k in x:
            self.add(k)

    def lookup(self, i):
        if i is None:
            return
        else:
            return self._flip[i]

    def lookup_many(self, x):
        return map(self.lookup, x)

    def __contains__(self, k):
        return k in self._mapping

    def __getitem__(self, k):
        try:
            return self._mapping[k]
        except KeyError:
            if self._frozen:
                raise ValueError('Alphabet is frozen. Key "%s" not found.' % (k,))
            if not self._growing:
                return
            if self._random_int:
                x = self._mapping[k] = randint(0, self._random_int)
            else:
                x = self._mapping[k] = self._i
                self._i += 1
            self._flip[x] = k
            return x

        return

    add = __getitem__

    def __setitem__(self, k, v):
        assert k not in self._mapping
        assert isinstance(v, int)
        self._mapping[k] = v
        self._flip[v] = k

    def __iter__(self):
        for i in xrange(len(self)):
            yield self._flip[i]

    def enum(self):
        for i in xrange(len(self)):
            yield (
             i, self._flip[i])

    def __len__(self):
        return len(self._mapping)

    def plaintext(self):
        """assumes keys are strings"""
        return ('\n').join(self)

    @classmethod
    def load(cls, filename):
        if not os.path.exists(filename):
            return cls()
        with file(filename) as (f):
            return cls.from_iterable(l.strip() for l in f)

    def save(self, filename):
        with file(filename, 'wb') as (f):
            f.write(self.plaintext())

    def __eq__(self, other):
        return self._mapping == other._mapping


if __name__ == '__main__':
    import doctest
    doctest.testmod()