# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bramin/__init__.py
# Compiled at: 2020-01-02 02:00:40
# Size of source mod 2**32: 181 bytes
__version__ = '0.0.1'
from .pipe import Pipe, END
from .pipe import placeholder
it = placeholder
P = Pipe
from .patch import patch_all
patch_all()
__all__ = [
 'P', 'it', 'END']