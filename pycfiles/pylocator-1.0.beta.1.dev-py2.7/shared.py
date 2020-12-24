# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/shared.py
# Compiled at: 2012-04-17 03:56:34
import os

class Shared(object):
    debug = False
    lastSel = ''
    labels = ['L', 'R', 'P', 'A', 'I', 'S']
    ratio = 3
    screenshot_cnt = 1
    planes_opacity = 1.0
    markers_opacity = 1.0
    marker_size = 3.0
    lastLabel = ''

    def set_file_selection(self, name):
        """
        Set the filename or dir of the most recent file selected
        """
        self.lastSel = name

    def get_last_dir(self):
        """
        Return the dir name of the most recent file selected
        """
        if os.path.isdir(self.lastSel):
            return self.lastSel
        else:
            return os.path.dirname(self.lastSel) + os.sep


shared = Shared()