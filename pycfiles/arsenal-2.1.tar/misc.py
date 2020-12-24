# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: arsenal/misc.py
# Compiled at: 2017-08-11 12:26:58
import re, os, sys, traceback, warnings, webbrowser, subprocess, tempfile, BaseHTTPServer
from functools import wraps
from StringIO import StringIO
from contextlib import contextmanager
from arsenal.terminal import colors

def open_diff(a, b, cmd='meld'):
    """View diff of string representations in dedicated diff program."""
    print >> file('/tmp/a', 'wb'), a
    print >> file('/tmp/b', 'wb'), b
    os.system('%s /tmp/a /tmp/b' % cmd)


def deprecated(use_instead=None):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """

    def wrapped(func):

        @wraps(func)
        def new_func(*args, **kwargs):
            message = 'Call to deprecated function %s.' % func.__name__
            if use_instead:
                message += ' Use %s instead.' % use_instead
            warnings.warn(message, stacklevel=2)
            return func(*args, **kwargs)

        return new_func

    return wrapped


class ddict(dict):
    """
    Variation on collections.defaultdict which allows default value callback to
    inspect missing key.
    """

    def __init__(self, f):
        self.f = f
        super(ddict, self).__init__()

    def __missing__(self, key):
        self[key] = c = self.f(key)
        return c


@contextmanager
def ignore_error(color='red'):
    try:
        yield
    except:
        etype, evalue, tb = sys.exc_info()
        tb = ('\n').join(traceback.format_exception(etype, evalue, tb))
        if color is not None:
            color = getattr(colors, color)
        else:
            color = '%s'
        print color % '*' * 80
        print color % tb
        print color % '*' * 80

    return


def force(g):
    """ force evaluation of generator `g`. """

    @wraps(g)
    def wrap(*args, **kw):
        return list(g(*args, **kw))

    return wrap


def piped():
    """ Returns piped input via stdin, else None. """
    if not sys.stdin.isatty():
        return sys.stdin
    else:
        return


def highlighter(p, flags=0):
    pattern = re.compile('%s' % p, flags)
    return lambda x: pattern.sub(colors.bold % colors.yellow % colors.bg_red % '\\1', x)


def browser(html):
    """
    Display html in the default web browser without creating a temp file.

    Instantiates a trivial http server and calls webbrowser.open with a URL
    to retrieve html from that server.
    """

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
            bufferSize = 1048576
            for i in xrange(0, len(html), bufferSize):
                self.wfile.write(html[i:i + bufferSize])

    server = BaseHTTPServer.HTTPServer(('127.0.0.1', 0), RequestHandler)
    webbrowser.open('http://127.0.0.1:%s' % server.server_port)
    server.handle_request()


def pager(s, cmd='less'):
    """Use the pager passed in and send string s through it."""
    subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(s)


def edit_with_editor(s=None):
    """
    Open os.environ['EDITOR'] and load in text s.

    Returns the text typed in the editor, after running strip().
    """
    with tempfile.NamedTemporaryFile() as (t):
        if s:
            t.write(str(s))
            t.seek(0)
        subprocess.call([os.environ.get('EDITOR', 'nano'), t.name])
        return t.read().strip()


editor = edit_with_editor

@contextmanager
def ctx_redirect_io(f=None):
    r"""
    Usage example:
      >>> with ctx_redirect_io() as io_target:
      ...    print 'how is this for io?'
      >>> io_target.getvalue()
      'how is this for io?\n'
    """
    target = f or StringIO()
    original_stdout = sys.stdout
    try:
        sys.stdout = target
        yield target
    finally:
        sys.stdout = original_stdout


def redirect_io(f):
    """
    redirect all of the output to standard out to a StringIO instance,
    which can be accessed as an attribute of the function, f.io_target

    Usage Example:
        >>> @redirect_io
        ... def foo(x):
        ...    print x
        >>> foo('hello?')
        >>> print foo.io_target.getvalue()    # doctest:+NORMALIZE_WHITESPACE
        hello?
        >>>
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        with ctx_redirect_io() as (io_target):
            wrap.io_target = io_target
            return f(*args, **kwargs)

    return wrap


if __name__ == '__main__':
    import doctest

    def run_tests():

        def test_redirect_io():

            @redirect_io
            def foo(x):
                print x

            msg = 'hello there?'
            foo(msg)
            assert str(foo.io_target.getvalue().strip()) == msg

        test_redirect_io()


    run_tests()
    print 'passed'
    doctest.testmod()