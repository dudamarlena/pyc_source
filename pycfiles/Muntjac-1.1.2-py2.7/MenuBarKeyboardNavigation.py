# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/menubar/MenuBarKeyboardNavigation.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.features.menubar.BasicMenuBar import BasicMenuBar
from muntjac.demo.sampler.features.menubar.MenuBarHiddenItems import MenuBarHiddenItems
from muntjac.demo.sampler.features.menubar.MenuBarWithIconsExample import MenuBarWithIconsExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.menubar.MenuBarWithIcons import MenuBarWithIcons
from muntjac.demo.sampler.features.menubar.MenuBarItemStyles import MenuBarItemStyles
from muntjac.demo.sampler.features.menubar.MenuBarCollapsing import MenuBarCollapsing
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.menu_bar import MenuBar

class MenuBarKeyboardNavigation(Feature):

    def getDescription(self):
        return 'As well as using the mouse you can also use the keyboard to select items from the menu bar. Make sure that the menu bar has keyboard focus and use the arrow keys to navigate in the menu. To select an item use the Enter and to close the menu use the Esc key.'

    def getName(self):
        return 'MenuBar keyboard navigation'

    def getRelatedAPI(self):
        return [
         APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [
         BasicMenuBar,
         MenuBarWithIcons,
         MenuBarCollapsing,
         MenuBarHiddenItems,
         MenuBarItemStyles]

    def getRelatedResources(self):
        return

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return MenuBarWithIconsExample()