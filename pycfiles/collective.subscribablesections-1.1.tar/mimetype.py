# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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