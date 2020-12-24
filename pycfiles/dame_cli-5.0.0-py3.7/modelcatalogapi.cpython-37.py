# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/modelcatalogapi.py
# Compiled at: 2020-05-04 13:31:17
# Size of source mod 2**32: 1971 bytes
from __future__ import print_function
import modelcatalog
from modelcatalog import ApiClient
from modelcatalog.rest import ApiException
from dame.configuration import get_credentials, DEFAULT_PROFILE
USERNAME = 'mint@isi.edu'

def api_configuration(profile):
    credentials = get_credentials(profile)
    if credentials is None:
        return (
         ApiClient(), USERNAME)
    configuration = modelcatalog.Configuration()
    configuration.host = credentials['server']
    return (ApiClient(configuration=configuration), credentials['username'])


def list_model_configuration(label=None, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.modelconfigurations_get(username=username)
        return api_response
    except ApiException as e:
        try:
            raise e
        finally:
            e = None
            del e


def get_model_configuration(_id, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.custom_modelconfigurations_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        try:
            raise e
        finally:
            e = None
            del e


def get_setup(_id, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        api_response = api_instance.custom_modelconfigurationsetups_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        try:
            raise e
        finally:
            e = None
            del e


def list_setup(label=None, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        api_response = api_instance.modelconfigurationsetups_get(username=username)
        return api_response
    except ApiException as e:
        try:
            raise e
        finally:
            e = None
            del e