# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/std_out_err_redirect_tqdm.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 933 bytes
"""Redirecting writing to tqdm (the progressbar).

See here: https://github.com/tqdm/tqdm#redirecting-writing
"""
import contextlib, sys
from tqdm import tqdm

class DummyTqdmFile(object):
    __doc__ = 'Dummy file-like that will write to tqdm.'
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)

    def flush(self):
        return getattr(self.file, 'flush', lambda : None)()


@contextlib.contextmanager
def std_out_err_redirect_tqdm():
    orig_out_err = (sys.stdout, sys.stderr)
    try:
        try:
            sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
            yield orig_out_err[0]
        except Exception as exc:
            raise exc

    finally:
        sys.stdout, sys.stderr = orig_out_err