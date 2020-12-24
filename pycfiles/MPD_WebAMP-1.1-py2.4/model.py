# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mpd_webamp/model.py
# Compiled at: 2007-06-11 06:34:27
from turbogears.database import PackageHub
from sqlobject import *
hub = PackageHub('mpd_webamp')
__connection__ = hub