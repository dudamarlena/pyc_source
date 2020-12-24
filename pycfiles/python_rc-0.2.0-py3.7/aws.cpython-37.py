# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/provider/aws.py
# Compiled at: 2020-01-09 18:00:21
# Size of source mod 2**32: 516 bytes
from rc.util import run
import json
from functools import lru_cache

@lru_cache(maxsize=1)
def _get_regions():
    regions = json.loads(run([
     'aws', 'ec2', 'describe-regions', '--region', 'us-west-1']).stdout)['Regions']
    return list(map(lambda region: region['RegionName'], regions))


def list():
    regions = _get_regions()
    instances = []
    for r in regions:
        region_instances = json.loads(run([
         'aws', 'ec2', 'describe-instances', '--region', r]).stdout)['Reservations'][0]