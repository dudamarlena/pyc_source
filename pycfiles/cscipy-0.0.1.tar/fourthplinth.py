# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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