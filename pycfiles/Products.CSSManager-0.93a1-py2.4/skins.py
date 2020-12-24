# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/CSSManager/skins.py
# Compiled at: 2008-09-18 15:18:08
"""Utility functions for manipulating portal_skins. portal_skins' native API is cumbersome for some common tasks; these wrappers make them easy."""

def deleteLayers(skinsTool, layersToDelete):
    """Remove each of the layers in `layersToDelete` from all skins.
    
    (We check them all, in case the user manually inserted it into some.)
    
    Pass getToolByName(portal, 'portal_skins') for `skinsTool`.
    
    """
    for skinName in skinsTool.getSkinSelections():
        layers = [ x.strip() for x in skinsTool.getSkinPath(skinName).split(',') ]
        try:
            for curLayer in layersToDelete:
                layers.remove(curLayer)

        except ValueError:
            pass

        skinsTool.addSkinSelection(skinName, (',').join(layers))