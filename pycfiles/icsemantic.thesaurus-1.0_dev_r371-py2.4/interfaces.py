# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/interfaces.py
# Compiled at: 2008-10-06 10:31:07
""" icsemantic.thesaurus interfaces.
"""
from zope import schema
from zope.interface import Interface
from icsemantic.core.i18n import _

class IThesaurus(Interface):
    """ Interface for Thesaurus Utility
    """
    __module__ = __name__


class IicSemanticManagementThesaurusUpload(Interface):
    """ Interface used for a thesaurus file upload.
    """
    __module__ = __name__
    thesaurus_file = schema.Bytes(title=_('Thesaurus file'), required=True, description=_('A thesaurus file located in your computer'))
    default_language = schema.Choice(title=_('heading_thesaurus_language', default='Default language'), description=_('description_site_language', default='If the uploaded thesaurus has no language, please enter the language in this field'), required=True, vocabulary='icsemantic.languages')
    thesaurus_context = schema.TextLine(title=_('heading_thesaurus_context', 'Default Context'), description=_('description_thesaurus_context', default='if the uploaded thesaurus has no context, please enter the context in this field'), required=False)
    thesaurus_format = schema.Choice(title=_('heading_file_format', 'File format'), description=_('description_file_format', 'Thesaurus File format'), required=True, vocabulary='icsemantic.core.thesaurus_formats')
    encoding = schema.Choice(title=_('heading_encodings', 'Encoding'), description=_('description_encodings', 'Encoding File format'), required=True, vocabulary='icsemantic.core.encodings')
    new = schema.Bool(title=_('heading_new', 'Start new thesaurus'), description=_('description_new', 'Clean old thesaurus and create one with this data.'), required=True)


class IicSemanticVerticalSelectTest(Interface):
    """ Interface used for test the vertical select widget.
    """
    __module__ = __name__
    vertical_select = schema.TextLine(title=_('heading_thesaurus_verticalselect', 'Vertical select'), description=_('description_thesaurus_verticalselect', default='Select a branch of concepts'), required=False)


class IicSemanticThesaurusConfiguration(Interface):
    __module__ = __name__
    keywords_incrementalsearchwidget = schema.Bool(title=_('heading_keywords_incrementalsearchwidget', 'Keywords widget'), description=_('description_keywords_incrementalsearchwidget', 'Use incremental search widget to choose thesaurus terms at documents properties form.\nWarning: This option aplies to the whole plone instance.'), required=True)