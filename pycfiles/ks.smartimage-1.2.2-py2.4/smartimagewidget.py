# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimageschema/smartimagewidget.py
# Compiled at: 2008-12-23 17:55:58
"""SmartImageWidger widget for the Zope 3 based smartimage package

$Id: smartimagewidget.py 12526 2007-10-31 16:50:35Z cray $
"""
__author__ = 'Andrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 12526 $'
__date__ = '$Date: 2007-10-31 18:50:35 +0200 (Wed, 31 Oct 2007) $'
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget as ObjectWidgetBase
from ks.smartimage.smartimage import SmartImage
from zope.security.proxy import removeSecurityProxy
from zope.app.form.utility import setUpWidgets, applyWidgetsChanges
from zope.app.container.contained import containedEvent, contained, ObjectAddedEvent
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.zapi import absoluteURL
from zope.app.form.browser.widget import renderElement
from zope.interface import Interface
from zope.component import ComponentLookupError, getUtility, getMultiAdapter
from ks.smartimage.smartimagecache.interfaces import ISmartImageProp
from ks.smartimage.smartimageadapter.interfaces import ISmartImageContainer
from smartimagedisplaywidget import ImageDisplay

class ObjectWidget(ImageDisplay, ObjectWidgetBase):
    __module__ = __name__

    def getInputValue(self):
        ob = removeSecurityProxy(super(ObjectWidget, self).getInputValue())
        return ob

    def applyChanges(self, content):
        field = self.context
        value = field.query(content, None)
        if value is None:
            value = self.factory()
        changes = applyWidgetsChanges(self, field.schema, target=value, names=self.names)
        if changes:
            if 'clearData' in self.names:
                clear = self.clearData_widget.getInputValue()
                if clear:
                    value.contentType = ''
                    value.data = ''
            field.set(content, value)
            return True
        return False

    def __call__(self):
        value = self.context.query(self.context.context, None)
        if value is None or value == self.context.missing_value:
            value = self.factory()
        return ('\n').join([self.imagedisplay(value), super(ObjectWidget, self).__call__()])


SmartImageWidget = CustomWidgetFactory(ObjectWidget, SmartImage)