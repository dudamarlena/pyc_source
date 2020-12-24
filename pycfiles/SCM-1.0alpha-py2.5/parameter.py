# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/parameter.py
# Compiled at: 2009-05-29 13:49:17


class Parameters(object):
    """ parameters for optimization
    """

    def __init__(self, name='', active=0, value=[], comment=''):
        self.name = name
        self.active = active
        self.value = value
        self.comment = comment

    def setValue(self, value):
        self.value = value

    def setActive(self, active):
        self.active = active

    def setComment(self, comment):
        self.comment = comment


if __name__ == '__main__':
    pass