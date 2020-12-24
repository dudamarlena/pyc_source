# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/muatik/dahi/dahi/matchers/abstracts.py
# Compiled at: 2016-07-22 09:14:22
import abc

class AbstractMatcher(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def match(self, text):
        """
        matches given text

        :param text:
        :return:
        """
        raise NotImplementedError