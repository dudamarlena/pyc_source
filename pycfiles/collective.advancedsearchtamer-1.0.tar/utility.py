# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/admin/utility.py
# Compiled at: 2009-01-02 10:57:30
from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
_ = MessageFactory('portal_adsadmin')

class IAdsPortal(Interface):
    """This interface defines the Utility."""
    __module__ = __name__


class IAdsAdminControlPanelForm(Interface):
    """Control Panel Form"""
    __module__ = __name__