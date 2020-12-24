# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/sources/dbexplorer.py
# Compiled at: 2015-10-11 07:17:06
import logging, xml.etree.ElementTree as ET
from urlparse import urlparse
from os.path import isfile
from dbmanagr.sources.source import Source
logger = logging.getLogger(__name__)

class DBExplorerSource(Source):

    def __init__(self, driver, file_, scheme, con_creator):
        Source.__init__(self)
        self.driver = driver
        self.file = file_
        self.scheme = scheme
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.warn('File %r does not exist (this file: %r)', self.file, realpath(__file__))
            return self._connections
        else:
            if not self._connections:
                try:
                    tree = ET.parse(self.file)
                except Exception as e:
                    logger.warn('Error parsing dbExplorer config file: %s', e.message)
                    return []

                root = tree.getroot()
                for c in root.iter('connection'):
                    url = urlparse(c.find('url').text.replace('jdbc:', ''))
                    if url.scheme == self.scheme:
                        host = url.netloc.split(':')[0]
                        port = 3306
                        database = '*'
                        usernode = c.find('user')
                        if usernode is not None:
                            user = usernode.text
                        else:
                            user = None
                        passwordnode = c.find('password')
                        if passwordnode is not None:
                            password = passwordnode.text
                        else:
                            password = None
                        connection = self.con_creator(self.driver, host, port, database, user, password)
                        self._connections.append(connection)

            return self._connections