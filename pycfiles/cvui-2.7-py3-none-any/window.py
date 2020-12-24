# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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