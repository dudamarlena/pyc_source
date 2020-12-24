# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceresini/repos/forseti-enforcer-ideas/policy-enforcer/resources/__init__.py
# Compiled at: 2019-01-25 11:32:48
from .base import ResourceBase
from .bucket import Bucket
from .sql import SQLInstance
from .bigquery import BQDataset

def resource_lookup(context):
    resource_kind_map = {'storage#bucket': Bucket, 
       'bigquery#dataset': BQDataset, 
       'sql#instance': SQLInstance}
    kind = context.get('resource_kind')
    if not kind:
        return None
    else:
        if kind not in resource_kind_map:
            return None
        return resource_kind_map.get(kind)