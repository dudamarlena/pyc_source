# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/animation_threading.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2349 bytes
import threading, time
from ..util import log

class AnimationThreading:
    __doc__ = '\n    AnimationThreading handles threading - and eventually multiprocessing - for\n    Animation.\n    '

    def __init__(self, runner, run):
        self.runner = runner
        self.run = run
        self.stop_event = threading.Event()
        self.thread = None
        self.frame_overrun = False
        self.sleep = time.sleep

    def set_project(self, project):
        self.sleep = project.clock.sleep

    def join(self, timeout=None):
        self.thread and self.thread.join(timeout)

    def is_alive(self):
        return self.thread and self.thread.is_alive()

    def cleanup(self):
        self.stop_event.set()

    def target(self):
        is_main = threading.current_thread() is threading.main_thread()
        log.debug('Animation starts on %s thread', 'main' if is_main else 'new')
        self.run()
        log.debug('Animation complete')

    def wait(self, wait_time, timestamps):
        if not wait_time:
            return
        else:
            elapsed_time = timestamps[(-1)] - timestamps[0]
            if elapsed_time >= wait_time + 0.001:
                logger = log.frame if self.frame_overrun else log.warning
                logger('Frame-time of %dms set, but took %dms', 1000 * wait_time, 1000 * elapsed_time)
                self.frame_overrun = True
            else:
                if self.runner.threaded:
                    self.stop_event.wait(wait_time - elapsed_time)
                else:
                    self.sleep(wait_time - elapsed_time)

    def start(self):
        self.stop_event.clear()

        def start_thread(target):
            self.thread = threading.Thread(target=target, daemon=True)
            self.thread.start()

        if self.runner.main:
            if self.runner.threaded:
                start_thread(self.target)
                self.runner.main()
            else:
                start_thread(self.runner.main)
                self.target()
        else:
            if self.runner.threaded:
                start_thread(self.target)
            else:
                self.target()
        self.thread and self.runner.main and self.thread.join()

    def stopped(self):
        return not self.is_alive()