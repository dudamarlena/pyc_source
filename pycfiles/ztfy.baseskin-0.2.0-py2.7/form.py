# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/interfaces/form.py
# Compiled at: 2014-09-23 11:13:48
__docformat__ = 'restructuredtext'
from z3c.form.interfaces import INPUT_MODE, IWidget, ISubForm, ISubmitWidget
from zope.component.interfaces import IObjectEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectModifiedEvent
from zope.viewlet.interfaces import IViewletManager, IViewlet
from zope.interface import Interface, Attribute
from zope.schema import Bool, TextLine, Choice, List, Dict, Object
from ztfy.baseskin import _

class IResetWidget(ISubmitWidget):
    """Reset button widget interface"""
    pass


class ICloseWidget(ISubmitWidget):
    """Close button widget interface"""
    pass


def checkSubmitButton(form):
    """Check form and widgets mode before displaying submit button"""
    if form.mode != INPUT_MODE:
        return False
    for widget in form.widgets.values():
        if widget.mode == INPUT_MODE:
            return True

    if IForm.providedBy(form):
        for subform in form.subforms:
            for widget in subform.widgets.values():
                if widget.mode == INPUT_MODE:
                    return True


class IWidgetsGroup(Interface):
    """Form widgets group interface"""
    id = TextLine(title=_('Group ID'), required=False)
    css_class = TextLine(title=_('CSS class'), required=False)
    legend = TextLine(title=_('Group legend'), required=False)
    help = TextLine(title=_('Group help'), required=False)
    widgets = List(title=_("Group's widgets list"), value_type=Object(schema=IWidget))
    switch = Bool(title=_('Switchable group?'), required=True, default=False)
    checkbox_switch = Bool(title=_('Group switched via checkbox?'), required=True, default=False)
    checkbox_field = TextLine(title=_('Field name matching switch checkbox?'), required=False)
    checkbox_widget = Object(schema=IWidget, required=False)
    checkbox_on = Attribute(_('Checkbox on?'))
    hide_if_empty = Bool(title=_('Hide group if empty?'), description=_("If 'Yes', a switchable group containing only widgets with default values is hidden"), required=True, default=False)
    visible = Attribute(_('Visible group?'))
    switchable = Attribute(_('Switchable group?'))


class IBaseForm(Interface):
    """Marker interface for any form"""
    pass


class IGroupsBasedForm(IBaseForm):
    """Groups based form"""
    groups = Attribute(_('Form groups'))

    def addGroup(self, group):
        """Add given group to form"""
        pass


class IForm(IBaseForm):
    """Base form interface"""
    title = TextLine(title=_('Form title'))
    legend = TextLine(title=_('Form legend'), required=False)
    subforms = List(title=_('Sub-forms'), value_type=Object(schema=ISubForm), required=False)
    subforms_legend = TextLine(title=_('Subforms legend'), required=False)
    tabforms = List(title=_('Tab-forms'), value_type=Object(schema=ISubForm), required=False)
    autocomplete = Choice(title=_('Auto-complete'), values=('on', 'off'), default='on')
    label_css_class = TextLine(title=_('Labels CSS class'), required=False, default='control-label col-md-3')
    input_css_class = TextLine(title=_('Inputs CSS class'), required=False, default='col-md-9')
    display_hints_on_widgets = Bool(title=_('Display hints on input widgets?'), required=True, default=False)
    handle_upload = Bool(title=_('Handle uploads in form?'), description=_('Set to true when form handle uploads to get progress bar'), required=True, default=False)
    callbacks = Dict(title=_('Widgets validation callbacks'), key_type=TextLine(), value_type=TextLine(), required=False)

    def isDialog(self):
        """Check to know if current form is in a modal dialog"""
        pass

    def getForms(self):
        """Get full list of main form and subforms"""
        pass

    def createSubForms(self):
        """Initialize sub-forms"""
        pass

    def createTabForms(self):
        """Initialize tab-forms"""
        pass

    def getWidgetCallback(self, widget):
        """Get submit callback associated with a given widget"""
        pass

    def updateContent(self, object, data):
        """Update given object with form data"""
        pass

    def getSubmitOutput(self, writer, changes):
        """Get submit output"""
        pass


class IAJAXForm(IForm):
    """AJAX form interface"""
    handler = TextLine(title=_('Form AJAX handler'), description=_('Relative URL of AJAX handler'), required=False)
    data_type = Choice(title=_('Form AJAX data type'), description=_(''), required=False, values=('json',
                                                                                                  'jsonp',
                                                                                                  'text',
                                                                                                  'html',
                                                                                                  'xml',
                                                                                                  'script'))
    form_options = Dict(title=_('Form AJAX data options'), required=False)
    callback = TextLine(title=_('Submit callback'), description=_('Name of a custom form submit callback'), required=False)

    def getFormOptions(self):
        """Get custom AJAX POST data"""
        pass

    def getAjaxErrors(self):
        """Get errors associated with their respective widgets in a JSON dictionary"""
        pass


class IInnerSubForm(ISubForm):
    """Inner subform marker interface"""
    pass


class IInnerTabForm(ISubForm):
    """Inner tabform marker interface"""
    tabLabel = TextLine(title=_('Tab label'), required=True)


class IViewletsBasedForm(IForm):
    """Viewlets based form interface"""
    managers = List(title=_('Names list of viewlets managers included in this form'), value_type=TextLine(), required=True)


class ISubFormViewlet(IViewlet):
    """Sub-form viewlet interface"""
    legend = Attribute(_('Sub-form legend'))
    switchable = Attribute(_('Can the subform be hidden ?'))
    visible = Attribute(_('Is the subform initially visible ?'))
    callbacks = Dict(title=_('Widgets callbacks'), key_type=TextLine(), value_type=TextLine())

    def getWidgetCallback(self, widget):
        """Get submit callback associated with a given widget"""
        pass


class ICustomExtractSubForm(ISubForm):
    """SubForm interface with custom extract method"""

    def extract(self):
        """Extract data and errors from input request"""
        pass


class ICustomUpdateSubForm(ISubForm):
    """SubForm interface with custom update method"""

    def updateContent(self, object, data):
        """Update custom content with given data"""
        pass


class IFormViewletsManager(IViewletManager):
    """Base forms viewlets manager interface"""
    pass


class IFormPrefixViewletsManager(IFormViewletsManager):
    """Form prefix viewlets manager interface"""
    pass


class IWidgetsPrefixViewletsManager(IFormViewletsManager):
    """Form widgets prefix viewlets manager interface"""
    pass


class IWidgetsSuffixViewletsManager(IFormViewletsManager):
    """Form widgets suffix viewlets manager interface"""
    pass


class IFormSuffixViewletsManager(IFormViewletsManager):
    """Form suffix viewlets manager interface"""
    pass


class IViewObjectEvent(IObjectEvent):
    """View object event interface"""
    view = Attribute(_('View in which event was fired'))


class IFormObjectCreatedEvent(IObjectCreatedEvent, IViewObjectEvent):
    """Object added event notify by form after final object creation"""
    pass


class IFormObjectModifiedEvent(IObjectModifiedEvent, IViewObjectEvent):
    """Form object modified event interface"""
    pass