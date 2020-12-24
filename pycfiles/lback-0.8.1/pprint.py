# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pprint.pyc
# Compiled at: 2011-03-08 12:43:22
"""Support to pretty-print lists, tuples, & dictionaries recursively.

Very simple, but useful, especially in debugging data structures.

Classes
-------

PrettyPrinter()
    Handle pretty-printing operations onto a stream using a configured
    set of formatting parameters.

Functions
---------

pformat()
    Format a Python object into a pretty-printed representation.

pprint()
    Pretty-print a Python object to a stream [default is sys.stdout].

saferepr()
    Generate a 'standard' repr()-like value, but protect against recursive
    data structures.

"""
import sys as _sys, warnings
from cStringIO import StringIO as _StringIO
__all__ = [
 'pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr',
 'PrettyPrinter']
_commajoin = (', ').join
_id = id
_len = len
_type = type

def pprint(object, stream=None, indent=1, width=80, depth=None):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)


def pformat(object, indent=1, width=80, depth=None):
    """Format a Python object into a pretty-printed representation."""
    return PrettyPrinter(indent=indent, width=width, depth=depth).pformat(object)


def saferepr(object):
    """Version of repr() which can handle recursive data structures."""
    return _safe_repr(object, {}, None, 0)[0]


def isreadable(object):
    """Determine if saferepr(object) is readable by eval()."""
    return _safe_repr(object, {}, None, 0)[1]


def isrecursive(object):
    """Determine if object requires a recursive representation."""
    return _safe_repr(object, {}, None, 0)[2]


def _sorted(iterable):
    with warnings.catch_warnings():
        if _sys.py3kwarning:
            warnings.filterwarnings('ignore', 'comparing unequal types not supported', DeprecationWarning)
        return sorted(iterable)


