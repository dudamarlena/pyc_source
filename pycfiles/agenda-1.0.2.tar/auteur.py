# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/auteur.py
# Compiled at: 2013-02-25 07:53:40
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from ageliaco.rd2 import MessageFactory
from interface import IAuteur
from plone.app.textfield import RichText
import datetime
from plone.indexer import indexer
from plone.formwidget.autocomplete import AutocompleteFieldWidget
import unicodedata
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

@indexer(IAuteur)
def searchableIndexer(context):
    return '%s %s %s %s %s %s' % (context.firstname,
     context.lastname,
     context.address,
     context.email,
     context.school,
     context.phone)


grok.global_adapter(searchableIndexer, name='SearchableText')

@indexer(IAuteur)
def firstnameIndexer(obj):
    if obj.firstname is None:
        return
    else:
        return obj.firstname


grok.global_adapter(firstnameIndexer, name='firstname')

@indexer(IAuteur)
def lastnameIndexer(obj):
    if obj.lastname is None:
        return
    else:
        return obj.lastname


grok.global_adapter(lastnameIndexer, name='lastname')

@indexer(IAuteur)
def emailIndexer(obj):
    if obj.email is None:
        return
    else:
        return obj.email


grok.global_adapter(emailIndexer, name='email')

@indexer(IAuteur)
def schoolIndexer(obj):
    if obj.school is None:
        return
    else:
        return obj.school


grok.global_adapter(schoolIndexer, name='school')

@indexer(IAuteur)
def sponsoraskedIndexer(obj):
    if obj.sponsorasked is None:
        return
    else:
        return obj.sponsorasked


grok.global_adapter(sponsoraskedIndexer, name='sponsorasked')

@indexer(IAuteur)
def sponsorSEMIndexer(obj):
    if obj.sponsorSEM is None:
        return
    else:
        return obj.sponsorSEM


grok.global_adapter(sponsorSEMIndexer, name='sponsorSEM')

@indexer(IAuteur)
def sponsorSchoolIndexer(obj):
    if obj.sponsorSchool is None:
        return
    else:
        return obj.sponsorSchool


grok.global_adapter(sponsorSchoolIndexer, name='sponsorSchool')

@indexer(IAuteur)
def sponsorRDIndexer(obj):
    if obj.sponsorRD is None:
        return
    else:
        return obj.sponsorRD


grok.global_adapter(sponsorRDIndexer, name='sponsorRD')