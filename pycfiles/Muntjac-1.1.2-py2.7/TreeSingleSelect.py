# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/trees/TreeSingleSelect.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tree import Tree
from muntjac.demo.sampler.features.trees.TreeMultiSelect import TreeMultiSelect
from muntjac.demo.sampler.features.trees.TreeActions import TreeActions
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TreeSingleSelect(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tree, single selection'

    def getDescription(self):
        return "In this example, you can select any single tree node and modify its 'name' property. Click again to de-select."

    def getRelatedAPI(self):
        return [
         APIResource(Tree)]

    def getRelatedFeatures(self):
        return [
         TreeMultiSelect, TreeActions]

    def getRelatedResources(self):
        return