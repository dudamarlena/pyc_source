# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/getpaid/pagseguro/interfaces.py
# Compiled at: 2009-04-20 19:03:52
"""
"""
from getpaid.core import interfaces
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.pagseguro')

def _vocabulary(*terms):
    return SimpleVocabulary([ SimpleTerm(token, token, title) for (token, title) in terms ])


class IPagseguroStandardProcessor(interfaces.IPaymentProcessor):
    """
    Pagseguro Processor
    """
    __module__ = __name__


class IPagseguroStandardOptions(interfaces.IPaymentProcessorOptions):
    """
    Pagseguro Standard Options
    """
    __module__ = __name__
    server_url = schema.Choice(title=_('Pagseguro Processador de Pagamentos'), values=('real',
                                                                                       'teste'))
    merchant_id = schema.ASCIILine(title=_('ID Pagseguro'))
    merchant_token = schema.ASCIILine(title=_('Token Pagseguro'))