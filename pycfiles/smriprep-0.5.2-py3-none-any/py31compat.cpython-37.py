# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/setuptools/setuptools/py31compat.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 838 bytes
__all__ = []
__metaclass__ = type
try:
    from tempfile import TemporaryDirectory
except ImportError:
    import shutil, tempfile

    class TemporaryDirectory:
        __doc__ = '\n        Very simple temporary directory context manager.\n        Will try to delete afterward, but will also ignore OS and similar\n        errors on deletion.\n        '

        def __init__(self, **kwargs):
            self.name = None
            self.name = (tempfile.mkdtemp)(**kwargs)

        def __enter__(self):
            return self.name

        def __exit__(self, exctype, excvalue, exctrace):
            try:
                shutil.rmtree(self.name, True)
            except OSError:
                pass

            self.name = None