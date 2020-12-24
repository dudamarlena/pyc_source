# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/file.py
# Compiled at: 2012-06-20 10:07:04
from z3c.form.interfaces import IFileWidget
from zope.schema.interfaces import IBytes
from z3c.form.converter import FileUploadDataConverter as BaseDataConverter
from zope.component import adapts

class FileUploadDataConverter(BaseDataConverter):
    adapts(IBytes, IFileWidget)

    def toWidgetValue(self, value):
        return value or ''