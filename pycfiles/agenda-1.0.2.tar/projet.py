# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/projet.py
# Compiled at: 2013-03-14 10:46:13
from five import grok
from zope import schema
from Products.ATContentTypes.lib import constraintypes
from plone.directives import form, dexterity
from zope.app.container.interfaces import IObjectAddedEvent
from plone.z3cform.textlines import TextLinesFieldWidget
from zope.interface import invariant, Invalid
from interface import IProjet, IAuteur, ICycle, idDefaultFromContext, InterfaceView
from interface import cycle_default_problematique, cycle_default_projet_presentation
from note import INote
import yafowil.plone, yafowil.loader
from yafowil.base import factory, UNSET, ExtractionError
from yafowil.controller import Controller
from yafowil.plone.form import Form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.utils import createContentInContainer
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.textfield.value import RichTextValue
from DateTime import DateTime
from plone.indexer import indexer
import datetime
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.security import checkPermission
from zope.app.content import queryContentType
from zope.schema import getFieldsInOrder
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from ageliaco.rd2 import MessageFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import ast

@grok.subscribe(IProjet, IObjectAddedEvent)
def setRealisation(projet, event):
    admid = 'realisation'
    try:
        cycles = projet[admid]
    except KeyError:
        rea = projet.invokeFactory('Folder', id=admid, title='Réalisation')
        rea.setConstrainTypesMode(constraintypes.ENABLED)
        rea.setLocallyAllowedTypes(['File', 'Folder', 'Image', 'Document', 'Link'])
        rea.setImmediatelyAddableTypes(['File', 'Folder', 'Image', 'Document', 'Link'])


@indexer(IProjet)
def searchableIndexer(context):
    keywords = (' ').join(context.keywords)
    return '%s %s %s %s' % (context.title, context.description, context.presentation, keywords)


grok.global_adapter(searchableIndexer, name='SearchableText')

def richtext():
    part = factory('fieldset', name='yafowilwidgetrichtext')
    part['richtext'] = factory('#field:richtext', props={'label': 'Richtext field', 
       'required': 'Text is required'})
    return {'widget': part, 'doc': 'Doc', 
       'title': 'Richtext'}


class View(grok.View, Form):
    grok.context(IProjet)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)

    def __call__(self):
        if 'optionsRadios' in self.request.form:
            title = ''
            projetpath, title = ast.literal_eval(self.request['optionsRadios'])
            context = aq_inner(self.context)
            catalog = getToolByName(self.context, 'portal_catalog')
            cat = catalog(object_provides=ICycle.__identifier__, path={'query': projetpath, 'depth': 1}, sort_on='modified', sort_order='reverse')
            portal_url = getToolByName(context, 'portal_url')
            portal = portal_url.getPortalObject()
            projet = portal.unrestrictedTraverse(projetpath)
            item = None
            if len(cat):
                try:
                    ids = context.manage_pasteObjects(projet.manage_copyObjects(cat[0].id))
                    cycleId = ids[0]['new_id']
                    item = context[cycleId]
                    new_id = idDefaultFromContext(context)
                    item.aq_parent.manage_renameObject(cycleId, str(new_id))
                    cycleId = new_id
                    item.setTitle(title)
                    if not item.presentation:
                        item.presentation = RichTextValue(raw=cycle_default_projet_presentation)
                    item.problematique = RichTextValue(raw=cycle_default_problematique)
                    cat = catalog(object_provides=INote.__identifier__, path={'query': ('/').join(item.getPhysicalPath()), 'depth': 1}, sort_on='modified', sort_order='reverse')
                    for note in cat:
                        del item[note.id]

                    cat = catalog(object_provides=IAuteur.__identifier__, path={'query': ('/').join(item.getPhysicalPath()), 'depth': 1}, sort_on='modified')
                    for auteur in cat:
                        if auteur.id[0:4] == 'copy':
                            del item[auteur.id]

                except:
                    new_id = idDefaultFromContext(context)
                    item = createContentInContainer(context, 'ageliaco.rd2.cycle', id=new_id, title='')
                    item.projet = projetpath
                    item.presentation = RichTextValue(raw=cycle_default_projet_presentation)
                    item.problematique = RichTextValue(raw=cycle_default_problematique)

            else:
                context = aq_inner(self.context)
                item = createContentInContainer(context, 'ageliaco.rd2.cycle', title=title)
            return self.request.response.redirect(item.absolute_url() + '/edit')
        else:
            return super(View, self).__call__()

    def activeProjets(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        cat = catalog(portal_type='ageliaco.rd2.projet', review_state='encours', sort_on='sortable_title')
        terms = [
         ('', '')]
        for brain in cat:
            terms.append((brain.getPath(), brain.Title))

        return terms

    def logo_url(self):
        context = aq_inner(self.context)
        portal_url = getToolByName(context, 'portal_url')
        if 'logo.png' in context.keys():
            return context.absolute_url() + '/logo.png'
        return portal_url + '/++resource++ageliaco.rd/screens.png'

    def noCycle(self):
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        cat = catalog(object_provides=ICycle.__identifier__, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='modified', sort_order='reverse')
        if len(cat) > 0:
            return False
        return True

    def canAddContent(self, context=None):
        if not context:
            context = self.context
        return checkPermission('cmf.AddPortalContent', context)

    def canModifyContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def cycles_obj(self):
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        cat = catalog(object_provides=ICycle.__identifier__, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='modified', sort_order='reverse')
        return cat

    def review_state(self):
        context = aq_inner(self.context)
        portal_workflow = getToolByName(context, 'portal_workflow')
        review_state = portal_workflow.getInfoFor(context, 'review_state')
        return review_state

    def isRepository(self):
        context = aq_inner(self.context)
        portal_workflow = getToolByName(context, 'portal_workflow')
        review_state = portal_workflow.getInfoFor(context, 'review_state')
        return review_state == 'repository'

    def contributeurs(self, cycle_id):
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        if cycle_id in context.keys():
            cycle = context[cycle_id]
            if cycle:
                cat = catalog(object_provides=IAuteur.__identifier__, path={'query': ('/').join(cycle.getPhysicalPath()), 'depth': 1}, sort_on='modified', sort_order='reverse')
                return cat
        return

    def hasRealisation(self):
        context = aq_inner(self.context)
        if not context.has_key('realisation'):
            return ''
        if len(context['realisation'].keys()) or self.canAddContent(context['realisation']):
            return context['realisation'].absolute_url()
        return ''

    def hasLink(self):
        context = aq_inner(self.context)
        if getattr(context, 'lien', 0):
            return context.lien
        return ''


class CyclesView(InterfaceView):
    grok.context(IProjet)
    grok.require('zope2.View')
    grok.name('cyclesview')