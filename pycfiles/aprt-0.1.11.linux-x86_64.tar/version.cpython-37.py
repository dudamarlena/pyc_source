# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/aprt/version.py
# Compiled at: 2019-08-02 08:01:39
# Size of source mod 2**32: 6166 bytes
import functools

def _split_if(string, condition):
    start = 0
    triggered = False
    for index, val in enumerate(string):
        if condition(val):
            yield string[start:index]
            start = index + 1

    yield string[start:]


def _cmp(a, b):
    return (a > b) - (a < b)


def _strcmp(a, b):
    for char_a, char_b in zip(a, b):
        if a == b:
            continue
        return _cmp(a, b)

    return _cmp(len(a), len(b))


@functools.total_ordering
class VersionComponent:
    __doc__ = '\n\tA version component which consists of a list of parts.\n\t'

    def __init__(self, component):
        self.original = component
        self.parts = list(self.__class__.split_parts(component))

    @staticmethod
    def split_parts(component):
        """
                Split a version component into alphabetical and decimal parts.
                The function is a string generator.
                """
        if not component:
            yield ''
            return
        start = 0
        numeric = component[0].isdecimal()
        for index, value in enumerate(component):
            if numeric != value.isdecimal():
                yield component[start:index]
                start = index
                numeric = not numeric

        yield component[start:]

    def __str__(self):
        return ''.join(self.parts)

    def __repr__(self):
        return repr(self.parts)

    def __cmp__(self, other):
        for me, him in zip(self.parts, other.parts):
            if me == him:
                continue
            else:
                me_decimal = me.isdecimal()
                him_decimal = him.isdecimal()
                if me_decimal != him_decimal:
                    return me_decimal - him_decimal
                if me_decimal and len(me) != len(him):
                    return _cmp(len(me), len(him))
            return _strcmp(me, him)

        return -1 * _cmp(len(self.parts), len(other.parts))

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0


def _format_pkgver(pkgver):
    return '.'.join(map(lambda x: str(x), pkgver))


@functools.total_ordering
class Version:
    __doc__ = '\n\tVersions consist of an optional epoch, a pkgver and an optional pkgrel.\n\tThe pkgver and pkgrel each consist of alphanumerical components,\n\twhich each consist of alphabetical and decimal parts.\n\t'

    def __init__(self, pkgver, pkgrel, epoch=0):
        self.pkgver_original = pkgver
        self.pkgrel_original = pkgrel
        self.pkgver = list(self.__class__.split_components(pkgver))
        self.pkgrel = list(self.__class__.split_components(pkgrel)) if pkgrel is not None else None
        self.epoch = int(epoch) if epoch is not None else 0

    @staticmethod
    def parse(string):
        """
                Parse a version string.
                """
        epoch, sep, rest = string.partition(':')
        if sep:
            epoch = int(epoch)
        else:
            rest = epoch
            epoch = 0
        pkgver, sep, pkgrel = rest.rpartition('-')
        if not sep:
            pkgver = pkgrel
            pkgrel = None
        return Version(pkgver, pkgrel, epoch)

    @staticmethod
    def split_components(component):
        """
                Split a version component into alphanumerical parts.
                """
        start = 0
        for index, val in enumerate(component):
            if not val.isalnum():
                yield VersionComponent(component[start:index])
                start = index + 1

        yield VersionComponent(component[start:])

    def withPkgrel(self, pkgrel):
        if pkgrel is not None:
            return Version(self.pkgver_original, str(pkgrel), self.epoch)
        return Version(self.pkgver_original, None, self.epoch)

    def withoutPkgrel(self):
        return self.withPkgrel(None)

    def __str__(self):
        if self.epoch == 0:
            if self.pkgrel is None:
                return '{}'.format(_format_pkgver(self.pkgver))
            return '{}-{}'.format(_format_pkgver(self.pkgver), _format_pkgver(self.pkgrel))
        else:
            if self.pkgrel is None:
                return '{}:{}'.format(self.epoch, _format_pkgver(self.pkgver))
            return '{}:{}-{}'.format(self.epoch, _format_pkgver(self.pkgver), _format_pkgver(self.pkgrel))

    def __repr__(self):
        return repr((self.pkgver, self.pkgrel, self.epoch))

    def __cmp__(self, other):
        if self.epoch != other.epoch:
            return _cmp(self.epoch, other.epoch)
        pkgver_dif = _cmp(self.pkgver, other.pkgver)
        if pkgver_dif != 0:
            return pkgver_dif
        if self.pkgrel is None or other.pkgrel is None:
            return 0
        return _cmp(self.pkgrel, other.pkgrel)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0