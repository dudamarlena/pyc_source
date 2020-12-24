# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/grouper.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3883 bytes
import re
from .utils import FlexibleIterator
to_group = (('+', '='), ('-', '='), ('*', '='), ('/', '='), ('%', '='), ('&', '='),
            ('|', '='), ('^', '='), ('@', '='), ('/', '/'), ('*', '*'), ('<', '<'),
            ('>', '>'), ('=', '='), ('!', '='), ('<', '>'), ('<', '='), ('>', '='),
            ('**', '='), ('//', '='), ('<<', '='), ('>>', '='), ('\r', '\n'), ('.', '.'),
            ('..', '.'), ('-', '>'))
to_group_keys, _ = list(zip(*to_group))

def group(sequence):
    return list(group_generator(sequence))


def match_on_next(regex, iterator):
    return iterator.show_next() and re.match(regex, iterator.show_next())


def group_generator(sequence):
    iterator = FlexibleIterator(sequence)
    current = None
    while True:
        if iterator.end():
            return
        else:
            current = next(iterator)
            if current in to_group_keys:
                if matching_found(to_group, current, iterator.show_next()):
                    current += next(iterator)
            if current in to_group_keys:
                if matching_found(to_group, current, iterator.show_next()):
                    current += next(iterator)
            if current in list('uUfFrRbB'):
                if str(iterator.show_next()).startswith(('"', "'")):
                    current += next(iterator)
            if str(current).lower() in ('ur', 'br', 'fr', 'rf'):
                if str(iterator.show_next()).startswith(('"', "'")):
                    current += next(iterator)
            if any([re.match(x, current) for x in ('^\\d+[eE]$', '^\\d+\\.\\d*[eE]$',
                                                   '^\\.\\d+[eE]$')]):
                current += next(iterator)
                current += next(iterator)
                if not re.match('^\\d+[eE][-+]?\\d+[jJ]?$', current):
                    assert re.match('^\\d*.\\d*[eE][-+]?\\d+[jJ]?$', current)
            if current == '\\':
                if iterator.show_next() in ('\n', '\r\n'):
                    current += next(iterator)
                    if re.match('^\\s+$', str(iterator.show_next())):
                        current += next(iterator)
            if current == '\\':
                if iterator.show_next() == '\r':
                    if iterator.show_next(2) == '\n':
                        current += next(iterator)
                        current += next(iterator)
                        if re.match('^\\s+$', str(iterator.show_next())):
                            current += next(iterator)
            if re.match('^\\s+$', current):
                if iterator.show_next() == '\\':
                    current += next(iterator)
                    current += next(iterator)
                    if iterator.show_next() == '\n':
                        current += next(iterator)
                    if re.match('^\\s+$', str(iterator.show_next())):
                        current += next(iterator)
            if re.match('^\\d+$', current) and match_on_next('^\\.$', iterator) or current == '.' and match_on_next('^\\d+([jJ]|[eE]\\d*)?$', iterator):
                current += next(iterator)
                if match_on_next('^\\d*[jJ]?$', iterator):
                    if match_on_next('^\\d*[jJ]?$', iterator).group():
                        current += next(iterator)
            if re.match('^\\d+\\.$', current):
                if match_on_next('^\\d*[eE]\\d*$', iterator):
                    current += next(iterator)
            if re.match('^\\d+\\.?[eE]$', current):
                if match_on_next('^\\d+$', iterator):
                    current += next(iterator)
            if re.match('^\\d*\\.?\\d*[eE]$', current):
                if not re.match('[eE]', current):
                    if match_on_next('^[-+]$', iterator):
                        if iterator.show_next(2):
                            if re.match('^\\d+$', iterator.show_next(2)):
                                current += next(iterator)
                                current += next(iterator)
        if current == '..':
            yield '.'
            yield '.'
        else:
            yield current


def matching_found(to_group, current, target):
    return target in [x[1] for x in to_group if x[0] == current]