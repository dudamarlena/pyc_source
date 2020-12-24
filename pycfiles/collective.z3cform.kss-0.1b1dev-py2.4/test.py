# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/z3cform/kss/test.py
# Compiled at: 2008-06-20 05:50:18
"""
<+ MODULE_NAME +>

Licensed under the <+ LICENSE +> license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: test.py 66971 2008-06-19 17:59:31Z jfroche $
"""
from zope import interface, schema
from z3c.form import form, field, button
from plone.z3cform.base import FormWrapper

class MySchema(interface.Interface):
    __module__ = __name__
    age = schema.Int(title='Age')


class MyForm(form.Form):
    __module__ = __name__
    fields = field.Fields(MySchema)
    ignoreContext = True
    __name__ = 'test-form'

    @button.buttonAndHandler('Apply')
    def handleApply(self, action):
        (data, errors) = self.extractData()
        print data['age']


class MyFormWrapper(FormWrapper):
    __module__ = __name__
    form = MyForm
    label = 'Please enter your age'