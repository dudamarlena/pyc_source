# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/botocore_patch.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 1605 bytes
from __future__ import absolute_import
from okera import odas, _default_context
import boto3, botocore
_original_make_api_call = None

def patch_botocore():
    global _original_make_api_call
    _original_make_api_call = botocore.client.BaseClient._make_api_call
    botocore.client.BaseClient._make_api_call = _patched_make_api_call


def _patched_make_api_call(client, operation_name, api_params):
    if _default_context and operation_name == 'GetObject':
        return _make_get_object_api_call(_default_context, client, api_params)
    return _original_make_api_call(client, operation_name, api_params)


def _make_get_object_api_call(planner, client, api_params):
    path = 's3://{0}/{1}'.format(api_params['Bucket'], api_params['Key'])
    urllib_response = planner.open(path, version=api_params.get('VersionId', None), preload_content=False)
    shape = client._service_model.shape_for('GetObjectOutput')
    op_model = client._service_model.operation_model('GetObject')
    http_response = botocore.awsrequest.AWSResponse(path, urllib_response.status, urllib_response.headers, urllib_response)
    response_dict = botocore.endpoint.convert_to_response_dict(http_response, op_model)
    return client._response_parser.parse(response_dict, shape)