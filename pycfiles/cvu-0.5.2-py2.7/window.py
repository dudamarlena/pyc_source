# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/window.py
# Compiled at: 2014-01-30 16:42:58
from traits.api import Handler, Instance
from traitsui.api import UIInfo

class ReconstructableWindow(Handler):
    info = Instance(UIInfo)

    def init_info(self, info):
        self.info = info

    def reconstruct(self, info):
        self.info.ui.dispose()
        self.info.object.edit_traits()