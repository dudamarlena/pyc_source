# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/autoself/testmeta.py
# Compiled at: 2007-09-17 22:11:18
import autoself
__metaclass__ = autoself.autoself

class Test1:
    __module__ = __name__

    def __init__(color, size):
        self.color = color
        self.size = size

    def show():
        print 'I am a ' + self.size + ', ' + self.color + ' thing'

    def myclass():
        return cls


t = Test1('blue', 'big')
if not t.color == 'blue':
    raise ValueError()
if not t.size == 'big':
    raise ValueError()
if not t.myclass() == Test1:
    raise ValueError()