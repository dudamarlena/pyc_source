# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/prototype/examples/tg2/browser.py
# Compiled at: 2008-06-02 11:15:04
from tg import expose, flash, redirect, TGController
import pylons
from toscawidgets.widgets.forms.fields import *
from toscawidgets.widgets.prototype.activeform import ActiveForm
from twtools.frameworks.tg2.activeform import ActiveFormResponseHandler
from formencode.validators import Int, String
children = [
 TextField('non_empty_string', validator=String(not_empty=True)),
 TextField('integer', validator=Int())]
activeForm = ActiveForm(id='myActiveForm', action='submit', children=children, clear_on_success=True, on_success="console.log('hello!')")

class ActiveFormBrowser(TGController):

    @expose('toscawidgets.widgets.prototype.examples.tg2.templates.index')
    def form(self, **kw):
        pylons.c.w.widget = activeForm
        return dict()

    def submitSuccess(self, **kw):
        print kw

    activeFormHandler = ActiveFormResponseHandler(activeForm, submitSuccess)
    submit = activeFormHandler.ajax_submit

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        tmpl_context.w = WidgetBunch()
        try:
            return TGController.__call__(self, environ, start_response)
        finally:
            pass