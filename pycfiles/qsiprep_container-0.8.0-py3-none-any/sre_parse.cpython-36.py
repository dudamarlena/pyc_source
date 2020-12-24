# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/qsiprep/wrapper/build/lib/python3.6/sre_parse.py
# Compiled at: 2019-03-22 00:31:36
# Size of source mod 2**32: 36536 bytes
"""Internal support module for sre"""
from sre_constants import *
SPECIAL_CHARS = '.\\[{()*+?^$|'
REPEAT_CHARS = '*+?{'
DIGITS = frozenset('0123456789')
OCTDIGITS = frozenset('01234567')
HEXDIGITS = frozenset('0123456789abcdefABCDEF')
ASCIILETTERS = frozenset('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
WHITESPACE = frozenset(' \t\n\r\x0b\x0c')
_REPEATCODES = frozenset({MIN_REPEAT, MAX_REPEAT})
_UNITCODES = frozenset({ANY, RANGE, IN, LITERAL, NOT_LITERAL, CATEGORY})
ESCAPES = {'\\a':(
  LITERAL, ord('\x07')), 
 '\\b':(
  LITERAL, ord('\x08')), 
 '\\f':(
  LITERAL, ord('\x0c')), 
 '\\n':(
  LITERAL, ord('\n')), 
 '\\r':(
  LITERAL, ord('\r')), 
 '\\t':(
  LITERAL, ord('\t')), 
 '\\v':(
  LITERAL, ord('\x0b')), 
 '\\\\':(
  LITERAL, ord('\\'))}
CATEGORIES = {'\\A':(
  AT, AT_BEGINNING_STRING), 
 '\\b':(
  AT, AT_BOUNDARY), 
 '\\B':(
  AT, AT_NON_BOUNDARY), 
 '\\d':(
  IN, [(CATEGORY, CATEGORY_DIGIT)]), 
 '\\D':(
  IN, [(CATEGORY, CATEGORY_NOT_DIGIT)]), 
 '\\s':(
  IN, [(CATEGORY, CATEGORY_SPACE)]), 
 '\\S':(
  IN, [(CATEGORY, CATEGORY_NOT_SPACE)]), 
 '\\w':(
  IN, [(CATEGORY, CATEGORY_WORD)]), 
 '\\W':(
  IN, [(CATEGORY, CATEGORY_NOT_WORD)]), 
 '\\Z':(
  AT, AT_END_STRING)}
FLAGS = {'i':SRE_FLAG_IGNORECASE, 
 'L':SRE_FLAG_LOCALE, 
 'm':SRE_FLAG_MULTILINE, 
 's':SRE_FLAG_DOTALL, 
 'x':SRE_FLAG_VERBOSE, 
 'a':SRE_FLAG_ASCII, 
 't':SRE_FLAG_TEMPLATE, 
 'u':SRE_FLAG_UNICODE}
GLOBAL_FLAGS = SRE_FLAG_ASCII | SRE_FLAG_LOCALE | SRE_FLAG_UNICODE | SRE_FLAG_DEBUG | SRE_FLAG_TEMPLATE

class Verbose(Exception):
    pass


class Pattern:

    def __init__(self):
        self.flags = 0
        self.groupdict = {}
        self.groupwidths = [None]
        self.lookbehindgroups = None

    @property
    def groups(self):
        return len(self.groupwidths)

    def opengroup(self, name=None):
        gid = self.groups
        self.groupwidths.append(None)
        if self.groups > MAXGROUPS:
            raise error('too many groups')
        if name is not None:
            ogid = self.groupdict.get(name, None)
            if ogid is not None:
                raise error('redefinition of group name %r as group %d; was group %d' % (
                 name, gid, ogid))
            self.groupdict[name] = gid
        return gid

    def closegroup(self, gid, p):
        self.groupwidths[gid] = p.getwidth()

    def checkgroup(self, gid):
        return gid < self.groups and self.groupwidths[gid] is not None

    def checklookbehindgroup(self, gid, source):
        if self.lookbehindgroups is not None:
            if not self.checkgroup(gid):
                raise source.error('cannot refer to an open group')
            if gid >= self.lookbehindgroups:
                raise source.error('cannot refer to group defined in the same lookbehind subpattern')


class SubPattern:

    def __init__(self, pattern, data=None):
        self.pattern = pattern
        if data is None:
            data = []
        self.data = data
        self.width = None

    def dump(self, level=0):
        nl = True
        seqtypes = (tuple, list)
        for op, av in self.data:
            print((level * '  ' + str(op)), end='')
            if op is IN:
                print()
                for op, a in av:
                    print((level + 1) * '  ' + str(op), a)

            elif op is BRANCH:
                print()
                for i, a in enumerate(av[1]):
                    if i:
                        print(level * '  ' + 'OR')
                    a.dump(level + 1)

            else:
                if op is GROUPREF_EXISTS:
                    condgroup, item_yes, item_no = av
                    print('', condgroup)
                    item_yes.dump(level + 1)
                    if item_no:
                        print(level * '  ' + 'ELSE')
                        item_no.dump(level + 1)
                else:
                    if isinstance(av, seqtypes):
                        nl = False
                        for a in av:
                            if isinstance(a, SubPattern):
                                if not nl:
                                    print()
                                a.dump(level + 1)
                                nl = True
                            else:
                                if not nl:
                                    print(' ', end='')
                                print(a, end='')
                                nl = False

                        if not nl:
                            print()
                    else:
                        print('', av)

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, index):
        del self.data[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SubPattern(self.pattern, self.data[index])
        else:
            return self.data[index]

    def __setitem__(self, index, code):
        self.data[index] = code

    def insert(self, index, code):
        self.data.insert(index, code)

    def append(self, code):
        self.data.append(code)

    def getwidth(self):
        if self.width is not None:
            return self.width
        else:
            lo = hi = 0
            for op, av in self.data:
                if op is BRANCH:
                    i = MAXREPEAT - 1
                    j = 0
                    for av in av[1]:
                        l, h = av.getwidth()
                        i = min(i, l)
                        j = max(j, h)

                    lo = lo + i
                    hi = hi + j
                elif op is CALL:
                    i, j = av.getwidth()
                    lo = lo + i
                    hi = hi + j
                elif op is SUBPATTERN:
                    i, j = av[(-1)].getwidth()
                    lo = lo + i
                    hi = hi + j
                elif op in _REPEATCODES:
                    i, j = av[2].getwidth()
                    lo = lo + i * av[0]
                    hi = hi + j * av[1]
                elif op in _UNITCODES:
                    lo = lo + 1
                    hi = hi + 1
                else:
                    if op is GROUPREF:
                        i, j = self.pattern.groupwidths[av]
                        lo = lo + i
                        hi = hi + j
                    else:
                        if op is GROUPREF_EXISTS:
                            i, j = av[1].getwidth()
                            if av[2] is not None:
                                l, h = av[2].getwidth()
                                i = min(i, l)
                                j = max(j, h)
                            else:
                                i = 0
                            lo = lo + i
                            hi = hi + j
                        elif op is SUCCESS:
                            break

            self.width = (
             min(lo, MAXREPEAT - 1), min(hi, MAXREPEAT))
            return self.width


class Tokenizer:

    def __init__(self, string):
        self.istext = isinstance(string, str)
        self.string = string
        if not self.istext:
            string = str(string, 'latin1')
        self.decoded_string = string
        self.index = 0
        self.next = None
        self._Tokenizer__next()

    def __next(self):
        index = self.index
        try:
            char = self.decoded_string[index]
        except IndexError:
            self.next = None
            return
        else:
            if char == '\\':
                index += 1
                try:
                    char += self.decoded_string[index]
                except IndexError:
                    raise error('bad escape (end of pattern)', self.string, len(self.string) - 1) from None

            self.index = index + 1
            self.next = char

    def match(self, char):
        if char == self.next:
            self._Tokenizer__next()
            return True
        else:
            return False

    def get(self):
        this = self.next
        self._Tokenizer__next()
        return this

    def getwhile(self, n, charset):
        result = ''
        for _ in range(n):
            c = self.next
            if c not in charset:
                break
            result += c
            self._Tokenizer__next()

        return result

    def getuntil(self, terminator):
        result = ''
        while True:
            c = self.next
            self._Tokenizer__next()
            if c is None:
                if not result:
                    raise self.error('missing group name')
                raise self.error('missing %s, unterminated name' % terminator, len(result))
            if c == terminator:
                if not result:
                    raise self.error('missing group name', 1)
                break
            result += c

        return result

    @property
    def pos(self):
        return self.index - len(self.next or '')

    def tell(self):
        return self.index - len(self.next or '')

    def seek(self, index):
        self.index = index
        self._Tokenizer__next()

    def error(self, msg, offset=0):
        return error(msg, self.string, self.tell() - offset)


def _class_escape(source, escape):
    code = ESCAPES.get(escape)
    if code:
        return code
    code = CATEGORIES.get(escape)
    if code:
        if code[0] is IN:
            return code
    try:
        c = escape[1:2]
        if c == 'x':
            escape += source.getwhile(2, HEXDIGITS)
            if len(escape) != 4:
                raise source.error('incomplete escape %s' % escape, len(escape))
            return (
             LITERAL, int(escape[2:], 16))
        if c == 'u':
            if source.istext:
                escape += source.getwhile(4, HEXDIGITS)
                if len(escape) != 6:
                    raise source.error('incomplete escape %s' % escape, len(escape))
                return (LITERAL, int(escape[2:], 16))
        if c == 'U' and source.istext:
            escape += source.getwhile(8, HEXDIGITS)
            if len(escape) != 10:
                raise source.error('incomplete escape %s' % escape, len(escape))
            c = int(escape[2:], 16)
            chr(c)
            return (LITERAL, c)
        if c in OCTDIGITS:
            escape += source.getwhile(2, OCTDIGITS)
            c = int(escape[1:], 8)
            if c > 255:
                raise source.error('octal escape value %s outside of range 0-0o377' % escape, len(escape))
            return (
             LITERAL, c)
        if c in DIGITS:
            raise ValueError
        if len(escape) == 2:
            if c in ASCIILETTERS:
                raise source.error('bad escape %s' % escape, len(escape))
            return (
             LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise source.error('bad escape %s' % escape, len(escape))


def _escape(source, escape, state):
    code = CATEGORIES.get(escape)
    if code:
        return code
    code = ESCAPES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == 'x':
            escape += source.getwhile(2, HEXDIGITS)
            if len(escape) != 4:
                raise source.error('incomplete escape %s' % escape, len(escape))
            return (
             LITERAL, int(escape[2:], 16))
        if c == 'u':
            if source.istext:
                escape += source.getwhile(4, HEXDIGITS)
                if len(escape) != 6:
                    raise source.error('incomplete escape %s' % escape, len(escape))
                return (LITERAL, int(escape[2:], 16))
        if c == 'U' and source.istext:
            escape += source.getwhile(8, HEXDIGITS)
            if len(escape) != 10:
                raise source.error('incomplete escape %s' % escape, len(escape))
            c = int(escape[2:], 16)
            chr(c)
            return (LITERAL, c)
        if c == '0':
            escape += source.getwhile(2, OCTDIGITS)
            return (LITERAL, int(escape[1:], 8))
        if c in DIGITS:
            if source.next in DIGITS:
                escape += source.get()
                if escape[1] in OCTDIGITS:
                    if escape[2] in OCTDIGITS:
                        if source.next in OCTDIGITS:
                            escape += source.get()
                            c = int(escape[1:], 8)
                            if c > 255:
                                raise source.error('octal escape value %s outside of range 0-0o377' % escape, len(escape))
                            return (LITERAL, c)
            group = int(escape[1:])
            if group < state.groups:
                if not state.checkgroup(group):
                    raise source.error('cannot refer to an open group', len(escape))
                state.checklookbehindgroup(group, source)
                return (GROUPREF, group)
            raise source.error('invalid group reference %d' % group, len(escape) - 1)
        if len(escape) == 2:
            if c in ASCIILETTERS:
                raise source.error('bad escape %s' % escape, len(escape))
            return (
             LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise source.error('bad escape %s' % escape, len(escape))


def _parse_sub(source, state, verbose, nested):
    items = []
    itemsappend = items.append
    sourcematch = source.match
    start = source.tell()
    while 1:
        itemsappend(_parse(source, state, verbose, nested + 1, not nested and not items))
        if not sourcematch('|'):
            break

    if len(items) == 1:
        return items[0]
    else:
        subpattern = SubPattern(state)
        subpatternappend = subpattern.append
        while True:
            prefix = None
            for item in items:
                if not item:
                    break
                if prefix is None:
                    prefix = item[0]
                elif item[0] != prefix:
                    break
            else:
                for item in items:
                    del item[0]

                subpatternappend(prefix)
                continue

            break

        for item in items:
            if len(item) != 1 or item[0][0] is not LITERAL:
                break
        else:
            subpatternappend((IN, [item[0] for item in items]))
            return subpattern

        subpattern.append((BRANCH, (None, items)))
        return subpattern


def _parse_sub_cond(source, state, condgroup, verbose, nested):
    item_yes = _parse(source, state, verbose, nested + 1)
    if source.match('|'):
        item_no = _parse(source, state, verbose, nested + 1)
        if source.next == '|':
            raise source.error('conditional backref with more than two branches')
    else:
        item_no = None
    subpattern = SubPattern(state)
    subpattern.append((GROUPREF_EXISTS, (condgroup, item_yes, item_no)))
    return subpattern


def _parse(source, state, verbose, nested, first=False):
    subpattern = SubPattern(state)
    subpatternappend = subpattern.append
    sourceget = source.get
    sourcematch = source.match
    _len = len
    _ord = ord
    while 1:
        this = source.next
        if this is None:
            break
        if this in '|)':
            break
        sourceget()
        if verbose:
            if this in WHITESPACE:
                pass
            elif this == '#':
                while 1:
                    this = sourceget()
                    if this is None or this == '\n':
                        break

                continue
        if this[0] == '\\':
            code = _escape(source, this, state)
            subpatternappend(code)
        else:
            if this not in SPECIAL_CHARS:
                subpatternappend((LITERAL, _ord(this)))
            else:
                if this == '[':
                    here = source.tell() - 1
                    set = []
                    setappend = set.append
                    if sourcematch('^'):
                        setappend((NEGATE, None))
                    else:
                        start = set[:]
                        while 1:
                            this = sourceget()
                            if this is None:
                                raise source.error('unterminated character set', source.tell() - here)
                            if this == ']':
                                if set != start:
                                    break
                            if this[0] == '\\':
                                code1 = _class_escape(source, this)
                            else:
                                code1 = (
                                 LITERAL, _ord(this))
                            if sourcematch('-'):
                                that = sourceget()
                                if that is None:
                                    raise source.error('unterminated character set', source.tell() - here)
                                if that == ']':
                                    if code1[0] is IN:
                                        code1 = code1[1][0]
                                    setappend(code1)
                                    setappend((LITERAL, _ord('-')))
                                    break
                                if that[0] == '\\':
                                    code2 = _class_escape(source, that)
                                else:
                                    code2 = (
                                     LITERAL, _ord(that))
                                if code1[0] != LITERAL or code2[0] != LITERAL:
                                    msg = 'bad character range %s-%s' % (this, that)
                                    raise source.error(msg, len(this) + 1 + len(that))
                                lo = code1[1]
                                hi = code2[1]
                                if hi < lo:
                                    msg = 'bad character range %s-%s' % (this, that)
                                    raise source.error(msg, len(this) + 1 + len(that))
                                setappend((RANGE, (lo, hi)))
                            else:
                                if code1[0] is IN:
                                    code1 = code1[1][0]
                                setappend(code1)

                        if _len(set) == 1:
                            if set[0][0] is LITERAL:
                                subpatternappend(set[0])
                        elif _len(set) == 2 and set[0][0] is NEGATE and set[1][0] is LITERAL:
                            subpatternappend((NOT_LITERAL, set[1][1]))
                        else:
                            subpatternappend((IN, set))
                else:
                    if this in REPEAT_CHARS:
                        here = source.tell()
                        if this == '?':
                            min, max = (0, 1)
                        else:
                            if this == '*':
                                min, max = 0, MAXREPEAT
                            else:
                                if this == '+':
                                    min, max = 1, MAXREPEAT
                                else:
                                    if this == '{':
                                        if source.next == '}':
                                            subpatternappend((LITERAL, _ord(this)))
                                            continue
                                        min, max = 0, MAXREPEAT
                                        lo = hi = ''
                                        while source.next in DIGITS:
                                            lo += sourceget()

                                        if sourcematch(','):
                                            while source.next in DIGITS:
                                                hi += sourceget()

                                        else:
                                            hi = lo
                                        sourcematch('}') or subpatternappend((LITERAL, _ord(this)))
                                        source.seek(here)
                                        continue
                                        if lo:
                                            min = int(lo)
                                            if min >= MAXREPEAT:
                                                raise OverflowError('the repetition number is too large')
                                        if hi:
                                            max = int(hi)
                                            if max >= MAXREPEAT:
                                                raise OverflowError('the repetition number is too large')
                                            if max < min:
                                                raise source.error('min repeat greater than max repeat', source.tell() - here)
                                    else:
                                        raise AssertionError('unsupported quantifier %r' % (char,))
                                    if subpattern:
                                        item = subpattern[-1:]
                                    else:
                                        item = None
                                if not item or _len(item) == 1 and item[0][0] is AT:
                                    raise source.error('nothing to repeat', source.tell() - here + len(this))
                                if item[0][0] in _REPEATCODES:
                                    raise source.error('multiple repeat', source.tell() - here + len(this))
                            if sourcematch('?'):
                                subpattern[-1] = (
                                 MIN_REPEAT, (min, max, item))
                            else:
                                subpattern[-1] = (
                                 MAX_REPEAT, (min, max, item))
                    else:
                        if this == '.':
                            subpatternappend((ANY, None))
                        else:
                            if this == '(':
                                start = source.tell() - 1
                                group = True
                                name = None
                                condgroup = None
                                add_flags = 0
                                del_flags = 0
                                if sourcematch('?'):
                                    char = sourceget()
                                    if char is None:
                                        raise source.error('unexpected end of pattern')
                                    if char == 'P':
                                        if sourcematch('<'):
                                            name = source.getuntil('>')
                                            if not name.isidentifier():
                                                msg = 'bad character in group name %r' % name
                                                raise source.error(msg, len(name) + 1)
                                        else:
                                            if sourcematch('='):
                                                name = source.getuntil(')')
                                                if not name.isidentifier():
                                                    msg = 'bad character in group name %r' % name
                                                    raise source.error(msg, len(name) + 1)
                                                gid = state.groupdict.get(name)
                                                if gid is None:
                                                    msg = 'unknown group name %r' % name
                                                    raise source.error(msg, len(name) + 1)
                                                if not state.checkgroup(gid):
                                                    raise source.error('cannot refer to an open group', len(name) + 1)
                                                state.checklookbehindgroup(gid, source)
                                                subpatternappend((GROUPREF, gid))
                                                continue
                                            else:
                                                char = sourceget()
                                                if char is None:
                                                    raise source.error('unexpected end of pattern')
                                                raise source.error('unknown extension ?P' + char, len(char) + 2)
                                    else:
                                        if char == ':':
                                            group = None
                                        else:
                                            if char == '#':
                                                while 1:
                                                    if source.next is None:
                                                        raise source.error('missing ), unterminated comment', source.tell() - start)
                                                    if sourceget() == ')':
                                                        break

                                                continue
                                            else:
                                                if char in '=!<':
                                                    dir = 1
                                                    if char == '<':
                                                        char = sourceget()
                                                        if char is None:
                                                            raise source.error('unexpected end of pattern')
                                                        if char not in '=!':
                                                            raise source.error('unknown extension ?<' + char, len(char) + 2)
                                                        dir = -1
                                                        lookbehindgroups = state.lookbehindgroups
                                                        if lookbehindgroups is None:
                                                            state.lookbehindgroups = state.groups
                                                    p = _parse_sub(source, state, verbose, nested + 1)
                                                    if dir < 0:
                                                        if lookbehindgroups is None:
                                                            state.lookbehindgroups = None
                                                    if not sourcematch(')'):
                                                        raise source.error('missing ), unterminated subpattern', source.tell() - start)
                                                    if char == '=':
                                                        subpatternappend((ASSERT, (dir, p)))
                                                    else:
                                                        subpatternappend((ASSERT_NOT, (dir, p)))
                                                        continue
                                                else:
                                                    if char == '(':
                                                        condname = source.getuntil(')')
                                                        group = None
                                                        if condname.isidentifier():
                                                            condgroup = state.groupdict.get(condname)
                                                            if condgroup is None:
                                                                msg = 'unknown group name %r' % condname
                                                                raise source.error(msg, len(condname) + 1)
                                                        else:
                                                            try:
                                                                condgroup = int(condname)
                                                                if condgroup < 0:
                                                                    raise ValueError
                                                            except ValueError:
                                                                msg = 'bad character in group name %r' % condname
                                                                raise source.error(msg, len(condname) + 1) from None

                                                        if not condgroup:
                                                            raise source.error('bad group number', len(condname) + 1)
                                                        if condgroup >= MAXGROUPS:
                                                            msg = 'invalid group reference %d' % condgroup
                                                            raise source.error(msg, len(condname) + 1)
                                                        state.checklookbehindgroup(condgroup, source)
                                                    else:
                                                        if char in FLAGS or char == '-':
                                                            flags = _parse_flags(source, state, char)
                                                            if flags is None:
                                                                if not first or subpattern:
                                                                    import warnings
                                                                    warnings.warn(('Flags not at the start of the expression %r%s' % (
                                                                     source.string[:20],
                                                                     ' (truncated)' if len(source.string) > 20 else '')),
                                                                      DeprecationWarning,
                                                                      stacklevel=(nested + 6))
                                                                if state.flags & SRE_FLAG_VERBOSE and not verbose:
                                                                    raise Verbose
                                                                    continue
                                                                    add_flags, del_flags = flags
                                                                    group = None
                                                        raise source.error('unknown extension ?' + char, len(char) + 1)
                                if group is not None:
                                    try:
                                        group = state.opengroup(name)
                                    except error as err:
                                        raise source.error(err.msg, len(name) + 1) from None

                                    if condgroup:
                                        p = _parse_sub_cond(source, state, condgroup, verbose, nested + 1)
                                    else:
                                        sub_verbose = (verbose or add_flags & SRE_FLAG_VERBOSE) and not del_flags & SRE_FLAG_VERBOSE
                                        p = _parse_sub(source, state, sub_verbose, nested + 1)
                                    if not source.match(')'):
                                        raise source.error('missing ), unterminated subpattern', source.tell() - start)
                                    if group is not None:
                                        state.closegroup(group, p)
                                    subpatternappend((SUBPATTERN, (group, add_flags, del_flags, p)))
                                else:
                                    if this == '^':
                                        subpatternappend((AT, AT_BEGINNING))
                                    else:
                                        if this == '$':
                                            subpattern.append((AT, AT_END))
                                        else:
                                            raise AssertionError('unsupported special character %r' % (char,))

    return subpattern


def _parse_flags(source, state, char):
    sourceget = source.get
    add_flags = 0
    del_flags = 0
    if char != '-':
        while 1:
            add_flags |= FLAGS[char]
            char = sourceget()
            if char is None:
                raise source.error('missing -, : or )')
            if char in ')-:':
                break
            if char not in FLAGS:
                msg = 'unknown flag' if char.isalpha() else 'missing -, : or )'
                raise source.error(msg, len(char))

    if char == ')':
        state.flags |= add_flags
        return
    else:
        if add_flags & GLOBAL_FLAGS:
            raise source.error('bad inline flags: cannot turn on global flag', 1)
        else:
            if char == '-':
                char = sourceget()
                if char is None:
                    raise source.error('missing flag')
                if char not in FLAGS:
                    msg = 'unknown flag' if char.isalpha() else 'missing flag'
                    raise source.error(msg, len(char))
                while 1:
                    del_flags |= FLAGS[char]
                    char = sourceget()
                    if char is None:
                        raise source.error('missing :')
                    if char == ':':
                        break
                    if char not in FLAGS:
                        msg = 'unknown flag' if char.isalpha() else 'missing :'
                        raise source.error(msg, len(char))

            else:
                assert char == ':'
                if del_flags & GLOBAL_FLAGS:
                    raise source.error('bad inline flags: cannot turn off global flag', 1)
            if add_flags & del_flags:
                raise source.error('bad inline flags: flag turned on and off', 1)
        return (
         add_flags, del_flags)


def fix_flags(src, flags):
    if isinstance(src, str):
        if flags & SRE_FLAG_LOCALE:
            raise ValueError('cannot use LOCALE flag with a str pattern')
        flags & SRE_FLAG_ASCII or flags |= SRE_FLAG_UNICODE
    else:
        if flags & SRE_FLAG_UNICODE:
            raise ValueError('ASCII and UNICODE flags are incompatible')
        elif flags & SRE_FLAG_UNICODE:
            raise ValueError('cannot use UNICODE flag with a bytes pattern')
        if flags & SRE_FLAG_LOCALE:
            if flags & SRE_FLAG_ASCII:
                raise ValueError('ASCII and LOCALE flags are incompatible')
        return flags


def parse(str, flags=0, pattern=None):
    source = Tokenizer(str)
    if pattern is None:
        pattern = Pattern()
    pattern.flags = flags
    pattern.str = str
    try:
        p = _parse_sub(source, pattern, flags & SRE_FLAG_VERBOSE, 0)
    except Verbose:
        pattern = Pattern()
        pattern.flags = flags | SRE_FLAG_VERBOSE
        pattern.str = str
        source.seek(0)
        p = _parse_sub(source, pattern, True, 0)

    p.pattern.flags = fix_flags(str, p.pattern.flags)
    if source.next is not None:
        assert source.next == ')'
        raise source.error('unbalanced parenthesis')
    if flags & SRE_FLAG_DEBUG:
        p.dump()
    return p


def parse_template(source, pattern):
    s = Tokenizer(source)
    sget = s.get
    groups = []
    literals = []
    literal = []
    lappend = literal.append

    def addgroup(index, pos):
        if index > pattern.groups:
            raise s.error('invalid group reference %d' % index, pos)
        if literal:
            literals.append(''.join(literal))
            del literal[:]
        groups.append((len(literals), index))
        literals.append(None)

    groupindex = pattern.groupindex
    while True:
        this = sget()
        if this is None:
            break
        if this[0] == '\\':
            c = this[1]
            if c == 'g':
                name = ''
                if not s.match('<'):
                    raise s.error('missing <')
                name = s.getuntil('>')
                if name.isidentifier():
                    try:
                        index = groupindex[name]
                    except KeyError:
                        raise IndexError('unknown group name %r' % name)

                else:
                    try:
                        index = int(name)
                        if index < 0:
                            raise ValueError
                    except ValueError:
                        raise s.error('bad character in group name %r' % name, len(name) + 1) from None

                    if index >= MAXGROUPS:
                        raise s.error('invalid group reference %d' % index, len(name) + 1)
                    addgroup(index, len(name) + 1)
            else:
                if c == '0':
                    if s.next in OCTDIGITS:
                        this += sget()
                        if s.next in OCTDIGITS:
                            this += sget()
                    lappend(chr(int(this[1:], 8) & 255))
                else:
                    if c in DIGITS:
                        isoctal = False
                        if s.next in DIGITS:
                            this += sget()
                            if c in OCTDIGITS:
                                if this[2] in OCTDIGITS:
                                    if s.next in OCTDIGITS:
                                        this += sget()
                                        isoctal = True
                                        c = int(this[1:], 8)
                                        if c > 255:
                                            raise s.error('octal escape value %s outside of range 0-0o377' % this, len(this))
                                        lappend(chr(c))
                        if not isoctal:
                            addgroup(int(this[1:]), len(this) - 1)
                    else:
                        try:
                            this = chr(ESCAPES[this][1])
                        except KeyError:
                            if c in ASCIILETTERS:
                                import warnings
                                warnings.warn(('bad escape %s' % this), DeprecationWarning,
                                  stacklevel=4)

                        lappend(this)
        else:
            lappend(this)

    if literal:
        literals.append(''.join(literal))
    if not isinstance(source, str):
        literals = [None if s is None else s.encode('latin-1') for s in literals]
    return (
     groups, literals)


def expand_template(template, match):
    g = match.group
    empty = match.string[:0]
    groups, literals = template
    literals = literals[:]
    try:
        for index, group in groups:
            literals[index] = g(group) or empty

    except IndexError:
        raise error('invalid group reference %d' % index)

    return empty.join(literals)