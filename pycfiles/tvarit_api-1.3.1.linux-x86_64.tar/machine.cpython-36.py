# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/machine.py
# Compiled at: 2019-09-30 09:28:30
# Size of source mod 2**32: 1937 bytes
from .base import Base

class Machine(Base):

    def __init__(self, api):
        super(Machine, self).__init__(api)
        self.api = api

    def get_machine_by_id(self, machine_id, brief=False, depends=False, rdepends=False, get_depends=False, resolve=None):
        if type(machine_id) == list:
            machine_id = ','.join([str(m) for m in machine_id])
        params = dict(brief=brief,
          depends=depends,
          rdepends=rdepends,
          get_depends=get_depends,
          resolve=(resolve or []))
        endpoint = '/machines/{}'.format(machine_id)
        return self.api.GET(endpoint, params=params)

    def create_machine(self, machine, update_if_exists=False):
        params = dict(update_if_exists=update_if_exists)
        endpoint = '/machines'
        return self.api.POST(endpoint, json=machine, params=params)

    def update_machine(self, machine_id, machine):
        endpoint = '/machines/{}'.format(machine_id)
        return self.api.PUT(endpoint, json=machine)

    def upload_machine_json(self, machines, strict=False):
        params = dict(strict=strict)
        endpoint = '/machines/json'
        return self.api.POST(endpoint, json=machines, params=params)

    def list_machines(self, detail=False, depends=False, rdepends=False, resolve=None, limit=100, page=0):
        params = dict(detail=detail,
          depends=depends,
          rdepends=rdepends,
          resolve=(resolve or []),
          limit=limit,
          page=page)
        endpoint = '/machines'
        return self.api.GET(endpoint, params=params)

    def delete_machine_by_id(self, machine_id):
        if type(machine_id) == list:
            machine_id = ','.join([str(m) for m in machine_id])
        endpoint = '/machines/{}'.format(machine_id)
        return self.api.DELETE(endpoint)