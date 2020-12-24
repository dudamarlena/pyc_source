# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/z3cform/kss/test.py
# Compiled at: 2008-06-20 05:50:18
__doc__ = '\n<+ MODULE_NAME +>\n\nLicensed under the <+ LICENSE +> license, see LICENCE.txt for more details.\nCopyright by Affinitic sprl\n\n$Id: test.py 66971 2008-06-19 17:59:31Z jfroche $\n'
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