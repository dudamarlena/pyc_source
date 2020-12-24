# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/update.py
# Compiled at: 2011-12-14 03:45:13
import tyrs, time, logging, threading

class UpdateThread(threading.Thread):
    """
    The only thread that update all timelines
    """

    def __init__(self):
        self.interface = tyrs.container['interface']
        self.conf = tyrs.container['conf']
        self.api = tyrs.container['api']
        threading.Thread.__init__(self, target=self.run)
        self._stopevent = threading.Event()

    def run(self):
        self.update_timeline()
        logging.info('Thread started')
        for i in range(self.conf.params['refresh'] * 60):
            time.sleep(1)
            if self._stopevent.isSet() or self.interface.stoped:
                logging.info('Thread forced to stop')
                return

        self.start_new_thread()
        logging.info('Thread stoped')
        self._Thread__stop()

    def stop(self):
        self._stopevent.set()

    def start_new_thread(self):
        update = UpdateThread()
        update.start()

    def update_timeline(self):
        while not self.interface.loop.screen._started:
            time.sleep(1)

        timeline = ('home', 'mentions', 'direct')
        for t in timeline:
            self.api.update_timeline(t)

        self.interface.display_timeline()
        self.interface.redraw_screen()