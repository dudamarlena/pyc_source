# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/route.py
# Compiled at: 2019-12-01 22:29:38
# Size of source mod 2**32: 539 bytes


class Route:
    type = 'route'

    def __init__(self):
        self.type = 'route'
        self.data = {}

    def __iter__(self):
        yield (
         'type', self.type)
        yield ('data', self.type)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Route: {}'.format(self.data)

    def show(self):
        print(str(self.__dict__()).replace(', ', ',\n').replace('{', '{\n').replace('}', '\n}'))