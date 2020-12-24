# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolecli/powermolecli/__init__.py
# Compiled at: 2020-05-11 18:02:37
# Size of source mod 2**32: 1847 bytes
"""
Import all parts from minitorcli here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .powermolecliexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
assert __version__
assert SetupFailed