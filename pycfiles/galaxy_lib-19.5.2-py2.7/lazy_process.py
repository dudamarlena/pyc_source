# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/lazy_process.py
# Compiled at: 2018-04-20 03:19:42
import subprocess, threading, time

class LazyProcess(object):
    """ Abstraction describing a command line launching a service - probably
    as needed as functionality is accessed in Galaxy.
    """

    def __init__(self, command_and_args):
        self.command_and_args = command_and_args
        self.thread_lock = threading.Lock()
        self.allow_process_request = True
        self.process = None
        return

    def start_process(self):
        with self.thread_lock:
            if self.allow_process_request:
                self.allow_process_request = False
                t = threading.Thread(target=self.__start)
                t.daemon = True
                t.start()

    def __start(self):
        with self.thread_lock:
            self.process = subprocess.Popen(self.command_and_args, close_fds=True)

    def shutdown(self):
        with self.thread_lock:
            self.allow_process_request = False
        if self.running:
            self.process.terminate()
            time.sleep(0.01)
            if self.running:
                self.process.kill()

    @property
    def running(self):
        return self.process and not self.process.poll()


class NoOpLazyProcess(object):
    """ LazyProcess abstraction meant to describe potentially optional
    services, in those cases where one is not configured or valid, this
    class can be used in place of LazyProcess.
    """

    def start_process(self):
        pass

    def shutdown(self):
        pass

    @property
    def running(self):
        return False