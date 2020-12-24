# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/preferences.py
# Compiled at: 2008-10-06 10:31:08
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
from icsemantic.core.annotations import KeywordBasedAnnotations
from fieldproperty import ToolDependentFieldProperty, AuthenticatedMemberFieldProperty
import interfaces

class icSemanticManagementContentTypes(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicSemanticManagementContentTypes)

    def __call__(self):
        import pdb
        pdb.set_trace()

    fallback_types = ToolDependentFieldProperty(interfaces.IicSemanticManagementContentTypes['fallback_types'])


def content_types_form_adapter(context):
    pcm = getUtility(interfaces.IicSemanticManagementContentTypes, name='icsemantic.configuration', context=context)
    return pcm


class icSemanticManagementUserLanguagesFactory(KeywordBasedAnnotations):
    __module__ = __name__
    implements(interfaces.IicSemanticManageUserLanguages)
    icsemantic_preferred_languages = AuthenticatedMemberFieldProperty(interfaces.IicSemanticManageUserLanguages['icsemantic_preferred_languages'], 'icsemantic.preferred_languages')