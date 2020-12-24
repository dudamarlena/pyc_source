# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/Field.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 669 bytes
import bitwarden_simple_cli.models.domain.CipherString as CipherString
from bitwarden_simple_cli.models.domain.DomainBase import Domain
import bitwarden_simple_cli.models.data.FieldData as FieldData
import bitwarden_simple_cli.enums.FieldType as FieldType

class Field(Domain):
    name: CipherString
    value: CipherString
    type: FieldType

    def __init__(self, obj, already_encrypted=False):
        super().__init__()
        if obj is None:
            return
        self.type = FieldType(int(obj['type']))
        self.build_domain_model(self, obj, {'name':None, 
         'value':None}, already_encrypted, [])