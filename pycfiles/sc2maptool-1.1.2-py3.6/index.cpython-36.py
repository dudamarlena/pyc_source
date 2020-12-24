# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2maptool\index.py
# Compiled at: 2018-10-07 15:04:33
# Size of source mod 2**32: 1385 bytes
from glob import glob
import os
from sc2maptool.mapRecord import MapRecord
from sc2maptool import constants as c

class IndexCache(object):

    def __init__(self):
        pass


cache = IndexCache()

def getIndex(folderPath=None):
    """parse the 'Maps' subfolder directory divining criteria for valid maps"""
    try:
        return cache.structure
    except AttributeError:
        pass

    if folderPath == None:
        from sc2maptool.startup import setup
        folderPath = setup()

    def folderSearch(path, attrList=[]):
        ret = []
        for item in glob(os.path.join(path, '*')):
            if item == os.sep:
                pass
            else:
                itemName = os.path.basename(item)
                if os.path.isdir(item):
                    ret += folderSearch(item, attrList + [itemName])
                else:
                    if itemName.endswith(c.SC2_MAP_EXT):
                        ret.append(MapRecord(itemName, item, attrList))

        return ret

    cache.structure = folderSearch(folderPath)
    return cache.structure