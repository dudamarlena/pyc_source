# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/widget.py
# Compiled at: 2014-04-02 10:53:17
from z3c.form.interfaces import IFormLayer, IFieldWidget
from ztfy.baseskin.interfaces.form import IResetWidget, ICloseWidget
from ztfy.baseskin.schema import IResetButton, ICloseButton
from z3c.form.action import Action
from z3c.form.browser.submit import SubmitWidget
from z3c.form.button import ButtonAction
from z3c.form.widget import FieldWidget
from zope.component import adapter, adapts
from zope.interface import implementer, implementsOnly

class ResetWidget(SubmitWidget):
    """A reset button of a form."""
    implementsOnly(IResetWidget)
    klass = 'reset-widget'
    css = 'reset'


@adapter(IResetButton, IFormLayer)
@implementer(IFieldWidget)
def ResetFieldWidget(field, request):
    reset = FieldWidget(field, ResetWidget(request))
    reset.value = field.title
    return reset


class ResetButtonAction(ResetWidget, ButtonAction):
    """Reset button action"""
    adapts(IFormLayer, IResetButton)

    def __init__(self, request, field):
        Action.__init__(self, request, field.title)
        ResetWidget.__init__(self, request)
        self.field = field


class CloseWidget(SubmitWidget):
    """A dialog close button"""
    implementsOnly(ICloseWidget)
    klass = 'close-widget'
    css = 'close'


@adapter(ICloseButton, IFormLayer)
@implementer(IFieldWidget)
def CloseFieldWidget(field, request):
    close = FieldWidget(field, CloseWidget(request))
    close.value = field.title
    return close


class CloseButtonAction(CloseWidget, ButtonAction):
    """Close button action"""
    adapts(IFormLayer, ICloseButton)

    def __init__(self, request, field):
        Action.__init__(self, request, field.title)
        CloseWidget.__init__(self, request)
        self.field = field