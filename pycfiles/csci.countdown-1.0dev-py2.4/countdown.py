# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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