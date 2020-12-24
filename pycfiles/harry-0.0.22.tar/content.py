# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/content.py
# Compiled at: 2012-06-19 11:02:04


class Content(object):

    def __init__(self, j):
        self.raw = j
        self.size = self.raw['size']
        if 'compression' in self.raw:
            self.compression = self.raw['compression']
        else:
            self.compression = ''
        self.mime_type = self.raw['mimeType']
        if 'text' in self.raw:
            self.text = self.raw['text']
        else:
            self.text = ''
        if 'encoding' in self.raw:
            self.encoding = self.raw['encoding']
        else:
            self.encoding = ''
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''