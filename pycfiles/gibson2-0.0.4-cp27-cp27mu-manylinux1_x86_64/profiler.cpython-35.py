# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fei/Development/gibsonv2/gibson2/core/render/profiler.py
# Compiled at: 2020-04-03 01:28:40
# Size of source mod 2**32: 1613 bytes
""" A simple profiler for logging """
import logging, time

class Profiler(object):

    def __init__(self, name, logger=None, level=logging.INFO, enable=True):
        self.name = name
        self.logger = logger
        self.level = level
        self.enable = enable

    def step(self, name):
        """ Returns the duration and stepname since last step/start """
        duration = self.summarize_step(start=self.step_start, step_name=name, level=self.level)
        now = time.time()
        self.step_start = now
        return duration

    def __enter__(self):
        self.start = time.time()
        self.step_start = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.enable:
            self.summarize_step(self.start)

    def summarize_step(self, start, level=None):
        duration = time.time() - start
        if self.logger:
            level = level or self.level
            self.logger.log(self.level, '{name}: {fps:.2f} fps, {duration:.5f} seconds'.format(name=self.name, fps=1 / duration, duration=duration))
        else:
            print('{name}: {fps:.2f} fps, {duration:.5f} seconds'.format(name=self.name, fps=1 / duration, duration=duration))
        return duration