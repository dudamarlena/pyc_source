# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/takumakanari/.pyenv/versions/japanese-numbers-py3/lib/python3.8/site-packages/japanese_numbers/parser/to_arabic_parser.py
# Compiled at: 2018-07-01 03:23:12
# Size of source mod 2**32: 2309 bytes
from __future__ import absolute_import, unicode_literals
from past.builtins import xrange
from japanese_numbers.result import ParsedResult
from japanese_numbers.token import Tokenized, NUMERICS
from japanese_numbers.kind import UNIT_KIND, NUMBERS_KIND, MULTIPLES_KIND, NUMERIC_KIND
import sys
PY3 = sys.version_info.major == 3
if PY3:
    unicode = str

def _collect_numerics(val, pos):
    stack = []
    for c in val[pos:]:
        if c not in NUMERICS:
            break
        stack.append(c)
    else:
        return (
         int(''.join(stack)), len(stack))


def to_arabic(val, encode='utf8'):
    stacks, numbers, texts, analyzing, index = ([], [], [], False, -1)
    results = []

    def _append_result():
        results.append(ParsedResult(text=(''.join(texts)), number=(sum(stacks) + sum(numbers)),
          index=index))

    decoded_val = val if isinstance(val, unicode) else val.decode(encode)
    token = Tokenized(decoded_val)
    while token.has_next():
        kind, num = token.kind, token.num_of_kind
        if kind == UNIT_KIND:
            if token.last_kind != UNIT_KIND:
                ret = (numbers[(-1)] if numbers else 1) * num
                if numbers:
                    numbers[-1] = ret
            else:
                numbers.append(ret)
        else:
            if kind in (NUMBERS_KIND, UNIT_KIND):
                numbers.append(num)
            else:
                if kind == MULTIPLES_KIND:
                    stacks.append(sum(numbers) * num)
                    numbers = []
                else:
                    if kind == NUMERIC_KIND:
                        n, s = _collect_numerics(token.val, token.pos)
                        numbers.append(n)
                        index = token.pos if index < 0 else index
                        texts.append(''.join((token.origin_char_at(x) for x in xrange(token.pos, token.pos + s))))
                        token.next(incr=s)
                    else:
                        if analyzing:
                            _append_result()
                            stacks, numbers, texts, analyzing, index = ([], [], [], False, -1)
        analyzing = kind is not None
        if analyzing:
            if kind != NUMERIC_KIND:
                texts.append(token.origin_char)
            if index < 0:
                if token.last_kind is None:
                    index = token.pos
        if kind != NUMERIC_KIND:
            token.next()

    if stacks or numbers:
        _append_result()
    return results


def to_arabic_numbers(val, encode='utf8'):
    return tuple((x.number for x in to_arabic(val, encode=encode)))