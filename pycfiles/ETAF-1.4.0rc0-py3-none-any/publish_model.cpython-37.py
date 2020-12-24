# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/manager/model_manager/publish_model.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 4927 bytes
import grpc
from arch.api.proto import model_service_pb2
from arch.api.proto import model_service_pb2_grpc
from fate_flow.settings import stat_logger
from fate_flow.utils import model_utils
from fate_flow.manager.model_manager import pipelined_model

def generate_publish_model_info(config_data):
    model_id = config_data['job_parameters']['model_id']
    model_version = config_data['job_parameters']['model_version']
    config_data['model'] = {}
    for role, role_party in config_data.get('role').items():
        config_data['model'][role] = {}
        for party_id in role_party:
            config_data['model'][role][party_id] = {'model_id':model_utils.gen_party_model_id(model_id, role, party_id), 
             'model_version':model_version}


def load_model(config_data):
    stat_logger.info(config_data)
    success = True
    for serving in config_data.get('servings'):
        with grpc.insecure_channel(serving) as (channel):
            stub = model_service_pb2_grpc.ModelServiceStub(channel)
            load_model_request = model_service_pb2.PublishRequest()
            for role_name, role_partys in config_data.get('role').items():
                for _party_id in role_partys:
                    load_model_request.role[role_name].partyId.append(_party_id)

            for role_name, role_model_config in config_data.get('model').items():
                for _party_id, role_party_model_config in role_model_config.items():
                    load_model_request.model[role_name].roleModelInfo[_party_id].tableName = role_party_model_config['model_version']
                    load_model_request.model[role_name].roleModelInfo[_party_id].namespace = role_party_model_config['model_id']

            stat_logger.info('request serving: {} load model'.format(serving))
            load_model_request.local.role = config_data.get('local').get('role')
            load_model_request.local.partyId = config_data.get('local').get('party_id')
            stat_logger.info(load_model_request)
            response = stub.publishLoad(load_model_request)
            stat_logger.info('{} {} load model status: {}'.format(load_model_request.local.role, load_model_request.local.partyId, response.statusCode))
            if response.statusCode != 0:
                success = False

    return success


def bind_model_service(config_data):
    service_id = config_data.get('service_id')
    initiator_role = config_data['initiator']['role']
    initiator_party_id = config_data['initiator']['party_id']
    model_id = config_data['job_parameters']['model_id']
    model_version = config_data['job_parameters']['model_version']
    status = True
    for serving in config_data.get('servings'):
        with grpc.insecure_channel(serving) as (channel):
            stub = model_service_pb2_grpc.ModelServiceStub(channel)
            publish_model_request = model_service_pb2.PublishRequest()
            publish_model_request.serviceId = service_id
            for role_name, role_party in config_data.get('role').items():
                publish_model_request.role[role_name].partyId.extend(role_party)

            publish_model_request.model[initiator_role].roleModelInfo[initiator_party_id].tableName = model_version
            publish_model_request.model[initiator_role].roleModelInfo[initiator_party_id].namespace = model_utils.gen_party_model_id(model_id, initiator_role, initiator_party_id)
            publish_model_request.local.role = initiator_role
            publish_model_request.local.partyId = initiator_party_id
            stat_logger.info(publish_model_request)
            response = stub.publishBind(publish_model_request)
            stat_logger.info(response)
            if response.statusCode != 0:
                status = False

    return (
     status, service_id)


def download_model(request_data):
    model = pipelined_model.PipelinedModel(model_id=(request_data.get('namespace')), model_version=(request_data.get('name')))
    model_data = model.collect_models(in_bytes=True)
    return model_data