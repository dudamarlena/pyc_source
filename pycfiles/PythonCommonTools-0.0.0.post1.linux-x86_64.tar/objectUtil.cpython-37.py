# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/objectUtil/objectUtil.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 9800 bytes
from hashlib import sha512
from sys import byteorder
from collections import OrderedDict
from enum import Enum, unique
from importlib import import_module
from copy import copy

@unique
class EncryptionMarkup(Enum):
    DICT = '__dict__'
    CLASS_NAME = 'className'
    MODULE = 'module'


def dumpObjetToDict(objectToDump):
    """INFO :
     - 'memoryview' object is a special one, without __dict__ attribut
       see : https://docs.python.org/3.3/library/stdtypes.html#memoryview
     - convert iterators elements (list,tuple,set,frozenset,dict)
     - some specific objects (i.e datetime.datetime) does not have __dict__ propertie
       so they can not be dumped to dictionnary or JSON
       so we finally use string to dump
    """
    objectType = type(objectToDump)
    if hasattr(objectToDump, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToDump.__dict__)
        if hasattr(objectToDump, '__class__'):
            if hasattr(objectToDump, '__module__'):
                objectDict[EncryptionMarkup.CLASS_NAME.value] = objectToDump.__class__.__name__
                objectDict[EncryptionMarkup.MODULE.value] = objectToDump.__module__
    else:
        if objectType == memoryview:
            objectDict = objectToDump.tobytes()
        else:
            if objectType == list:
                objectDict = [dumpObjetToDict(_) for _ in objectToDump]
            else:
                if objectType == tuple:
                    objectDict = [dumpObjetToDict(_) for _ in objectToDump]
                    objectDict = tuple(objectDict)
                else:
                    if objectType == set:
                        objectDict = [dumpObjetToDict(_) for _ in objectToDump]
                        objectDict = set(objectDict)
                    else:
                        if objectType == frozenset:
                            objectDict = [dumpObjetToDict(_) for _ in objectToDump]
                            objectDict = frozenset(objectDict)
                        else:
                            if objectType == dict:
                                objectDict = {}
                                for key, value in objectToDump.items():
                                    newKey = dumpObjetToDict(key)
                                    newValue = dumpObjetToDict(value)
                                    objectDict[newKey] = newValue

                            else:
                                if objectToDump and objectType not in {bool, int, float, complex, range, str, bytes, bytearray}:
                                    objectDict = str(objectToDump)
                                else:
                                    objectDict = copy(objectToDump)
    return objectDict


def loadObjectFromDict(baseDict):
    baseType = type(baseDict)
    instantiatedObject = copy(baseDict)
    if baseType == list:
        instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
    else:
        if baseType == tuple:
            instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
            instantiatedObject = tuple(instantiatedObject)
        else:
            if baseType == set:
                instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
                instantiatedObject = set(instantiatedObject)
            else:
                if baseType == frozenset:
                    instantiatedObject = [loadObjectFromDict(_) for _ in baseDict]
                    instantiatedObject = frozenset(instantiatedObject)
                else:
                    if baseType == dict:
                        instantiatedObject = {}
                        for key, value in baseDict.items():
                            instantiatedObject[key] = loadObjectFromDict(value)

                        if EncryptionMarkup.CLASS_NAME.value in baseDict and EncryptionMarkup.MODULE.value in baseDict:
                            attributs = copy(instantiatedObject)
                            importedModule = import_module(baseDict[EncryptionMarkup.MODULE.value])
                            loadedClass = getattr(importedModule, baseDict[EncryptionMarkup.CLASS_NAME.value])
                            instantiatedObject = loadedClass()
                            instantiatedObject.__dict__.update(attributs)
                            if hasattr(instantiatedObject, EncryptionMarkup.MODULE.value):
                                delattr(instantiatedObject, EncryptionMarkup.MODULE.value)
                            if hasattr(instantiatedObject, EncryptionMarkup.CLASS_NAME.value):
                                delattr(instantiatedObject, EncryptionMarkup.CLASS_NAME.value)
                    return instantiatedObject


