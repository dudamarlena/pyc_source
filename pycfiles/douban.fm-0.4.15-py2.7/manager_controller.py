# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/controller/manager_controller.py
# Compiled at: 2016-06-22 17:23:26
"""
暂时没用
"""
import logging
from threading import Thread
from doubanfm.views import manager_view
logger = logging.getLogger('doubanfm')

class ManagerController(object):
    """
    按键控制
    """

    def __init__(self, player, data, queue):
        self.player = player
        self.data = data
        self._bind_view()
        self.queue = queue

    def _bind_view(self):
        self.view = manager_view.Manager(self.data)

    def run(self, switch_queue):
        u"""
        每个controller需要提供run方法, 来提供启动
        """
        self.switch_queue = switch_queue
        self.quit = False
        Thread(target=self._watchdog_queue).start()
        Thread(target=self._watchdog_time).start()

    def _watchdog_time(self):
        u"""
        标题时间显示
        """
        while not self.quit:
            self.data.time = self.player.time_pos
            self.view.display()
            time.sleep(1)

    def _watchdog_queue(self):
        u"""
        从queue里取出字符执行命令
        """
        while not self.quit:
            k = self.queue.get()
            if k == 'q':
                self.quit = True
                self.switch_queue.put('main')