# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Globals.py
# Compiled at: 2019-02-16 11:54:10
# Size of source mod 2**32: 1672 bytes
from __future__ import print_function
import sys, os
from pypref import SinglePreferences

class Preferences(SinglePreferences):

    def custom_init(self):
        prefs = {}
        if sys.platform == 'win32':
            exePath = None
            for p in [fname for fname in os.listdir('C:\\') if 'Program Files' in fname]:
                path = os.path.join('C:\\', p, 'University of Illinois', 'VMD', 'vmd.exe')
                if os.path.exists(path):
                    exePath = path

            prefs['VMD_PATH'] = exePath
        else:
            if sys.platform == 'darwin':
                exePath = None
                if os.path.exists('/Applications'):
                    exePath = '/Applications'
                    files = [fname for fname in os.listdir(exePath) if 'VMD' in fname]
                    if not len(files):
                        exePath = None
                if exePath is not None:
                    exePath = os.path.join(exePath, files[0], 'Contents', 'vmd')
                    files = [fname for fname in os.listdir(exePath) if 'vmd_MACOS' in fname]
                    if not len(files):
                        exePath = None
                if exePath is not None:
                    exePath = os.path.join(exePath, files[0])
                prefs['VMD_PATH'] = exePath
            else:
                exePath = None
                if os.path.exists('/usr/local/bin/vmd'):
                    exePath = '/usr/local/bin/vmd'
                prefs['VMD_PATH'] = exePath
        if sorted(self.preferences.keys()) != sorted(prefs.keys()):
            self.set_preferences(prefs)


PREFERENCES = Preferences(filename='pdbparserParams.py')