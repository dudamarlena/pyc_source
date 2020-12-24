# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/sources/navicat.py
# Compiled at: 2015-10-11 07:17:06
import logging
from plistlib import readPlist
from os.path import isfile
from dbmanagr.sources.source import Source
logger = logging.getLogger(__name__)

class NavicatSource(Source):

    def __init__(self, uri, file_, key, con_creator):
        Source.__init__(self)
        self.uri = uri
        self.file = file_
        self.key = key
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.warn('File %r does not exist (this file: %r)', self.file, realpath(__file__))
            return self._connections
        else:
            if not self._connections:
                plist = readPlist(self.file)
                for _, v in plist[self.key]['servers'].items():
                    connection = self.con_creator(self.uri, None, None, v['dbfilename'], None, None)
                    self._connections.append(connection)

            return self._connections