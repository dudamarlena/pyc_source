# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/p10userdata/userdataschema.py
# Compiled at: 2011-10-06 05:10:48
from zope.interface import Interface, implements
from zope import schema
from ageliaco.p10userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

def validateAccept(value):
    if not value == True:
        return False
    return True


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    firstname = schema.TextLine(title=_('label_firstname', default='First name'), description=_('help_firstname', default='Fill in your given name.'), required=False)
    lastname = schema.TextLine(title=_('label_lastname', default='Last name'), description=_('help_lastname', default='Fill in your surname or your family name.'), required=False)
    school = schema.TextLine(title=_('label_scool', default='School'), description=_('help_school', default='Fill in the school which is responsible for you.'), required=False)
    reference = schema.TextLine(title=_('label_reference', default='Reference number'), description=_('help_reference', default='Institutional reference number'), required=False)