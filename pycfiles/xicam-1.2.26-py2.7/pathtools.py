# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\pathtools.py
# Compiled at: 2018-08-27 17:21:06
import os, string
from PySide import QtGui
import sys, re, msg
from appdirs import *
user_config_dir = user_config_dir('xicam')

def similarframe(path, N):
    """
    Get the file path N ahead (or behind) the provided path frame.
    """
    try:
        expr = '(?<=_)[\\d]+(?=[_.])'
        frame = re.search(expr, os.path.basename(path)).group(0)
        leadingzeroslen = len(frame)
        framenum = int(frame)
        prevframenum = int(framenum) + N
        prevframenum = ('{:0>{}}').format(prevframenum, leadingzeroslen)
        return re.sub(expr, prevframenum, path)
    except ValueError:
        msg.logMessage('No earlier frame found for ' + path + ' with ' + N, msg.ERROR)
        return

    return


def path2nexus(path):
    """
    Get the path to corresponding nexus file
    """
    return os.path.splitext(path)[0] + '.nxs'


def getRoot():
    if sys.platform == 'linux2':
        return '/'
    else:
        if sys.platform == 'darwin':
            return '/Volumes'
        if sys.platform == 'win32':
            return QtGui.QFileSystemModel().myComputer()
        print 'WARNING: Unknown platform "' + sys.platform + '"'
        return