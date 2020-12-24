# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\tests\test_nested_form_controllers.py
# Compiled at: 2011-07-14 07:57:24
from turbogears import controllers, error_handler, expose, testutil, validate, validators, widgets

def setup_module():
    global app
    app = testutil.make_app(NestedFormController)
    testutil.start_server()


def teardown_module():
    testutil.stop_server()


nestedform = widgets.TableForm(fields=[widgets.FieldSet(name='p_data', fields=[widgets.TextField(name='name'), widgets.TextField(name='age', validator=validators.Int())])])

class NestedFormController(controllers.RootController):
    __module__ = __name__

    def set_errors(self):
        return dict(has_errors=True)

    @expose()
    @error_handler(set_errors)
    @validate(nestedform)
    def testform(self, p_data):
        name = p_data['name']
        age = p_data['age']
        return dict(name=name, age=age)


def test_form_translation_new_style():
    """Form input is translated into properly converted parameters"""
    response = app.get('/testform?p_data.name=ed&p_data.age=5')
    assert response.raw['name'] == 'ed'
    assert response.raw['age'] == 5


def test_invalid_form_with_error_handling():
    """Invalid forms can be handled by the method"""
    response = app.get('/testform?p_data.name=ed&p_data.age=edalso')
    assert response.raw['has_errors']