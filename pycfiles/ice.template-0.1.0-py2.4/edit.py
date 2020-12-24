# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/browser/edit.py
# Compiled at: 2009-05-04 14:30:04
from Cheetah.Template import Template
from z3c.formui import form
from z3c.form import field, button
from zope.schema import Text
from ice.template import _
TFIELD_NAME = 'body'

class Pagelet(form.EditForm):
    __module__ = __name__
    form.extends(form.EditForm)
    fields = field.Fields(field.Field(Text(required=False), name=TFIELD_NAME))
    ignoreContext = True
    templates = property(lambda self: self.context.__parent__)
    tname = property(lambda self: self.context.__name__)
    preview = None

    def updateWidgets(self):
        super(Pagelet, self).updateWidgets()
        widget = self.widgets[TFIELD_NAME]
        if not self.request.get(widget.name):
            widget.value = self.templates.getTemplate(self.tname)

    def checkVariables(self):
        varnames = self.templates.getVariables(self.tname)
        variables = dict(((v, '***') for v in varnames))
        text = self.extractData()[0].get(TFIELD_NAME)
        try:
            return unicode(Template(text, variables))
        except:
            return

        return

    def applyChanges(self, data):
        if self.checkVariables() is not None:
            return super(Pagelet, self).applyChanges(data)
        self.noChangesMessage = _('There are some errors in the template')
        return

    @button.buttonAndHandler(_('Reset from source'))
    def handleReset(self, action):
        self.widgets[TFIELD_NAME].value = self.templates.getSource(self.tname)

    @button.buttonAndHandler(_('Refresh'))
    def handleRefresh(self, action):
        self.widgets[TFIELD_NAME].value = self.templates.getTemplate(self.tname)

    @button.buttonAndHandler(_('Preview and Test'))
    def handlePreview(self, action):
        self.preview = self.checkVariables()
        self.status = self.preview is not None and _('Ok') or _('There are some errors in the template')
        return


class TemplateTextField(object):
    __module__ = __name__
    query = lambda self, *args: self.get()
    canAccess = lambda self: True
    canWrite = lambda self: True

    def __init__(self, context, field):
        self.templates = context.__parent__
        self.name = context.__name__
        self.field = field

    def get(self):
        return self.templates.getTemplate(self.name)

    def set(self, value):
        self.templates.setTemplate(self.name, value)