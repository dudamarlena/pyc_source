# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/memberdata/languages.py
# Compiled at: 2008-10-06 10:31:08
"""
Adapters y Utilities para el manejo de multi lenguajes

@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
from AccessControl import getSecurityManager
from zope.interface import implements
from zope.i18n.interfaces import IUserPreferredLanguages

class icSemanticPropertyPreferredLanguages(object):
    """
    icsemantic.preferred_languages property utility
    """
    __module__ = __name__
    implements(IUserPreferredLanguages)

    def getPreferredLanguages(self, user=None):
        if not user:
            self.user = getSecurityManager().getUser()
        try:
            psheet = self.user.getPropertysheet('mutable_properties')
            return list(psheet.getProperty('icsemantic.preferred_languages'))
        except:
            return []


authenticated_member_icsemantic_languages_property = icSemanticPropertyPreferredLanguages()
member_icsemantic_languages_property = icSemanticPropertyPreferredLanguages()

class PlonePreferredLanguage(object):
    """
    icsemantic.preferred_languages property utility
    """
    __module__ = __name__
    implements(IUserPreferredLanguages)

    def getPreferredLanguages(self, user=None):
        if not user:
            self.user = getSecurityManager().getUser()
        try:
            psheet = self.user.getPropertysheet('mutable_properties')
            language = psheet.getProperty('language')
            if language:
                return [
                 language]
        except:
            pass

        return []


authenticated_member_plone_preferred_languages = PlonePreferredLanguage()
member_plone_preferred_languages = PlonePreferredLanguage()