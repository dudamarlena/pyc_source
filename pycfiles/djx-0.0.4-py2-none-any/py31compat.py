# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/py31compat.py
# Compiled at: 2019-02-06 16:42:30
__all__ = []
__metaclass__ = type
try:
    from tempfile import TemporaryDirectory
except ImportError:
    import shutil, tempfile

    class TemporaryDirectory:
        """
        Very simple temporary directory context manager.
        Will try to delete afterward, but will also ignore OS and similar
        errors on deletion.
        """

        def __init__(self):
            self.name = None
            self.name = tempfile.mkdtemp()
            return

        def __enter__(self):
            return self.name

        def __exit__(self, exctype, excvalue, exctrace):
            try:
                shutil.rmtree(self.name, True)
            except OSError:
                pass

            self.name = None
            return