def objectStringRepresentation(objectToStr):
    objectDict = dumpObjetToDict(objectToStr)
    objectStr = str(objectDict)
    return objectStr


def convertObjectToOrderedDict(objectToConvert):
    objectType = type(objectToConvert)
    objectOrderedDict = objectToConvert
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        objectDict = dumpObjetToDict(objectToConvert)
        objectOrderedDict = convertObjectToOrderedDict(objectDict)
    else:
        if objectType == memoryview:
            objectOrderedDict = objectToConvert.tobytes()
        else:
            if objectType in {list, tuple, set, frozenset}:
                objectOrderedDict = [convertObjectToOrderedDict(_) for _ in objectToConvert]
                objectOrderedDict = [str(_) for _ in objectOrderedDict]
                objectOrderedDict.sort()
                objectOrderedDict = tuple(objectOrderedDict)
            else:
                if objectType == dict:
                    stringKeyDict = {}
                    for oldKey, oldValue in objectToConvert.items():
                        orderedKey = convertObjectToOrderedDict(oldKey)
                        stringKey = str(orderedKey)
                        orderedValue = convertObjectToOrderedDict(oldValue)
                        stringKeyDict[stringKey] = orderedValue

                    orderedStringKeys = convertObjectToOrderedDict(stringKeyDict.keys())
                    objectOrderedDict = OrderedDict()
                    for orderedKey in orderedStringKeys:
                        objectOrderedDict[orderedKey] = stringKeyDict[orderedKey]

    return objectOrderedDict


def objectHash(objectToHash):
    objectOrderedDict = convertObjectToOrderedDict(objectToHash)
    hashAlgorithm = sha512()
    hashAlgorithm.update(str(objectOrderedDict).encode())
    digest = hashAlgorithm.digest()
    hash = int.from_bytes(digest, byteorder=byteorder, signed=False)
    return hash


def objectComparison(originalObject, modelObject):
    """INFO :
     - normally, in python 0.==0 even if type(0.)!=type(0)
       however, for consistency and stability, we will ensure types are equals
     - convert iterators elements (list,tuple,set,frozenset,dict)
       furthermore, python can have issues with multi dimensional arrays : The truth value of an array with more than one element is ambiguous
       so we adapt comparison method
     """
    comparison = False
    if type(originalObject) == type(modelObject):
        originalDict = dumpObjetToDict(originalObject)
        modelDict = dumpObjetToDict(modelObject)
        if type(originalDict) == dict:
            originalKeys = tuple(originalDict.keys())
            modelKeys = tuple(modelDict.keys())
            comparison = objectComparison(originalKeys, modelKeys)
            if comparison:
                for key, originalValue in originalDict.items():
                    modelValue = modelDict[key]
                    comparison = objectComparison(originalValue, modelValue)
                    if not comparison:
                        break

        if type(originalDict) in {list, tuple}:
            comparison = len(originalDict) == len(modelDict)
            if comparison:
                for index, originalElement in enumerate(originalDict):
                    modelElement = modelDict[index]
                    comparison = objectComparison(originalElement, modelElement)
                    if not comparison:
                        break

        else:
            if type(originalDict) in {set, frozenset}:
                comparison = len(originalDict) == len(modelDict)
                if comparison:
                    for originalElement in originalDict:
                        comparison = originalElement in modelDict
                        if not comparison:
                            break

            else:
                comparison = originalDict == modelDict
    return comparison


def methodArgsStringRepresentation(parametersList, localValuesDict):
    methodArgsDict = dict()
    for parameter in parametersList:
        parameterName = parameter
        if hasattr(parameter, 'name'):
            parameterName = parameter.name
        if parameterName in localValuesDict:
            methodArgsDict[parameterName] = localValuesDict[parameterName]

    methodArgsString = str(methodArgsDict)
    return methodArgsString