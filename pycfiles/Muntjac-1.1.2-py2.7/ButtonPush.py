# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/buttons/ButtonPush.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Button
from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
from muntjac.demo.sampler.features.blueprints.ProminentPrimaryAction import ProminentPrimaryAction
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.buttons.CheckBoxes import CheckBoxes
from muntjac.demo.sampler.Feature import Feature, Version

class ButtonPush(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Push button'

    def getDescription(self):
        return "A push-button, which can be considered a 'regular' button," + " returns to it's 'unclicked' state after emitting an event" + ' when the user clicks it.'

    def getRelatedAPI(self):
        return [
         APIResource(Button)]

    def getRelatedFeatures(self):
        return [
         ButtonLink, CheckBoxes, ProminentPrimaryAction]

    def getRelatedResources(self):
        return