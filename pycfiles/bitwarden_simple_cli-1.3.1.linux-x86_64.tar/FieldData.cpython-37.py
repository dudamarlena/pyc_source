# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/data/FieldData.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 446 bytes
import bitwarden_simple_cli.enums.FieldType as FieldType
import bitwarden_simple_cli.models.api.FieldApi as FieldApi

class FieldData:
    type: FieldType
    name: str
    value: str

    def __init__(self, response: FieldApi):
        if response is None:
            return
        self.type = response.type
        self.name = response.name
        self.value = response.value

    def __getattr__(self, item):
        return self.item