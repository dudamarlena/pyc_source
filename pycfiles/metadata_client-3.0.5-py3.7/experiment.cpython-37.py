# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/modules/experiment.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 3658 bytes
"""Experiment module class"""
from apis.experiment_api import ExperimentApi
from common.base import Base
from ..common.config import *
MODULE_NAME = EXPERIMENT

class Experiment(ExperimentApi):

    def __init__(self, metadata_client, name, experiment_type_id, proposal_id, flg_available, publisher, contributor, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.doi = None
        self.experiment_type_id = experiment_type_id
        self.proposal_id = proposal_id
        self.flg_available = flg_available
        self.publisher = publisher
        self.contributor = contributor
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_experiment_api(self._Experiment__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_experiment_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_experiment_api(self.id, self._Experiment__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, experiment_id):
        response = mdc_client.get_experiment_by_id_api(experiment_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name_and_proposal_id(mdc_client, name, proposal_id):
        response = mdc_client.get_all_experiments_by_name_and_proposal_id_api(name, proposal_id)
        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_proposal_id(mdc_client, proposal_id):
        resp = mdc_client.get_all_experiments_by_proposal_id_api(proposal_id)
        Base.cal_debug(MODULE_NAME, 'get_all_by_proposal_id', resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name_and_proposal_id(mdc_client, name, proposal_id):
        res = Experiment.get_all_by_name_and_proposal_id(mdc_client, name, proposal_id)
        if res['success']:
            res = Base.unique_key_format_result(res=res, module_name=MODULE_NAME,
              unique_id=name)
        return res

    def __get_resource(self):
        experiment = {MODULE_NAME: {'name':self.name, 
                       'doi':self.doi, 
                       'experiment_type_id':self.experiment_type_id, 
                       'proposal_id':self.proposal_id, 
                       'flg_available':self.flg_available, 
                       'publisher':self.publisher, 
                       'contributor':self.contributor, 
                       'description':self.description}}
        return experiment