# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/Limit.py
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

def getLimitList(auth, cache):
    limitList = []
    response = sendCommand('GET', 'limits', None, auth)
    for item in response:
        limit = Limit(auth, cache, item)
        limit.onCommit = 'modify'
        limitList.append(limit)

    return tuple(limitList)


def getLimitFromId(auth, cache, id):
    limit = searchCache(cache, 'limits', id)
    if limit != False:
        return limit
    for limit in getLimitList(auth, cache):
        if hasattr(limit, 'id') and getattr(limit, 'id') == id:
            return limit

    raise LimitNotFoundError('id %s not found' % (id,))


def getLimitObjectFromName(auth, cache, name):
    limit = searchCacheByName(cache, 'limits', name)
    if name is None:
        return
    else:
        if limit != False:
            return limit
        for limit in getLimitList(auth, cache):
            if hasattr(limit, 'name') and getattr(limit, 'name').upper() == name.upper():
                return limit

        raise LimitNotFoundError('name %s not found' % (name,))
        return


class Limit(Base):
    SPECIALATTRS = [
     'ROLLOVER', 'RESET_DAY']
    ROLLOVER = {False: 'false', True: 'true'}
    RESET_DAY = {False: 0, True: 1}

    def getAccount(self):
        if self.account_id == False:
            return
        else:
            account = searchCacheById(self.cache, 'accounts', self.account_id)
            if account != False:
                return account
            return getAccountFromId(self.auth, self.cache, self.account_id)
            return

    def getCategory(self):
        if self.category_id == False:
            return
        else:
            category = searchCache(self.cache, 'categories', self.category_id)
            if category != False:
                return category
            return getCategoryFromId(self.auth, self.cache, self.category_id)
            return

    def cloneLimit(self):
        return cloneObject(self)