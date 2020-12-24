# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/mark.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 10869 bytes
""" generic mechanism for marking and selecting python functions. """
import py

class MarkerError(Exception):
    __doc__ = 'Error in use of a pytest marker/attribute.'


def pytest_namespace():
    return {'mark': MarkGenerator()}


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group._addoption('-k',
      action='store',
      dest='keyword',
      default='',
      metavar='EXPRESSION',
      help="only run tests which match the given substring expression. An expression is a python evaluatable expression where all names are substring-matched against test names and their parent classes. Example: -k 'test_method or test other' matches all test functions and classes whose name contains 'test_method' or 'test_other'. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which have names assigned directly to them.")
    group._addoption('-m',
      action='store',
      dest='markexpr',
      default='',
      metavar='MARKEXPR',
      help="only run tests matching given mark expression.  example: -m 'mark1 and not mark2'.")
    group.addoption('--markers',
      action='store_true', help='show markers (builtin, plugin and per-project ones).')
    parser.addini('markers', 'markers for test functions', 'linelist')


def pytest_cmdline_main(config):
    if config.option.markers:
        config.do_configure()
        tw = py.io.TerminalWriter()
        for line in config.getini('markers'):
            name, rest = line.split(':', 1)
            tw.write(('@pytest.mark.%s:' % name), bold=True)
            tw.line(rest)
            tw.line()

        config.do_unconfigure()
        return 0


pytest_cmdline_main.tryfirst = True

def pytest_collection_modifyitems(items, config):
    keywordexpr = config.option.keyword
    matchexpr = config.option.markexpr
    if not keywordexpr:
        if not matchexpr:
            return
    if keywordexpr.startswith('-'):
        keywordexpr = 'not ' + keywordexpr[1:]
    selectuntil = False
    if keywordexpr[-1:] == ':':
        selectuntil = True
        keywordexpr = keywordexpr[:-1]
    remaining = []
    deselected = []
    for colitem in items:
        if keywordexpr and not matchkeyword(colitem, keywordexpr):
            deselected.append(colitem)
        else:
            if selectuntil:
                keywordexpr = None
            if matchexpr:
                if not matchmark(colitem, matchexpr):
                    deselected.append(colitem)
                    continue
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining


class MarkMapping:
    __doc__ = 'Provides a local mapping for markers where item access\n    resolves to True if the marker is present. '

    def __init__(self, keywords):
        mymarks = set()
        for key, value in keywords.items():
            if isinstance(value, MarkInfo) or isinstance(value, MarkDecorator):
                mymarks.add(key)

        self._mymarks = mymarks

    def __getitem__(self, name):
        return name in self._mymarks


class KeywordMapping:
    __doc__ = 'Provides a local mapping for keywords.\n    Given a list of names, map any substring of one of these names to True.\n    '

    def __init__(self, names):
        self._names = names

    def __getitem__(self, subname):
        for name in self._names:
            if subname in name:
                return True

        return False


def matchmark(colitem, markexpr):
    """Tries to match on any marker names, attached to the given colitem."""
    return eval(markexpr, {}, MarkMapping(colitem.keywords))


def matchkeyword(colitem, keywordexpr):
    """Tries to match given keyword expression to given collector item.

    Will match on the name of colitem, including the names of its parents.
    Only matches names of items which are either a :class:`Class` or a
    :class:`Function`.
    Additionally, matches on names in the 'extra_keyword_matches' set of
    any item, as well as names directly assigned to test functions.
    """
    mapped_names = set()
    import pytest
    for item in colitem.listchain():
        if not isinstance(item, pytest.Instance):
            mapped_names.add(item.name)

    for name in colitem.listextrakeywords():
        mapped_names.add(name)

    if hasattr(colitem, 'function'):
        for name in colitem.function.__dict__:
            mapped_names.add(name)

    mapping = KeywordMapping(mapped_names)
    if ' ' not in keywordexpr:
        return mapping[keywordexpr]
    else:
        if keywordexpr.startswith('not '):
            if ' ' not in keywordexpr[4:]:
                return not mapping[keywordexpr[4:]]
        return eval(keywordexpr, {}, mapping)


def pytest_configure(config):
    import pytest
    if config.option.strict:
        pytest.mark._config = config


