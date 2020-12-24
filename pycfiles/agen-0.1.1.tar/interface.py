# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/interface.py
# Compiled at: 2013-03-15 12:01:58
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
from plone.app.textfield.value import RichTextValue
import plone.dexterity.browser
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.indexer import indexer
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
import unicodedata
from zope.interface import invariant, Invalid, Interface
from ageliaco.rd2 import MessageFactory
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
import datetime, z3c.form
from Products.CMFPlone.utils import log
from zope.schema.interfaces import IContextSourceBinder
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from plone.namedfile.field import NamedImage
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from zope.security import checkPermission
from AccessControl.interfaces import IRoleManager
import yafowil.plone, yafowil.loader
from yafowil.base import factory, UNSET, ExtractionError
from yafowil.controller import Controller
from yafowil.plone.form import Form
from AccessControl.interfaces import IRoleManager
schools = {'ECGGR': ['EC Bougeries', 'CEC'], 'CEBOU': [
           'Nicolas-Bouvier', 'CEC'], 
   'CECHA': [
           'André-Chavanne', 'CEC'], 
   'CEGOU': [
           'Emilie-Gourd', 'CEC'], 
   'ECASE': [
           'Madame-de-Stael', 'CEC'], 
   'ECSTI': [
           'EC Aimée-Stitelmann', 'CEC'], 
   'CALV': [
          'Calvin', 'COLLEGES'], 
   'CAND': [
          'Candolle', 'COLLEGES'], 
   'CLAP': [
          'Claparède', 'COLLEGES'], 
   'COPAD': [
           'Alice-Rivaz', 'COLLEGES'], 
   'ROUS': [
          'Rousseau', 'COLLEGES'], 
   'SAUS': [
          'Saussure', 'COLLEGES'], 
   'SISM': [
          'Sismondi', 'COLLEGES'], 
   'VOLT': [
          'Voltaire', 'COLLEGES'], 
   'ECBGR': [
           'ECG RHONE', 'ECG'], 
   'DUNAN': [
           'Henry-Dunand', 'ECG'], 
   'MAILL': [
           'Ella-Maillart', 'ECG'], 
   'ECGJP': [
           'Jean-Piaget', 'ECG'], 
   'CFPC': [
          'CFPC', 'ECOLES PROFESSIONNELLES'], 
   'CFPS': [
          'CFPS', 'ECOLES PROFESSIONNELLES'], 
   'CFPT': [
          'CFPT', 'ECOLES PROFESSIONNELLES'], 
   'CFPSH': [
           'CFPSHR-EGEI', 'ECOLES PROFESSIONNELLES'], 
   'BOUV': [
          'CFPCOM-Bouvier', 'ECOLES PROFESSIONNELLES'], 
   'CFPNE': [
           'CFPNE', 'ECOLES PROFESSIONNELLES'], 
   'CFPAA': [
           'CFPAA', 'ECOLES PROFESSIONNELLES'], 
   'SCAI': [
          'SCAI', 'INSERTION'], 
   'COUDR': [
           'CO Coudriers', 'CYCLES']}
sponsorships = {'0': ['0', 0], '0.25': [
          '0.25', 0.25], 
   '0.50': [
          '0.50', 0.5], 
   '0.75': [
          '0.75', 0.75], 
   '1.00': [
          '1.00', 1.0], 
   '1.25': [
          '1.25', 1.25], 
   '1.50': [
          '1.50', 1.5], 
   '1.75': [
          '1.75', 1.75], 
   '2.00': [
          '2.00', 2.0], 
   '2.25': [
          '2.25', 2.25], 
   '2.50': [
          '2.50', 2.5], 
   '2.75': [
          '2.75', 2.75], 
   '3.00': [
          '3.00', 3.0], 
   '3.25': [
          '3.25', 3.25], 
   '3.50': [
          '3.50', 3.5], 
   '3.75': [
          '3.75', 3.75], 
   '4.00': [
          '4.00', 4.0]}

class SchoolsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        for school in sorted(schools.keys()):
            terms.append(SimpleVocabulary.createTerm(unicodedata.normalize('NFKC', school).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', schools[school][0]).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', schools[school][0]).encode('ascii', 'ignore')))

        return SimpleVocabulary(terms)


grok.global_utility(SchoolsVocabulary, name='ageliaco.rd2.schools')

class SponsorshipVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        for sponsorship in sorted(sponsorships.keys()):
            terms.append(SimpleVocabulary.createTerm(unicodedata.normalize('NFKC', sponsorship).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', sponsorships[sponsorship][0]).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', sponsorships[sponsorship][0]).encode('ascii', 'ignore')))

        return SimpleVocabulary(terms)


