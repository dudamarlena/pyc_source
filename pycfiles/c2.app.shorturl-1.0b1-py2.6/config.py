# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/config.py
# Compiled at: 2010-08-19 05:10:29
"""
config.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
PROJECTNAME = 'c2.app.shorturl'
from persistent import Persistent
from zope.interface import implements
from c2.app.shorturl.interfaces import IShortUrlConfig

class ShortUrlConfig(Persistent):
    """ utility to hold the configuration related to Short URL """
    implements(IShortUrlConfig)

    def __init__(self):
        self.base_url = ''
        self.folder_id = ''

    def getId(self):
        """ return a unique id to be used with GenericSetup """
        return 'shorturl_config'