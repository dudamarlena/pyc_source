# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\mock.py
# Compiled at: 2011-10-24 15:11:22


class MockDroopy(object):

    def __init__(self, text, attributes, operators):
        self.text = text
        self.attributes = attributes
        self.operators = operators

    def __getattr__(self, attr):
        if attr in self.attributes.keys():
            return self.attributes[attr]
        if attr in self.operators.keys():

            def wrapper(*args):
                return self.operators[attr]

            return wrapper


def _(text, attributes, operators):
    return MockDroopy(text, attributes, operators)