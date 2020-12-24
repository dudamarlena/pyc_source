# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyzenobase/main.py
# Compiled at: 2015-03-08 08:20:05
# Size of source mod 2**32: 4862 bytes
import time, json
from pprint import pprint
import unittest
from random import randint
from datetime import datetime
import pytz
from tzlocal import get_localzone
import requests

class ZenobaseAPI:
    HOST = 'https://api.zenobase.com'

    def __init__(self, username=None, password=None):
        payload = {}
        if username is not None:
            payload = {'grant_type': 'password',  'username': username,  'password': password}
        else:
            payload = {'grant_type': 'client_credentials'}
        r = requests.post(self.HOST + '/oauth/token', data=payload)
        data = r.json()
        if 'error' in data:
            raise Exception('Invalid Zenobase credentials')
        self.access_token = data['access_token']
        self.client_id = data['client_id']

    def _request(self, method, endpoint, data=None, headers={}):
        url = self.HOST + endpoint
        headers['Authorization'] = 'Bearer {}'.format(self.access_token)
        headers['Content-Type'] = 'application/json'
        args = [url]
        kwargs = {'data': json.dumps(data),  'headers': headers}
        r = method(*args, **kwargs)
        if not 200 <= r.status_code < 300:
            raise Exception('Status code was not 2xx: {}'.format(r))
        if 'content-type' in r.headers:
            if 'application/json' in r.headers['content-type']:
                return r.json()
        return r.text

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def list_buckets(self):
        return self._get('/users/{}/buckets/'.format(self.client_id))

    def get_bucket(self, bucket_id):
        return self._get('/buckets/{}'.format(bucket_id))

    def create_bucket(self, label, description=''):
        if not 1 <= len(label) <= 20:
            raise Exception('Bucket name must be 1-20 chars and can only contain [a-zA-Z0-9-_ ]')
        return self._post('/buckets/', data={'label': label,  'description': description})

    def create_or_get_bucket(self, label, description=''):
        data = self.list_buckets()
        for bucket in data['buckets']:
            if bucket['label'] == label:
                return bucket

        return self.create_bucket(label, description=description)

    def delete_bucket(self, bucket_id):
        self._delete('/buckets/{}'.format(bucket_id))

    def list_events(self, bucket_id):
        return self._get('/buckets/{}/'.format(bucket_id))

    def create_event(self, bucket_id, event):
        if not isinstance(event, ZenobaseEvent):
            assert isinstance(event, dict)
            return self._post('/buckets/{}/'.format(bucket_id), data=event)

    def create_events(self, bucket_id, events):
        assert isinstance(events, list)
        for event in events:
            if not isinstance(event, ZenobaseEvent):
                if not isinstance(event, dict):
                    raise AssertionError

        return self._post('/buckets/' + bucket_id + '/', data={'events': events})

    def close(self):
        return self._delete('/authorizations/' + self.access_token)


_VALID_FIELDS = [
 'bits', 'concentration', 'count', 'currency', 'distance',
 'distance/volume', 'duration', 'energy', 'frequency', 'height',
 'humidity', 'location', 'moon', 'note', 'pace', 'percentage',
 'pressure', 'rating', 'resource', 'sound', 'source', 'tag',
 'temperature', 'timestamp', 'velocity', 'volume', 'weight']

class ZenobaseEvent(dict):
    __doc__ = '\n        Provides simple structure checking\n    '

    def __init__(self, data):
        for field in data:
            assert field in _VALID_FIELDS
            self[field] = data[field]

        if 'timestamp' in self:
            self._check_timestamp()
            if type(self['timestamp']) == list:
                pass
            datetimes_to_string = --- This code section failed: ---

 L. 112         0  LOAD_GLOBAL              type
                3  LOAD_FAST                'x'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  LOAD_GLOBAL              datetime
               12  COMPARE_OP               ==
               15  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_GLOBAL              fmt_datetime
               21  LOAD_FAST                'x'
               24  CALL_FUNCTION_1       1  '1 positional, 0 named'
               27  RETURN_END_IF_LAMBDA
             28_0  COME_FROM            15  '15'
               28  LOAD_FAST                'x'
               31  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            self['timestamp'] = list(map(datetimes_to_string, self['timestamp']))
        elif type(self['timestamp']) == datetime:
            self['timestamp'] = fmt_datetime(self['timestamp'])

    def _check_timestamp(self):
        if type(self['timestamp']) not in (str, datetime, list):
            if type(self['timestamp']) != list or all(map(lambda x: type(x) in (str, datetime), self['timestamp'])):
                raise TypeError('timestamp must be string, datetime or list of strings/datetimes')


def fmt_datetime(dt, timezone=str(get_localzone())):
    tz = pytz.timezone(timezone)
    dt = dt.astimezone(tz) if dt.tzinfo else tz.localize(dt)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000%z')