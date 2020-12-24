# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\test_form_controllers.py
# Compiled at: 2011-07-14 09:46:05
from datetime import datetime
import cherrypy
from turbogears import config, controllers, expose, mochikit, testutil, validate, validators, widgets
from turbogears.testutil import make_app

def setup_module():
    global app
    app = make_app(MyRoot)
    testutil.start_server()


def teardown_module():
    testutil.stop_server()


class MyFormFields(widgets.WidgetsList):
    __module__ = __name__
    name = widgets.TextField(validator=validators.String())
    age = widgets.TextField(validator=validators.Int(), default=0)
    date = widgets.CalendarDatePicker(validator=validators.DateConverter(if_empty=datetime.now()))


myfields = MyFormFields()
myform = widgets.TableForm(fields=MyFormFields())

class State(object):
    __module__ = __name__
    counter = 0


class AddingValidator(validators.FancyValidator):
    __module__ = __name__

    def _to_python(self, value, state=None):
        state.counter += 1
        return value


class AddingSchema(validators.Schema):
    __module__ = __name__
    a = AddingValidator()
    b = AddingValidator()


class AddingNestedSchema(AddingSchema):
    __module__ = __name__
    c = AddingSchema()


class MyTableForm(widgets.TableForm):
    __module__ = __name__
    fields = MyFormFields()
    j0 = widgets.JSSource('js_order=5;', order=5)
    j1 = widgets.JSSource('js_def_order')
    mochikit.order = 10
    css0 = widgets.CSSSource('CSS_order:4-1', order=4)
    css1 = widgets.CSSSource('CSS_order:-3', order=-3)
    css2 = widgets.CSSSource('CSS_order:4-2', order=4)
    javascript = [
     mochikit, j0, j1]
    css = [css0, css1, css2]


myform2 = MyTableForm()

class MyRoot(controllers.RootController):
    __module__ = __name__

    @expose('kid:turbogears.tests.form')
    def index(self):
        return dict(form=myform)

    @expose('kid:turbogears.tests.form')
    def fields(self):
        myfields.display = lambda **kw: kw.values()
        return dict(form=myfields)

    @expose('kid:turbogears.tests.form')
    def usemochi(self):
        return dict(mochi=mochikit, form=myform)

    @expose('kid:turbogears.tests.form')
    def order_js_css(self):
        return dict(form=myform2)

    @expose('kid:turbogears.tests.othertemplate')
    @validate(form=myform)
    def testform(self, name, date, age, tg_errors=None):
        if tg_errors:
            self.has_errors = True
        return dict(name=name, user_age=age, birthdate=date)

    @expose()
    @validate(form=myform)
    def testform_new_style(self, name, date, age):
        if cherrypy.request.validation_errors:
            self.has_errors = True
        return dict(name=name, age=age, date=date)

    @expose()
    @validate(validators=AddingNestedSchema(), state_factory=State)
    def validation(self, a, b, c):
        return 'counter: %d' % cherrypy.request.validation_state.counter


def test_form_translation():
    """Form input is translated into properly converted parameters"""
    response = app.get('/testform?name=ed&date=11/05/2005&age=5')
    assert response.raw['name'] == 'ed'
    assert response.raw['user_age'] == 5


def test_form_translation_new_style():
    """Form input is translated into properly converted parameters (new style)"""
    response = app.get('/testform_new_style?name=ed&date=11/05/2005&age=5&')
    assert response.raw['name'] == 'ed'
    assert response.raw['age'] == 5


def test_invalid_form_with_error_handling():
    """Invalid forms can be handled by the method"""
    response = app.get('/testform?name=ed&age=edalso&date=11/05/2005')
    assert 'This is the other template.' in response.body


def test_css_should_appear():
    """CSS should appear when asked for"""
    response = app.get('/')
    assert 'calendar-system.css' in response
    response = app.get('/fields')
    assert 'calendar-system.css' in response


def test_javascript_should_appear():
    """JavaScript should appear when asked for"""
    response = app.get('/')
    assert 'calendar.js' in response
    response = app.get('/fields')
    assert 'calendar.js' in response


def test_include_mochikit():
    """JSLinks (and MochiKit especially) can be included easily"""
    response = app.get('/usemochi')
    assert 'MochiKit.js' in response


def test_js_order():
    response = app.get('/order_js_css')
    assert 'MochiKit.js' in response
    assert 'js_order=5;' in response
    assert 'js_def_order' in response
    assert response.body.find('js_def_order') < response.body.find('js_order=5;')
    assert response.body.find('js_order=5;') < response.body.find('MochiKit.js')
    assert 'CSS_order:4-1' in response
    assert 'CSS_order:4-2' in response
    assert 'CSS_order:-3' in response
    assert response.body.find('CSS_order:4-1') < response.body.find('CSS_order:4-2')
    assert response.body.find('CSS_order:-3') < response.body.find('CSS_order:4-1')


def test_suppress_mochikit():
    """MochiKit inclusion can be suppressed"""
    config.update({'global': {'tg.mochikit_suppress': True}})
    suppressed = app.get('/usemochi')
    config.update({'global': {'tg.mochikit_suppress': False}})
    included = app.get('/usemochi')
    assert 'MochiKit.js' not in suppressed.body
    assert 'MochiKit.js' in included.body


def test_mochikit_everywhere():
    """MochiKit can be included everywhere by setting tg.mochikit_all"""
    config.update({'global': {'tg.mochikit_all': True}})
    response = app.get('/')
    config.update({'global': {'tg.mochikit_all': False}})
    assert 'MochiKit.js' in response


def test_mochikit_nowhere():
    """Setting tg.mochikit_suppress will prevent including it everywhere"""
    config.update({'global': {'tg.mochikit_all': True}})
    config.update({'global': {'tg.mochikit_suppress': True}})
    response = app.get('/')
    config.update({'global': {'tg.mochikit_all': False}})
    config.update({'global': {'tg.mochikit_suppress': False}})
    assert 'MochiKit.js' not in response


def test_include_widgets():
    """Any widget can be included everywhere by setting tg.include_widgets"""
    config.update({'global': {'tg.include_widgets': ['mochikit']}})
    response = app.get('/')
    config.update({'global': {'tg.include_widgets': []}})
    assert 'MochiKit.js' in response


def test_counter_is_incremented():
    url = '/validation?a=1&b=2&c.a=3&c.b=4'
    response = app.get(url)
    msg = 'Validation state is not handled properly'
    assert 'counter: 4' in response.body, msg