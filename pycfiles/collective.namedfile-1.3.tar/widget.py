# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/collective/namedblobfile/widget.py
# Compiled at: 2008-04-23 22:44:43
from collective.namedfile.widget import NamedFileWidget, NamedImageWidget, NamedFileDisplayWidget, NamedImageDisplayWidget
from blobfile import NamedBlobFile

class NamedBlobFileWidget(NamedFileWidget):
    __module__ = __name__

    def _toFieldValue(self, input):
        value = super(NamedFileWidget, self)._toFieldValue(input)
        if value is not self.context.missing_value:
            filename = getattr(input, 'filename', None)
            contenttype = input.headers.get('content-type', 'application/octet-stream')
            value = NamedBlobFile(value, contenttype, filename)
        return value


class NamedBlobImageWidget(NamedImageWidget):
    __module__ = __name__


class NamedBlobFileDisplayWidget(NamedFileDisplayWidget):
    __module__ = __name__


class NamedBlobImageDisplayWidget(NamedImageDisplayWidget):
    __module__ = __name__