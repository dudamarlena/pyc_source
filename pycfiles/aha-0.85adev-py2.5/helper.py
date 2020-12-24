# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/helper.py
# Compiled at: 2010-10-22 05:16:12
""" helper module """
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import re, new

class helpers(object):

    @classmethod
    def extend(cls, name, func):
        """
        A method to extend helper function
        """
        if name not in cls.__dict__:
            setattr(cls, name, staticmethod(func))


def get_helpers():
    return helpers


hlps = dir()
for h in hlps:
    if not re.match('^__', h):
        method = eval('%s' % h)
        if callable(method):
            helpers.extend(h, method)