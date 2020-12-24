# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/JsonFile.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 1211 bytes
import json
from fastr.datatypes import URLType
from fastr.helpers.checksum import hashsum

class JsonFile(URLType):
    description = 'json file'
    extension = 'json'

    def _validate(self):
        try:
            with open(self.parsed_value) as (fh_in):
                json.load(fh_in)
                return True
        except ValueError:
            return False

    def checksum(self):
        with open(self.parsed_value) as (fh_in):
            data = json.load(fh_in)
        return hashsum([data])