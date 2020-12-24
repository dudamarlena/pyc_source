# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_vendor/colorama/initialise.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 1915 bytes
import atexit, contextlib, sys
from .ansitowin32 import AnsiToWin32
orig_stdout = None
orig_stderr = None
wrapped_stdout = None
wrapped_stderr = None
atexit_done = False

def reset_all():
    global orig_stdout
    if AnsiToWin32 is not None:
        AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):
    global atexit_done
    global orig_stderr
    global orig_stdout
    global wrapped_stderr
    global wrapped_stdout
    if not wrap:
        if any([autoreset, convert, strip]):
            raise ValueError('wrap=False conflicts with any other arg=True')
    else:
        orig_stdout = sys.stdout
        orig_stderr = sys.stderr
        if sys.stdout is None:
            wrapped_stdout = None
        else:
            sys.stdout = wrapped_stdout = wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
        if sys.stderr is None:
            wrapped_stderr = None
        else:
            sys.stderr = wrapped_stderr = wrap_stream(orig_stderr, convert, strip, autoreset, wrap)
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def deinit():
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr


@contextlib.contextmanager
def colorama_text(*args, **kwargs):
    init(*args, **kwargs)
    try:
        yield
    finally:
        deinit()


def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream, convert=convert,
          strip=strip,
          autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream