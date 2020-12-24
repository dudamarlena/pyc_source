# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/language.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.iso639 import ISO639_2

class Language:
    __module__ = __name__

    def __init__(self, code):
        code = str(code)
        if code not in ISO639_2:
            raise ValueError('Invalid language code: %r' % code)
        self.code = code

    def __cmp__(self, other):
        if other.__class__ != Language:
            return 1
        return cmp(self.code, other.code)

    def __unicode__(self):
        return ISO639_2[self.code]

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return "<Language '%s', code=%r>" % (unicode(self), self.code)