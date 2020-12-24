# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/votec/workspace/git/redisy/redisy/converter.py
# Compiled at: 2018-07-24 23:26:57
# Size of source mod 2**32: 702 bytes
import pickle, json, gzip

class Converter:
    CONVERT_METHOD_MAP = {'raw':0, 
     'json':1, 
     'pickle':2, 
     'gz':3}
    from_impl = [
     lambda x: x,
     lambda x: json.dumps(x),
     lambda x: pickle.dumps(x),
     lambda x: gzip.compress(pickle.dumps(x))]
    to_impl = [
     lambda x: x.decode,
     lambda x: json.loads(x),
     lambda x: pickle.loads(x),
     lambda x: gzip.decompress(pickle.loads(x))]

    def __init__(self, method='json'):
        self.method_ = self.CONVERT_METHOD_MAP[method]
        self.from_value = self.from_impl[self.method_]
        self.to_value = self.to_impl[self.method_]