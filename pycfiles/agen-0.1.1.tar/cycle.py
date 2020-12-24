# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/cycle.py
# Compiled at: 2013-03-15 12:01:48
import os.path
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.browser.add import DefaultAddView, DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import plone.dexterity.browser, yafowil.plone, yafowil.loader
from yafowil.base import factory, UNSET, ExtractionError
from yafowil.controller import Controller
from yafowil.plone.form import Form
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.indexer import indexer
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
import datetime, z3c.form
from Products.CMFPlone.utils import log
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid, Interface
from Acquisition import aq_inner, aq_parent
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from zope.security import checkPermission
from ageliaco.rd2 import MessageFactory
from interface import ICycle, IAuteur, InterfaceView

class Single_view(dexterity.DisplayForm):
    grok.context(ICycle)
    grok.require('zope2.View')
    grok.name('single_view')

    def canReviewContent(self):
        return checkPermission('cmf.ReviewPortalContent', self.context)

    def canAddContent(self):
        return checkPermission('cmf.AddPortalContent', self.context)

    def canModifyContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def parent_url(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        return parent.absolute_url()


class View(InterfaceView):
    grok.context(ICycle)
    grok.require('zope2.View')
    grok.name('view')

    def auteurs(self):
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        log('context path : ' + context.absolute_url())
        return catalog(object_provides=[IAuteur.__identifier__], path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='sortable_title')

    def delAuteur(self, auteur):
        context = aq_inner(self.context)
        if auteur in context.keys():
            del context[auteur]
        return context.absolute_url()

    def parent_url(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        return parent.absolute_url()

    def schoolyear(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        an = int(parent.start)
        retour = '%s-%s' % (an, an + 1)
        return retour

    def cycle_url(self):
        context = aq_inner(self.context)
        return context.absolute_url()

    def contributeur(self, auteur):
        context = aq_inner(self.context)
        if auteur in context.keys():
            return context[auteur]
        else:
            return


@indexer(ICycle)
def searchableIndexer(context):
    try:
        return '%s %s %s %s' % (context.title,
         context.description,
         context.problematique,
         context.presentation)
    except:
        log('tOO BAD an INDEX (bad cycle) : ' + context.absolute_url())
        return ''


grok.global_adapter(searchableIndexer, name='SearchableText')

@indexer(ICycle)
def authorsIndexer(obj):
    return obj.contributor


grok.global_adapter(authorsIndexer, name='authors')

@indexer(ICycle)
def supervisorIndexer(obj):
    return obj.supervisor


grok.global_adapter(supervisorIndexer, name='supervisor')