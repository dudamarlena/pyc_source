# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/xz.py
# Compiled at: 2016-08-17 00:26:57
# Size of source mod 2**32: 2559 bytes
"""
gzopen.py - open (may) gzip/bz2 files
XU Yu, <xuyu@genomics.org.cn>
2012-07-07 19:33:41 CST
add compatibility support for Python3
Sein Tao, <sein.tao@gmail.com>
2015-08-17 18:30:15 CST
"""
import sys
PY3 = sys.version_info > (3, )
if PY3:
    import builtins
else:
    import __builtin__ as builtins
__all__ = [
 'xzFile', 'xzopen', 'open']

class xzFile:
    __doc__ = "handle (might) compressed file properly.\n    recoganizable name/suffix: '-' for pipe, '.gz' for gzip,\n        '.bz2' for bz2, '.bgz' or '.b.gz' for bgzip,\n        other suffix as plain text file\n    "

    def __init__(self, file, mode='r', *args, **kwargs):
        self.fh = None
        (self.open)(file, mode, *args, **kwargs)

    def __enter__(self):
        try:
            return self.fh.__enter__()
        except AttributeError:
            return self.fh

    def __exit__(self, type, value, traceback):
        try:
            return self.fh.__exit__(type, value, traceback)
        except AttributeError:
            try:
                self.fh.close()
            finally:
                return

            return

    def __iter__(self):
        return iter(self.fh)

    def __next__(self):
        return next(self.fh)

    def open(self, file, mode='r', *args, **kwargs):
        self.fh = _xzopen(file, mode, *args, **kwargs)

    def __getattr__(self, attr):
        """Caution for subclassing: call self.fh.method instead of super().method"""
        return getattr(self.fh, attr)


def xzopen(file, mode='r', *args, **kwargs):
    """wrapper to construct xzFile object"""
    return xzFile(file, mode, *args, **kwargs)


def _xzopen(file, mode='r', *args, **kargs):
    """construct an IO stream"""
    if file == '-':
        if 'w' in mode:
            return sys.stdout
        return sys.stdin
    else:
        if 'b' not in mode:
            if 't' not in mode:
                mode += 't'
            if file.endswith('.bgz') or file.endswith('.b.gz'):
                from .bgzip import open as bgzip_open
                return bgzip_open(file, mode, *args, **kargs)
        else:
            if file.endswith('.gz'):
                import gzip
                return (gzip.open)(file, mode, *args, **kargs)
            if file.endswith('.bz2'):
                import bz2
                return (bz2.open)(file, mode, *args, **kargs)
        return (builtins.open)(file, mode, *args, **kargs)


open = xzopen
if __name__ == '__main__':
    pass