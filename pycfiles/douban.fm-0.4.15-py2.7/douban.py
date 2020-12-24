# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/douban.py
# Compiled at: 2016-06-22 17:23:26
"""
豆瓣fm主程序
"""
from threading import Thread
import subprocess, logging, Queue, sys, os
from doubanfm import data
from doubanfm import getch
from doubanfm.player import MPlayer
from doubanfm.controller.main_controller import MainController
from doubanfm.controller.lrc_controller import LrcController
from doubanfm.controller.help_controller import HelpController
from doubanfm.controller.manager_controller import ManagerController
from doubanfm.controller.quit_controller import QuitController
reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(format='%(asctime)s - [%(process)d]%(filename)s:%(lineno)d - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%I:%S', filename=os.path.expanduser('~/.doubanfm.log'), level=logging.INFO)
logger = logging.getLogger('doubanfm')
logger.setLevel(logging.INFO)

class Router(object):
    """
    管理view之间的切换
    """

    def __init__(self):
        self.player = MPlayer()
        self.data = data.Data()
        self.quit_quit = False
        self.current_controller = None
        self.switch_queue = Queue.Queue(0)
        self.key_queue = Queue.Queue(0)
        self.view_control_map = {'main': MainController(self.player, self.data, self.key_queue), 
           'lrc': LrcController(self.player, self.data, self.key_queue), 
           'help': HelpController(self.player, self.data, self.key_queue), 
           'manager': ManagerController(self.player, self.data, self.key_queue), 
           'quit': QuitController(self.player, self.data, self.key_queue)}
        Thread(target=self._watchdog_switch).start()
        Thread(target=self._watchdog_key).start()
        return

    def _watchdog_switch(self):
        u"""
        切换页面线程
        """
        self.current_controller = self.view_control_map['main']
        self.current_controller.run(self.switch_queue)
        while not self.quit_quit:
            key = self.switch_queue.get()
            if key == 'quit_quit':
                self.quit_quit = True
            else:
                self.current_controller = self.view_control_map[key]
                self.current_controller.run(self.switch_queue)

        self.quit()
        os._exit(0)

    def quit(self):
        self.data.save()
        subprocess.call('echo -e "\x1b[?25h";clear', shell=True)

    def _watchdog_key(self):
        u"""
        接受按键, 存入queue
        """
        while True:
            k = getch.getch()
            self.key_queue.put(k)


def main():
    router = Router()
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def index():
        router.key_queue.put(request.form['ch'])
        return 'OK'

    app.run()


if __name__ == '__main__':
    main()