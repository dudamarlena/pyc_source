# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/userschema/interfaces.py
# Compiled at: 2007-01-23 10:51:04
""" userschema.interfaces

$Id: interfaces.py,v 1.1.1.1 2007/01/23 15:51:04 tseaver Exp $
"""
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('zope')
from zope.schema import Field
from zope.schema import TextLine
from zope.schema._field import Set
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ISet

class IChoiceSet(ISet):
    __module__ = __name__
    value_type = Field(title=_('Value Type'), description=_('Must be an IChoice field whose vocabulary is a simple string list.'))
    default = Set(value_type=TextLine(), title=_('Default'), description=_('Default values for the choice set.'))