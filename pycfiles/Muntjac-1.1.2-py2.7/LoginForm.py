# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/form/LoginForm.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui import login_form
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class LoginForm(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Login form'

    def getDescription(self):
        return "Using normal Muntjac components to build a login form is sometimes sufficient, but in many cases you'll want the browser to remember the credentials later on. Using the LoginForm helps in that case. You can override methods from LoginForm if you wish to specify the generated HTML yourself."

    def getRelatedAPI(self):
        return [
         APIResource(login_form.LoginForm)]

    def getRelatedFeatures(self):
        return

    def getRelatedResources(self):
        return