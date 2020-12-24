# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/config.py
# Compiled at: 2012-01-15 13:09:38
import os
PROJECTNAME = 'ZenPacks.oie.KannelMonitor'
SKINS_DIR = path.join(path.dirname(__file__), 'skins')
SKINNAME = PROJECTNAME
GLOBALS = globals()
DATAPOINTS = ('recvqueue', 'sentqueue', 'storesize', 'recv', 'sent')
GRAPHPOINTS = {'smsc': ('recvqueue', 'sentqueue', 'recv', 'sent'), 'store': ('storesize', )}