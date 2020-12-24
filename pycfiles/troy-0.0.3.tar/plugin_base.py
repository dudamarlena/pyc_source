# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/plugin_base.py
# Compiled at: 2014-02-24 20:40:00
from troy.constants import *
import troy

class PluginBase(object):

    def __init__(self, description):
        self.description = description
        self.type = '%(type)s' % description
        self.name = '%(name)s' % description
        self.longname = '%(type)s_%(name)s' % description
        self.config_path = '%(type)s:%(name)s' % description

    def init_plugin(self, session, scope):
        self.session = session
        self.troy_cfg = session.get_config()
        self.cfg = session.get_config('%s:%s' % (scope, self.config_path))
        troy._logger.info('init plugin %s' % self.longname)
        self.init()

    def init(self):
        pass