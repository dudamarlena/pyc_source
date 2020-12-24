# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/beans/JSONer.py
# Compiled at: 2018-02-02 06:38:50
import json
from abc import ABCMeta, abstractmethod

class JSONer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def as_dict(self):
        pass

    def json(self, pretty=False):
        if pretty:
            return json.dumps(self.as_dict(), indent=2, separators=(',', ':'))
        return json.dumps(self.as_dict(), separators=(',', ':'))