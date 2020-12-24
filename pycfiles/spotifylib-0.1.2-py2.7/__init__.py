# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/spotifylib/__init__.py
# Compiled at: 2017-10-03 05:20:45
"""
spotifylib package

Imports all parts from spotifylib here
"""
from ._version import __version__
from .constants import *
from spotifylib import Spotify
from spotifylibexceptions import SpotifyError
__author__ = 'Oriol Fabregas'
__email__ = 'fabregas.oriol@gmail.com'
assert __version__
assert Spotify
assert SpotifyError