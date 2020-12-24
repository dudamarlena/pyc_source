# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sunwatcher/ifttt/maker.py
# Compiled at: 2016-08-14 13:04:41
# Size of source mod 2**32: 665 bytes
MAKER_ENDPOINT = 'https://maker.ifttt.com/trigger/%s/with/key/%s'
import requests

class Maker(object):

    def __init__(self, key):
        self.key = key

    def trigger(self, event, values=[]):
        if len(values) > 3:
            raise ValueError('Can only supply up to 3 values')
        data = {}
        if len(values) >= 1:
            data['value1'] = values[0]
        if len(values) >= 2:
            data['value2'] = values[1]
        if len(values) >= 3:
            data['value3'] = values[2]
        url = MAKER_ENDPOINT % (event, self.key)
        r = requests.post(url, json=data)
        return r.status_code == 200