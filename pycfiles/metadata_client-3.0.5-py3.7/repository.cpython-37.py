# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/modules/repository.py
# Compiled at: 2019-08-14 10:42:37
# Size of source mod 2**32: 3556 bytes
"""Repository module class"""
from apis.repostory_api import RepositoryApi
from common.base import Base
from ..common.config import *
MODULE_NAME = REPOSITORY

class Repository(RepositoryApi):

    def __init__(self, metadata_client, name, identifier, mount_point, transfer_agent_identifier, transfer_agent_server_url, flg_context, flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.identifier = identifier
        self.mount_point = mount_point
        self.transfer_agent_identifier = transfer_agent_identifier
        self.transfer_agent_server_url = transfer_agent_server_url
        self.flg_context = flg_context
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_repository_api(self._Repository__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_repository_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_repository_api(self.id, self._Repository__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, repository_id):
        response = mdc_client.get_repository_by_id_api(repository_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(mdc_client, name):
        response = mdc_client.get_all_repositories_by_name_api(name)
        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_identifier(mdc_client, identifier):
        response = mdc_client.get_all_repositories_by_identifier_api(identifier)
        Base.cal_debug(MODULE_NAME, 'get_all_by_identifier', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name(mdc_client, name):
        res = Repository.get_all_by_name(mdc_client, name)
        if res['success']:
            res = Base.unique_key_format_result(res=res, module_name=MODULE_NAME,
              unique_id=name)
        return res

    def __get_resource(self):
        repository = {MODULE_NAME: {'name':self.name, 
                       'identifier':self.identifier, 
                       'mount_point':self.mount_point, 
                       'transfer_agent_identifier':self.transfer_agent_identifier, 
                       'transfer_agent_server_url':self.transfer_agent_server_url, 
                       'flg_context':self.flg_context, 
                       'flg_available':self.flg_available, 
                       'description':self.description}}
        return repository