# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/willdo/interfaces.py
# Compiled at: 2008-04-22 18:15:36
from zope.interface import Interface
from zope.schema import List, TextLine, Bool, Date

class IDoItTomorrow(Interface):
    __module__ = __name__


class IWillDoList(Interface):
    __module__ = __name__
    day = Date(title='Day', description='Day that I will do the items on this list', required=True)
    closed = Bool(title='Closed', description='Is this a closed list?', default=False)
    tasks = List(title='Task list', description='List of tasks that I will do this day', required=False, value_type=TextLine(title='Task'))