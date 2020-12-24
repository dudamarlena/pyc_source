# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/comment/schema.py
# Compiled at: 2012-06-26 16:37:02
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import IText
from zope.interface import implements
from zope.schema import Text

class ICommentField(IText):
    """Interface field for comments body"""
    pass


class CommentField(Text):
    implements(ICommentField)