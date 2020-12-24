# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/logger.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 787 bytes


class Logger:

    def __init__(self, keys, writer, logging_steps, local_rank):
        self.d = {key:list() for key in keys}
        self.step = {key:0 for key in keys}
        self.writer = writer
        self.logging_steps = logging_steps
        self.local_rank = local_rank

    def log(self, **kwargs):
        for key in kwargs.keys():
            self.d[key].append(kwargs[key])
            if len(self.d[key]) % self.logging_steps == 0:
                if self.local_rank <= 0:
                    self.d[key] = [k for k in self.d[key] if k is not None]
                    if len(self.d[key]) > 0:
                        self.writer.add_scalar(key, sum(self.d[key]) / len(self.d[key]), self.step[key])
                self.step[key] += 1
                self.d[key] = list()