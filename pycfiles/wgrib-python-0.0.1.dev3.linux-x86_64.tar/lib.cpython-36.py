# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/envs/py36/lib/python3.6/site-packages/wgrib/lib.py
# Compiled at: 2018-03-01 12:05:25
# Size of source mod 2**32: 5484 bytes
"""
Simple wrapper around main function in wgrib.c
Compile wgrib.c with GRIB_MAIN=wgrib_main defined using c preprocessor
"""
from __future__ import print_function, unicode_literals
import ctypes, io, os, sys, threading, time, sys
from glob import glob
from functools import wraps
try:
    from contextlib import redirect_stdout, redirect_stderr
except ImportError:
    from contextlib2 import redirect_stdout, redirect_stderr

class WGribSharedLib(object):
    __doc__ = 'Mocks wgrib C extension using ctypes'

    @staticmethod
    def wgrib(args=sys.argv, version=None):
        """Use shared library/DLL to call wgrib"""
        _dir = os.path.abspath(os.path.dirname(__file__))
        if sys.platform.startswith('win'):
            lib_prefix = ''
            lib_suffix = ''
            lib_ext = '.dll'
        else:
            lib_prefix = 'lib'
            try:
                s = sys.implementation
                lib_suffix = '.{}m-{}'.format(s.cachetag, s._multiarch)
            except AttributeError:
                lib_suffix = ''

            lib_ext = '.so'
        LP_c_char = ctypes.POINTER(ctypes.c_char)
        LP_LP_c_char = ctypes.POINTER(LP_c_char)
        _wgrib = 'wgrib{}'.format('2' if version == 2 else '')
        _libname = os.path.join(_dir, lib_prefix + _wgrib + lib_suffix + lib_ext)
        if not os.path.exists(_libname):
            _libname = glob(os.path.join(_dir, '*' + _wgrib + '*' + lib_ext))[0]
        _lib = ctypes.CDLL(_libname)
        _main = _lib.wgrib
        _main.restype = ctypes.c_int
        _main.argtypes = [ctypes.c_int, LP_LP_c_char]
        argc = len(args)
        argv = LP_c_char * (argc + 1)()
        for i, arg in enumerate(args):
            argv[i] = ctypes.create_string_buffer(arg.encode('utf-8'))

        return _main(argc, argv)


try:
    from .wgrib import main as wgrib
except ImportError:
    wgrib = WGribSharedLib.wgrib

try:
    from .wgrib2 import main as wgrib2
    WGRIB2_SUPPORT = True
except ImportError:
    WGRIB2_SUPPORT = False

class OutputGrabber(object):
    __doc__ = '\n    Class used to grab standard output or another stream.\n    '
    escape_char = '\x08'

    def __init__(self, stream=None, threaded=False):
        self.sleep = time.sleep
        self.origstream = stream or sys.stdout
        self.threaded = threaded
        self.origstreamfd = self.origstream.fileno()
        self.capturedtext = ''
        self.pipe_out, self.pipe_in = os.pipe()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        """
        Start capturing the stream data.
        """
        self.capturedtext = ''
        self.streamfd = os.dup(self.origstreamfd)
        os.dup2(self.pipe_in, self.origstreamfd)
        if self.threaded:
            self.workerThread = threading.Thread(target=(self.readOutput))
            self.workerThread.start()
            time.sleep(0.5)

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        self.origstream.write(self.escape_char)
        self.origstream.flush()
        if self.threaded:
            self.workerThread.join()
        else:
            self.readOutput()
        os.close(self.pipe_out)
        os.dup2(self.streamfd, self.origstreamfd)

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while True:
            char = os.read(self.pipe_out, 1)
            if not char or self.escape_char in char:
                break
            self.capturedtext += str(char)


def grab_output(func, out_stream=sys.stdout, err_stream=sys.stderr):
    """Captures low-level (C level) stdout/stderr"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        with OutputGrabber(out_stream) as (stdout):
            with OutputGrabber(err_stream) as (stderr):
                func(*args, **kwargs)
        try:
            out, err = stdout.capturedtext, stderr.capturedtext
            time.sleep(0.5)
        except TypeError:
            pass

        return (out, err)

    return wrapper


@grab_output
def check_wgrib_output(args=sys.argv, wgrib=WGribSharedLib.wgrib):
    """Returns tuple of (stdout, stderr) from wgrib CLI call"""
    if wgrib == 2 or wgrib == 'wgrib2':
        if WGRIB2_SUPPORT:
            return wgrib2(args)
    return wgrib(args)