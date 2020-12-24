# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/util.py
# Compiled at: 2019-03-06 14:02:08
# Size of source mod 2**32: 16316 bytes
from __future__ import unicode_literals
import sys
from codecs import iterencode
from inspect import isfunction, isclass
from operator import methodcaller
from collections import deque, namedtuple, Sized, Iterable
from pkg_resources import iter_entry_points
from xml.sax.saxutils import quoteattr
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    from types import StringTypes as stringy
    try:
        from cStringIO import StringIO
    except:
        from StringIO import StringIO

    bytes = str
    str = unicode
    py = 2
    reduce = reduce
except:
    from io import StringIO
    stringy = str
    bytes = bytes
    str = str
    py = 3

try:
    from sys import pypy_version_info
    pypy = True
except ImportError:
    pypy = False

Iteration = namedtuple('Iteration', ['first', 'last', 'index', 'total', 'value'])

def stream(input, encoding=None, errors='strict'):
    """Safely iterate a template generator, ignoring ``None`` values and optionally stream encoding.
        
        Used internally by ``cinje.flatten``, this allows for easy use of a template generator as a WSGI body.
        """
    input = (i for i in input if i)
    if encoding:
        input = iterencode(input, encoding, errors=errors)
    return input


def flatten(input, file=None, encoding=None, errors='strict'):
    """Return a flattened representation of a cinje chunk stream.
        
        This has several modes of operation.  If no `file` argument is given, output will be returned as a string.
        The type of string will be determined by the presence of an `encoding`; if one is given the returned value is a
        binary string, otherwise the native unicode representation.  If a `file` is present, chunks will be written
        iteratively through repeated calls to `file.write()`, and the amount of data (characters or bytes) written
        returned.  The type of string written will be determined by `encoding`, just as the return value is when not
        writing to a file-like object.  The `errors` argument is passed through when encoding.
        
        We can highly recommend using the various stremaing IO containers available in the
        [`io`](https://docs.python.org/3/library/io.html) module, though
        [`tempfile`](https://docs.python.org/3/library/tempfile.html) classes are also quite useful.
        """
    input = stream(input, encoding, errors)
    if file is None:
        if encoding:
            return ''.join(input)
        return ''.join(input)
    counter = 0
    for chunk in input:
        file.write(chunk)
        counter += len(chunk)

    return counter


def fragment(string, name='anonymous', **context):
    """Translate a template fragment into a callable function.
        
        **Note:** Use of this function is discouraged everywhere except tests, as no caching is implemented at this time.
        
        Only one function may be declared, either manually, or automatically. If automatic defintition is chosen the
        resulting function takes no arguments.  Additional keyword arguments are passed through as global variables.
        """
    if isinstance(string, bytes):
        string = string.decode('utf-8')
    elif ': def' in string or ':def' in string:
        code = string.encode('utf8').decode('cinje')
        name = None
    else:
        code = ': def {name}\n\n{string}'.format(name=name,
          string=string).encode('utf8').decode('cinje')
    environ = dict(context)
    exec(code, environ)
    if name is None:
        if not environ.get('__tmpl__', None):
            raise RuntimeError('Template fragment does not contain a function: ' + repr(environ.get('__tmpl__', None)) + '\n\n' + code)
        return environ[environ['__tmpl__'][(-1)]]
    return environ[name]


def interruptable(iterable):
    """Allow easy catching of a generator interrupting operation when using "yield from"."""
    for i in iterable:
        if i is None:
            return
        yield i


def iterate(obj):
    """Loop over an iterable and track progress, including first and last state.
        
        On each iteration yield an Iteration named tuple with the first and last flags, current element index, total
        iterable length (if possible to acquire), and value, in that order.
        
                for iteration in iterate(something):
                        iteration.value  # Do something.
        
        You can unpack these safely:
        
                for first, last, index, total, value in iterate(something):
                        pass
        
        If you want to unpack the values you are iterating across, you can by wrapping the nested unpacking in parenthesis:
        
                for first, last, index, total, (foo, bar, baz) in iterate(something):
                        pass
        
        Even if the length of the iterable can't be reliably determined this function will still capture the "last" state
        of the final loop iteration.  (Basically: this works with generators.)
        
        This process is about 10x slower than simple enumeration on CPython 3.4, so only use it where you actually need to
        track state.  Use `enumerate()` elsewhere.
        """
    global Iteration
    global next
    next = next
    Iteration = Iteration
    total = len(obj) if isinstance(obj, Sized) else None
    iterator = iter(obj)
    first = True
    last = False
    i = 0
    try:
        value = next(iterator)
    except StopIteration:
        return
    else:
        while True:
            try:
                next_value = next(iterator)
            except StopIteration:
                last = True

            yield Iteration(first, last, i, total, value)
            if last:
                return
            value = next_value
            i += 1
            first = False


def xmlargs(_source=None, **values):
    global Iterable
    global str
    global stringy
    from cinje.helpers import bless
    str = str
    Iterable = Iterable
    stringy = stringy
    ejoin = ' '.join
    parts = []
    pappend = parts.append
    if _source:
        values.update(_source)
    for k in sorted(values):
        key = str(k).rstrip('_').replace('__', ':').replace('_', '-')
        value = values[k]
        if not (k[0] == '_' or value):
            if value is False or value != 0:
                continue
            else:
                if value is True:
                    pappend(key)
                    continue
                if isinstance(value, Iterable):
                    value = isinstance(value, stringy) or ejoin((str(i) for i in value))
            pappend(key + '=' + quoteattr(str(value)))

    if parts:
        return bless(' ' + ejoin(parts))
    return ''


def chunk(line, mapping={None:'text',  '${':'escape',  '#{':'bless',  '&{':'args',  '%{':'format',  '@{':'json'}):
    """Chunkify and "tag" a block of text into plain text and code sections.
        
        The first delimeter is blank to represent text sections, and keep the indexes aligned with the tags.
        
        Values are yielded in the form (tag, text).
        """
    skipping = 0
    start = None
    last = 0
    i = 0
    text = line.line
    while i < len(text):
        if start is not None:
            if text[i] == '{':
                skipping += 1
            elif text[i] == '}':
                if skipping:
                    skipping -= 1
                else:
                    yield line.clone(kind=(mapping[text[start - 2:start]]), line=(text[start:i]))
                    start = None
                    last = i = i + 1
                    continue
        elif text[i:i + 2] in mapping:
            if last is not None:
                if last != i:
                    yield line.clone(kind=(mapping[None]), line=(text[last:i]))
                    last = None
            start = i = i + 2
            continue
        i += 1

    if last < len(text):
        yield line.clone(kind=(mapping[None]), line=(text[last:]))


def ensure_buffer(context, separate=True):
    if 'text' in context.flag or 'buffer' not in context.flag:
        return
    else:
        if separate:
            yield Line(0, '')
        yield Line(0, '_buffer = []')
        pypy or (yield Line(0, '__w, __ws = _buffer.extend, _buffer.append'))
    yield Line(0, '')
    context.flag.add('text')


class Line(object):
    """Line"""
    __slots__ = ('number', 'line', 'scope', 'kind', 'continued')

    def __init__(self, number, line, scope=None, kind=None):
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        self.number = number
        self.line = line
        self.scope = scope
        self.kind = kind
        self.continued = self.stripped.endswith('\\')
        if not kind:
            self.process()
        super(Line, self).__init__()

    def process(self):
        if self.stripped.startswith('#'):
            self.kind = self.stripped.startswith('#{') or 'comment'
        elif self.stripped.startswith(':'):
            self.kind = 'code'
            self.line = self.stripped[1:].lstrip()
        else:
            self.kind = 'text'

    @property
    def stripped(self):
        return self.line.strip()

    @property
    def partitioned(self):
        prefix, _, remainder = self.stripped.partition(' ')
        return (
         prefix.rstrip(), remainder.lstrip())

    def __repr__(self):
        return '{0.__class__.__name__}({0.number}, {0.kind}, "{0.stripped}")'.format(self)

    def __bytes__(self):
        return str(self).encode('utf8')

    def __str__(self):
        if self.scope is None:
            return self.line
        return '\t' * self.scope + self.line.lstrip()

    if py == 2:
        __unicode__ = __str__
        __str__ = __bytes__
        del __bytes__

    def clone(self, **kw):
        values = dict(number=(self.number),
          line=(self.line),
          scope=(self.scope),
          kind=(self.kind))
        values.update(kw)
        instance = (self.__class__)(**values)
        return instance


class Lines(object):
    """Lines"""
    __slots__ = [
     'Line', 'source', 'buffer']

    def __init__(self, input=None, Line=Line):
        self.Line = Line
        if input is None:
            self.source = None
            self.buffer = deque()
        elif hasattr(input, 'readlines'):
            self.source = list((self.Line(i + 1, j) for i, j in enumerate(input.readlines())))
            self.buffer = deque(self.source)
        else:
            self.source = list((self.Line(i + 1, j) for i, j in enumerate(input.split('\n'))))
            self.buffer = deque(self.source)
        super(Lines, self).__init__()

    @property
    def count(self):
        return len(self.buffer)

    def __len__(self):
        return self.count

    def __repr__(self):
        return 'Lines({0.count})'.format(self)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __str__(self):
        return '\n'.join((str(i) for i in self))

    def next(self):
        if not self.buffer:
            raise StopIteration()
        return self.buffer.popleft()

    def peek(self):
        if self.buffer:
            return self.buffer[0]

    def push(self, *lines):
        self.buffer.extendleft(((i if isinstance(i, self.Line) else self.Line(self.buffer[0].number if self.buffer else 0, i)) for i in reversed(lines)))

    def reset(self):
        self.buffer = deque(self.source)

    def append(self, *lines):
        self.buffer.extend(((i if isinstance(i, self.Line) else self.Line(self.buffer[(-1)].number if self.buffer else 0, i)) for i in lines))


class Context(object):
    """Context"""
    __slots__ = ('input', 'scope', 'flag', '_handler', 'templates', 'handlers', 'mapping')

    def __init__(self, input):
        self.input = Lines(input.decode('utf8') if isinstance(input, bytes) else input)
        self.scope = 0
        self.flag = set()
        self._handler = []
        self.handlers = []
        self.templates = []
        self.mapping = None
        for translator in map(methodcaller('load'), iter_entry_points('cinje.translator')):
            self.handlers.append(translator)

    def __repr__(self):
        return 'Context({!r}, {}, {})'.format(self.input, self.scope, self.flag)

    def prepare(self):
        """Prepare the ordered list of transformers and reset context state to initial."""
        self.scope = 0
        self.mapping = deque([0])
        self._handler = [i() for i in sorted((self.handlers), key=(lambda handler: handler.priority))]

    @property
    def stream(self):
        """The workhorse of cinje: transform input lines and emit output lines.
                
                After constructing an instance with a set of input lines iterate this property to generate the template.
                """
        if 'init' not in self.flag:
            root = True
            self.prepare()
        else:
            root = False
        mapping = self.mapping
        for line in self.input:
            handler = self.classify(line)
            if line.kind == 'code':
                if line.stripped == 'end':
                    return
            assert handler, 'Unable to identify handler for line; this should be impossible!'
            self.input.push(line)
            for line in handler(self):
                if root:
                    mapping.appendleft(line.number or )
                if line.scope is None:
                    line = line.clone(scope=(self.scope))
                yield line

    def classify(self, line):
        """Identify the correct handler for a given line of input."""
        for handler in self._handler:
            if handler.match(self, line):
                return handler


class Pipe(object):
    """Pipe"""
    __slots__ = ('callable', 'args', 'kwargs')

    def __init__(self, callable, *args, **kw):
        super(Pipe, self).__init__()
        self.callable = callable
        self.args = args if args else ()
        self.kwargs = kw if kw else {}

    def __repr__(self):
        return 'Pipe({self.callable!r}{0}{1})'.format((', ' + ', '.join((repr(i) for i in self.args)) if self.args else ''),
          (', ' + ', '.join(('{0}={1!r}'.format(i, j) for i, j in self.kwargs.items())) if self.kwargs else ''),
          self=self)

    def __ror__(self, other):
        """The main machinery of the Pipe, calling the chosen callable with the recorded arguments."""
        return (self.callable)(*(self.args) + (other,), **self.kwargs)

    def __call__(self, *args, **kw):
        """Allow for the preserved args and kwargs to be updated, returning a mutated copy.
                
                This allows for usage with arguments, as in the following example:
                
                        "Hello!" | encode('utf8')
                
                This also allows for easy construction of custom mutated copies for use later, a la:
                
                        utf8 = encode('utf8')
                        "Hello!" | utf8
                """
        return (self.__class__)(self.callable, *args, **kw)


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()