grok.global_utility(SponsorshipVocabulary, name='ageliaco.rd2.sponsorship')

class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById(self.group_name)
        terms = []
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)


class ProjetsVoc(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, projet_name):
        self.projet_name = projet_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById(self.projet_name)
        terms = []
        terms.append(SimpleVocabulary.createTerm('', str(''), ''))
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)


class IAuteur(form.Schema):
    """
    Auteur de projet
    """
    id = schema.TextLine(title=MessageFactory('id'), description=MessageFactory('Identifiant (login)'), required=True)
    lastname = schema.TextLine(title=MessageFactory('Nom'), description=MessageFactory('Nom de famille'), required=True)
    firstname = schema.TextLine(title=MessageFactory('Prénom'), description=MessageFactory('Prénom'), required=True)
    school = schema.Choice(title=MessageFactory('Ecole'), description=MessageFactory('Etablissement scolaire de référence'), vocabulary='ageliaco.rd2.schools', default='', required=True)
    address = schema.Text(title=MessageFactory('Adresse'), description=MessageFactory('Adresse postale'), required=False)
    email = schema.TextLine(title=MessageFactory('Email'), description=MessageFactory('Adresse courrielle'), required=True)
    phone = schema.TextLine(title=MessageFactory('Téléphone'), description=MessageFactory('Téléphone'), required=False)
    sponsorasked = schema.Choice(title=MessageFactory('Dégrèvement demandé'), description=MessageFactory('Dégrèvement total demandé pour cet auteur'), vocabulary='ageliaco.rd2.sponsorship', required=True)
    dexterity.read_permission(sponsorSEM='cmf.ReviewPortalContent')
    dexterity.write_permission(sponsorSEM='cmf.ReviewPortalContent')
    sponsorSEM = schema.Choice(title=MessageFactory('Dégrèvement SEM'), description=MessageFactory('Dégrèvement SEM attribué pour cet auteur'), vocabulary='ageliaco.rd2.sponsorship', required=False)
    dexterity.read_permission(sponsorRD='cmf.ReviewPortalContent')
    dexterity.write_permission(sponsorRD='cmf.ReviewPortalContent')
    sponsorRD = schema.Choice(title=MessageFactory('Dégrèvement R&D'), description=MessageFactory('Dégrèvement R&D attribué pour cet auteur'), vocabulary='ageliaco.rd2.sponsorship', required=False)
    dexterity.read_permission(sponsorSchool='cmf.ReviewPortalContent')
    dexterity.write_permission(sponsorSchool='cmf.ReviewPortalContent')
    sponsorSchool = schema.Choice(title=MessageFactory('Dégrèvement Ecole'), description=MessageFactory('Dégrèvement école attribué pour cet auteur'), vocabulary='ageliaco.rd2.sponsorship', required=False)


@grok.subscribe(IAuteur, IObjectAddedEvent)
def setAuteur(auteur, event):
    portal_url = getToolByName(auteur, 'portal_url')
    acl_users = getToolByName(auteur, 'acl_users')
    portal = portal_url.getPortalObject()
    cycles = auteur.aq_parent
    user = acl_users.getUserById(auteur.id)


class IProjet(form.Schema):
    """
    Projet RD
    """
    start = schema.TextLine(title=MessageFactory('Année'), description=MessageFactory("L'année à laquelle le projet a commencé ou devrait commencer"), required=True)
    duration = schema.Int(title=MessageFactory('Durée'), description=MessageFactory('Durée (en années) du projet, prévue ou effective'), required=True)
    presentation = RichText(title=MessageFactory('Présentation'), description=MessageFactory('Présentation synthétique du projet (présentation publiée)'), required=True)
    picture = NamedImage(title=MessageFactory('Chargez une image pour le projet'), required=False)
    lien = schema.TextLine(title=MessageFactory('Lien vers la réalisation'), description=MessageFactory('Lien extérieur vers la réalisation'), required=False)


@grok.subscribe(IProjet, IObjectAddedEvent)
def setRealisation(projet, event):
    admid = 'realisation'
    try:
        cycles = projet[admid]
    except KeyError:
        rea = projet.invokeFactory('Folder', id=admid, title='Réalisation')


@grok.provider(IContextSourceBinder)
def activeProjects(context):
    catalog = getToolByName(context, 'portal_catalog')
    cat = catalog(portal_type='ageliaco.rd2.projet', review_state='encours', sort_on='sortable_title')
    log('catalogue : %s items' % len(cat))
    terms = []
    for brain in cat:
        terms.append(SimpleVocabulary.createTerm(brain.getPath(), brain.id, brain.Title))

    return SimpleVocabulary(terms)


