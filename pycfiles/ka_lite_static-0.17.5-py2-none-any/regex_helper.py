# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/regex_helper.py
# Compiled at: 2018-07-11 18:15:30
"""
Functions for reversing a regular expression (used in reverse URL resolving).
Used internally by Django and not intended for external use.

This is not, and is not intended to be, a complete reg-exp decompiler. It
should be good enough for a large class of URLS, however.
"""
from __future__ import unicode_literals
from django.utils import six
from django.utils.six.moves import zip
ESCAPE_MAPPINGS = {b'A': None, 
   b'b': None, 
   b'B': None, 
   b'd': b'0', 
   b'D': b'x', 
   b's': b' ', 
   b'S': b'x', 
   b'w': b'x', 
   b'W': b'!', 
   b'Z': None}

class Choice(list):
    """
    Used to represent multiple possibilities at this point in a pattern string.
    We use a distinguished type, rather than a list, so that the usage in the
    code is clear.
    """
    pass


class Group(list):
    """
    Used to represent a capturing group in the pattern string.
    """
    pass


class NonCapture(list):
    """
    Used to represent a non-capturing group in the pattern string.
    """
    pass


def normalize(pattern):
    r"""
    Given a reg-exp pattern, normalizes it to an iterable of forms that
    suffice for reverse matching. This does the following:

    (1) For any repeating sections, keeps the minimum number of occurrences
        permitted (this means zero for optional groups).
    (2) If an optional group includes parameters, include one occurrence of
        that group (along with the zero occurrence case from step (1)).
    (3) Select the first (essentially an arbitrary) element from any character
        class. Select an arbitrary character for any unordered class (e.g. '.'
        or '\w') in the pattern.
    (5) Ignore comments and any of the reg-exp flags that won't change
        what we construct ("iLmsu"). "(?x)" is an error, however.
    (6) Raise an error on all other non-capturing (?...) forms (e.g.
        look-ahead and look-behind matches) and any disjunctive ('|')
        constructs.

    Django's URLs for forward resolving are either all positional arguments or
    all keyword arguments. That is assumed here, as well. Although reverse
    resolving can be done using positional args when keyword args are
    specified, the two cannot be mixed in the same reverse() call.
    """
    result = []
    non_capturing_groups = []
    consume_next = True
    pattern_iter = next_char(iter(pattern))
    num_args = 0
    try:
        ch, escaped = next(pattern_iter)
    except StopIteration:
        return [
         (
          b'', [])]

    try:
        while True:
            if escaped:
                result.append(ch)
            elif ch == b'.':
                result.append(b'.')
            elif ch == b'|':
                raise NotImplementedError
            elif ch == b'^':
                pass
            elif ch == b'$':
                break
            elif ch == b')':
                start = non_capturing_groups.pop()
                inner = NonCapture(result[start:])
                result = result[:start] + [inner]
            elif ch == b'[':
                ch, escaped = next(pattern_iter)
                result.append(ch)
                ch, escaped = next(pattern_iter)
                while escaped or ch != b']':
                    ch, escaped = next(pattern_iter)

            elif ch == b'(':
                ch, escaped = next(pattern_iter)
                if ch != b'?' or escaped:
                    name = b'_%d' % num_args
                    num_args += 1
                    result.append(Group((b'%%(%s)s' % name, name)))
                    walk_to_end(ch, pattern_iter)
                else:
                    ch, escaped = next(pattern_iter)
                    if ch in b'iLmsu#':
                        walk_to_end(ch, pattern_iter)
                    elif ch == b':':
                        non_capturing_groups.append(len(result))
                    elif ch != b'P':
                        raise ValueError(b"Non-reversible reg-exp portion: '(?%s'" % ch)
                    else:
                        ch, escaped = next(pattern_iter)
                        if ch not in ('<', '='):
                            raise ValueError(b"Non-reversible reg-exp portion: '(?P%s'" % ch)
                        if ch == b'<':
                            terminal_char = b'>'
                        else:
                            terminal_char = b')'
                        name = []
                        ch, escaped = next(pattern_iter)
                        while ch != terminal_char:
                            name.append(ch)
                            ch, escaped = next(pattern_iter)

                        param = (b'').join(name)
                        if terminal_char != b')':
                            result.append(Group((b'%%(%s)s' % param, param)))
                            walk_to_end(ch, pattern_iter)
                        else:
                            result.append(Group((b'%%(%s)s' % param, None)))
            elif ch in b'*?+{':
                count, ch = get_quantifier(ch, pattern_iter)
                if ch:
                    consume_next = False
                if count == 0:
                    if contains(result[(-1)], Group):
                        result[-1] = Choice([None, result[(-1)]])
                    else:
                        result.pop()
                elif count > 1:
                    result.extend([result[(-1)]] * (count - 1))
            else:
                result.append(ch)
            if consume_next:
                ch, escaped = next(pattern_iter)
            else:
                consume_next = True

    except StopIteration:
        pass
    except NotImplementedError:
        return [(b'', [])]

    return list(zip(*flatten_result(result)))


