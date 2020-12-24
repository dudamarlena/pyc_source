# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/config.py
# Compiled at: 2016-01-07 05:48:00
# Size of source mod 2**32: 662 bytes
import os
__all__ = ('INITPY_FILENAME', 'SOURCE_SUFFIXES', 'AUTODOC_OPTIONS')
INITPY_FILENAME = '__init__.py'
SOURCE_SUFFIXES = frozenset(['.py', '.pyx'])
if 'SPHINX_APIDOC_OPTIONS' in os.environ:
    __autodoc_options = os.environ['SPHINX_APIDOC_OPTIONS'].split(',')
else:
    __autodoc_options = [
     'members',
     'undoc-members',
     'show-inheritance']
AUTODOC_OPTIONS = __autodoc_options