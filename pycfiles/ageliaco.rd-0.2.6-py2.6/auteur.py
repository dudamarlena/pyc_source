# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/auteur.py
# Compiled at: 2012-01-06 07:43:53
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from ageliaco.rd import _
from attribution import schools
from plone.app.textfield import RichText
import datetime
from plone.indexer import indexer
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
import unicodedata
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

class SchoolsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        for school in schools.keys():
            terms.append(SimpleVocabulary.createTerm(unicodedata.normalize('NFKC', school).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', schools[school][0]).encode('ascii', 'ignore'), unicodedata.normalize('NFKC', schools[school][0]).encode('ascii', 'ignore')))

        return SimpleVocabulary(terms)


grok.global_utility(SchoolsVocabulary, name='ageliaco.rd.schools')

class IAuteur(form.Schema):
    """
    Auteur de projet
    """
    id = schema.TextLine(title=_('id'), description=_('Identifiant (login)'), required=True)
    lastname = schema.TextLine(title=_('Nom'), description=_('Nom de famille'), required=True)
    firstname = schema.TextLine(title=_('Prénom'), description=_('Prénom'), required=True)
    school = schema.Choice(title=_('Ecole'), description=_('Etablissement scolaire de référence'), vocabulary='ageliaco.rd.schools', required=True)
    address = schema.Text(title=_('Adresse'), description=_('Adresse postale'), required=False)
    email = schema.TextLine(title=_('Email'), description=_('Adresse courrielle'), required=True)
    phone = schema.TextLine(title=_('Téléphone'), description=_('Téléphone'), required=False)


@grok.subscribe(IAuteur, IObjectAddedEvent)
def setAuteur(auteur, event):
    portal_url = getToolByName(auteur, 'portal_url')
    acl_users = getToolByName(auteur, 'acl_users')
    portal = portal_url.getPortalObject()
    cycles = auteur.aq_parent
    print 'auteur id : ' + auteur.id
    user = acl_users.getUserById(auteur.id)
    if user is not None:
        member_name = user.getProperty('fullname') or auteur.id
        auteur.email = user.getProperty('email') or ''
        auteur.firstname = user.getProperty('firstname') or ''
        auteur.lastname = user.getProperty('lastname') or ''
        auteur.school = user.getProperty('school')
        schools = auteur.school
        print 'Ecoles : ' + schools
        if schools in [list, tuple] and len(schools) > 0:
            auteur.school = schools[0]
        print 'auteur : %s %s, %s, %s' % (auteur.firstname, auteur.lastname, auteur.email, auteur.school)
    return