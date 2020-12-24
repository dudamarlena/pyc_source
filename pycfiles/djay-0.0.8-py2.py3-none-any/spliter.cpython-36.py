# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/spliter.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3003 bytes
import string
from .utils import FlexibleIterator, BaronError

def split(sequence):
    return list(split_generator(sequence))


class UntreatedError(BaronError):
    pass


def split_generator(sequence):
    iterator = FlexibleIterator(sequence)
    while not iterator.end():
        not_found = True
        if iterator.next_in('#'):
            not_found = False
            result = iterator.grab(lambda iterator: iterator.show_next() not in '\r\n')
            yield result
        for section in ("'", '"'):
            if iterator.next_starts_with(section * 3):
                not_found = False
                result = next(iterator)
                result += next(iterator)
                result += next(iterator)
                result += iterator.grab_string(lambda iterator: not iterator.next_starts_with(section * 3))
                try:
                    result += next(iterator)
                    result += next(iterator)
                    result += next(iterator)
                except StopIteration:
                    pass

                yield result
            else:
                if iterator.next_in(section):
                    not_found = False
                    result = next(iterator)
                    result += iterator.grab_string(lambda iterator: iterator.show_next() not in section)
                    try:
                        result += next(iterator)
                    except StopIteration:
                        pass

                    yield result

        for section in (string.ascii_letters + '_' + '1234567890', ' \t'):
            if iterator.next_in(section):
                not_found = False
                yield iterator.grab(lambda iterator: iterator.show_next() in section)

        for one in '@,.;()=*:+-/^%&<>|\r\n~[]{}!``\\':
            if iterator.next_in(one):
                not_found = False
                yield next(iterator)

        if iterator.show_next().__repr__().startswith("'\\x"):
            not_found = False
            next(iterator)
        if not_found:
            raise UntreatedError('Untreated elements: %s' % iterator.rest_of_the_sequence().__repr__()[:50])