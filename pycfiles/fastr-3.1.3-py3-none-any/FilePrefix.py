# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/FilePrefix.py
# Compiled at: 2019-06-04 03:03:06
import os
from fastr.data import url
from fastr.datatypes import URLType
from fastr.utils.checksum import hashsum

class FilePrefix(URLType):
    description = 'Prefix for another file, including the path'
    extension = None

    def _validate(value):
        value = value.value
        try:
            if url.isurl(value):
                value = url.get_path_from_url(value)
        except ValueError:
            return False

        return os.path.isdir(os.path.dirname(value))

    def _parse(self):
        return self.value

    def checksum(self):
        return hashsum(self.value)