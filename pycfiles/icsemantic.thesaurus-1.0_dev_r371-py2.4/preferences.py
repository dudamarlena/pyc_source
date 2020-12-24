# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/preferences.py
# Compiled at: 2008-10-06 10:31:07
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
from icsemantic.core.fieldproperty import ToolDependentFieldProperty
from icsemantic.thesaurus import exist_keywords_incrementalsearchwidget_property
from icsemantic.thesaurus import keywords_incrementalsearchwidget
import interfaces

class icSemanticManagementThesaurusUpload:
    __module__ = __name__
    implements(interfaces.IicSemanticManagementThesaurusUpload)

    def __init__(self, context):
        """
        """
        self.context = context

    def __call__(self):
        pass

    thesaurus_file = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['thesaurus_file'])
    default_language = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['default_language'])
    thesaurus_context = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['thesaurus_context'])
    thesaurus_format = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['thesaurus_format'])
    encoding = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['encoding'])
    new = FieldProperty(interfaces.IicSemanticManagementThesaurusUpload['new'])


class icSemanticVerticalSelectTest:
    __module__ = __name__
    implements(interfaces.IicSemanticVerticalSelectTest)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        pass

    vertical_select = FieldProperty(interfaces.IicSemanticVerticalSelectTest['vertical_select'])


def thesaurus_upload_adapter(context):
    return icSemanticManagementThesaurusUpload(context)


def vertical_select_test_adapter(context):
    return icSemanticVerticalSelectTest(context)


class icSemanticThesaurusConfiguration(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicSemanticThesaurusConfiguration)
    keywords_incrementalsearchwidget = ToolDependentFieldProperty(interfaces.IicSemanticThesaurusConfiguration['keywords_incrementalsearchwidget'])


def icSemanticThesaurusConfiguration_adapter(context):
    pcm = getUtility(interfaces.IicSemanticThesaurusConfiguration, name='icsemantic.thesaurus.configuration', context=context)
    app = context.restrictedTraverse('/')
    if exist_keywords_incrementalsearchwidget_property(app):
        pcm.keywords_incrementalsearchwidget = keywords_incrementalsearchwidget(app)
    return pcm