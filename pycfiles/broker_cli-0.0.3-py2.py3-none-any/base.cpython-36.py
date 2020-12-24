# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/diogo.munaro/workspace/brokerpackager/brokerpackager/managers/base.py
# Compiled at: 2017-08-16 14:21:12
# Size of source mod 2**32: 858 bytes
import logging

class BaseManager(object):

    def __init__(self, log_file=''):
        self.logger = logging.getLogger('broker-packager')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        if log_file:
            hdlr = logging.FileHandler(log_file)
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.WARNING)

    def install(self, package, version, git, *args):
        raise NotImplementedError

    def install_list(self, package_list, extra_config={}):
        raise NotImplementedError

    def log_install(self, package, *args):
        self.logger.info('Installing {} with args: "{}"'.format(package, ', '.join(map(str, args))))