# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/widgets.py
# Compiled at: 2016-03-08 06:27:04
from django.forms.widgets import FileInput

class FileMultiInput(FileInput):

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        super(FileMultiInput, self).__init__(attrs)
        return

    def value_from_datadict(self, data, files, name):
        if not hasattr(files, 'getlist'):
            return []
        return files.getlist(name)