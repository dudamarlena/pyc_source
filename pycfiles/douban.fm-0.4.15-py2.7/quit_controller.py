# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/controller/quit_controller.py
# Compiled at: 2016-06-22 17:23:26
import logging
from doubanfm.views import quit_view
from doubanfm.controller.lrc_controller import LrcController
logger = logging.getLogger('doubanfm')

class QuitController(LrcController):
    """
    按键控制
    """

    def __init__(self, player, data, queue):
        super(QuitController, self).__init__(player, data, queue)

    def _bind_view(self):
        self.view = quit_view.Quit(self.data)

    def _watchdog_queue(self):
        u"""
        从queue里取出字符执行命令
        """
        k = self.queue.get()
        if k == self.keys['QUIT']:
            self.player.quit()
            self.switch_queue.put('quit_quit')
        else:
            self.switch_queue.put('main')
        self.quit = True