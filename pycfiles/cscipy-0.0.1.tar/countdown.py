# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/countdown/interfaces/countdown.py
# Compiled at: 2009-09-15 11:10:09
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.countdown import countdownMessageFactory as _

class Icountdown(Interface):
    """Count down to a date"""
    __module__ = __name__
    tweetschedule = schema.List(title=_('schedules tweets for today:'), required=False, description=_('Field description'))
    tpass = schema.TextLine(title=_('Twitter Password'), required=False, description=_('password'))
    tuser = schema.TextLine(title=_('New Field'), required=False, description=_('username'))
    debugmode = schema.Bool(title=_('New Field'), required=False, description=_('debug mode to create schedule every time'))
    abovecount = schema.SourceText(title=_('Text Above count'), required=True, description=_('enter <daystogo> to include the days left'))
    target = schema.TextLine(title=_('Target Date and Time'), required=True, description=_('dd/mm/yy HH:MM'))