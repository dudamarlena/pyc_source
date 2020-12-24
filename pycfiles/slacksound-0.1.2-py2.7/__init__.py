# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/slacksound/__init__.py
# Compiled at: 2017-10-14 14:17:13
"""
slacksound package

Import all parts from slacksound here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .spotifyclient import SpotifyClient
from .slackapi import Slack
__author__ = 'Oriol Fabregas <fabregas.oriol@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-10-13'
__copyright__ = 'Copyright 2017, Oriol Fabregas'
__license__ = 'MIT'
__maintainer__ = 'Oriol Fabregas'
__email__ = '<fabregas.oriol@gmail.com>'
__status__ = 'Development'
assert __version__
assert SpotifyClient
assert Slack