# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/metaconfigure.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.component import provideUtility
from interfaces import IAdverlet
from adverlet import Adverlet

def registerAdverlet(_context, name, description=None, default=None, wysiwyg=True):
    adverlet = Adverlet()
    adverlet.__name__ = name
    adverlet.description = description
    adverlet.default = default
    adverlet.wysiwyg = wysiwyg
    adverlet.newlines = not wysiwyg
    provideUtility(adverlet, IAdverlet, name=name)