# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/link/LinkCurrentWindow.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.link import Link
from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
from muntjac.demo.sampler.features.link.LinkSizedWindow import LinkSizedWindow
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.link.LinkNoDecorations import LinkNoDecorations
from muntjac.demo.sampler.Feature import Feature, Version

class LinkCurrentWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link'

    def getDescription(self):
        return 'By default, links open in the current browser window (use the browser back-button to get back).'

    def getRelatedAPI(self):
        return [
         APIResource(Link)]

    def getRelatedFeatures(self):
        return [
         LinkNoDecorations, LinkSizedWindow, ButtonLink]

    def getRelatedResources(self):
        return