cycle_default_projet_presentation = '\n<h2><span style="color: rgb(204, 0, 0); ">Discipline(s) concernée(s) par le projet :<br /></span></h2>\n<p class="callout">&nbsp;\xa0</p>\n<h2><span style="color: rgb(1, 40, 0); "><span style="color: rgb(204, 0, 0); ">Description synthétique de l\'ensemble du projet :</span><br /></span></h2>\n<p><i><span class="discreet noprint">Décrire brièvement votre projet en vue de sa promotion sur le site Ressources et développement.</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0);">Thématique:</span></h2>\n<h3>Quel est le thème du projet ?</h3>\n<p><i><span class="discreet noprint">Expliciter en quelques lignes le(s) contenu(s) sur le(s)quel(s) les participants au projet souhaitent travailler.</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0); ">Contexte :</span></h2>\n<h3>a. Sur quelles expériences ou connaissances préalables repose le projet ?</h3>\n<p><i><span class="discreet noprint">Quels sont le travail et la réflexion déjà  entamés dans le domaine de la recherche proposée : bibliographie, \n inventaire d\'expérience, etc.</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h3>b.\xa0\xa0 Quels éléments de la situation présente sont à l\'origine du besoin exprimé ?</h3>\n<p><i><span class="discreet noprint">Justification et preuves du besoin : études, enquête, sondage, argumentaire précis, etc..</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0); ">Objectifs pédagogiques :</span></h2>\n<h3>Quels sont les objectifs généraux du projet ?</h3>\n<p><i><span class="discreet noprint">Changements et actions concrets auxquels on peut s\'attendre à court et à long terme</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0); ">Résultats pédagogiques pour les élèves et les maîtres :</span></h2>\n<h3>a. \xa0Quels sont le public visé et les établissements concernés ?</h3>\n<p class="callout">&nbsp;\xa0</p>\n<h3>b. \xa0Quelle forme prend le produit fini au terme du projet ?</h3>\n<p><i><span class="discreet noprint">Brochure, site, etc..</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0); ">Organisation :</span></h2>\n<h3>a. \xa0Quelle est la durée estimée du projet, en année(s) scolaire(s) ?</h3>\n<p class="callout">&nbsp;\xa0</p>\n<h3>b.\xa0 Quels sont les objectifs spécifiques du projet pour l\'(es) année(s) scolaire(s) ?</h3>\n<p class="callout">&nbsp;\xa0</p>\n'
cycle_default_problematique = '\n<h2><span style="color: rgb(204, 0, 0); ">Planification et répartition des tâches pour l\'année en cours :</span></h2>\n<h3>a. \xa0Quelle planification est prévue ? (étapes) :</h3>\n<p class="callout">&nbsp;\xa0</p>\n<h3>b.\xa0 Quel rôle et quelle répartition des tâches sont prévus par participant?</h3>\n<p class="callout">&nbsp;\xa0</p>\n<p>\xa0</p>\n<h2><span style="color: rgb(204, 0, 0); ">Modalités de travail :</span></h2>\n<h3>Quelles sont les modalités de travail qui faciliteraient la réalisation de votre projet ?</h3>\n<p><i><span class="discreet noprint">Plateforme pour un travail à distance,   horaire aménagé sur 2 heures hebdomadaires, etc. (à préciser également  \n dans les vœux horaires dans votre établissement.)</span></i></p>\n<p class="callout">&nbsp;</p><br />\n<h2><span style="color: rgb(204, 0, 0); ">Ressources supplémentaires :</span></h2>\n<p><i><span class="discreet noprint">Accompagnement par des experts du Service   Ecole Media, par des experts sous forme de demi-journées d\'étude, par  \n des séminaires de formation continue, etc.</span></i></p>\n<p class="callout">&nbsp;\xa0</p>\n<br />\n<p style="text-align: center; "><span style="color: rgb(204, 0, 0); "><strong>\n<img alt="Sourire" border="0" src="../plugins/emotions/img/smiley-smile.gif" title="Sourire" /> \nLe secteur Ressources et développement vous remercie d\'avoir complété ce formulaire auquel il portera toute son attention</strong>\n</span><i><span> \n<img alt="Sourire" border="0" src="../plugins/emotions/img/smiley-smile.gif" title="Sourire" /><br /></span></i></p>\n<p>&nbsp;</p>\n'

