# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/subrip2html/mimetype.py
# Compiled at: 2010-12-29 09:38:12
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem

class SubRipMimetype(MimeTypeItem):
    __module__ = __name__
    __name__ = 'SubRip'
    mimetypes = ('text/srt', 'application/x-subrip', 'text/plain')
    extensions = ('srt', )
    globs = ('*.srt', )
    binary = 0