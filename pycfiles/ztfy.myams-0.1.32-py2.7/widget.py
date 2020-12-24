# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/widget.py
# Compiled at: 2015-12-07 08:24:14
__docformat__ = 'restructuredtext'
from z3c.form.interfaces import IFieldWidget
from ztfy.myams.interfaces.widget import ISelect2Widget
from zope.schema.interfaces import IChoice
from z3c.form.browser.select import SelectWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer, implementer_only
from ztfy.myams.layer import MyAMSLayer
from ztfy.myams import _

@implementer_only(ISelect2Widget)
class Select2Widget(SelectWidget):
    """Select2 widget"""
    noValueMessage = _('(no selected value)')

    def get_content(self, entry):
        return translate(entry['content'], context=self.request)


@adapter(IChoice, MyAMSLayer)
@implementer(IFieldWidget)
def ChoiceFieldWidget(field, request):
    return FieldWidget(field, Select2Widget(request))