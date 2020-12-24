# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/Errors.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.demo.sampler.features.notifications.NotificationError import NotificationError
from muntjac.demo.sampler.features.form.FormBasic import FormBasic
from muntjac.demo.sampler.features.commons.Validation import Validation
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class Errors(Feature):
    _desc = "<p>You can set a <i>component error</i> property to indicate an error situation - an error indicator icon will appear beside or inside the component, depending on the component and the containing layout, and an error message will appear as a 'tooltip' when the mouse pointer hovers over the component.</p><p>You can set the error on almost any component, but please note that, from a usability standpoint, it may not always be the best solution. It is usually not a good idea to set an error on a Button: the user can not click 'Save' differently to correct the error. The <i>component error</i> property is most useful for indicating what component is causing an error, so that the user can find and correct the problem.</p><p>If there is no specific component that causes the error, consider using a (styled) Label or a Notification to indicate the error.</p><p>The Form component displays an error of a contained field in a special error indicator area at the bottom of the form. If there are multiple fields with an error, only the first is displayed.</p>"

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Error indicator'

    def getDescription(self):
        return self._desc

    def getRelatedAPI(self):
        return [
         APIResource(AbstractComponent)]

    def getRelatedFeatures(self):
        return [
         Validation, FormBasic, NotificationError]

    def getRelatedResources(self):
        return