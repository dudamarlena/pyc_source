# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/content/address.py
# Compiled at: 2008-09-03 11:14:43
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone.app.content.item import Item
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress

class Address(Item):
    """
    """
    __module__ = __name__
    implements(IAddress)
    portal_type = 'Address'
    firstname = FieldProperty(IAddress['firstname'])
    lastname = FieldProperty(IAddress['lastname'])
    company_name = FieldProperty(IAddress['company_name'])
    address_1 = FieldProperty(IAddress['address_1'])
    zip_code = FieldProperty(IAddress['zip_code'])
    city = FieldProperty(IAddress['city'])
    country = FieldProperty(IAddress['country'])
    phone = FieldProperty(IAddress['phone'])
    email = FieldProperty(IAddress['email'])
    country = ''

    def Title(self):
        """
        """
        return self.getName()

    def getName(self, reverse=False):
        """
        """
        if reverse:
            name = self.lastname
            if name != '':
                name += ', '
            name += self.firstname
        else:
            name = self.firstname
            if name != '':
                name += ' '
            name += self.lastname
        return name


addressFactory = Factory(Address, title=_('Create a new address'))