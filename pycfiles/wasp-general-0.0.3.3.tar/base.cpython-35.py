# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/base.py
# Compiled at: 2017-06-28 10:27:57
# Size of source mod 2**32: 2205 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_type

class WTask(metaclass=ABCMeta):
    __doc__ = ' Basic task prototype. Must implement the only thing - to start\n\t'

    @abstractmethod
    def start(self):
        """ Start this task

                :return: None
                """
        raise NotImplementedError('This method is abstract')


class WStoppableTask(WTask):
    __doc__ = ' Task that can be stopped (graceful shutdown)\n\t'

    @abstractmethod
    def stop(self):
        """ Stop this task (graceful shutdown)

                :return: None
                """
        raise NotImplementedError('This method is abstract')


class WTerminatableTask(WStoppableTask):
    __doc__ = ' Task that can be terminated (rough shutdown)\n\t'

    @abstractmethod
    def terminate(self):
        """ Terminate this task (rough shutdown)

                :return: None
                """
        raise NotImplementedError('This method is abstract')


class WSyncTask(WStoppableTask, metaclass=ABCMeta):
    __doc__ = ' This class is some kind of declaration, that the following task is executed in foreground.\n\t'

    def __init__(self):
        WStoppableTask.__init__(self)

    def stop(self):
        """ Stop this task. This implementation does nothing.

                :return: None
                """
        pass