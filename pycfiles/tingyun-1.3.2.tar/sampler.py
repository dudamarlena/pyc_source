# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/sampler/sampler.py
# Compiled at: 2016-06-30 06:13:10
"""this module define the sampler controller for sampler the data.
"""
import logging
console = logging.getLogger(__name__)

class SamplerController(object):
    """
    """

    def __init__(self, sampler, *args):
        """
        :param sampler:
        :param args:
        :return:
        """
        self.name = args[0]
        self.sampler = sampler
        self.args = args
        self.instance = None
        return

    def start(self):
        """
        :return:
        """
        if self.instance is None:
            self.instance = self.sampler(self.args)
        if hasattr(self.instance, 'start'):
            self.instance.start()
            return
        else:
            return

    def stop(self):
        if hasattr(self.instance, 'stop'):
            self.instance.stop()
        else:
            self.instance = None
        return

    def metrics(self, *args):
        if self.instance is None:
            return []
        else:
            return self.instance(*args)