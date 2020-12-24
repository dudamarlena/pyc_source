# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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