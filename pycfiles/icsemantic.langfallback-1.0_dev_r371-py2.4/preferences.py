# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/preferences.py
# Compiled at: 2008-10-06 10:31:06
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
from zope.component import queryUtility
from icsemantic.core.annotations import KeywordBasedAnnotations
from icsemantic.core.fieldproperty import AuthenticatedMemberFieldProperty
from icsemantic.langfallback import interfaces

class ManagementUserLanguagesFactory(KeywordBasedAnnotations):
    __module__ = __name__
    implements(interfaces.IManageUserLanguages)
    icsemantic_languages = AuthenticatedMemberFieldProperty(interfaces.IManageUserLanguages['icsemantic_languages'], 'icsemantic.language')