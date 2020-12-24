# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/interfaces/tweetfolder.py
# Compiled at: 2009-11-16 05:42:59
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.tweetsite import tweetsiteMessageFactory as _

class Itweetfolder(Interface):
    """folder contatining tweets"""
    __module__ = __name__