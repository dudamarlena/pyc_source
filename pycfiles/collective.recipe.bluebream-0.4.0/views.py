# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aclark/Developer/collective/collective.recipe.bluebream/collective/recipe/bluebream/welcome/views.py
# Compiled at: 2012-04-08 15:58:16
from zope.browserpage import ViewPageTemplateFile
from zope.container.interfaces import INameChooser
from zope.formlib import form
from interfaces import ISampleApplication
from app import SampleApplication

class RootDefaultView(form.DisplayForm):
    __call__ = ViewPageTemplateFile('index.pt')


class AddSampleApplication(form.AddForm):
    form_fields = form.Fields(ISampleApplication)

    def createAndAdd(self, data):
        name = data['name']
        description = data.get('description')
        namechooser = INameChooser(self.context)
        app = SampleApplication()
        name = namechooser.chooseName(name, app)
        app.name = name
        app.description = description
        self.context[name] = app
        self.request.response.redirect(name)


class SampleApplicationDefaultView(form.DisplayForm):

    def __call__(self):
        return 'Welcome to the Sample application'