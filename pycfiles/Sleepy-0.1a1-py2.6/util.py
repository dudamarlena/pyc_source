# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/util.py
# Compiled at: 2010-12-16 02:11:51
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class MakoDef(object):

    def __init__(self, template, deff, kwargs):
        self.template = template
        self.deff = deff
        self.kwargs = kwargs