# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/channelsmtp/channelsmtp.py
# Compiled at: 2008-10-27 17:53:09
"""Channel class for the Zope 3 based channel package

$Id: channelsmtp.py 35341 2008-10-21 09:09:24Z anatoly $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 35341 $'
__date__ = '$Date: 2008-10-21 12:09:24 +0300 (Tue, 21 Oct 2008) $'
from persistent import Persistent
from zope.component import getUtility
from zope.interface import implements
from zope.app.container.contained import Contained
from zope.sendmail.interfaces import IMailDelivery
from ks.lib.mailtemplate import mailtemplate
from ks.mailersmtp.interfaces import IMailerSMTP
from interfaces import IChannelSMTP

class ChannelSMTP(Persistent, Contained):
    __module__ = __name__
    implements(IChannelSMTP)
    addresses = ()
    delivery = None
    fromAddress = None
    bccAddress = None

    @property
    def _delivery(self):
        return getUtility(IMailDelivery, name=self.delivery, context=self)

    def send(self, **kw):
        self.sendTo(self.addresses, **kw)

    def sendTo(self, addresses, **kw):
        delivery = self._delivery
        mailer = IMailerSMTP(self)
        mail = mailer.execute(**kw)
        for toAddress in addresses:
            mailtemplate.set_address_header(mail, 'From', self.fromAddress, 'us-ascii')
            mailtemplate.set_address_header(mail, 'To', toAddress, 'us-ascii')
            toList = [
             toAddress]
            if self.bccAddress:
                toList.append(self.bccAddress)
            delivery.send(self.fromAddress, toList, mail.as_string())