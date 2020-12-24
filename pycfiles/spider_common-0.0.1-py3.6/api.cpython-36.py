# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/clue/api.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 2441 bytes
from parser_engine.singleton import Singleton
import requests
from .models import Clue
from ..common_utils import ApiCallException, InitArgsException

@Singleton
class ClueApi:

    def __init__(self, **kwargs):
        self.api = kwargs.pop('api')
        if not self.api:
            raise InitArgsException('ClueApi no api config')

    def _switch(self, api):
        self.api = api

    def get_by_id(self, clue_id):
        resp = requests.get(self.api + '/' + str(clue_id))
        if resp.status_code == 200:
            if resp.json()['code'] == 0:
                return Clue(resp.json()['data'])
        else:
            if resp.status_code == 404:
                raise ApiCallException(404)
            else:
                raise ApiCallException(resp.status_code)

    def partial_get_by_id(self, clue_id, keys):
        resp = requests.get(self.api + '/' + str(clue_id), {'keys': ','.join(keys)})
        if resp.status_code == 200:
            if resp.json()['code'] == 0:
                return resp.json()['data']
        else:
            if resp.status_code == 404:
                raise ApiCallException(404)
            else:
                raise ApiCallException(resp.status_code)

    def update(self, data):
        clue_id = data.pop('id')
        resp = requests.put((self.api + '/' + str(clue_id)), json=data)
        return resp.status_code == 200 and resp.json()['code'] == 0

    def create(self, data, project=None, spider=None, from_clue_id=0):
        """

        :param data:
        :param project:
        :param spider:
        :param from_clue_id:
        :return: [{clue}]
        """
        if isinstance(data, list):
            if project is not None:
                if spider is not None:
                    resp = requests.post(url=(self.api + '/'), json={'project':project, 
                     'spider':spider,  'from_clue_id':from_clue_id,  'clues':data})
        else:
            resp = requests.post(url=(self.api + '/'), json={'project':data.pop('project', data.pop('channel')), 
             'spider':data.pop('spider', data.pop('name')), 
             'from_clue_id':data.pop('from_clue_id', 0), 
             'clues':[
              data]})
        if resp.status_code == 200:
            if resp.json()['code'] == 0:
                return [Clue(item) for item in resp.json()['data']]
        raise ApiCallException('create clue failed', resp.status_code)