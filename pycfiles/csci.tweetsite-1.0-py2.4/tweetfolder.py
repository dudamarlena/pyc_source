# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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