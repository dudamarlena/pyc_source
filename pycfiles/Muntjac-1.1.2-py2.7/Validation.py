# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/Validation.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Form
from muntjac.data.validatable import IValidatable
from muntjac.data.validator import IValidator
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.demo.sampler.features.form.FormPojoExample import FormPojoExample

class Validation(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Validation'

    _desc = '<p>Field components can have <i>validators</i> that check' + ' the values entered by a user. Validation is most useful when ' + 'used within a Form, but' + ' you can use validation for single stand-alone fields as well.</p>'

    def getExample(self):
        return FormPojoExample()

    def getDescription(self):
        return self._desc

    def getRelatedAPI(self):
        return [
         APIResource(IValidatable),
         APIResource(IValidator),
         APIResource(Form)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Forms
        from muntjac.demo.sampler.features.commons.Errors import Errors
        return [
         Errors, Forms]

    def getRelatedResources(self):
        return