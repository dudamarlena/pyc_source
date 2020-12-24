# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/cloud-harness/gbdx_cloud_harness/utils/printer.py
# Compiled at: 2016-10-31 16:11:18
import json, sys

def printer(data):
    """
    response is json or straight text.
    :param data:
    :return:
    """
    data = str(data)
    if not isinstance(data, str):
        output = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    elif hasattr(data, 'json'):
        output = data.json()
    else:
        output = data
    sys.stdout.write(output)
    sys.stdout.write('\n')
    sys.stdout.flush()