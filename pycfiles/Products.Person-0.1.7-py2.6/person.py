# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Person/content/person.py
# Compiled at: 2011-06-07 12:12:26
from zope.interface import implements
from Products.CMFCore import permissions
try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Person import config
from Products.Person.interfaces import IPerson
from Products.Person import PersonMessageFactory as _
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import finalizeATCTSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
PersonSchema = ATDocument.schema.copy() + atapi.Schema((
 atapi.StringField(name='firstName', languageIndependent=True, required=True, searchable=True, widget=atapi.StringWidget(label='First name', label_msgid='Person_label_firstName')),
 atapi.StringField(name='middleName', searchable=True, languageIndependent=True, widget=atapi.StringWidget(label='Middle name', label_msgid='Person_label_middleName')),
 atapi.StringField(name='lastName', searchable=True, languageIndependent=True, widget=atapi.StringWidget(label='Last name', label_msgid='Person_label_lastName')),
 atapi.ComputedField(name='title', accessor='Title', user_property='fullname', searchable=True, widget=atapi.ComputedField._properties['widget'](label='Full name', visible={'edit': 'invisible', 'view': 'visible'}, label_msgid='Person_label_fullName')),
 atapi.StringField('contact_email', required=False, searchable=True, languageIndependent=True, validators=('isEmail', ), widget=atapi.StringWidget(description='', label=_('label_contact_email', default='Contact E-mail')))))
finalizeATCTSchema(PersonSchema)

class Person(atapi.OrderedBaseFolder, ATDocument, HistoryAwareMixin):
    """An Archetype for an Person application"""
    implements(IPerson)
    security = ClassSecurityInfo()
    PersonSchema.moveField('firstName', before='description')
    PersonSchema.moveField('middleName', after='firstName')
    PersonSchema.moveField('lastName', after='middleName')
    PersonSchema['text'].widget.label = 'Biography'
    portal_type = meta_type = 'Person'
    schema = PersonSchema
    _at_rename_after_creation = True

    def canSetDefaultPage(self):
        return False

    security.declareProtected(View, 'Title')

    def ContactEmail(self):
        return self.getContact_email()

    def Title(self):
        """Return the Title as firstName middleName(when available) lastName, suffix(when available)"""
        try:
            fn = self.getFirstName()
            ln = self.getLastName()
        except AttributeError:
            return 'new person'
        else:
            if self.getMiddleName():
                mn = ' ' + self.getMiddleName() + ' '
            else:
                mn = ' '

        t = fn + mn + ln
        return t


atapi.registerType(Person, config.PROJECTNAME)