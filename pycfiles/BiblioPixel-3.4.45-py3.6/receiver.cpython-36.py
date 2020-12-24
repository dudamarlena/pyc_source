# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/receiver.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 495 bytes
import abc

class Receiver(abc.ABC):
    __doc__ = '\n    Several classes receive data and route it to a target, and this is their\n    base class, mainly for documentation.\n\n    Receivers must have two methods, `set_project` and `receive`.  `set_project`\n    must be called exactly once for each Receiver, and this must be before\n    `receive` is ever.\n    '

    @abc.abstractmethod
    def set_project(self, project):
        pass

    @abc.abstractmethod
    def receive(self, values):
        pass