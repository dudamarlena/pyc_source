# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/config.py
# Compiled at: 2013-07-12 11:47:33
"""
module that provides configuration file functionality 
"""
import logging, abc
from ConfigParser import SafeConfigParser
logging.getLogger(__name__)
log = logging.getLogger()

class Configurable(object):
    """abstract class with factory method from a config file

    to subclass, need to define

    _types: types for properties
    _section: section on the confifg file"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.cfg = SafeConfigParser()
        if not len(self.cfg.read([path])):
            raise ValueError('cannot load %s' % path)
        log.info('loaded settings from %s', path)
        self._config_check()

    def getAttr(self, attr):
        return self.cfg.get(self._section, attr)

    def setAttr(self, attr, val):
        return self.cfg.set(self._section, attr, val)

    @abc.abstractmethod
    def _config_check(self):
        """check as much as you can that values of params make sense"""
        raise NotImplemented