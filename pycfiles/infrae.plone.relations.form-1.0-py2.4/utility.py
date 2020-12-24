# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.0-STABLE-i386/egg/infrae/plone/relations/form/utility.py
# Compiled at: 2008-06-12 04:00:15
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: utility.py 29119 2008-06-11 10:34:14Z sylvain $'
from zope.app.form import CustomWidgetFactory
from infrae.plone.relations.form import PloneRelationEditWidget
from infrae.plone.relations.form import PloneRelationSearchAddWidget, PloneRelationListAddWidget
from infrae.plone.relations.form import PloneRelationVocabularyAddWidget
from infrae.plone.relations.schema import BasePloneRelationContextFactory as PRCF

def buildListAddWidget(content_type, review_state=None, context_factory=None):
    """Utility to get shorter code in forms.
    """
    return CustomWidgetFactory(PloneRelationEditWidget, add_widget=PloneRelationListAddWidget, add_widget_args=dict(content_type=content_type, review_state=review_state), context_factory=context_factory)


def buildSearchAddWidget(content_type, review_state=None, context_factory=None):
    """Utility to get shorter code in forms.
    """
    return CustomWidgetFactory(PloneRelationEditWidget, add_widget=PloneRelationSearchAddWidget, add_widget_args=dict(content_type=content_type, review_state=review_state), context_factory=context_factory)


def buildVocabularyAddWidget(vocabulary, context_factory=None):
    """Utility to get shorter code in forms.
    """
    return CustomWidgetFactory(PloneRelationEditWidget, add_widget=PloneRelationVocabularyAddWidget, add_widget_args=dict(vocabulary=vocabulary), context_factory=context_factory)