# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/message_generator/message_generator.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 266 bytes
from abc import ABC, abstractmethod

class MessageGenerator(ABC):

    @abstractmethod
    def get_message(self, diff: str) -> str:
        """
        Generates a commit message from the given diff string
        :param diff: diff of the file to commit
        """
        pass