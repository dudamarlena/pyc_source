# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/storage_service.py
# Compiled at: 2017-03-29 00:21:31
from abc import ABCMeta, abstractmethod

class StorageService(object):
    """ The abstract class for Storage Services. you must impl following functions.

    `path` is `/path/to/your/object`
    `localpath` is full local path.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self, path, localpath):
        """ downloads object from service, and saves to local disk

        :param path: path on Services
        :param localpath: local path on Disk
        :return: success or failure
        """
        pass

    @abstractmethod
    def upload(self, path, localpath):
        """ uploads local file to service

        :param path: path on Service
        :param localpath: local path on Disk
        :return: success or failure
        """
        pass

    @abstractmethod
    def exists(self, path):
        """ query for existence of object

        :param path: path on Service
        :return:
        """
        pass

    @abstractmethod
    def list(self):
        """
        :return: iterator for 'a/b/c.txt', 'a/b/d.txt', not starts with '/'
        """
        pass