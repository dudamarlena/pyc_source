# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/projets.py
# Compiled at: 2012-01-03 10:48:53
from five import grok
from zope import schema
from plone.directives import form, dexterity
from z3c.form import field, button
from ageliaco.rd import _
from Products.CMFPlone.utils import log
from projet import IProjet
from cycle import ICycle
from auteur import IAuteur
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from plone.app.textfield import RichText
from collective.gtags.field import Tags
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from plone.app.layout.viewlets.interfaces import IAboveContent
import datetime
from zope.component import getMultiAdapter

def getView(context, request, name):
    context = aq_inner(context)
    view = getMultiAdapter((context, request), name=name)
    view.context = context
    view.request = request
    return view


class IProjets(form.Schema):
    """
    Projets de Projet RD
    """
    presentation = RichText(title=_('Projets R&D'), required=True)


class IBaseAuteur(form.Schema):
    """
    Info de base pour generer plus tard les Auteurs de projet
    """
    firstname = schema.TextLine(title=_('Prénom'), description=_('Prénom'), required=True)
    lastname = schema.TextLine(title=_('Nom'), description=_('Nom de famille'), required=True)
    school = schema.Choice(title=_('Ecole'), description=_('Etablissement scolaire de référence'), vocabulary='ageliaco.rd.schools', required=False)
    address = schema.Text(title=_('Adresse'), description=_('Adresse postale'), required=False)
    email = schema.TextLine(title=_('Email'), description=_('Adresse courrielle'), required=True)


class INewProjet(form.Schema):
    """
    to gather fields from both parents
    """
    contributor = schema.List(title=_('Contributeurs'), value_type=schema.Object(title='Auteur', schema=IBaseAuteur), required=False)
    duration = schema.Int(title=_('Durée'), description=_('Durée (en années) du projet, prévue ou effective'), required=True)
    presentation = RichText(title=_('Présentation'), description=_('Présentation synthétique du projet (présentation publiée)'), required=True)
    problematique = RichText(title=_('Problématique'), description=_("Problématique et contexte du projet pour l'année à venir"), required=True)
    objectifs = RichText(title=_('Objectifs'), description=_("Objectifs du projet pour l'année"), required=True)
    resultats = RichText(title=_('Résultats'), description=_("Retombées (profs et/ou élèves) du projet pour l'année"), required=True)
    moyens = RichText(title=_('Moyens'), description=_("Moyens nécessaires pour l'année"), required=True)
    subject = Tags(title=_('Domaines'))

    def applyChanges(self, data):
        """
        Reflect confirmed status to Archetypes schema.
    
        @param data: Dictionary of cleaned form data, keyed by field
        """
        print 'Apply Changes : ', data['contributor']


class ProjectListing(grok.View):
    """
    End user visible product card presentation.
    """
    grok.context(IProjets)
    grok.require('zope2.View')
    summary_template = ViewPageTemplateFile('projets_templates/projectlisting.pt')

    def update(self):
        context = aq_inner(self.context)
        print 'coucou 1'

    def render_table(self, options):
        """ Render summary box

        @return: Resulting HTML code as Python string
        """
        print self.__dict__
        print options
        return self.summary_template(options)


class View(grok.View):
    grok.context(IProjets)
    grok.require('zope2.View')

    def projets(self, wf_state='all'):
        """Return a catalog search result of projects to show
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        log("context's physical path : " + ('/').join(context.getPhysicalPath()))
        log('all projects')
        if wf_state == 'all':
            log('all projets')
            log(('/').join(context.getPhysicalPath()))
            return catalog(object_provides=IProjet.__identifier__, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='start', sort_order='reverse')
        return catalog(object_provides=[IProjet.__identifier__], review_state=wf_state, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='sortable_title')

    def cycles(self, projectPath, wf_state='all'):
        """Return a catalog search result of cycles from a project
        """
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        log('cycle : ' + projectPath)
        log(wf_state + ' state chosen')
        if wf_state == 'all':
            log('all cycles')
            return catalog(object_provides=ICycle.__identifier__, path={'query': projectPath, 'depth': 1}, sort_on='modified', sort_order='reverse')
        return catalog(object_provides=[ICycle.__identifier__], review_state=wf_state, path={'query': projectPath, 'depth': 2}, sort_on='sortable_title')

    def authors(self, projectPath):
        """Return a catalog search result of authors from a project
        """
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        log('authors : ' + projectPath)
        cat = catalog(object_provides=[IAuteur.__identifier__], path={'query': projectPath, 'depth': 2}, sort_on='sortable_title')
        return cat

    def render_table(self, projets):
        """ return a table of projets """
        projectlisting = ProjectListing(self.context, self.request)
        listingview = getView(self.context, self.request, name='projectlisting')
        options = {}
        options['projets'] = projets
        return projectlisting.render_table(options=options)


class NewProjetForm(form.Form):
    grok.context(IFolderish)
    grok.name('newprojet')
    grok.require('cmf.AddPortalContent')
    ignoreContext = True
    fields = field.Fields(INewProjet)

    @button.buttonAndHandler('Submit')
    def handleApply(self, action):
        (data, errors) = self.extractData()