# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/jsonEncoderDecoder/complexJsonEncoderDecoder.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 10435 bytes
from pythoncommontools.objectUtil.objectUtil import EncryptionMarkup, loadObjectFromDict
from copy import copy
from pythoncommontools.jsonEncoderDecoder.simpleJsonEncoderDecoder import dumpObjectToSimpleJson, loadObjectFromSimpleJson

class ComplexeSurrogate:

    def __init__(self, originalObject=complex(0, 0)):
        self.real = originalObject.real
        self.imaginary = originalObject.imag


class RangeSurrogate:

    def __init__(self, originalObject=range(0, 0)):
        self.start = originalObject.start
        self.stop = originalObject.stop
        self.step = originalObject.step


class BytesSurrogate:

    def __init__(self, originalObject=bytes()):
        self.list = list(originalObject)


class BytearraySurrogate:

    def __init__(self, originalObject=bytearray()):
        self.list = list(originalObject)


class MemoryviewSurrogate:

    def __init__(self, originalObject=memoryview(b'')):
        self.list = list(originalObject)


class TupleSurrogate:

    def __init__(self, originalObject=tuple()):
        self.list = [convertObjectToComplexJsonObject(_) for _ in originalObject]


class SetSurrogate:

    def __init__(self, originalObject=set()):
        self.list = [convertObjectToComplexJsonObject(_) for _ in originalObject]


class FrozensetSurrogate:

    def __init__(self, originalObject=frozenset()):
        self.list = [convertObjectToComplexJsonObject(_) for _ in originalObject]


def convertDictKeyToJsonName(keyValue, keyType):
    if keyType in {list, tuple, set, frozenset}:
        keyString = [IterableKeyElementSurrogate(_) for _ in keyValue]
    else:
        if keyType == range:
            keyString = [
             keyType.start, keyType.stop, keyType.step]
        else:
            if keyType in {bytes, bytearray}:
                keyString = keyValue.decode()
            else:
                if keyType == memoryview:
                    keyString = bytes(keyValue).decode()
                else:
                    keyString = copy(keyValue)
    return keyString


class IterableKeyElementSurrogate:

    def __init__(self, originalObject=None):
        elementType = type(originalObject)
        self.keyType = elementType.__name__
        self.keyValue = convertDictKeyToJsonName(originalObject, elementType)


class ItemSurrogate:

    def __init__(self, originalItem=(None, None)):
        key = originalItem[0]
        keyType = type(key)
        self.keyType = keyType.__name__
        self.keyValue = convertDictKeyToJsonName(key, keyType)
        self.value = convertObjectToComplexJsonObject(originalItem[1])


class DictSurrogate:

    def __init__(self, originalDict=dict()):
        self.list = list()
        for item in originalDict.items():
            currentItemSurrogate = ItemSurrogate(item)
            self.list.append(currentItemSurrogate)


def convertObjectToComplexJsonObject(objectToConvert):
    """
    convert to JSON complex object
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    """
    if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
        complexJSonObject = copy(objectToConvert)
        shallowAttributs = objectToConvert.__dict__
        for attribut, oldValue in shallowAttributs.items():
            newValue = convertObjectToComplexJsonObject(oldValue)
            setattr(complexJSonObject, attribut, newValue)

    else:
        if type(objectToConvert) == complex:
            complexJSonObject = ComplexeSurrogate(objectToConvert)
        else:
            if type(objectToConvert) == range:
                complexJSonObject = RangeSurrogate(objectToConvert)
            else:
                if type(objectToConvert) == bytes:
                    complexJSonObject = BytesSurrogate(objectToConvert)
                else:
                    if type(objectToConvert) == bytearray:
                        complexJSonObject = BytearraySurrogate(objectToConvert)
                    else:
                        if type(objectToConvert) == memoryview:
                            complexJSonObject = MemoryviewSurrogate(objectToConvert)
                        else:
                            if type(objectToConvert) == list:
                                complexJSonObject = [convertObjectToComplexJsonObject(_) for _ in objectToConvert]
                            else:
                                if type(objectToConvert) == tuple:
                                    complexJSonObject = TupleSurrogate(objectToConvert)
                                else:
                                    if type(objectToConvert) == set:
                                        complexJSonObject = SetSurrogate(objectToConvert)
                                    else:
                                        if type(objectToConvert) == frozenset:
                                            complexJSonObject = FrozensetSurrogate(objectToConvert)
                                        else:
                                            if type(objectToConvert) == dict:
                                                complexJSonObject = DictSurrogate(objectToConvert)
                                            else:
                                                complexJSonObject = copy(objectToConvert)
    return complexJSonObject


def dumpObjectToComplexJson(objectToDump):
    complexJSonObject = convertObjectToComplexJsonObject(objectToDump)
    dumpedJson = dumpObjectToSimpleJson(complexJSonObject)
    return dumpedJson


