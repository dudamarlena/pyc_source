# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/signals.py
# Compiled at: 2016-06-01 06:08:22
# Size of source mod 2**32: 635 bytes
import logging
logger = logging.getLogger(__name__)

def object_on_pre_save(sender, instance, **kwargs):
    from .manager import Manager
    man = Manager()
    man.start(sender, instance, **kwargs)


class SignalBlocker(object):
    __doc__ = '\n    Class used to block the models signals in certains cases\n    '

    def __init__(self, signal):
        self.signal = signal
        self.receivers = signal.receivers

    def __enter__(self, *args, **kwargs):
        self.signal.receivers = []

    def __exit__(self, *args, **kwargs):
        self.signal.receivers = self.receivers