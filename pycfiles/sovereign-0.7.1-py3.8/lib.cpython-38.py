# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/sources/lib.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 809 bytes
"""
Source abstract class
---------------------
This class can be subclassed, installed as an entry point, and then
used via configuration.

`todo entry point install guide`
"""
import abc
from sovereign.logs import LOG
from sovereign.schemas import Instances

class Source(metaclass=abc.ABCMeta):

    def __init__(self, config: dict, scope: str):
        """
        :param config: arbitrary configuration which can be used by the subclass
        """
        self.logger = LOG
        self.config = config
        self.scope = scope

    def setup(self):
        """
        Optional method which is invoked prior to the Source running self.get()
        """
        pass

    @abc.abstractmethod
    def get(self) -> Instances:
        """
        Required method to retrieve data from an arbitrary source
        """
        pass