class ICycle(form.Schema):
    """
    Cycle de projet RD
    """
    form.mode(id='hidden')
    id = schema.TextLine(title=MessageFactory('Identifiant'), description=MessageFactory('Ne pas changer celui donné par défaut! Merci!'), required=True)
    title = schema.TextLine(title=MessageFactory('Titre'), description=MessageFactory('Titre bref du projet'), required=True)
    description = schema.Text(title=MessageFactory('Sous-titre'), description=MessageFactory('Sous-titre du projet'), required=False)
    presentation = RichText(title=MessageFactory('Présentation succincte du projet'), description=MessageFactory('Présentation succincte du projet (synopsis)'), required=True)
    projet = schema.Choice(title=MessageFactory('Projet existant'), description=MessageFactory('Lien vers un projet existant'), source=activeProjects, required=False)
    dexterity.write_permission(supervisor='cmf.ReviewPortalContent')
    supervisor = schema.Choice(title=MessageFactory('Superviseur'), description=MessageFactory('Personne de R&D qui supervise ce projet'), source=GroupMembers('superviseur'), required=False)
    problematique = RichText(title=MessageFactory('Problématique'), description=MessageFactory('Problématique et contexte du projet'), required=False)


def idDefaultFromContext(context):
    """context must be a ageliaco.rd2.projet object"""
    newId = ''
    indice = 1
    start = ''
    catalog = getToolByName(context, 'portal_catalog')
    cat = catalog.unrestrictedSearchResults(object_provides=ICycle.__identifier__, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='modified', sort_order='reverse')
    if hasattr(context, 'start'):
        start = context.start
    else:
        start = str(datetime.datetime.today().year)
    if len(cat):
        for cycle in cat:
            lastId = cycle.id
            index = lastId.find('-')
            if index > -1 and lastId[:index] == start:
                indice = int(lastId[index + 1:])
                indice += 1
                break

    newId = '%s-%s' % (start, indice)
    while newId in context.objectIds():
        indice += 1
        newId = '%s-%s' % (start, indice)

    return newId


@form.default_value(field=ICycle['id'])
def idDefaultValue(data):
    context = data.context
    newId = idDefaultFromContext(context)
    return newId


@form.default_value(field=ICycle['presentation'])
def presentationDefaultValue(data):
    return RichTextValue(raw=cycle_default_projet_presentation)


@form.default_value(field=ICycle['problematique'])
def problematiqueDefaultValue(data):
    return RichTextValue(raw=cycle_default_problematique)


@grok.subscribe(ICycle, IObjectModifiedEvent)
def setSupervisor(cycle, event):
    if not cycle.supervisor:
        return
    if IRoleManager.providedBy(cycle):
        cycle.manage_addLocalRoles(cycle.supervisor, ['Reader', 'Contributor', 'Editor'])
    log('Role added to %s for %s' % (cycle.id, cycle.supervisor))


@grok.subscribe(ICycle, IObjectAddedEvent)
def setAuteurs(cycle, event):
    if not cycle.projet:
        return
    catalog = getToolByName(cycle, 'portal_catalog')
    cat = catalog(portal_type='ageliaco.rd2.cycle', path={'query': cycle.projet, 'depth': 1}, sort_on='id', sort_order='reverse')
    log('catalogue des cycles : %s items' % len(cat))
    if len(cat):
        lastCyclePath = cat[0].getPath()
        lastCycle = cat[0].getObject()
        auteurBrains = catalog(portal_type='ageliaco.rd2.auteur', path={'query': lastCyclePath, 'depth': 1})
        for brain in auteurBrains:
            auteur = brain.getObject()
            cb_copy_data = lastCycle.manage_copyObjects([auteur.id])
            cycle.manage_pasteObjects(cb_copy_data)


