# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/channelsmtp/interfaces.py
# Compiled at: 2008-10-27 17:46:10
"""Interfaces for the Zope 3 based channelsmtp package

$Id: interfaces.py 35341 2008-10-21 09:09:24Z anatoly $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 35341 $'
__date__ = '$Date: 2008-10-21 12:09:24 +0300 (Tue, 21 Oct 2008) $'
from zope.interface import Interface
from zope.schema import Choice, ASCIILine
from ks.channel.interfaces import IChannel
from ks.channelsmtp import _

class IChannelSMTP(IChannel):
    __module__ = __name__
    fromAddress = ASCIILine(title=_('"From" address'))
    bccAddress = ASCIILine(title=_('"BCC" addreses (use commas as splitter)'), required=False, default='')
    delivery = Choice(title=_('Mail Delivery Name'), vocabulary='Mail Delivery Names')

    def sendTo(addresses, **kw):
        """Send emails to specified addressess instead of configured ones"""
        pass