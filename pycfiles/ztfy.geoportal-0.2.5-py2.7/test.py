# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/geoportal/browser/test.py
# Compiled at: 2012-07-04 13:23:38
from persistent import Persistent
from z3c.form import field
from zope.container.contained import Contained
from zope.interface import implements, Interface
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.geoportal.schema import LocationField
from ztfy.skin.form import AddForm, EditForm
from ztfy.skin.menu import MenuItem

class IGeoportalTest(Interface):
    """GeoPortal test interface"""
    title = TextLine(title='Title', required=True)
    location = LocationField(title='GPS location', required=False)


class GeoportalTest(Persistent, Contained):
    """GeoPortal test class"""
    implements(IGeoportalTest)
    title = FieldProperty(IGeoportalTest['title'])
    location = FieldProperty(IGeoportalTest['location'])


class GeoportalTestAddFormMenuItem(MenuItem):
    """GeoPortal test add menu item"""
    title = ':: Add GeoPortal test...'


class GeoportalTestAddForm(AddForm):
    """GeoPortal test add form"""
    fields = field.Fields(IGeoportalTest)

    def create(self, data):
        test = GeoportalTest()
        test.title = data.get('title')
        return test

    def add(self, object):
        self.context[object.title] = object

    def nextURL(self):
        return '%s/@@contents.html' % absoluteURL(self.context, self.request)


class GeoportalTestEditForm(EditForm):
    """GeoPortal test edit form"""
    fields = field.Fields(IGeoportalTest)