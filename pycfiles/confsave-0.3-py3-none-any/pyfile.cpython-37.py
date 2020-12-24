# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/loaders/pyfile.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 1464 bytes
__doc__ = 'Loader for Python files.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ..core import config
from . import base

class PythonFile(base.ConfigurationFile):
    """PythonFile"""

    def __init__(self, *args, **kwargs):
        (super(PythonFile, self).__init__)(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the code object which represents the compiled Python file.

        This property is cached and only parses the content once.
        """
        if not self._parsed:
            self._parsed = compile(self.content, self.path, 'exec')
        return self._parsed

    @property
    def config(self):
        """Get a Configuration object from the file contents."""
        exec(self.parsed, {}, None)
        return config.Configuration()

    @property
    def namespaces(self):
        """Get an empty iterable.

        An iterable of namespaces cannot be generated from Python files.
        """
        return ()

    def items(self, namespace):
        """Get an empty iterable.

        An iterable of items cannot be generated from Python files.
        """
        return ()