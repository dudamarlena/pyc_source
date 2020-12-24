# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/opsbro-oss/opsbro/misc/colorama/initialise.py
# Compiled at: 2017-05-30 15:25:14
import atexit, sys
from .ansitowin32 import AnsiToWin32
orig_stdout = sys.stdout
orig_stderr = sys.stderr
wrapped_stdout = sys.stdout
wrapped_stderr = sys.stderr
atexit_done = False

def reset_all():
    AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):
    global atexit_done
    global wrapped_stderr
    global wrapped_stdout
    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')
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
    return


def deinit():
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr
    return


def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr
    return


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream, convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream