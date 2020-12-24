# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/controller/help_controller.py
# Compiled at: 2016-06-22 17:23:26
import logging
from doubanfm.views import help_view
from doubanfm.controller.lrc_controller import LrcController
logger = logging.getLogger('doubanfm')

class HelpController(LrcController):
    """
    按键控制
    """

    def __init__(self, player, data, queue):
        super(HelpController, self).__init__(player, data, queue)
        self.view = help_view.Help(self.data)

    def _bind_view(self):
        self.view = help_view.Help(self.data)