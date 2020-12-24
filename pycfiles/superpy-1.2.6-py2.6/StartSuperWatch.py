# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\scripts\StartSuperWatch.py
# Compiled at: 2010-06-04 07:07:11
"""Script to start SuperWatch application
"""
import logging
from superpy.SuperWatch import SPGui
if __name__ == '__main__':
    logging.info('Starting SuperWatch GUI.')
    (root, my_tk, myMonitor) = SPGui.StartSuperWatchGUI()
    logging.info('Finished SuperWatch GUI.')