class MarkGenerator:
    __doc__ = " Factory for :class:`MarkDecorator` objects - exposed as\n    a ``pytest.mark`` singleton instance.  Example::\n\n         import py\n         @pytest.mark.slowtest\n         def test_function():\n            pass\n\n    will set a 'slowtest' :class:`MarkInfo` object\n    on the ``test_function`` object. "

    def __getattr__(self, name):
        if name[0] == '_':
            raise AttributeError('Marker name must NOT start with underscore')
        if hasattr(self, '_config'):
            self._check(name)
        return MarkDecorator(name)

    def _check(self, name):
        try:
            if name in self._markers:
                return
        except AttributeError:
            pass

        self._markers = l = set()
        for line in self._config.getini('markers'):
            beginning = line.split(':', 1)
            x = beginning[0].split('(', 1)[0]
            l.add(x)

        if name not in self._markers:
            raise AttributeError('%r not a registered marker' % (name,))


def istestfunc(func):
    return hasattr(func, '__call__') and getattr(func, '__name__', '<lambda>') != '<lambda>'


class MarkDecorator:
    __doc__ = " A decorator for test functions and test classes.  When applied\n    it will create :class:`MarkInfo` objects which may be\n    :ref:`retrieved by hooks as item keywords <excontrolskip>`.\n    MarkDecorator instances are often created like this::\n\n        mark1 = pytest.mark.NAME              # simple MarkDecorator\n        mark2 = pytest.mark.NAME(name1=value) # parametrized MarkDecorator\n\n    and can then be applied as decorators to test functions::\n\n        @mark2\n        def test_function():\n            pass\n\n    When a MarkDecorator instance is called it does the following:\n      1. If called with a single class as its only positional argument and no\n         additional keyword arguments, it attaches itself to the class so it\n         gets applied automatically to all test cases found in that class.\n      2. If called with a single function as its only positional argument and\n         no additional keyword arguments, it attaches a MarkInfo object to the\n         function, containing all the arguments already stored internally in\n         the MarkDecorator.\n      3. When called in any other case, it performs a 'fake construction' call,\n         i.e. it returns a new MarkDecorator instance with the original\n         MarkDecorator's content updated with the arguments passed to this\n         call.\n\n    Note: The rules above prevent MarkDecorator objects from storing only a\n    single function or class reference as their positional argument with no\n    additional keyword or positional arguments.\n\n    "

    def __init__(self, name, args=None, kwargs=None):
        self.name = name
        self.args = args or ()
        self.kwargs = kwargs or {}

    @property
    def markname(self):
        return self.name

    def __repr__(self):
        d = self.__dict__.copy()
        name = d.pop('name')
        return '<MarkDecorator %r %r>' % (name, d)

    def __call__(self, *args, **kwargs):
        """ if passed a single callable argument: decorate it with mark info.
            otherwise add *args/**kwargs in-place to mark information. """
        if args and not kwargs:
            func = args[0]
            if len(args) == 1 and (istestfunc(func) or hasattr(func, '__bases__')):
                if hasattr(func, '__bases__'):
                    if hasattr(func, 'pytestmark'):
                        l = func.pytestmark
                        func.pytestmark = isinstance(l, list) or [
                         l, self]
                    else:
                        l.append(self)
                else:
                    func.pytestmark = [
                     self]
            else:
                holder = getattr(func, self.name, None)
                if holder is None:
                    holder = MarkInfo(self.name, self.args, self.kwargs)
                    setattr(func, self.name, holder)
                else:
                    holder.add(self.args, self.kwargs)
            return func
        else:
            kw = self.kwargs.copy()
            kw.update(kwargs)
            args = self.args + args
            return self.__class__((self.name), args=args, kwargs=kw)


class MarkInfo:
    __doc__ = ' Marking object created by :class:`MarkDecorator` instances. '

    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self._arglist = [(args, kwargs.copy())]

    def __repr__(self):
        return '<MarkInfo %r args=%r kwargs=%r>' % (
         self.name, self.args, self.kwargs)

    def add(self, args, kwargs):
        """ add a MarkInfo with the given args and kwargs. """
        self._arglist.append((args, kwargs))
        self.args += args
        self.kwargs.update(kwargs)

    def __iter__(self):
        """ yield MarkInfo objects each relating to a marking-call. """
        for args, kwargs in self._arglist:
            yield MarkInfo(self.name, args, kwargs)