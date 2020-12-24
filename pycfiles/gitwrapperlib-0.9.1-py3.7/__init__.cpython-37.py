# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gitwrapperlib/__init__.py
# Compiled at: 2018-08-18 13:39:05
# Size of source mod 2**32: 1960 bytes
"""
gitwrapperlib package

Import all parts from gitwrapperlib here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .gitwrapperlibexceptions import ExecutableNotFound
from .gitwrapperlib import Git
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2018-01-02'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
assert __version__
assert ExecutableNotFound
assert Git