# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/server.py
# Compiled at: 2016-05-27 19:49:05
from __future__ import unicode_literals
import os, json, requests
from raspautomation_cli.presence import Presence
from raspautomation_cli.io import IO
from raspautomation_cli.sensor import Sensor
from raspautomation_cli.camera import Camera
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

CONF_FILE = os.path.expanduser(b'~/.config/raspautomation_cli.conf')

class Server(object):
    url = None
    token = None
    presence = None
    io = []
    sensor = []
    camera = []

    def __init__(self, url, token, data={}):
        self.url = url
        self.token = token
        self._load_data(data)

    @property
    def api_url(self):
        return self.url + b'api/'

    @property
    def name(self):
        return urlparse(self.url).netloc.split(b'.')[0]

    @property
    def data(self):
        return {b'presence': self.presence.to_json(), 
           b'io': [ io.to_json() for key, io in self.io.items()
                ], 
           b'sensor': [ sensor.to_json() for key, sensor in self.sensor.items()
                    ], 
           b'camera': [ camera.to_json() for key, camera in self.camera.items()
                    ]}

    def _load_data(self, data):
        self.presence = Presence(self, data.get(b'presence', {}))
        self.io = {io.get(b'name'):IO(self, io) for io in data.get(b'io', [])}
        self.sensor = {sensor.get(b'name'):Sensor(self, sensor) for sensor in data.get(b'sensor', [])}
        self.camera = {camera.get(b'name'):Camera(self, camera) for camera in data.get(b'camera', [])}

    def _request(self, endpoint, method, data={}, reraise=True):
        headers = {b'Authorization': b'Token %s' % self.token}
        if not endpoint.endswith(b'/'):
            endpoint += b'/'
        r = getattr(requests, method)(self.api_url + endpoint, params={b'format': b'json'}, json=data, headers=headers, verify=False)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print b'Authentication failed.'
            if reraise:
                raise
            return False

        return r

    def get(self, endpoint, data={}, reraise=True):
        return self._request(endpoint, b'get', data=data, reraise=reraise)

    def post(self, endpoint, data={}, reraise=True):
        return self._request(endpoint, b'post', data=data, reraise=reraise)

    def patch(self, endpoint, data={}, reraise=True):
        return self._request(endpoint, b'patch', data=data, reraise=reraise)

    def test_auth(self):
        return self.get(b'', reraise=False).status_code == 200

    def refresh_data(self):
        self._load_data(self.get(b'all').json())
        self.save()

    @staticmethod
    def load():
        if not os.path.exists(CONF_FILE):
            return {}
        with open(CONF_FILE, b'r') as (f):
            return json.loads(f.read())

    @staticmethod
    def find(name):
        s = Server.load().get(name, None)
        if s is None:
            raise ValueError(b'Server not found.')
        return Server(**s)

    def save(self):
        to_save = {b'url': self.url, 
           b'token': self.token, 
           b'data': self.data}
        servers = Server.load()
        servers[self.name] = to_save
        with open(CONF_FILE, b'w') as (f):
            f.write(json.dumps(servers))