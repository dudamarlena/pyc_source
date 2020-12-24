# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/trees/TreeActions.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tree import Tree
from muntjac.demo.sampler.features.trees.TreeSingleSelectExample import TreeSingleSelectExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TreeActions(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tree, context menu'

    def getDescription(self):
        return 'In this example, actions have been attached to the tree component. Try clicking the secondary mouse button on an item in the tree.'

    def getRelatedAPI(self):
        return [
         APIResource(Tree)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.trees.TreeMouseEvents import TreeMouseEvents
        from muntjac.demo.sampler.features.trees.TreeSingleSelect import TreeSingleSelect
        from muntjac.demo.sampler.features.trees.TreeMultiSelect import TreeMultiSelect
        return [
         TreeSingleSelect, TreeMultiSelect, TreeMouseEvents]

    def getRelatedResources(self):
        return

    def getExample(self):
        return TreeSingleSelectExample()