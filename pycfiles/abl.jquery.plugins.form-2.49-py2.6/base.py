# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/abl/jquery/examples/form/base.py
# Compiled at: 2011-02-18 13:05:59
from formencode.validators import NotEmpty
from tg import TGController, expose, validate
from tg import tmpl_context as c
from tg.decorators import with_trailing_slash
from tw.api import WidgetsList
from tw.forms import TableForm, TextField
from abl.jquery.core.widgets import AjaxUpdateContentWidget
from abl.jquery.plugins.form.widgets import AjaxFormMixin, AjaxFormUpdateMixin

class MyForm(TableForm, AjaxFormMixin):

    class children(WidgetsList):
        text = TextField(validator=NotEmpty())


class MyUpdateForm(TableForm, AjaxFormUpdateMixin):

    class children(WidgetsList):
        text = TextField(validator=NotEmpty())


my_form = MyForm('my_form', action='submit/')
my_update_form = MyUpdateForm('my_update_form', action='submit_update/')
update_widget = AjaxUpdateContentWidget('update_widget')

class FormController(TGController):

    @expose('abl.jquery.examples.form.templates.index')
    @with_trailing_slash
    def index(self, **kwargs):
        c.my_form = my_form
        c.my_update_form = my_update_form
        c.update_widget = update_widget
        return dict()

    @expose('abl.jquery.plugins.form.templates.error_handler')
    def submit_error_handler(self, **kwargs):
        c.form = my_form
        return dict()

    @expose('abl.jquery.examples.form.templates.submit')
    @with_trailing_slash
    @validate(form=my_form, error_handler=submit_error_handler)
    def submit(self, text):
        return dict(text=text)

    @expose('abl.jquery.core.templates.update_content')
    @with_trailing_slash
    def get_form(self):
        return dict(content=dict(formbox=my_form()))

    @expose('abl.jquery.plugins.form.templates.error_handler')
    def submit_update_error_handler(self, **kwargs):
        c.form = my_update_form
        return dict()

    @expose('abl.jquery.core.templates.update_content')
    @with_trailing_slash
    @validate(form=my_update_form, error_handler=submit_update_error_handler)
    def submit_update(self, text):
        return dict(content=dict(formbox2=my_update_form(), result=text))