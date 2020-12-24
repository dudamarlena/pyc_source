# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/projets.py
# Compiled at: 2013-02-27 07:43:07
from five import grok
from zope import schema
from plone.directives import form, dexterity
from z3c.form import field, button
from ageliaco.rd2 import MessageFactory
from Products.CMFPlone.utils import log
from interface import IProjet, ICycle, IAuteur, InterfaceView
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from plone.app.textfield import RichText
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from plone.app.layout.viewlets.interfaces import IAboveContent
import datetime
from zope.component import getMultiAdapter
from zope.app.component.hooks import setHooks, setSite, getSite
import yafowil.plone, yafowil.loader
from yafowil.base import factory, UNSET, ExtractionError
from yafowil.controller import Controller
from yafowil.plone.form import Form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interface import ICycle, IAuteur, InterfaceView

class IProjets(form.Schema):
    """
    Projets de Projet RD
    """
    presentation = RichText(title=MessageFactory('Projets R&D'), required=True)


class View(InterfaceView):
    grok.context(IProjets)
    grok.require('zope2.View')
    grok.name('view')

    def results(self):
        return self.cat

    def _form_action(self, widget, data):
        return '%s/@@localsearch' % self.context.absolute_url()

    def _form_handler(self, widget, data):
        self.searchterm = data['searchterm'].extracted

    def form(self):
        form = factory('form', name='search', props={'action': self._form_action})
        form['searchterm'] = factory('field:label:error:text', props={'label': MessageFactory('Rechercher dans les projets:'), 
           'field.class': 'myFieldClass', 
           'text.class': 'myInputClass', 
           'size': '20'})
        form['submit'] = factory('field:submit', props={'label': MessageFactory('Lancer la recherche'), 
           'submit.class': '', 
           'handler': self._form_handler, 
           'action': 'search'})
        controller = Controller(form, self.request)
        return controller.rendered

    def results(self):
        if not hasattr(self, 'searchterm') or not self.searchterm:
            return []
        context = aq_inner(self.context)
        cat = getToolByName(self.context, 'portal_catalog')
        query = {}
        qterm = self.searchterm
        if qterm:
            qterm = '%s' % qterm
            query['SearchableText'] = qterm.decode('utf-8')
            query['path'] = {'query': ('/').join(context.getPhysicalPath())}
        return cat(**query)


class KeywordView(InterfaceView):
    grok.context(IProjets)
    grok.require('zope2.View')
    grok.name('keywordview')


class StateView(View):
    grok.context(IProjets)
    grok.require('zope2.View')
    grok.name('stateview')


class LocalSearch(View):
    grok.context(IProjets)
    grok.require('zope2.View')
    grok.name('localsearch')


class CyclesView(InterfaceView):
    grok.context(IProjets)
    grok.require('zope2.View')
    grok.name('cyclesview')