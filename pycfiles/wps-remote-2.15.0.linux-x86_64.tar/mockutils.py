# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/mockutils.py
# Compiled at: 2016-02-23 09:09:22
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import os

class FileLikeObjectMock(object):

    def __init__(self, lines, linesep='\n'):
        if type(lines) is list:
            self._lines = lines
        else:
            self._lines = lines.split(linesep)
            self._lines = map(lambda l: l.strip(), self._lines)
        self._lp = 0

    def readline(self):
        if self._lp - 1 >= len(self._lines):
            return ''
        else:
            self._lp += 1
            return self._lines[(self._lp - 1)]