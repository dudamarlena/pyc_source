# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/interfaces.py
# Compiled at: 2008-10-06 10:31:06
""" icsemantic.langfallback interfaces.
"""
from zope.interface import Interface
from zope import schema
from icsemantic.core.i18n import _

class IMemberDataTool(Interface):
    """
    Decorate user objects with site-local data.
    First we need some mock class...
        >>> from minimock import Mock
        >>> from icsemantic.langfallback.interfaces import IMemberDataTool

        >>> memberdata = Mock('memberdata')
        >>> memberdata = self.portal.portal_memberdata
        >>> IMemberDataTool.providedBy(memberdata)
        True

    """
    __module__ = __name__


class IPartialTranslated(Interface):
    """
    """
    __module__ = __name__


class IManageUserLanguages(Interface):
    """
    """
    __module__ = __name__
    icsemantic_languages = schema.List(title=_('User Languages'), required=False, default=[], description=_('User Languages'), value_type=schema.Choice(vocabulary='icsemantic.languages'))