def next_char(input_iter):
    r"""
    An iterator that yields the next character from "pattern_iter", respecting
    escape sequences. An escaped character is replaced by a representative of
    its class (e.g. \w -> "x"). If the escaped character is one that is
    skipped, it is not returned (the next character is returned instead).

    Yields the next character, along with a boolean indicating whether it is a
    raw (unescaped) character or not.
    """
    for ch in input_iter:
        if ch != b'\\':
            yield (
             ch, False)
            continue
        ch = next(input_iter)
        representative = ESCAPE_MAPPINGS.get(ch, ch)
        if representative is None:
            continue
        yield (
         representative, True)

    return


def walk_to_end(ch, input_iter):
    """
    The iterator is currently inside a capturing group. We want to walk to the
    close of this group, skipping over any nested groups and handling escaped
    parentheses correctly.
    """
    if ch == b'(':
        nesting = 1
    else:
        nesting = 0
    for ch, escaped in input_iter:
        if escaped:
            continue
        elif ch == b'(':
            nesting += 1
        elif ch == b')':
            if not nesting:
                return
            nesting -= 1


def get_quantifier(ch, input_iter):
    """
    Parse a quantifier from the input, where "ch" is the first character in the
    quantifier.

    Returns the minimum number of occurences permitted by the quantifier and
    either None or the next character from the input_iter if the next character
    is not part of the quantifier.
    """
    if ch in b'*?+':
        try:
            ch2, escaped = next(input_iter)
        except StopIteration:
            ch2 = None

        if ch2 == b'?':
            ch2 = None
        if ch == b'+':
            return (1, ch2)
        return (0, ch2)
    else:
        quant = []
        while ch != b'}':
            ch, escaped = next(input_iter)
            quant.append(ch)

        quant = quant[:-1]
        values = (b'').join(quant).split(b',')
        try:
            ch, escaped = next(input_iter)
        except StopIteration:
            ch = None

        if ch == b'?':
            ch = None
        return (
         int(values[0]), ch)


def contains(source, inst):
    """
    Returns True if the "source" contains an instance of "inst". False,
    otherwise.
    """
    if isinstance(source, inst):
        return True
    if isinstance(source, NonCapture):
        for elt in source:
            if contains(elt, inst):
                return True

    return False


def flatten_result(source):
    """
    Turns the given source sequence into a list of reg-exp possibilities and
    their arguments. Returns a list of strings and a list of argument lists.
    Each of the two lists will be of the same length.
    """
    if source is None:
        return ([b''], [[]])
    else:
        if isinstance(source, Group):
            if source[1] is None:
                params = []
            else:
                params = [
                 source[1]]
            return ([source[0]], [params])
        result = [
         b'']
        result_args = [[]]
        pos = last = 0
        for pos, elt in enumerate(source):
            if isinstance(elt, six.string_types):
                continue
            piece = (b'').join(source[last:pos])
            if isinstance(elt, Group):
                piece += elt[0]
                param = elt[1]
            else:
                param = None
            last = pos + 1
            for i in range(len(result)):
                result[i] += piece
                if param:
                    result_args[i].append(param)

            if isinstance(elt, (Choice, NonCapture)):
                if isinstance(elt, NonCapture):
                    elt = [
                     elt]
                inner_result, inner_args = [], []
                for item in elt:
                    res, args = flatten_result(item)
                    inner_result.extend(res)
                    inner_args.extend(args)

                new_result = []
                new_args = []
                for item, args in zip(result, result_args):
                    for i_item, i_args in zip(inner_result, inner_args):
                        new_result.append(item + i_item)
                        new_args.append(args[:] + i_args)

                result = new_result
                result_args = new_args

        if pos >= last:
            piece = (b'').join(source[last:])
            for i in range(len(result)):
                result[i] += piece

        return (
         result, result_args)