class InterfaceView(grok.View, Form):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('interface')
    objectPath = ''
    degrevements = {}
    withTotal = False
    multikey = '@@keywordview'
    indx = 'Subject'
    searchType = IProjet.__identifier__
    pathDepth = 0
    allauthors = 'cycle,author.id,author.lastname,author.firstname,author.school,ordre,author.sponsorasked,author.sponsorSEM,author.sponsorRD,author.sponsorSchool'

    def set2float(self, value):
        if not value:
            return 0.0
        else:
            return float(value)

    def canReviewContent(self):
        return checkPermission('cmf.ReviewPortalContent', self.context)

    def canAddContent(self):
        return checkPermission('cmf.AddPortalContent', self.context)

    def canModifyContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def setObjectPath(self, objectPath, withTotal=False):
        self.objectPath = objectPath
        self.withTotal = withTotal
        if withTotal:
            self.degrevements[objectPath] = [
             0.0,
             0.0,
             0.0,
             0.0,
             0.0]
        return self.objectPath

    def getObjectPath(self):
        return self.objectPath

    def authors(self, projectPath=''):
        """Return a catalog search result of authors from a project
        problem : same author appears several times 
        """
        auteurs = []
        auteurIDs = []
        context = aq_inner(self.context)
        if not projectPath:
            projectPath = ('/').join(context.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        cat = catalog(object_provides=[IAuteur.__identifier__], path={'query': projectPath, 'depth': 2}, sort_on='modified', sort_order='reverse')
        for auteur in cat:
            if auteur.id not in auteurIDs:
                auteurs.append(auteur)
                auteurIDs.append(auteur.id)

        return auteurs

    def getSponsoring(self):
        if self.withTotal:
            return self.degrevements[self.objectPath]
        else:
            return {}

    def sponsorasked(self, auteur):
        context = aq_inner(self.context)
        author = auteur.getObject()
        ordre = ''
        if author.school in schools.keys():
            ordre = schools[author.school][1]
        oneauthor = '\n%s,%s,%s,%s,%s,%s,%s,%d,%d,%d' % (auteur.getPath().split('/')[(-2)], author.id, author.lastname,
         author.firstname, author.school, ordre,
         self.set2float(author.sponsorasked), self.set2float(author.sponsorSEM),
         self.set2float(author.sponsorRD), self.set2float(author.sponsorSchool))
        self.allauthors += oneauthor
        if self.withTotal:
            self.degrevements[self.objectPath][0] += self.set2float(author.sponsorasked)
            self.degrevements[self.objectPath][1] += self.set2float(author.sponsorSEM)
            self.degrevements[self.objectPath][2] += self.set2float(author.sponsorRD)
            self.degrevements[self.objectPath][3] += self.set2float(author.sponsorSchool)
            self.degrevements[self.objectPath][4] += self.set2float(author.sponsorSchool) + self.set2float(author.sponsorRD) + self.set2float(author.sponsorSEM)
        return (author.sponsorasked, author.sponsorSEM, author.sponsorRD, author.sponsorSchool)

    def multiselect(self, indx='Subject', pathDepth=0):
        self.indx = indx
        self.pathDepth = pathDepth
        catalog = getToolByName(self.context, 'portal_catalog')
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if indx == 'Subject':
            keywords = catalog.uniqueValuesFor('Subject')
            self.multikey = '@@keywordview'
            label = 'Selectionner un ou plusieurs mots-clé'
            self.searchType = IProjet.__identifier__
        else:
            keywords = catalog.uniqueValuesFor('review_state')
            self.multikey = '@@cyclesview'
            label = 'Selectionner un ou plusieurs états'
            self.searchType = ICycle.__identifier__
        form = factory('form', name='search', props={'action': self._form_action})
        form['searchterm'] = factory('#field:multiselect', props={'label': label, 
           'vocabulary': keywords, 
           'format': 'block', 
           'multivalued': True})
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
        query[self.indx] = self.searchterm
        query['object_provides'] = self.searchType
        if self.pathDepth:
            localpath = {'query': ('/').join(context.getPhysicalPath()), 'depth': self.pathDepth}
            query['path'] = localpath
        return cat(**query)

    def _form_action(self, widget, data):
        return '%s/%s' % (self.context.absolute_url(), self.multikey)

    def _form_handler(self, widget, data):
        self.searchterm = data['searchterm'].extracted

    def projets(self, wf_state='all'):
        """Return a catalog search result of projects to show
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        if wf_state == 'all':
            return catalog(portal_type='ageliaco.rd2.projet', path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='start', sort_order='reverse')
        cat = catalog(portal_type='ageliaco.rd2.projet', review_state=wf_state, path={'query': ('/').join(context.getPhysicalPath()), 'depth': 1}, sort_on='sortable_title')
        log('catalogue : %s items' % len(cat))
        return cat

    def cycles(self, projectPath, wf_state='all'):
        """Return a catalog search result of cycles from a project
        """
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        if wf_state == 'all':
            cat = catalog(object_provides=ICycle.__identifier__, path={'query': projectPath, 'depth': 1}, sort_on='modified', sort_order='reverse')
            return cat
        return catalog(object_provides=[ICycle.__identifier__], review_state=wf_state, path={'query': projectPath, 'depth': 2}, sort_on='sortable_title')

    def getPortal(self):
        return getSite()