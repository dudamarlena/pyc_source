# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/megrok/form/fields.py
# Compiled at: 2008-04-23 23:50:41
from zope import interface, schema
from collective.namedfile.field import NamedImage as Image
from collective.namedfile.field import NamedFile as File
from collective.namedblobfile.field import NamedBlobImage as BlobImage
from collective.namedblobfile.field import NamedBlobFile as BlobFile
import constraints, interfaces

class Email(schema.TextLine):
    __module__ = __name__

    def __init__(self, **kw):
        kw['constraint'] = constraints.isEmail
        super(Email, self).__init__(**kw)


class HTML(schema.Text):
    __module__ = __name__
    interface.implements(interfaces.IHTML)