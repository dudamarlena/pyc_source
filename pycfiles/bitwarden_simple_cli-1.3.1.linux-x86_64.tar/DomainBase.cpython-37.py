# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/DomainBase.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 712 bytes
import bitwarden_simple_cli.models.domain.CipherString as CipherString

class Domain:

    def __setitem__(self, item, value):
        setattr(self, item, value)

    @staticmethod
    def build_domain_model(domain, data_obj, mapping, already_encrypted, not_enc_list):
        for prop in mapping:
            if prop not in data_obj:
                continue
            obj_prop = data_obj[(mapping[prop] or prop)]
            if already_encrypted or prop in not_enc_list:
                domain[prop] = obj_prop if obj_prop else None
            else:
                domain[prop] = CipherString.CipherString(obj_prop) if obj_prop else None

    def __getitem__(self, item):
        return getattr(self, item)