def regenerateKeysList(keys):
    fullLoadedKeySurrogates = [loadObjectFromDict(_) for _ in keys]
    regeneratedKeys = [regenerateKey(_.keyType, _.keyValue) for _ in fullLoadedKeySurrogates]
    return regeneratedKeys


def regenerateKey(keyType, keyValue):
    if keyType == 'NoneType':
        regeneratedKey = None
    else:
        if keyType == 'complex':
            regeneratedKey = complex(keyValue)
        else:
            if keyType == 'bytes':
                regeneratedKey = keyValue.encode()
            else:
                if keyType == 'bytearray':
                    regeneratedKey = bytearray(keyValue.encode())
                else:
                    if keyType == 'memoryview':
                        regeneratedKey = memoryview(keyValue.encode())
                    else:
                        if keyType == 'range':
                            regeneratedKey = range(keyValue[0], keyValue[1], keyValue[2])
                        else:
                            if keyType == 'list':
                                regeneratedKey = regenerateKeysList(keyValue)
                            else:
                                if keyType == 'tuple':
                                    regeneratedKeys = regenerateKeysList(keyValue)
                                    regeneratedKey = tuple(regeneratedKeys)
                                else:
                                    if keyType == 'set':
                                        regeneratedKeys = regenerateKeysList(keyValue)
                                        regeneratedKey = set(regeneratedKeys)
                                    else:
                                        if keyType == 'frozenset':
                                            regeneratedKeys = regenerateKeysList(keyValue)
                                            regeneratedKey = frozenset(regeneratedKeys)
                                        else:
                                            regeneratedKey = copy(keyValue)
    return regeneratedKey


def convertComplexJsonObjectToObject(objectToConvert):
    """
    convert to JSON complex object
    INFO :
     - some types are unknown in JSON (complex,bytes,bytearray,range,tuple,set,frozenset)
     - convert iterators elements (list,tuple,set,frozenset,dict)
    """
    if type(objectToConvert) == ComplexeSurrogate:
        finalObject = complex(objectToConvert.real, objectToConvert.imaginary)
    else:
        if type(objectToConvert) == RangeSurrogate:
            finalObject = range(objectToConvert.start, objectToConvert.stop, objectToConvert.step)
        else:
            if type(objectToConvert) == BytesSurrogate:
                finalObject = bytes(objectToConvert.list)
            else:
                if type(objectToConvert) == BytearraySurrogate:
                    finalObject = bytearray(objectToConvert.list)
                else:
                    if type(objectToConvert) == MemoryviewSurrogate:
                        finalObject = memoryview(bytes(objectToConvert.list))
                    else:
                        if type(objectToConvert) == list:
                            finalObject = [convertComplexJsonObjectToObject(_) for _ in objectToConvert]
                        else:
                            if type(objectToConvert) == TupleSurrogate:
                                surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
                                finalObject = tuple(surrogateList)
                            else:
                                if type(objectToConvert) == SetSurrogate:
                                    surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
                                    finalObject = set(surrogateList)
                                else:
                                    if type(objectToConvert) == FrozensetSurrogate:
                                        surrogateList = [convertComplexJsonObjectToObject(_) for _ in objectToConvert.list]
                                        finalObject = frozenset(surrogateList)
                                    else:
                                        if type(objectToConvert) == DictSurrogate:
                                            fullLoadedItemSurrogates = [loadObjectFromDict(_) for _ in objectToConvert.list]
                                            finalObject = {}
                                            for itemSurrogate in fullLoadedItemSurrogates:
                                                regeneratedKey = regenerateKey(itemSurrogate.keyType, itemSurrogate.keyValue)
                                                value = convertComplexJsonObjectToObject(itemSurrogate.value)
                                                finalObject[regeneratedKey] = value

                                        else:
                                            if type(objectToConvert) == dict:
                                                if EncryptionMarkup.CLASS_NAME.value in objectToConvert and EncryptionMarkup.MODULE.value in objectToConvert:
                                                    rawObject = loadObjectFromDict(objectToConvert)
                                                    finalObject = convertComplexJsonObjectToObject(rawObject)
                                                else:
                                                    finalObject = {}
                                                    for key, oldValue in objectToConvert.items():
                                                        newValue = convertComplexJsonObjectToObject(oldValue)
                                                        finalObject[key] = newValue

                                            else:
                                                if hasattr(objectToConvert, EncryptionMarkup.DICT.value):
                                                    finalObject = copy(objectToConvert)
                                                    shallowAttributs = objectToConvert.__dict__
                                                    for attribut, oldValue in shallowAttributs.items():
                                                        newValue = convertComplexJsonObjectToObject(oldValue)
                                                        setattr(finalObject, attribut, newValue)

                                                else:
                                                    finalObject = copy(objectToConvert)
    return finalObject


def loadObjectFromComplexJson(json):
    instantiatedObject = loadObjectFromSimpleJson(json)
    finalObject = convertComplexJsonObjectToObject(instantiatedObject)
    return finalObject