# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/Documents/projects/poolhub/poolhub/threads/threader.py
# Compiled at: 2017-04-11 07:01:42
# Size of source mod 2**32: 838 bytes
import threading

class Thread(threading.Thread):

    def __init__(self, *args, **kwargs):
        self.parent = threading.current_thread()
        self.status = 'Started'
        self.exception = None
        super(Thread, self).__init__(*args, **kwargs)

    def run(self):
        """just like threading.py def run() but with an except to capture exception"""
        try:
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                self.exception = e.__class__.__name__
                raise

        finally:
            del self._target
            del self._args
            del self._kwargs


def monkey_patch_threads():
    threading.Thread = Thread