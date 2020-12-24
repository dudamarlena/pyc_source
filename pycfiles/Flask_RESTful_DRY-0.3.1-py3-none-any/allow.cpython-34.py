# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/allow.py
# Compiled at: 2015-04-14 08:45:00
# Size of source mod 2**32: 4807 bytes
"""Allow/deny objects.

All of these objects are intended to be immutable.
"""
__all__ = ('Allow', 'Deny')

class base:

    def __init__(self, *names):
        self._names = frozenset(names)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, sorted(self._names))

    def intersection(self, other):
        """Returns the intersection of self and other.

        Returns a new Allowed object.
        """
        if isinstance(other, Deny):
            return self.denying(*other._names)
        return self.intersection_allowed(other._names)

    def test(self, allowed, denied):
        a, d = self.allowed_denied(allowed)
        assert a == frozenset(allowed)
        assert not d
        a, d = self.allowed_denied(denied)
        assert not a
        assert d == frozenset(denied)


class Allow(base):
    __doc__ = "Allows a specific set of names.\n\n    These actually work for any hashable type.\n\n        >>> a = Allow('a', 'b', None)\n        >>> a.allow('a')\n        True\n        >>> a.allow(None)\n        True\n        >>> a.allow('d')\n        False\n        >>> a.test(('b', None), 'cd')\n    "

    def intersection_allowed(self, allowed):
        """Returns intersection with allowed set.

            >>> a = Allow('a', 'b')
            >>> b = Allow('b', 'c')
            >>> c = a.intersection(b)
            >>> c.test('b', 'acd')

            >>> b = Deny('b', 'c')
            >>> c = a.intersection(b)
            >>> c.test('a', 'bcd')
        """
        return Allow(*self._names.intersection(allowed))

    def allowing(self, *allow):
        """Create a copy allowing additional names.

            >>> a = Allow('a')
            >>> b = a.allowing('b', 'c')
            >>> a.test('a', 'bcd')
            >>> b.test('abc', 'd')
        """
        return Allow(*self._names.union(allow))

    def denying(self, *denied):
        """Create a copy denying specified names.

            >>> a = Allow('a', 'b')
            >>> b = a.denying('b')
            >>> a.test('ab', 'c')
            >>> b.test('a', 'bc')
        """
        return Allow(*self._names.difference(denied))

    def allow(self, name):
        """Return True iff `name` is allowed.

            >>> a = Allow('a', 'b')
            >>> a.allow('a')
            True
            >>> a.allow('c')
            False
        """
        return name in self._names

    def allowed_denied(self, names):
        """Determines the allowed and denied names from `names`.

        Returns two frozensets of names: allowed_names, denied_names.

            >>> a = Allow('a', 'b')
            >>> a.allowed_denied('ac')
            (frozenset({'a'}), frozenset({'c'}))
        """
        names = frozenset(names)
        allowed = self._names.intersection(names)
        return (allowed, names.difference(allowed))


class Deny(base):
    __doc__ = "Denies a specific set of names.\n\n        >>> d = Deny('a', 'b', None)\n        >>> d.allow('a')\n        False\n        >>> d.allow(None)\n        False\n        >>> d.allow('d')\n        True\n        >>> d.test('cd', ('b', None))\n    "

    def intersection_allowed(self, allowed):
        """Returns intersection with allowed set.

            >>> a = Deny('a', 'b')
            >>> b = Deny('b', 'c')
            >>> c = a.intersection(b)
            >>> c.test('d', 'abc')

            >>> b = Allow('b', 'c')
            >>> c = a.intersection(b)
            >>> c.test('c', 'abd')
        """
        return Allow(*allowed.difference(self._names))

    def allowing(self, *allowed):
        """Create a copy allowing additional names.

            >>> a = Deny('a', 'b')
            >>> b = a.allowing('b', 'c')
            >>> a.test('cd', 'ab')
            >>> b.test('bcd', 'a')
        """
        return Deny(*self._names.difference(allowed))

    def denying(self, *denied):
        """Create a copy denying specified names.

            >>> a = Deny('a', 'b')
            >>> b = a.denying('b', 'c')
            >>> a.test('cd', 'ab')
            >>> b.test('d', 'abc')
        """
        return Deny(*self._names.union(denied))

    def allow(self, name):
        """Return True iff `name` is allowed.

            >>> d = Deny('a', 'b')
            >>> d.allow('a')
            False
            >>> d.allow('c')
            True
        """
        return name not in self._names

    def allowed_denied(self, names):
        """Determines the allowed and denied names from `names`.

        Returns two frozensets of names: allowed_names, denied_names.

            >>> d = Deny('a', 'b')
            >>> d.allowed_denied('ac')
            (frozenset({'c'}), frozenset({'a'}))
        """
        names = frozenset(names)
        denied = self._names.intersection(names)
        return (names.difference(denied), denied)