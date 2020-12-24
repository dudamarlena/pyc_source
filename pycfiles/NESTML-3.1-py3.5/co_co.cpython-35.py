# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1600 bytes
from abc import ABCMeta, abstractmethod

class CoCo:
    __doc__ = '\n    This class represents an abstract super-class for all concrete context conditions to check. All concrete CoCos\n    have to inherit from this class. Hereby, the description can be used to state the condition the CoCo checks.\n    Attributes:\n        description type(str): This field can be used to give a short description regarding the properties which\n                                are checked by this coco.\n    '
    __metaclass__ = ABCMeta
    description = None

    @abstractmethod
    def check_co_co(self, node):
        """
        This is an abstract method which should be implemented by all concrete cocos.
        :param node: a single neuron instance on which the coco will be checked.
        :type node: ast_neuron
        :return: True, if CoCo holds, otherwise False.
        :rtype: bool
        """
        pass