# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/note.py
# Compiled at: 2013-02-25 07:53:40
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from ageliaco.rd2 import MessageFactory
import datetime
from Acquisition import aq_inner, aq_parent
from plone.app.textfield import RichText
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

@grok.provider(IContextSourceBinder)
def possibleAttendees(context):
    acl_users = getToolByName(context, 'acl_users')
    parent = context.__parent__
    terms = []
    group = parent.getContributor()
    group.append(parent.getSupervisor())
    group.append(parent.getSupervisor2())
    if group is not None:
        for member in group:
            terms.append(member)

    return SimpleVocabulary(terms)


class INote(form.Schema):
    """
    Note de suivi de rendez-vous
    """
    title = schema.TextLine(title=MessageFactory('Titre'), required=False)
    presence = schema.Text(title=MessageFactory('Personnes présentes'), required=False)
    absence = schema.Text(title=MessageFactory('Personnes absentes'), required=False)
    presentation = RichText(title=MessageFactory('Notes de séance'), description=MessageFactory("Compte-rendu de l'avancement du projet"), required=False)
    dexterity.read_permission(reviewNotes='cmf.ReviewPortalContent')
    dexterity.write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = RichText(title=MessageFactory('Notes internes'), description=MessageFactory('Notes visibles que par R&D'), required=False)
    nextmeeting = schema.Datetime(title=MessageFactory('Date du prochain rendez-vous'), required=False)
    meetingplace = schema.TextLine(title=MessageFactory('Lieu du prochain rendez-vous'), required=False)


@form.default_value(field=INote['title'])
def startDefaultValue(data):
    day = datetime.datetime.today()
    return 'Note-' + day.strftime('%Y-%m-%d')