class PrettyPrinter:

    def __init__--- This code section failed: ---

 L. 100         0  LOAD_GLOBAL           0  'int'
                3  LOAD_FAST             1  'indent'
                6  CALL_FUNCTION_1       1  None
                9  STORE_FAST            1  'indent'

 L. 101        12  LOAD_GLOBAL           0  'int'
               15  LOAD_FAST             2  'width'
               18  CALL_FUNCTION_1       1  None
               21  STORE_FAST            2  'width'

 L. 102        24  LOAD_FAST             1  'indent'
               27  LOAD_CONST               0
               30  COMPARE_OP            5  >=
               33  POP_JUMP_IF_TRUE     45  'to 45'
               36  LOAD_ASSERT              AssertionError
               39  LOAD_CONST               'indent must be >= 0'
               42  RAISE_VARARGS_2       2  None

 L. 103        45  LOAD_FAST             3  'depth'
               48  LOAD_CONST               None
               51  COMPARE_OP            8  is
               54  POP_JUMP_IF_TRUE     78  'to 78'
               57  LOAD_FAST             3  'depth'
               60  LOAD_CONST               0
               63  COMPARE_OP            4  >
               66  POP_JUMP_IF_TRUE     78  'to 78'
               69  LOAD_ASSERT              AssertionError
               72  LOAD_CONST               'depth must be > 0'
               75  RAISE_VARARGS_2       2  None

 L. 104        78  LOAD_FAST             2  'width'
               81  POP_JUMP_IF_TRUE     93  'to 93'
               84  LOAD_ASSERT              AssertionError
               87  LOAD_CONST               'width must be != 0'
               90  RAISE_VARARGS_2       2  None

 L. 105        93  LOAD_FAST             3  'depth'
               96  LOAD_FAST             0  'self'
               99  STORE_ATTR            3  '_depth'

 L. 106       102  LOAD_FAST             1  'indent'
              105  LOAD_FAST             0  'self'
              108  STORE_ATTR            4  '_indent_per_level'

 L. 107       111  LOAD_FAST             2  'width'
              114  LOAD_FAST             0  'self'
              117  STORE_ATTR            5  '_width'

 L. 108       120  LOAD_FAST             4  'stream'
              123  LOAD_CONST               None
              126  COMPARE_OP            9  is-not
              129  POP_JUMP_IF_FALSE   144  'to 144'

 L. 109       132  LOAD_FAST             4  'stream'
              135  LOAD_FAST             0  'self'
              138  STORE_ATTR            6  '_stream'
              141  JUMP_FORWARD         12  'to 156'

 L. 111       144  LOAD_GLOBAL           7  '_sys'
              147  LOAD_ATTR             8  'stdout'
              150  LOAD_FAST             0  'self'
              153  STORE_ATTR            6  '_stream'
            156_0  COME_FROM           141  '141'
              156  LOAD_CONST               None
              159  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 156

    def pprint(self, object):
        self._format(object, self._stream, 0, 0, {}, 0)
        self._stream.write('\n')

    def pformat(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]

    def isreadable(self, object):
        s, readable, recursive = self.format(object, {}, 0, 0)
        return readable and not recursive

    def _format(self, object, stream, indent, allowance, context, level):
        level = level + 1
        objid = _id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        else:
            rep = self._repr(object, context, level - 1)
            typ = _type(object)
            sepLines = _len(rep) > self._width - 1 - indent - allowance
            write = stream.write
            if self._depth and level > self._depth:
                write(rep)
                return
            r = getattr(typ, '__repr__', None)
            if issubclass(typ, dict) and r is dict.__repr__:
                write('{')
                if self._indent_per_level > 1:
                    write((self._indent_per_level - 1) * ' ')
                length = _len(object)
                if length:
                    context[objid] = 1
                    indent = indent + self._indent_per_level
                    items = _sorted(object.items())
                    key, ent = items[0]
                    rep = self._repr(key, context, level)
                    write(rep)
                    write(': ')
                    self._format(ent, stream, indent + _len(rep) + 2, allowance + 1, context, level)
                    if length > 1:
                        for key, ent in items[1:]:
                            rep = self._repr(key, context, level)
                            if sepLines:
                                write(',\n%s%s: ' % (' ' * indent, rep))
                            else:
                                write(', %s: ' % rep)
                            self._format(ent, stream, indent + _len(rep) + 2, allowance + 1, context, level)

                    indent = indent - self._indent_per_level
                    del context[objid]
                write('}')
                return
            if issubclass(typ, list) and r is list.__repr__ or issubclass(typ, tuple) and r is tuple.__repr__ or issubclass(typ, set) and r is set.__repr__ or issubclass(typ, frozenset) and r is frozenset.__repr__:
                length = _len(object)
                if issubclass(typ, list):
                    write('[')
                    endchar = ']'
                elif issubclass(typ, set):
                    if not length:
                        write('set()')
                        return
                    write('set([')
                    endchar = '])'
                    object = _sorted(object)
                    indent += 4
                elif issubclass(typ, frozenset):
                    if not length:
                        write('frozenset()')
                        return
                    write('frozenset([')
                    endchar = '])'
                    object = _sorted(object)
                    indent += 10
                else:
                    write('(')
                    endchar = ')'
                if self._indent_per_level > 1 and sepLines:
                    write((self._indent_per_level - 1) * ' ')
                if length:
                    context[objid] = 1
                    indent = indent + self._indent_per_level
                    self._format(object[0], stream, indent, allowance + 1, context, level)
                    if length > 1:
                        for ent in object[1:]:
                            if sepLines:
                                write(',\n' + ' ' * indent)
                            else:
                                write(', ')
                            self._format(ent, stream, indent, allowance + 1, context, level)

                    indent = indent - self._indent_per_level
                    del context[objid]
                if issubclass(typ, tuple) and length == 1:
                    write(',')
                write(endchar)
                return
            write(rep)
            return

    def _repr(self, object, context, level):
        repr, readable, recursive = self.format(object, context.copy(), self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the object represents a recursive construct.
        """
        return _safe_repr(object, context, maxlevels, level)


def _safe_repr(object, context, maxlevels, level):
    typ = _type(object)
    if typ is str:
        if 'locale' not in _sys.modules:
            return (repr(object), True, False)
        if "'" in object and '"' not in object:
            closure = '"'
            quotes = {'"': '\\"'}
        else:
            closure = "'"
            quotes = {"'": "\\'"}
        qget = quotes.get
        sio = _StringIO()
        write = sio.write
        for char in object:
            if char.isalpha():
                write(char)
            else:
                write(qget(char, repr(char)[1:-1]))

        return (
         '%s%s%s' % (closure, sio.getvalue(), closure), True, False)
    else:
        r = getattr(typ, '__repr__', None)
        if issubclass(typ, dict) and r is dict.__repr__:
            if not object:
                return ('{}', True, False)
            objid = _id(object)
            if maxlevels and level >= maxlevels:
                return ('{...}', False, objid in context)
            if objid in context:
                return (_recursion(object), False, True)
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            saferepr = _safe_repr
            for k, v in _sorted(object.items()):
                krepr, kreadable, krecur = saferepr(k, context, maxlevels, level)
                vrepr, vreadable, vrecur = saferepr(v, context, maxlevels, level)
                append('%s: %s' % (krepr, vrepr))
                readable = readable and kreadable and vreadable
                if krecur or vrecur:
                    recursive = True

            del context[objid]
            return (
             '{%s}' % _commajoin(components), readable, recursive)
        if issubclass(typ, list) and r is list.__repr__ or issubclass(typ, tuple) and r is tuple.__repr__:
            if issubclass(typ, list):
                if not object:
                    return ('[]', True, False)
                format = '[%s]'
            else:
                if _len(object) == 1:
                    format = '(%s,)'
                else:
                    if not object:
                        return ('()', True, False)
                    format = '(%s)'
                objid = _id(object)
                if maxlevels and level >= maxlevels:
                    return (format % '...', False, objid in context)
                if objid in context:
                    return (_recursion(object), False, True)
                context[objid] = 1
                readable = True
                recursive = False
                components = []
                append = components.append
                level += 1
                for o in object:
                    orepr, oreadable, orecur = _safe_repr(o, context, maxlevels, level)
                    append(orepr)
                    if not oreadable:
                        readable = False
                    if orecur:
                        recursive = True

            del context[objid]
            return (
             format % _commajoin(components), readable, recursive)
        rep = repr(object)
        return (rep, rep and not rep.startswith('<'), False)


def _recursion(object):
    return '<Recursion on %s with id=%s>' % (
     _type(object).__name__, _id(object))


def _perfcheck(object=None):
    import time
    if object is None:
        object = [
         (
          'string', (1, 2), [3, 4], {5: 6, 7: 8})] * 100000
    p = PrettyPrinter()
    t1 = time.time()
    _safe_repr(object, {}, None, 0)
    t2 = time.time()
    p.pformat(object)
    t3 = time.time()
    print '_safe_repr:', t2 - t1
    print 'pformat:', t3 - t2
    return


if __name__ == '__main__':
    _perfcheck()