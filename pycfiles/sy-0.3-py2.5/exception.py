# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sy/exception.py
# Compiled at: 2010-12-14 04:34:03
"""
sy.exception
------------
   :synopsis: Exceptions used by the library

.. moduleauthor: Paul Diaconescu <p@afajl.com>
"""

class Error(Exception):
    """ Base exception for the sy  """

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self)

    def __unicode__(self):
        return self.msg

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self))

    __str__ = __unicode__