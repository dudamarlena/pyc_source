# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/fourthplinth/interfaces/fourthplinth.py
# Compiled at: 2009-09-04 08:59:29
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.fourthplinth import fourthplinthMessageFactory as _

class Ifourthplinth(Interface):
    """Fourth Plinth"""
    __module__ = __name__
    debugmode = schema.Bool(title=_('Debug Mode'), required=False, description=_('enter debug mode'))
    tschedule = schema.Text(title=_('Generated schedule for today'), required=False, description=_('Field description'))
    tpassword = schema.TextLine(title=_('Twitter Password'), required=True, description=_('Password'))
    tusername = schema.TextLine(title=_('New Field'), required=False, description=_('Field description'))