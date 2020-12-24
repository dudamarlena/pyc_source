# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/trees/TreeKeyboardNavigation.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tree import Tree
from muntjac.demo.sampler.features.trees.TreeMouseEvents import TreeMouseEvents
from muntjac.demo.sampler.features.trees.TreeMultiSelectExample import TreeMultiSelectExample
from muntjac.demo.sampler.features.trees.TreeSingleSelect import TreeSingleSelect
from muntjac.demo.sampler.features.trees.TreeMultiSelect import TreeMultiSelect
from muntjac.demo.sampler.features.trees.TreeActions import TreeActions
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TreeKeyboardNavigation(Feature):

    def getDescription(self):
        return 'You can use the keyboard to view and edit the tree selection. To move in the tree use the up, down,left and right arrow keys. The up and down keys moves up and down in the tree while the left and right keys expands and collapses the tree branches. <br/>By holding the CTRL key down you can move the selection head up and down and by pressing SPACE while holding the CTRL key down you can select multiple items. To select a range of items hold down SHIFT and move up or down using the arrow keys.<br>To expand a branch use the right arrow key and to collapse a branch use the left arrow key.'

    def getName(self):
        return 'Tree, keyboard navigation'

    def getRelatedAPI(self):
        return [
         APIResource(Tree)]

    def getRelatedFeatures(self):
        return [
         TreeSingleSelect,
         TreeActions,
         TreeMouseEvents,
         TreeMultiSelect]

    def getRelatedResources(self):
        return

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TreeMultiSelectExample()