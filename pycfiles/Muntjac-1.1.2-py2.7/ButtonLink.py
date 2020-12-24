# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/buttons/ButtonLink.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Button
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class ButtonLink(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link button'

    def getDescription(self):
        return 'A link-styled button works like a push button, but looks like' + ' a Link.<br/> It does not actually link somewhere, but' + ' triggers a server-side event, just like a regular button.'

    def getRelatedAPI(self):
        return [
         APIResource(Button)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Links
        from muntjac.demo.sampler.features.buttons.ButtonPush import ButtonPush
        from muntjac.demo.sampler.features.buttons.CheckBoxes import CheckBoxes
        from muntjac.demo.sampler.features.blueprints.ProminentPrimaryAction import ProminentPrimaryAction
        from muntjac.demo.sampler.features.link.LinkCurrentWindow import LinkCurrentWindow
        return [
         ButtonPush, CheckBoxes, LinkCurrentWindow,
         ProminentPrimaryAction, Links]

    def getRelatedResources(self):
        return