# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.0-STABLE-i386/egg/infrae/plone/relations/form/example.py
# Compiled at: 2008-06-13 09:07:00
from zope.interface import Interface
from infrae.plone.relations.schema import PloneRelation

class IPloneRelationExample(Interface):
    """An example for plone relation.
    """
    __module__ = __name__
    relation = PloneRelation(title='Relation field', description='Field with a relation', relation='plone relation', unique=True)


from infrae.plone.relations.form import PloneRelationEditWidget
from infrae.plone.relations.form import PloneRelationSearchAddWidget
from zope.app.form import CustomWidgetFactory
widget_factory = CustomWidgetFactory(PloneRelationEditWidget, add_widget=PloneRelationSearchAddWidget, add_widget_args=dict(content_type='Document'))
from Products.Five.formlib import formbase
from zope.formlib import form

class PloneRelationEditForm(formbase.EditForm):
    __module__ = __name__
    label = 'Plone relation edit form'
    description = 'Form to edit with relations'
    form_fields = form.Fields(IPloneRelationExample)
    form_fields['relation'].custom_widget = widget_factory


class PloneRelationViewForm(formbase.DisplayForm):
    __module__ = __name__
    label = 'Plone relation view form'
    description = 'Form to view relations'
    form_fields = form.Fields(IPloneRelationExample)


from Products.ATContentTypes.content.document import ATDocument
from zope.interface import classImplements
classImplements(ATDocument, IPloneRelationExample)
from zope import schema

class IPloneRelationContext(Interface):
    __module__ = __name__
    float_value = schema.Float(title='Float value')
    string_value = schema.TextLine(title='String value')


class IPloneRelationCtxtExample(Interface):
    __module__ = __name__
    relation = PloneRelation(title='Relation with a context', relation='relation context', context_schema=IPloneRelationContext, unique=True, required=False, max_length=1)


from infrae.plone.relations.schema import BasePloneRelationContext
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

class PloneRelationContext(BasePloneRelationContext):
    __module__ = __name__
    implements(IPloneRelationContext)
    float_value = FieldProperty(IPloneRelationContext['float_value'])
    string_value = FieldProperty(IPloneRelationContext['string_value'])


from infrae.plone.relations.form.utility import buildListAddWidget
from infrae.plone.relations.schema import BasePloneRelationContextFactory
context_factory = BasePloneRelationContextFactory(PloneRelationContext, IPloneRelationContext)
widget_factory_ctxt = buildListAddWidget('Folder', context_factory=context_factory, review_state='published')

class PloneRelationCtxtEditForm(formbase.EditForm):
    __module__ = __name__
    label = 'Plone relation edit form with context'
    description = 'Form to edit with relations with context'
    form_fields = form.Fields(IPloneRelationCtxtExample)
    form_fields['relation'].custom_widget = widget_factory_ctxt


from Products.ATContentTypes.content.folder import ATFolder
classImplements(ATFolder, IPloneRelationCtxtExample)

class IPloneRelationVocExample(Interface):
    __module__ = __name__
    relation = PloneRelation(title='Relation based on a vocabulary', relation='relation vocabulary', required=False)


from infrae.plone.relations.form.utility import buildVocabularyAddWidget
widget_factory_voc = buildVocabularyAddWidget('My vocabulary')

class PloneRelationVocEditForm(formbase.EditForm):
    __module__ = __name__
    label = 'Plone relation edit form based on a vocabulary'
    description = 'Form using vocabulary'
    form_fields = form.Fields(IPloneRelationVocExample)
    form_fields['relation'].custom_widget = widget_factory_voc


classImplements(ATFolder, IPloneRelationVocExample)
from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

class MyVocabularyFactory(object):
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = context.portal_catalog(portal_type='Document', path=dict(query=('/').join(context.getPhysicalPath()), depth=1))
        terms = [ SimpleTerm(e.getObject(), token=e.getId, title=e.Title) for e in items ]
        return SimpleVocabulary(terms)


MyVocabulary = MyVocabularyFactory()