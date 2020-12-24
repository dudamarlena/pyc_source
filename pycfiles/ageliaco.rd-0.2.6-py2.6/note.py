# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/note.py
# Compiled at: 2011-10-12 13:31:11
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from ageliaco.rd import _
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
    title = schema.TextLine(title=_('Titre'), required=False)
    presence = schema.Text(title=_('Personnes présentes'), required=False)
    absence = schema.Text(title=_('Personnes absentes'), required=False)
    presentation = RichText(title=_('Notes de séance'), description=_("Compte-rendu de l'avancement du projet"), required=False)
    dexterity.read_permission(reviewNotes='cmf.ReviewPortalContent')
    dexterity.write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = RichText(title=_('Notes internes'), description=_('Notes visibles que par R&D'), required=False)
    nextmeeting = schema.Date(title=_('Date du prochain rendez-vous'), required=False)
    meetingplace = schema.TextLine(title=_('Lieu du prochain rendez-vous'), required=False)


@form.default_value(field=INote['title'])
def startDefaultValue(data):
    day = datetime.datetime.today()
    return 'Note-' + day.strftime('%Y-%m-%d')