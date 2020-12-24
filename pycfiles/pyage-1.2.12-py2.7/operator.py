# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/operator.py
# Compiled at: 2015-12-21 17:12:58


class Operator(object):

    def __init__(self, type=None):
        super(Operator, self).__init__()
        self.required_type = type

    def process(self, population):
        raise NotImplementedError()

    def is_compatible(self, operator):
        return self.required_type == None or operator.required_type == None or operator.required_type == self.required_type