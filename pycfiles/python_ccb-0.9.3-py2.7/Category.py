# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/Category.py
# Compiled at: 2012-11-09 16:40:24
"""
Copyright 2012 Oscar Curero

This code is free software; you can redistribute it and/or modify it
under the terms of the GPL 3 license (see the file
COPYING.txt included with the distribution).
"""
from Utils import *
from Exceptions import *
from Base import *

def getCategoryList(auth, cache):
    categoryList = []
    response = sendCommand('GET', 'categories', None, auth)
    for item in response:
        category = Category(auth, cache, item)
        category.onCommit = 'modify'
        categoryList.append(category)

    return tuple(categoryList)


def getCategoryObjectFromId(auth, cache, id):
    category = searchCacheById(cache, 'categories', id)
    if id is None:
        return
    else:
        if category != False:
            return category
        for category in getCategoryList(auth, cache):
            if hasattr(category, 'id') and getattr(category, 'id') == id:
                return category

        raise CategoryNotFoundError('id %s not found' % (id,))
        return


def getCategoryObjectFromName(auth, cache, name):
    category = searchCacheByName(cache, 'categories', name)
    if name is None:
        return
    else:
        if category != False:
            return category
        for category in getCategoryList(auth, cache):
            if hasattr(category, 'name') and getattr(category, 'name').upper() == name.upper():
                return category

        raise CategoryNotFoundError('name %s not found' % (name,))
        return


class Category(Base):
    SPECIALATTRS = ['PARENT']
    PARENT = {None: 0}

    def getParent(self):
        if self.parent == 0:
            return
        else:
            return searchCacheById(self.cache, 'categories', self.parent)
            return

    def refreshCategory(self):
        category = getCategoryObjectFromId(self.auth, None, self.id)
        for attr in dir(category):
            if attr != 'cache' and callable(getattr(newData, attr)) == False:
                setattr(self, attr, getattr(category, attr))

        return

    def cloneCategory(self):
        return cloneObject(self)