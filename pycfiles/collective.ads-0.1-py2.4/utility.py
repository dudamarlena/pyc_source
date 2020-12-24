# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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