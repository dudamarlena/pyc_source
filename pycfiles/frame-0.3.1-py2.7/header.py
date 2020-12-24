# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/header.py
# Compiled at: 2013-08-10 12:52:27


class Header(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return '%s: %s' % (self.key, self.value)

    def __repr__(self):
        return '<Header(%s)>' % str(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other.key
        else:
            return self is other