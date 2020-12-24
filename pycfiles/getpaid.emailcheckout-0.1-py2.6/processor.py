# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/getpaid/emailcheckout/processor.py
# Compiled at: 2010-05-31 16:45:40
"""
"""
from getpaid.emailcheckout.interfaces import IEmailProcessor
from getpaid.emailcheckout.interfaces import IEmailOptions
from zope import interface
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces

class EmailProcessor(object):
    interface.implements(IEmailProcessor)
    options_interface = IEmailOptions

    def __init__(self, context):
        self.context = context

    def refund(self, order, amount):
        pass

    def capture(self, order, price):
        """we can't check if the customer can pay right now.
        this is done later by our staff
        """
        return GetPaidInterfaces.keys.results_async

    def authorize(self, order, payment):
        """we need not authorize the payment here
        """
        return GetPaidInterfaces.keys.results_success