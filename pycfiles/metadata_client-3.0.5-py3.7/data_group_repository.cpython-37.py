# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/modules/data_group_repository.py
# Compiled at: 2017-06-28 20:05:41
# Size of source mod 2**32: 4492 bytes
"""DataGroupRepository module class"""
from apis.data_group_repository_api import DataGroupRepositoryApi
from common.base import Base
from ..common.config import *
MODULE_NAME = DATA_GROUP_REPOSITORY

class DataGroupRepository(DataGroupRepositoryApi):

    def __init__(self, metadata_client, data_group_id, repository_id, flg_available, id=None):
        self.metadata_client = metadata_client
        self.id = id
        self.data_group_id = data_group_id
        self.repository_id = repository_id
        self.flg_available = flg_available

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_data_group_repository_api(self._DataGroupRepository__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_data_group_repository_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_data_group_repository_api(self.id, self._DataGroupRepository__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def set_from_dict(mdc_client, data_group_repository):
        resp = DataGroupRepository.get_all_by_data_group_id_and_repository_id(mdc_client, data_group_repository['data_group_id'], data_group_repository['repository_id'])
        if resp['success']:
            if resp['data'] != []:
                existing_data_group_repository = DataGroupRepository(metadata_client=mdc_client,
                  id=(resp['data'][0]['id']),
                  data_group_id=(data_group_repository['data_group_id']),
                  repository_id=(data_group_repository['repository_id']),
                  flg_available=(data_group_repository['flg_available']))
                resp = existing_data_group_repository.update()
                return resp
        new_data_group_repository = DataGroupRepository(metadata_client=mdc_client,
          data_group_id=(data_group_repository['data_group_id']),
          repository_id=(data_group_repository['repository_id']),
          flg_available=(data_group_repository['flg_available']))
        resp = new_data_group_repository.create()
        return resp

    @staticmethod
    def create_from_dict(mdc_client, data_group_repository):
        new_data_group_repository = DataGroupRepository(metadata_client=mdc_client,
          data_group_id=(data_group_repository['data_group_id']),
          repository_id=(data_group_repository['repository_id']),
          flg_available=(data_group_repository['flg_available']))
        resp = new_data_group_repository.create()
        return resp

    @staticmethod
    def get_by_id(mdc_client, data_group_repository_id):
        response = mdc_client.get_data_group_repository_by_id_api(data_group_repository_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_data_group_id(mdc_client, data_group_id):
        response = mdc_client.get_all_by_data_group_id_api(data_group_id)
        Base.cal_debug(MODULE_NAME, 'get_all_by_data_group_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_data_group_id_and_repository_id(mdc_client, data_group_id, repository_id):
        resp = mdc_client.get_all_by_data_group_id_and_repository_id_api(data_group_id, repository_id)
        Base.cal_debug(MODULE_NAME, 'get_all_by_data_group_id_and_repository_id_api', resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    def __get_resource(self):
        data_group_repository = {MODULE_NAME: {'data_group_id':self.data_group_id, 
                       'repository_id':self.repository_id, 
                       'flg_available':self.flg_available}}
        return data_group_repository