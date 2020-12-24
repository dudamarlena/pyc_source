# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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