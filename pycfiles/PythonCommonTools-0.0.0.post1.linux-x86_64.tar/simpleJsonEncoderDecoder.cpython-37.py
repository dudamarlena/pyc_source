# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/jsonEncoderDecoder/simpleJsonEncoderDecoder.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 1942 bytes
from copy import copy
from json import dumps, loads
from pythoncommontools.objectUtil.objectUtil import EncryptionMarkup, dumpObjetToDict, loadObjectFromDict

def convertObjectToJsonDict(objectToConvert):
    """
    convert to JSON native
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    """
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToConvert)
        objectJsonDict = convertObjectToJsonDict(objectDict)
    else:
        if type(objectToConvert) == complex:
            objectJsonDict = str(objectToConvert)
        else:
            if type(objectToConvert) in {memoryview, bytes, bytearray}:
                objectJsonDict = list(objectToConvert)
            else:
                if type(objectToConvert) in {list, tuple, set, frozenset, range}:
                    objectJsonDict = [convertObjectToJsonDict(_) for _ in objectToConvert]
                else:
                    if type(objectToConvert) == dict:
                        objectJsonDict = {}
                        for oldKey, oldValue in objectToConvert.items():
                            newKey = convertObjectToJsonDict(oldKey)
                            newKey = str(newKey)
                            newValue = convertObjectToJsonDict(oldValue)
                            objectJsonDict[newKey] = newValue

                    else:
                        objectJsonDict = copy(objectToConvert)
    return objectJsonDict


def dumpObjectToSimpleJson(objectToDump):
    objectJsonDict = convertObjectToJsonDict(objectToDump)
    dumpedJson = dumps(objectJsonDict)
    return dumpedJson


def loadObjectFromSimpleJson(json):
    dictToLoad = loads(json)
    instantiatedObject = loadObjectFromDict(dictToLoad)
    return instantiatedObject