# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/dev/python/piep/test/test_helper.py
# Compiled at: 2019-01-10 05:16:44
# Size of source mod 2**32: 1342 bytes
import os, sys, itertools, contextlib, shutil, tempfile, subprocess
from io import StringIO
from piep import main
from piep.pycompat import *

def limit_heap_size():
    import resource
    limit = 204800000
    resource.setrlimit(resource.RLIMIT_DATA, (0, limit))


limit_heap_size()

def run(*args):
    args = list(args)
    input_lines = args.pop()
    opts, args = main.parse_args(args)
    old_stdin = sys.stdin
    sys.stdin = map(str, input_lines)
    try:
        return [str(line) for line in main.run(opts, args)]
    finally:
        sys.stdin = old_stdin


def run_full(*args):
    args = list(args)
    stdin = args.pop()
    if isinstance(stdin, str):
        stdin = stdin.encode('ascii')
    proc = subprocess.Popen(([sys.executable, '-m', 'piep'] + args), stdin=(subprocess.PIPE),
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      env={'PYTHONPATH': os.path.dirname(os.path.dirname(main.__file__))})
    out, err = proc.communicate(stdin)
    if proc.returncode != 0:
        raise AssertionError('Command failed\nout: %s\nerr: %s' % (out, err))
    return out.decode('utf-8')


@contextlib.contextmanager
def cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@contextlib.contextmanager
def temp_cwd():
    path = tempfile.mkdtemp()
    try:
        with cwd(path):
            yield
    finally:
        shutil.rmtree(path)