# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/link/LinkSizedWindow.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.link import Link

class LinkSizedWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link, sized window'

    def getDescription(self):
        return 'Links can configure the size of the opened window.<br/>These links open a small fixed size window without decorations.'

    def getRelatedAPI(self):
        return [
         APIResource(Link)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
        from muntjac.demo.sampler.features.link.LinkCurrentWindow import LinkCurrentWindow
        from muntjac.demo.sampler.features.link.LinkNoDecorations import LinkNoDecorations
        return [
         LinkCurrentWindow, LinkNoDecorations, ButtonLink]

    def getRelatedResources(self):
        return