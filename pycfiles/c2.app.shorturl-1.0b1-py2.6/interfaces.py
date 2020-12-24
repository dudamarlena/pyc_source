# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/interfaces.py
# Compiled at: 2010-08-19 05:10:29
"""
interfaces.py

Created by Manabu Terada on 2010-08-12.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from zope.interface import Interface
from zope.schema import Bool, Int, List, TextLine
from c2.app.shorturl import ShortUrlMessageFactory as _

class IShortUrlSchema(Interface):
    base_url = TextLine(title=_('Base URL'), default='', description=_('Prefix URL (eg: http://www.cmscom.jp)'))
    folder_id = TextLine(title=_('Folder ID'), default='', description=_('Container for Short URL'))


class IShortUrlConfig(IShortUrlSchema):
    """ utility to hold the configuration related to Short URL """
    pass