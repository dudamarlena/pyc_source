# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/repeat/browser/repeatwidget.py
# Compiled at: 2008-12-22 08:23:19
"""The widget for repeated fields.

$Id: repeatwidget.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Arvid'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.interface import implements
from zope.schema.interfaces import ValidationError
from zope.app.form.interfaces import WidgetInputError
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.textwidgets import TextWidget, PasswordWidget
from zope.schema.fieldproperty import FieldProperty
from interfaces import IRepeatWidget
from ks.schema.repeat import _

class NotRepeated(ValidationError):
    __module__ = __name__
    __doc__ = _('Incorrect Repeat')


class RepeatWidget(SimpleInputWidget):
    """base widget to repeat another fields"""
    __module__ = __name__
    implements(IRepeatWidget)
    checkfield = FieldProperty(IRepeatWidget['checkfield'])

    def getInputValue(self):
        value = super(RepeatWidget, self).getInputValue()
        try:
            if self.request.get(self.checkfield) != value:
                raise NotRepeated
        except NotRepeated, v:
            self._error = WidgetInputError(self.context.__name__, self.label, v)
            raise self._error

        return value


class PasswordRepeatWidget(PasswordWidget, RepeatWidget):
    """password repeat widget"""
    __module__ = __name__