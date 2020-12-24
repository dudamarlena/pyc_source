# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/objectUtil/POPO.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 4124 bytes
from copy import copy
from pythoncommontools.objectUtil.objectUtil import dumpObjetToDict, loadObjectFromDict, objectStringRepresentation, objectHash, objectComparison
from pythoncommontools.jsonEncoderDecoder.simpleJsonEncoderDecoder import dumpObjectToSimpleJson, loadObjectFromSimpleJson
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import dumpObjectToComplexJson, loadObjectFromComplexJson

def normalizePopoAttribut(popoAttribut):
    popoAttributType = type(popoAttribut)
    if issubclass(popoAttributType, POPO):
        normalizedPopo = popoAttribut.instanciateNormalize()
    else:
        if popoAttributType in {list, tuple}:
            normalizedPopo = [normalizePopoAttribut(_) for _ in popoAttribut]
        else:
            if popoAttributType in {set, frozenset}:
                normalizedPopo = normalizePopoAttribut(list(popoAttribut))
                normalizedPopo = frozenset(normalizedPopo)
            else:
                if popoAttributType == dict:
                    normalizedPopo = {}
                    for key, value in popoAttribut.items():
                        normalizedPopo[key] = normalizePopoAttribut(value)

                else:
                    if hasattr(popoAttribut, '__dict__'):
                        normalizedPopo = copy(popoAttribut)
                        for attribute, value in popoAttribut.__dict__.items():
                            newValue = normalizePopoAttribut(value)
                            setattr(normalizedPopo, attribute, newValue)

                    else:
                        normalizedPopo = popoAttribut
    return normalizedPopo


class POPO:

    def dumpToDict(self):
        return dumpObjetToDict(self)

    def __repr__(self):
        return objectStringRepresentation(self)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return objectHash(self)

    def __eq__(self, other):
        normalizedSelf = self.instanciateNormalize()
        if hasattr(other, 'instanciateNormalize'):
            normalizedOther = other.instanciateNormalize()
        else:
            normalizedOther = other
        return objectComparison(normalizedSelf, normalizedOther)

    @staticmethod
    def loadFromDict(baseDict):
        instantiatedObject = loadObjectFromDict(baseDict)
        return instantiatedObject

    def instanciateNormalize(self):
        normalizedSelf = copy(self)
        for attribute, value in self.__dict__.items():
            newValue = normalizePopoAttribut(value)
            setattr(normalizedSelf, attribute, newValue)

        return normalizedSelf

    def dumpToSimpleJson(self):
        dumpedJson = dumpObjectToSimpleJson(self)
        return dumpedJson

    @staticmethod
    def loadFromSimpleJson(json):
        instantiatedObject = loadObjectFromSimpleJson(json)
        return instantiatedObject

    def dumpToComplexJson(self):
        dumpedJson = dumpObjectToComplexJson(self)
        return dumpedJson

    @staticmethod
    def loadFromComplexJson(json):
        instantiatedObject = loadObjectFromComplexJson(json)
        return instantiatedObject