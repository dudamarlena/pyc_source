# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/interfaces.py
# Compiled at: 2010-08-19 05:10:29
__doc__ = '\ninterfaces.py\n\nCreated by Manabu Terada on 2010-08-12.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
from zope.interface import Interface
from zope.schema import Bool, Int, List, TextLine
from c2.app.shorturl import ShortUrlMessageFactory as _

class IShortUrlSchema(Interface):
    base_url = TextLine(title=_('Base URL'), default='', description=_('Prefix URL (eg: http://www.cmscom.jp)'))
    folder_id = TextLine(title=_('Folder ID'), default='', description=_('Container for Short URL'))


class IShortUrlConfig(IShortUrlSchema):
    """ utility to hold the configuration related to Short URL """