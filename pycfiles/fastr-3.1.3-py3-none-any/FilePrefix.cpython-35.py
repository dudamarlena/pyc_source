# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/FilePrefix.py
# Compiled at: 2018-08-22 15:09:33
# Size of source mod 2**32: 1329 bytes
import os
from fastr.data import url
from fastr.datatypes import URLType
from fastr.helpers.checksum import hashsum

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