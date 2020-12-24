# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yhoorneman/Git/opsgenielib/opsgenielib/__init__.py
# Compiled at: 2019-11-29 09:45:23
# Size of source mod 2**32: 1977 bytes
"""
opsgenielib package.

Import all parts from opsgenielib here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .opsgenielib import Opsgenie
from .opsgenielibexceptions import InvalidApiKey
__author__ = 'Yorick Hoorneman <yhoorneman@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '12-04-2019'
__copyright__ = 'Copyright 2019, Yorick Hoorneman'
__license__ = 'MIT'
__maintainer__ = 'Yorick Hoorneman'
__email__ = '<yhoorneman@schubergphilis.com>'
__status__ = 'Development'
assert __version__
assert InvalidApiKey
assert Opsgenie