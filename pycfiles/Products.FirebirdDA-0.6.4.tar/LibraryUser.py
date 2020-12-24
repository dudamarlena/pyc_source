# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/FinisAfricae/content/LibraryUser.py
# Compiled at: 2008-07-28 16:57:49
from os.path import join
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Acquisition import aq_chain, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.utils import createViewName, classImplements, implementedBy
from Products.Archetypes.public import *
from Products.ATSchemaEditorNG.ParentManagedSchema import ParentOrToolManagedSchema
from Products.Membrane.interfaces.group import IGroup
from Products.Membrane.interfaces.user import IUser
from Products.Membrane.types.UserMixin import Authentication, Properties, Groups
LibraryUserSchema = BaseSchema + Schema((
 StringField('userName', languageIndependent=1, searchable=1, required=1, widget=StringWidget(description='Username for a person.')),
 StringField('password', languageIndependent=1, required=1, searchable=0, widget=StringWidget(description='Password.')),
 StringField('firstname', searchable=1, required=1, schemata='personal', widget=StringWidget(label='Firstname', label_msgid='label_firstname', description=None, description_msgid='help_firstname')),
 StringField('surname', searchable=1, required=1, schemata='personal', widget=StringWidget(label='Surname', label_msgid='label_surname', description=None, description_msgid='help_surname')),
 StringField('gender', vocabulary='getGenderList', schemata='personal', widget=SelectionWidget(format='select', label='Gender', label_msgid='label_gender', description=None, description_msgid='help_gender')),
 StringField('address', searchable=1, required=1, schemata='personal', widget=StringWidget(label='Address', label_msgid='label_address', description=None, description_msgid='help_address')),
 StringField('city', searchable=1, required=1, schemata='personal', widget=StringWidget(label='City', label_msgid='label_city', description=None, description_msgid='help_city')),
 StringField('zipcode', searchable=1, required=1, schemata='personal', widget=StringWidget(label='ZIP', label_msgid='label_zipcode', description=None, description_msgid='help_zipcode')),
 StringField('state', searchable=1, required=1, schemata='personal', widget=StringWidget(label='State', label_msgid='label_state', description=None, description_msgid='help_state')),
 StringField('country', searchable=1, required=1, schemata='personal', vocabulary='getCountryList', widget=StringWidget(label='Country', label_msgid='label_country', description=None, description_msgid='help_country')),
 StringField('email', searchable=1, schemata='personal', widget=StringWidget(label='e-Mail', label_msgid='label_email', description=None, description_msgid='help_email'))))

class LibraryUser(ParentOrToolManagedSchema, Authentication, Properties, Groups, BaseContent):
    """ Library User
    """
    schema = LibraryUserSchema
    archetype_name = 'Library User'
    portal_type = meta_type = 'LibraryUser'
    global_allow = 0
    security = ClassSecurityInfo()
    _at_rename_after_creation = True

    def getSelectionValues(self, prop_name):
        """make vocabulary out of given property"""
        pp = getToolByName(self, 'portal_properties')
        ip = getattr(pp, 'atcontent_type_properties')
        labels = ip.getProperty(prop_name, [])
        values = list(labels)
        del values[0]
        values.insert(0, '')
        return DisplayList(zip(values, labels))

    def getCountryList(self):
        """vocabulary of countries """
        labels = ('Argentina', 'Uruguay')
        values = list(labels)
        return DisplayList(zip(values, labels))

    def getGenderList(self):
        """vocabulary of genders"""
        labels = ('Mujer', 'Hombre')
        values = list(labels)
        return DisplayList(zip(values, labels))

    def getSchema(self):
        """override variable schema"""
        return self.schema

    def getPhones(self):
        """generate phones string"""
        phones = []
        if self.getPhone():
            phones.append(self.getPhone())
        if self.getPhone2():
            phones.append(self.getPhone2())
        if self.getMobiel():
            phones.append(self.getMobiel())
        return phones

    def getFullName(self):
        """compute the full name"""
        name = []
        if self.getFirstname():
            name.append(self.getFirstname())
        if self.getSurname():
            name.append(self.getSurname())
        res = (' ').join(name)
        return res.lstrip()

    def manage_afterAdd(self, item, container):
        self.updateSchemaFromEditor()
        BaseContent.manage_afterAdd(self, item, container)

    def _getPassword(self):
        return self.Schema()['password'].get(self)

    def getUserId(self):
        return self.UID()

    def getUserName(self):
        return self.getFullName()

    security.declarePrivate('getUserPropertySchematas')

    def getUserPropertySchemata(self):
        return [
         'userinfo']

    security.declarePrivate('getGroupRelationships')

    def getGroupRelationships(self):
        return [
         'participatesInProject']


classImplements(LibraryUser, *(tuple(implementedBy(LibraryUser)) + (
 IUser,)))
registerType(LibraryUser)