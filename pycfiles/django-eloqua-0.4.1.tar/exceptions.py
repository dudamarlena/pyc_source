# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/lib/python2.7/site-packages/eloqua/exceptions.py
# Compiled at: 2013-03-01 07:44:52


class ObjectNotFound(Exception):

    def __init__(self, key=None):
        msg = 'Object could not be found by the given key: %s' % key
        super(ObjectNotFound, self).__init__(msg)