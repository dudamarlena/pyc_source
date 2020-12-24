# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/__init__.py
# Compiled at: 2008-12-19 12:41:15
from content import Content
from interfaces import IContent

def content():
    return Content()


import convertors

def search(query, sort=None):
    """returns an IResultSet, spec allows searching, sorting, etc"""
    pass


def get(id):
    """returns the IContent specified by the id"""
    pass


def store(content):
    """stores the supplied content object"""
    pass