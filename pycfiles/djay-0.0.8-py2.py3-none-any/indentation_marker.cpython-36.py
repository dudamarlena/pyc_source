# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/indentation_marker.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3878 bytes
from .utils import FlexibleIterator
import sys

def mark_indentation(sequence):
    return list(mark_indentation_generator(sequence))


def transform_tabs_to_spaces(string):
    return string.replace('\t', '        ')


def get_space(node):
    """ Return space formatting information of node.

    If the node does not have a third formatting item - like in
    a ('ENDL', '
') node - then we return None as a flag value. This is
    maybe not the best behavior but it seems to work for now.
    """
    if len(node) < 4 or len(node[3]) == 0:
        return
    else:
        return transform_tabs_to_spaces(node[3][0][1])


def mark_indentation_generator(sequence):
    iterator = FlexibleIterator(sequence)
    current = (None, None)
    indentations = []
    while True:
        if iterator.end():
            return
        else:
            current = next(iterator)
            if current is None:
                return
            if current[0] == 'ENDMARKER':
                if indentations:
                    while len(indentations) > 0:
                        yield ('DEDENT', '')
                        indentations.pop()

            if current[0] == 'COLON' and iterator.show_next(1)[0] == 'ENDL':
                if iterator.show_next(2)[0] not in ('ENDL', ):
                    indentations.append(get_space(iterator.show_next()))
                    yield current
                    yield next(iterator)
                    yield ('INDENT', '')
                    continue
                else:
                    yield current
                    for i in iterator:
                        if i[0] == 'ENDL' and iterator.show_next()[0] not in ('ENDL', ):
                            indentations.append(get_space(i))
                            yield ('INDENT', '')
                            yield i
                            break
                        yield i

                    continue
            if indentations:
                if current[0] == 'ENDL':
                    the_indentation_level_changed = get_space(current) is None or get_space(current) != indentations[(-1)]
                    if the_indentation_level_changed:
                        if iterator.show_next()[0] not in ('ENDL', 'COMMENT'):
                            new_indent = get_space(current) if len(current) == 4 else ''
                            yield current
                            while indentations and string_is_bigger(indentations[(-1)], new_indent):
                                indentations.pop()
                                yield ('DEDENT', '')

                            yield next(iterator)
                            continue
        yield current


def string_is_bigger(s1, s2):
    """ Return s1 > s2 by taking into account None values.

    None is always smaller than any string.

    None > "string" works in python2 but not in python3. This function
    makes it work in python3 too.
    """
    if s1 is None:
        return False
    else:
        if s2 is None:
            return True
        return s1 > s2