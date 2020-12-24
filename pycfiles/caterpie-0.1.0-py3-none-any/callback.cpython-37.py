# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/callback.py
# Compiled at: 2019-08-07 08:55:31
# Size of source mod 2**32: 1736 bytes
import time, logging

class Callback:
    COMMIT_KAFKA_MESSAGE = 0

    def __init__(self, target=None, args=None, kwargs=None, mode=None):
        self.target = target
        self.mode = mode
        self.args = args
        self.kwargs = kwargs

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if value is None:
            self._args = []
        elif isinstance(value, list):
            self._args = value
        else:
            self._args = [
             value]

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if value is None:
            self._kwargs = {}
        else:
            self._kwargs = value

    def __bool__(self):
        if self.target != None:
            return True
        return False

    def execute(self):
        if not self:
            logging.error('callback without target.')
            return
        if self.mode == self.COMMIT_KAFKA_MESSAGE:
            self._execute_kafka_commit()
            return
        self._execute()

    def _execute(self):
        (self.target)(*self._args, **self._kwargs)

    def _execute_kafka_commit(self):
        done = False
        attempts = 0
        while not done:
            try:
                self._execute()
                done = True
            except Exception as e:
                try:
                    if 'UNKNOWN_MEMBER_ID' in str(e):
                        raise Exception('Cannot commit a message (timeout).')
                    logging.exception(f"Trying to commit a message ({attempts})...")
                    attempts += 1
                    time.sleep(1)
                finally:
                    e = None
                    del e