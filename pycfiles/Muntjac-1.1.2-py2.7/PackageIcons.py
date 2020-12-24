# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/PackageIcons.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.Feature import Feature, Version

class PackageIcons(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Runo theme icons'

    def getDescription(self):
        return '<p>The alternative built-in <i>Runo</i> theme contains many useful free icons. The icons are not restricted to the Runo theme and you can use them just as well in any other theme.</p><p>The icons are located in the Runo theme folder <tt>VAADIN/themes/runo/icons</tt>; you can copy them to your own theme from there.</p><p>The icons are available in three sizes: 16x16, 32x32, and 64x64 pixels.</p>'

    def getRelatedAPI(self):
        return []

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.commons.Icons import Icons
        return [
         Icons]

    def getRelatedResources(self):
        return