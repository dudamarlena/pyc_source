# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/utils/model_utils.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 924 bytes
from arch.api.utils import dtable_utils

def gen_party_model_id(model_id, role, party_id):
    if model_id:
        return dtable_utils.gen_party_namespace_by_federated_namespace(federated_namespace=model_id, role=role, party_id=party_id)