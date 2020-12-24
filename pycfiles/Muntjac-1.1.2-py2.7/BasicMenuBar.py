# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/menubar/BasicMenuBar.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar

class BasicMenuBar(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Basic MenuBar'

    def getDescription(self):
        return 'The drop down menus can have separators between menu items and single items can be disabled.'

    def getRelatedAPI(self):
        return [
         APIResource(MenuBar)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.menubar.MenuBarTooltips import MenuBarTooltips
        from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
        from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
        from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
        from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing
        return [
         MenuBarWithIcons,
         MenuBarCollapsing,
         MenuBarHiddenItems,
         MenuBarItemStyles,
         MenuBarTooltips]

    def getRelatedResources(self):
        return