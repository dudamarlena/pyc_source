# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: avython/download/driver.py
# Compiled at: 2017-02-05 16:31:12
from abc import ABCMeta, abstractmethod
import logging, os, subprocess
logging.basicConfig(filename='log.log', level=logging.DEBUG)
log = logging.getLogger('avython')

class AbstractDriver(object):
    __metaclass__ = ABCMeta
    command_to_get = None

    @abstractmethod
    def download(self, remote_dir, local_dir):
        pass


class BaseDriver(AbstractDriver):

    def download(self, remote_dir, local_dir):
        log.info(('Start download {}...').format(remote_dir))
        process = subprocess.Popen(self.command_to_get.format(remote_dir, local_dir), shell=True, stdout=subprocess.PIPE)
        process.wait()
        log.info(('Finish download {} to ').format(remote_dir, local_dir))
        return os.path.isfile(local_dir) or os.path.isdir(local_dir)