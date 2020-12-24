# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/ant/code/dj/build/lib/python3.6/sre_compile.py
# Compiled at: 2019-07-30 17:44:34
# Size of source mod 2**32: 19338 bytes
"""Internal support module for sre"""
import _sre, sre_parse
from sre_constants import *
assert _sre.MAGIC == MAGIC, 'SRE module mismatch'
_LITERAL_CODES = {
 LITERAL, NOT_LITERAL}
_REPEATING_CODES = {REPEAT, MIN_REPEAT, MAX_REPEAT}
_SUCCESS_CODES = {SUCCESS, FAILURE}
_ASSERT_CODES = {ASSERT, ASSERT_NOT}
_equivalences = ((105, 305), (115, 383), (181, 956), (837, 953, 8126), (912, 8147),
                 (944, 8163), (946, 976), (949, 1013), (952, 977), (954, 1008), (960, 982),
                 (961, 1009), (962, 963), (966, 981), (7777, 7835), (64261, 64262))
_ignorecase_fixes = {i:tuple(j for j in t if i != j) for t in _equivalences for i in t}

def _compile(code, pattern, flags):
    emit = code.append
    _len = len
    LITERAL_CODES = _LITERAL_CODES
    REPEATING_CODES = _REPEATING_CODES
    SUCCESS_CODES = _SUCCESS_CODES
    ASSERT_CODES = _ASSERT_CODES
    if flags & SRE_FLAG_IGNORECASE:
        if not flags & SRE_FLAG_LOCALE:
            if flags & SRE_FLAG_UNICODE:
                if not flags & SRE_FLAG_ASCII:
                    fixes = _ignorecase_fixes
    else:
        fixes = None
    for op, av in pattern:
        if op in LITERAL_CODES:
            if flags & SRE_FLAG_IGNORECASE:
                lo = _sre.getlower(av, flags)
                if fixes:
                    if lo in fixes:
                        emit(IN_IGNORE)
                        skip = _len(code)
                        emit(0)
                        if op is NOT_LITERAL:
                            emit(NEGATE)
                        for k in (lo,) + fixes[lo]:
                            emit(LITERAL)
                            emit(k)

                        emit(FAILURE)
                        code[skip] = _len(code) - skip
                else:
                    emit(OP_IGNORE[op])
                    emit(lo)
            else:
                emit(op)
                emit(av)
        elif op is IN:
            if flags & SRE_FLAG_IGNORECASE:
                emit(OP_IGNORE[op])

                def fixup(literal, flags=flags):
                    return _sre.getlower(literal, flags)

            else:
                emit(op)
                fixup = None
            skip = _len(code)
            emit(0)
            _compile_charset(av, flags, code, fixup, fixes)
            code[skip] = _len(code) - skip
        else:
            if op is ANY:
                if flags & SRE_FLAG_DOTALL:
                    emit(ANY_ALL)
                else:
                    emit(ANY)
            else:
                if op in REPEATING_CODES:
                    if flags & SRE_FLAG_TEMPLATE:
                        raise error('internal: unsupported template operator %r' % (op,))
                    elif _simple(av) and op is not REPEAT:
                        if op is MAX_REPEAT:
                            emit(REPEAT_ONE)
                        else:
                            emit(MIN_REPEAT_ONE)
                        skip = _len(code)
                        emit(0)
                        emit(av[0])
                        emit(av[1])
                        _compile(code, av[2], flags)
                        emit(SUCCESS)
                        code[skip] = _len(code) - skip
                    else:
                        emit(REPEAT)
                        skip = _len(code)
                        emit(0)
                        emit(av[0])
                        emit(av[1])
                        _compile(code, av[2], flags)
                        code[skip] = _len(code) - skip
                        if op is MAX_REPEAT:
                            emit(MAX_UNTIL)
                        else:
                            emit(MIN_UNTIL)
                elif op is SUBPATTERN:
                    group, add_flags, del_flags, p = av
                    if group:
                        emit(MARK)
                        emit((group - 1) * 2)
                else:
                    _compile(code, p, (flags | add_flags) & ~del_flags)
                    if group:
                        emit(MARK)
                        emit((group - 1) * 2 + 1)
                    else:
                        if op in SUCCESS_CODES:
                            emit(op)
                        else:
                            if op in ASSERT_CODES:
                                emit(op)
                                skip = _len(code)
                                emit(0)
                                if av[0] >= 0:
                                    emit(0)
                                else:
                                    lo, hi = av[1].getwidth()
                                    if lo != hi:
                                        raise error('look-behind requires fixed-width pattern')
                                    emit(lo)
                                _compile(code, av[1], flags)
                                emit(SUCCESS)
                                code[skip] = _len(code) - skip
                            else:
                                if op is CALL:
                                    emit(op)
                                    skip = _len(code)
                                    emit(0)
                                    _compile(code, av, flags)
                                    emit(SUCCESS)
                                    code[skip] = _len(code) - skip
                                else:
                                    if op is AT:
                                        emit(op)
                                        if flags & SRE_FLAG_MULTILINE:
                                            av = AT_MULTILINE.get(av, av)
                                        if flags & SRE_FLAG_LOCALE:
                                            av = AT_LOCALE.get(av, av)
                                        else:
                                            if flags & SRE_FLAG_UNICODE:
                                                if not flags & SRE_FLAG_ASCII:
                                                    av = AT_UNICODE.get(av, av)
                                        emit(av)
                                    else:
                                        if op is BRANCH:
                                            emit(op)
                                            tail = []
                                            tailappend = tail.append
                                            for av in av[1]:
                                                skip = _len(code)
                                                emit(0)
                                                _compile(code, av, flags)
                                                emit(JUMP)
                                                tailappend(_len(code))
                                                emit(0)
                                                code[skip] = _len(code) - skip

                                            emit(FAILURE)
                                            for tail in tail:
                                                code[tail] = _len(code) - tail

                                        else:
                                            if op is CATEGORY:
                                                emit(op)
                                                if flags & SRE_FLAG_LOCALE:
                                                    av = CH_LOCALE[av]
                                                else:
                                                    if flags & SRE_FLAG_UNICODE:
                                                        if not flags & SRE_FLAG_ASCII:
                                                            av = CH_UNICODE[av]
                                                emit(av)
                                            else:
                                                if op is GROUPREF:
                                                    if flags & SRE_FLAG_IGNORECASE:
                                                        emit(OP_IGNORE[op])
                                                    else:
                                                        emit(op)
                                                    emit(av - 1)
                                                else:
                                                    if op is GROUPREF_EXISTS:
                                                        emit(op)
                                                        emit(av[0] - 1)
                                                        skipyes = _len(code)
                                                        emit(0)
                                                        _compile(code, av[1], flags)
                                                        if av[2]:
                                                            emit(JUMP)
                                                            skipno = _len(code)
                                                            emit(0)
                                                            code[skipyes] = _len(code) - skipyes + 1
                                                            _compile(code, av[2], flags)
                                                            code[skipno] = _len(code) - skipno
                                                        else:
                                                            code[skipyes] = _len(code) - skipyes + 1
                                                    else:
                                                        raise error('internal: unsupported operand type %r' % (op,))


