# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/subscribers.py
# Compiled at: 2006-12-07 13:02:03
from zope.component import handle

def redirectShortcutObjectEvents(object, event):
    handle(object.target, event)