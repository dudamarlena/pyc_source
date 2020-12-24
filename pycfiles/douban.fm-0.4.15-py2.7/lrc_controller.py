# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/controller/lrc_controller.py
# Compiled at: 2016-06-22 17:23:26
import logging
from doubanfm.views import lrc_view
from doubanfm.controller.main_controller import MainController
logger = logging.getLogger('doubanfm')

class LrcController(MainController):
    """
    按键控制
    """

    def __init__(self, player, data, queue):
        self.player = player
        self.data = data
        self.keys = data.keys
        self.quit = False
        self.rate_times = 0
        self.queue = queue
        self._bind_view()

    def _bind_view(self):
        self.view = lrc_view.Lrc(self.data)

    def _watchdog_queue(self):
        u"""
        从queue里取出字符执行命令
        """
        while not self.quit:
            k = self.queue.get()
            if k == self.keys['QUIT']:
                self.quit = True
                self.switch_queue.put('main')
            elif k == self.keys['BYE']:
                self.data.bye()
                self.player.start_queue(self)
            elif k == self.keys['LOOP']:
                self.set_loop()
            elif k == self.keys['RATE']:
                self.set_rate()
            elif k == self.keys['OPENURL']:
                self.set_url()
            elif k == self.keys['HIGH']:
                self.set_high()
            elif k == self.keys['PAUSE']:
                self.set_pause()
            elif k == self.keys['NEXT']:
                self.player.next()
            elif k == '-' or k == '_':
                self.set_volume(-1)
            elif k == '+' or k == '=':
                self.set_volume(1)
            elif k == self.keys['MUTE']:
                self.set_mute()
            elif k in ('1', '2', '3', '4'):
                self.set_theme(k)
            elif k == self.keys['UP'] or k == 'B':
                self.up()
            elif k == self.keys['DOWN'] or k == 'A':
                self.down()