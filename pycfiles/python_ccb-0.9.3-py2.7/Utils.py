# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/Utils.py
# Compiled at: 2012-11-09 16:42:01
"""
Copyright 2012 Oscar Curero

This code is free software; you can redistribute it and/or modify it
under the terms of the GPL 3 license (see the file
COPYING.txt included with the distribution).
"""
import restclient
from copy import copy
from httplib2 import ServerNotFoundError
from Exceptions import *
from decimal import *
BASEURL = 'https://www.clearcheckbook.com/api/'
null = None
false = False
true = True

def sendCommand(requestType, command, data, auth, mode=False):
    request = getattr(restclient, requestType)
    response = request('%s%s' % (BASEURL, command), params=data, credentials=auth, async=mode)
    try:
        response = eval(response.replace('\\/', '/'))
    except:
        pass

    return response


def castAttribute(attribute):
    if type(attribute) != str:
        return attribute
    else:
        try:
            return int(attribute)
        except:
            try:
                return Decimal(attribute)
            except:
                if attribute is None:
                    return
                else:
                    if attribute.lower() == 'false':
                        return bool(0)
                    if attribute.lower() == 'true':
                        return bool(1)
                    return str(attribute).decode('raw_unicode_escape')

        return


def replaceAttributes(object, direction):
    if not hasattr(object, 'SPECIALATTRS'):
        return
    else:
        attributesDict = {}
        for specialAttr in object.SPECIALATTRS:
            if direction == 'fromOutside':
                for item in getattr(object, specialAttr).copy().items():
                    attributesDict[item[1]] = item[0]

            elif direction == 'toOutside':
                attributesDict = getattr(object, specialAttr)
            if hasattr(object, specialAttr.lower()):
                attribute = getattr(object, specialAttr.lower())
                newValue = attributesDict.get(attribute, getattr(object, specialAttr.lower()))
                if direction == 'fromOutside':
                    newValue = castAttribute(newValue)
                setattr(object, specialAttr.lower(), newValue)

        return


def loadDataToObject(object, data):
    object.attributes = []
    for name, value in data.items():
        if name.upper() not in object.SPECIALATTRS:
            value = castAttribute(value)
        setattr(object, name, value)
        object.attributes.append(name)


def unloadDataFromObject(object):
    data = {}
    for name in object.attributes:
        attr = getattr(object, name)
        if type(attr) == unicode:
            attr = attr.encode('raw_unicode_escape')
        data[name] = attr

    return data


def cloneObject(object):
    newObject = copy(object)
    newObject.id = None
    newObject.onCommit = 'create'
    return newObject


def searchCacheById(cache, cacheType, index):
    if cache != None and index in cache[cacheType].keys():
        return cache[cacheType][index]
    else:
        return False
        return


def searchCacheByName(cache, cacheType, name):
    if cache != None:
        for object in cache[cacheType].values():
            if hasattr(object, 'name'):
                if object.name.upper() == name.upper():
                    return object

    return False


def addCache(cache, object, index):
    if cache == None:
        return
    else:
        if object.__class__.__name__ == 'Account':
            cacheType = 'accounts'
        elif object.__class__.__name__ == 'Category':
            cacheType = 'categories'
        elif object.__class__.__name__ == 'Reminder':
            cacheType = 'reminders'
        elif object.__class__.__name__ == 'Limit':
            cacheType = 'limits'
        else:
            if object.__class__.__name__ == 'Transaction':
                return
            raise CacheError('%s is not a valid object type' % (object.__class__.__name__,))
        if searchCacheById(cache, cacheType, index) == False:
            cache[cacheType][index] = object
        return


def deleteCache(cache, object, index):
    if cache == None:
        return
    else:
        if object.__class__.__name__ == 'Account':
            cacheType = 'accounts'
        elif object.__class__.__name__ == 'Category':
            cacheType = 'categories'
        elif object.__class__.__name__ == 'Reminder':
            cacheType = 'reminders'
        elif object.__class__.__name__ == 'Limit':
            cacheType = 'limits'
        else:
            if object.__class__.__name__ == 'Transaction':
                return
            raise CacheError('%s is not a valid object type' % (object.__class__,))
        if searchCacheById(cache, cacheType, index) != False:
            del cache[cacheType][index]
        return