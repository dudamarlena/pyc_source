# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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