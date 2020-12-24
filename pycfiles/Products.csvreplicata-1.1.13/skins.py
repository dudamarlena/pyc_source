# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/CSSManager/skins.py
# Compiled at: 2008-09-18 15:18:08
__doc__ = "Utility functions for manipulating portal_skins. portal_skins' native API is cumbersome for some common tasks; these wrappers make them easy."

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