def _compile_charset(charset, flags, code, fixup=None, fixes=None):
    emit = code.append
    for op, av in _optimize_charset(charset, fixup, fixes):
        emit(op)
        if op is NEGATE:
            continue
        if op is LITERAL:
            emit(av)
        elif op is RANGE or op is RANGE_IGNORE:
            emit(av[0])
            emit(av[1])
        elif op is CHARSET:
            code.extend(av)
        else:
            if op is BIGCHARSET:
                code.extend(av)
            else:
                if op is CATEGORY:
                    if flags & SRE_FLAG_LOCALE:
                        emit(CH_LOCALE[av])
                    else:
                        if flags & SRE_FLAG_UNICODE:
                            if not flags & SRE_FLAG_ASCII:
                                emit(CH_UNICODE[av])
                        emit(av)
                else:
                    raise error('internal: unsupported set operator %r' % (op,))

    emit(FAILURE)


def _optimize_charset(charset, fixup, fixes):
    out = []
    tail = []
    charmap = bytearray(256)
    for op, av in charset:
        while True:
            try:
                if op is LITERAL:
                    if fixup:
                        lo = fixup(av)
                        charmap[lo] = 1
                        if fixes:
                            if lo in fixes:
                                for k in fixes[lo]:
                                    charmap[k] = 1

                    else:
                        charmap[av] = 1
                else:
                    if op is RANGE:
                        r = range(av[0], av[1] + 1)
                        if fixup:
                            r = map(fixup, r)
                        elif fixup and fixes:
                            for i in r:
                                charmap[i] = 1
                                if i in fixes:
                                    for k in fixes[i]:
                                        charmap[k] = 1

                        else:
                            for i in r:
                                charmap[i] = 1

                    else:
                        if op is NEGATE:
                            out.append((op, av))
                        else:
                            tail.append((op, av))
            except IndexError:
                if len(charmap) == 256:
                    charmap += b'\x00' * 65280
                    continue
                if fixup:
                    if op is RANGE:
                        op = RANGE_IGNORE
                tail.append((op, av))

            break

    runs = []
    q = 0
    while True:
        p = charmap.find(1, q)
        if p < 0:
            break
        if len(runs) >= 2:
            runs = None
            break
        q = charmap.find(0, p)
        if q < 0:
            runs.append((p, len(charmap)))
            break
        runs.append((p, q))

    if runs is not None:
        for p, q in runs:
            if q - p == 1:
                out.append((LITERAL, p))
            else:
                out.append((RANGE, (p, q - 1)))

        out += tail
        if fixup or len(out) < len(charset):
            return out
        return charset
    else:
        if len(charmap) == 256:
            data = _mk_bitmap(charmap)
            out.append((CHARSET, data))
            out += tail
            return out
        charmap = bytes(charmap)
        comps = {}
        mapping = bytearray(256)
        block = 0
        data = bytearray()
        for i in range(0, 65536, 256):
            chunk = charmap[i:i + 256]
            if chunk in comps:
                mapping[i // 256] = comps[chunk]
            else:
                mapping[i // 256] = comps[chunk] = block
                block += 1
                data += chunk

        data = _mk_bitmap(data)
        data[0:0] = [block] + _bytes_to_codes(mapping)
        out.append((BIGCHARSET, data))
        out += tail
        return out


_CODEBITS = _sre.CODESIZE * 8
MAXCODE = (1 << _CODEBITS) - 1
_BITS_TRANS = b'0' + b'1' * 255

def _mk_bitmap(bits, _CODEBITS=_CODEBITS, _int=int):
    s = bits.translate(_BITS_TRANS)[::-1]
    return [_int(s[i - _CODEBITS:i], 2) for i in range(len(s), 0, -_CODEBITS)]


def _bytes_to_codes(b):
    a = memoryview(b).cast('I')
    if not a.itemsize == _sre.CODESIZE:
        raise AssertionError
    elif not len(a) * a.itemsize == len(b):
        raise AssertionError
    return a.tolist()


def _simple(av):
    lo, hi = av[2].getwidth()
    return lo == hi == 1 and av[2][0][0] != SUBPATTERN


def _generate_overlap_table(prefix):
    """
    Generate an overlap table for the following prefix.
    An overlap table is a table of the same size as the prefix which
    informs about the potential self-overlap for each index in the prefix:
    - if overlap[i] == 0, prefix[i:] can't overlap prefix[0:...]
    - if overlap[i] == k with 0 < k <= i, prefix[i-k+1:i+1] overlaps with
      prefix[0:k]
    """
    table = [
     0] * len(prefix)
    for i in range(1, len(prefix)):
        idx = table[(i - 1)]
        while prefix[i] != prefix[idx]:
            if idx == 0:
                table[i] = 0
                break
            idx = table[(idx - 1)]
        else:
            table[i] = idx + 1

    return table


def _get_literal_prefix(pattern):
    prefix = []
    prefixappend = prefix.append
    prefix_skip = None
    for op, av in pattern.data:
        if op is LITERAL:
            prefixappend(av)
        else:
            if op is SUBPATTERN:
                group, add_flags, del_flags, p = av
                if add_flags & SRE_FLAG_IGNORECASE:
                    break
                prefix1, prefix_skip1, got_all = _get_literal_prefix(p)
                if prefix_skip is None:
                    if group is not None:
                        prefix_skip = len(prefix)
                    elif prefix_skip1 is not None:
                        prefix_skip = len(prefix) + prefix_skip1
                prefix.extend(prefix1)
                if not got_all:
                    break
            else:
                break
    else:
        return (
         prefix, prefix_skip, True)

    return (
     prefix, prefix_skip, False)


def _get_charset_prefix(pattern):
    charset = []
    charsetappend = charset.append
    if pattern.data:
        op, av = pattern.data[0]
        if op is SUBPATTERN:
            group, add_flags, del_flags, p = av
            if p:
                if not add_flags & SRE_FLAG_IGNORECASE:
                    op, av = p[0]
                    if op is LITERAL:
                        charsetappend((op, av))
                    elif op is BRANCH:
                        c = []
                        cappend = c.append
                        for p in av[1]:
                            if not p:
                                break
                            op, av = p[0]
                            if op is LITERAL:
                                cappend((op, av))
                            else:
                                break
                        else:
                            charset = c

        else:
            if op is BRANCH:
                c = []
                cappend = c.append
                for p in av[1]:
                    if not p:
                        break
                    op, av = p[0]
                    if op is LITERAL:
                        cappend((op, av))
                    else:
                        break
                else:
                    charset = c

            elif op is IN:
                charset = av
    return charset


def _compile_info(code, pattern, flags):
    lo, hi = pattern.getwidth()
    if hi > MAXCODE:
        hi = MAXCODE
    if lo == 0:
        code.extend([INFO, 4, 0, lo, hi])
        return
    prefix = []
    prefix_skip = 0
    charset = []
    prefix, prefix_skip, got_all = flags & SRE_FLAG_IGNORECASE or _get_literal_prefix(pattern)
    if not prefix:
        charset = _get_charset_prefix(pattern)
    else:
        emit = code.append
        emit(INFO)
        skip = len(code)
        emit(0)
        mask = 0
        if prefix:
            mask = SRE_INFO_PREFIX
            if prefix_skip is None:
                if got_all:
                    mask = mask | SRE_INFO_LITERAL
        else:
            if charset:
                mask = mask | SRE_INFO_CHARSET
        emit(mask)
        if lo < MAXCODE:
            emit(lo)
        else:
            emit(MAXCODE)
        prefix = prefix[:MAXCODE]
    emit(min(hi, MAXCODE))
    if prefix:
        emit(len(prefix))
        if prefix_skip is None:
            prefix_skip = len(prefix)
        emit(prefix_skip)
        code.extend(prefix)
        code.extend(_generate_overlap_table(prefix))
    else:
        if charset:
            _compile_charset(charset, flags, code)
    code[skip] = len(code) - skip


def isstring(obj):
    return isinstance(obj, (str, bytes))


def _code(p, flags):
    flags = p.pattern.flags | flags
    code = []
    _compile_info(code, p, flags)
    _compile(code, p.data, flags)
    code.append(SUCCESS)
    return code


def compile(p, flags=0):
    if isstring(p):
        pattern = p
        p = sre_parse.parse(p, flags)
    else:
        pattern = None
    code = _code(p, flags)
    groupindex = p.pattern.groupdict
    indexgroup = [None] * p.pattern.groups
    for k, i in groupindex.items():
        indexgroup[i] = k

    return _sre.compile(pattern, flags | p.pattern.flags, code, p.pattern.groups - 1, groupindex, indexgroup)