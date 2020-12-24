# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/tests/util.py
# Compiled at: 2012-12-17 09:52:34
"""
    Sphinx test suite utilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import sys, StringIO, tempfile, shutil, re
from codecs import open
try:
    from functools import wraps
except ImportError:
    wraps = lambda f: lambda w: w

from sphinx import application
from sphinx.ext.autodoc import AutoDirective
from path import path
from nose import tools, SkipTest
__all__ = [
 'test_root', 'raises', 'raises_msg',
 'skip_if', 'skip_unless', 'skip_unless_importable', 'Struct',
 'ListOutput', 'TestApp', 'with_app', 'gen_with_app',
 'path', 'with_tempdir', 'write_file',
 'sprint', 'remove_unicode_literals']
test_root = path(__file__).parent.joinpath('root').abspath()

def _excstr(exc):
    if type(exc) is tuple:
        return str(tuple(map(_excstr, exc)))
    return exc.__name__


def raises(exc, func, *args, **kwds):
    """
    Raise :exc:`AssertionError` if ``func(*args, **kwds)`` does not
    raise *exc*.
    """
    try:
        func(*args, **kwds)
    except exc:
        pass
    else:
        raise AssertionError('%s did not raise %s' % (
         func.__name__, _excstr(exc)))


def raises_msg--- This code section failed: ---

 L.  66         0  SETUP_EXCEPT         17  'to 20'

 L.  67         3  LOAD_FAST             2  'func'
                6  LOAD_FAST             3  'args'
                9  LOAD_FAST             4  'kwds'
               12  CALL_FUNCTION_VAR_KW_0     0  None
               15  POP_TOP          
               16  POP_BLOCK        
               17  JUMP_FORWARD         56  'to 76'
             20_0  COME_FROM             0  '0'

 L.  68        20  DUP_TOP          
               21  LOAD_FAST             0  'exc'
               24  COMPARE_OP           10  exception-match
               27  POP_JUMP_IF_FALSE    75  'to 75'
               30  POP_TOP          
               31  STORE_FAST            5  'err'
               34  POP_TOP          

 L.  69        35  LOAD_FAST             1  'msg'
               38  LOAD_GLOBAL           0  'str'
               41  LOAD_FAST             5  'err'
               44  CALL_FUNCTION_1       1  None
               47  COMPARE_OP            6  in
               50  POP_JUMP_IF_TRUE    107  'to 107'
               53  LOAD_ASSERT              AssertionError
               56  LOAD_CONST               '"%s" not in "%s"'
               59  LOAD_FAST             1  'msg'
               62  LOAD_FAST             5  'err'
               65  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               69  RAISE_VARARGS_2       2  None
               72  JUMP_FORWARD         32  'to 107'
               75  END_FINALLY      
             76_0  COME_FROM            17  '17'

 L.  71        76  LOAD_GLOBAL           1  'AssertionError'
               79  LOAD_CONST               '%s did not raise %s'

 L.  72        82  LOAD_FAST             2  'func'
               85  LOAD_ATTR             2  '__name__'
               88  LOAD_GLOBAL           3  '_excstr'
               91  LOAD_FAST             0  'exc'
               94  CALL_FUNCTION_1       1  None
               97  BUILD_TUPLE_2         2 
              100  BINARY_MODULO    
              101  CALL_FUNCTION_1       1  None
              104  RAISE_VARARGS_1       1  None
            107_0  COME_FROM            75  '75'

Parse error at or near `END_FINALLY' instruction at offset 75


def skip_if(condition, msg=None):
    """Decorator to skip test if condition is true."""

    def deco(test):

        @tools.make_decorator(test)
        def skipper(*args, **kwds):
            if condition:
                raise SkipTest(msg or 'conditional skip')
            return test(*args, **kwds)

        return skipper

    return deco


def skip_unless(condition, msg=None):
    """Decorator to skip test if condition is false."""
    return skip_if(not condition, msg)


def skip_unless_importable(module, msg=None):
    """Decorator to skip test if module is not importable."""
    try:
        __import__(module)
    except ImportError:
        return skip_if(True, msg)

    return skip_if(False, msg)


class Struct(object):

    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class ListOutput(object):
    """
    File-like object that collects written text in a list.
    """

    def __init__(self, name):
        self.name = name
        self.content = []

    def reset(self):
        del self.content[:]

    def write(self, text):
        self.content.append(text)


class TestApp(application.Sphinx):
    """
    A subclass of :class:`Sphinx` that runs on the test root, with some
    better default values for the initialization parameters.
    """

    def __init__(self, srcdir=None, confdir=None, outdir=None, doctreedir=None, buildername='html', confoverrides=None, status=None, warning=None, freshenv=None, warningiserror=None, tags=None, confname='conf.py', cleanenv=False):
        application.CONFIG_FILENAME = confname
        self.cleanup_trees = [
         test_root / 'generated']
        if srcdir is None:
            srcdir = test_root
        if srcdir == '(temp)':
            tempdir = path(tempfile.mkdtemp())
            self.cleanup_trees.append(tempdir)
            temproot = tempdir / 'root'
            test_root.copytree(temproot)
            srcdir = temproot
        else:
            srcdir = path(srcdir)
        self.builddir = srcdir.joinpath('_build')
        if confdir is None:
            confdir = srcdir
        if outdir is None:
            outdir = srcdir.joinpath(self.builddir, buildername)
            if not outdir.isdir():
                outdir.makedirs()
            self.cleanup_trees.insert(0, outdir)
        if doctreedir is None:
            doctreedir = srcdir.joinpath(srcdir, self.builddir, 'doctrees')
            if cleanenv:
                self.cleanup_trees.insert(0, doctreedir)
        if confoverrides is None:
            confoverrides = {}
        if status is None:
            status = StringIO.StringIO()
        if warning is None:
            warning = ListOutput('stderr')
        if freshenv is None:
            freshenv = False
        if warningiserror is None:
            warningiserror = False
        application.Sphinx.__init__(self, srcdir, confdir, outdir, doctreedir, buildername, confoverrides, status, warning, freshenv, warningiserror, tags)
        return

    def cleanup(self, doctrees=False):
        AutoDirective._registry.clear()
        for tree in self.cleanup_trees:
            shutil.rmtree(tree, True)


def with_app(*args, **kwargs):
    """
    Make a TestApp with args and kwargs, pass it to the test and clean up
    properly.
    """

    def generator(func):

        @wraps(func)
        def deco(*args2, **kwargs2):
            app = TestApp(*args, **kwargs)
            func(app, *args2, **kwargs2)
            app.cleanup()

        return deco

    return generator


def gen_with_app(*args, **kwargs):
    """
    Decorate a test generator to pass a TestApp as the first argument to the
    test generator when it's executed.
    """

    def generator(func):

        @wraps(func)
        def deco(*args2, **kwargs2):
            app = TestApp(*args, **kwargs)
            for item in func(app, *args2, **kwargs2):
                yield item

            app.cleanup()

        return deco

    return generator


def with_tempdir(func):

    def new_func(*args, **kwds):
        tempdir = path(tempfile.mkdtemp())
        func(tempdir, *args, **kwds)
        tempdir.rmtree()

    new_func.__name__ = func.__name__
    return new_func


def write_file(name, contents, encoding=None):
    if encoding is None:
        mode = 'wb'
        if isinstance(contents, unicode):
            contents = contents.encode('ascii')
    else:
        mode = 'w'
    f = open(str(name), mode, encoding=encoding)
    f.write(contents)
    f.close()
    return


def sprint(*args):
    sys.stderr.write((' ').join(map(str, args)) + '\n')


_unicode_literals_re = re.compile('u(".*?")|u(\\\'.*?\\\')')

def remove_unicode_literals(s):
    return _unicode_literals_re.sub(lambda x: x.group(1) or x.group(2), s)