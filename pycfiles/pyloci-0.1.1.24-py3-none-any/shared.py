# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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