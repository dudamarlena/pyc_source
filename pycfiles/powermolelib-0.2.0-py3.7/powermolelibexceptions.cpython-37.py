# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolelib/powermolelib/powermolelibexceptions.py
# Compiled at: 2020-05-11 18:06:39
# Size of source mod 2**32: 1991 bytes
__doc__ = '\nCustom exception code for minitorcorelib.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'

class InvalidConfigurationFile(Exception):
    """InvalidConfigurationFile"""
    pass