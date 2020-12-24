# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/__init__.py
# Compiled at: 2012-11-09 16:40:24
"""
Copyright 2012 Oscar Curero

This code is free software; you can redistribute it and/or modify it
under the terms of the GPL 3 license (see the file
COPYING.txt included with the distribution).
"""
from Connect import Connect
from Filtertransact import Filtertransact
from Clearcheckbook import Clearcheckbook

def login(username, password, useCache=True):
    dataUser = Connect(username, password)
    return Clearcheckbook(username, password, dataUser, useCache)


def filter(username, password, data=None):
    dataUser = Connect(username, password)
    return Filtertransact(Clearcheckbook(username, password, dataUser, True), data)