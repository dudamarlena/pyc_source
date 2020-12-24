# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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