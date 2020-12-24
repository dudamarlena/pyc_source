# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/sources/anypass.py
# Compiled at: 2015-10-11 07:17:06
import logging
from os.path import isfile, abspath
from dbmanagr.sources.source import Source
logger = logging.getLogger(__name__)

class AnyPassSource(Source):

    def __init__(self, driver, file_, con_creator):
        Source.__init__(self)
        self.driver = driver
        self.file = file_
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.info('File %r does not exist (this file: %r)', self.file, realpath(__file__))
            return self._connections
        if not self._connections:
            with open(self.file) as (f):
                anypass = f.readlines()
            for line in anypass:
                connection = self.con_creator(self.driver, *line.strip().split(':'))
                self._connections.append(connection)

        logger.debug('Connections: %s', self._connections)
        return self._connections


class AnyFilePassSource(AnyPassSource):

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.info('File %r does not exist (this file: %r)', self.file, realpath(__file__))
            return self._connections
        else:
            if not self._connections:
                with open(self.file) as (f):
                    anypass = f.readlines()
                for line in anypass:
                    filepath = abspath(line.strip())
                    if isfile(filepath):
                        connection = self.con_creator(self.driver, None, None, filepath, None, None)
                        self._connections.append(connection)

            logger.debug('Connections: %s', self._connections)
            return self._connections