# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pdfkit/source.py
# Compiled at: 2016-12-19 08:41:12
import os, io

class Source(object):

    def __init__(self, url_or_file, type_):
        self.source = url_or_file
        self.type = type_
        if self.type is 'file':
            self.checkFiles()

    def isUrl(self):
        return 'url' in self.type

    def isFile(self, path=None):
        if path:
            return isinstance(path, io.IOBase) or path.__class__.__name__ == 'StreamReaderWriter'
        else:
            return 'file' in self.type

    def checkFiles(self):
        if isinstance(self.source, list):
            for path in self.source:
                if not os.path.exists(path):
                    raise IOError('No such file: %s' % path)

        elif not hasattr(self.source, 'read') and not os.path.exists(self.source):
            raise IOError('No such file: %s' % self.source)

    def isString(self):
        return 'string' in self.type

    def isFileObj(self):
        return hasattr(self.source, 'read')

    def to_s(self):
        return self.source