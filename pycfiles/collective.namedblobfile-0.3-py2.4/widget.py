# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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