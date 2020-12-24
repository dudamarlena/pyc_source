# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/winter_project/plugins/UIConfig/UIConfig.py
# Compiled at: 2011-04-27 01:28:05
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from winterstone.base import WinterPlugin

class UIConfig(WinterPlugin):

    def activate(self):
        self.api.toolBar.setIconSize(QSize(self.config.options.tbicon_size, self.config.options.tbicon_size))
        self.api.toolBar.setMovable(self.config.options.tb_movable)
        self.api.ex('resize')(self.config.options.width, self.config.options.height)
        self.api.info('%s: start' % self.name)
        return WinterPlugin.activate(self)

    def deactivate(self):
        self.api.info('%s: stop' % self.name)
        return WinterPlugin.deactivate(self)