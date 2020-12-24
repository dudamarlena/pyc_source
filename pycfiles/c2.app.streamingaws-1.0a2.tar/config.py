# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/config.py
# Compiled at: 2010-08-19 05:10:29
__doc__ = '\nconfig.py\n\nCreated by Manabu Terada on 2010-08-03.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
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