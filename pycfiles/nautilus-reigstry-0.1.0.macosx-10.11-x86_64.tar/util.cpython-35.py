# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/nautilus-registry/util.py
# Compiled at: 2016-06-22 05:46:09
# Size of source mod 2**32: 2103 bytes
import json, requests
from nautilus.conventions.services import api_gateway_name
from .registry import service_location_by_name

def query_graphql_service(url, name, fields, filters=None, query_type='query'):
    """ A graphql query wrapper factory """
    args = ''
    if filters:
        arg_string = ', '.join(['{}: {}'.format(key, json.dumps(value)) for key, value in filters.items()])
        args = '(%s)' % arg_string if len(arg_string) > 0 else ''
    field_list = ', '.join(fields)
    query = '%s { %s %s { %s } }' % (query_type, name, args, field_list)
    data_request = requests.get(url + '?query=' + query).json()
    if 'errors' in data_request and data_request['errors']:
        raise RuntimeError(data_request['errors'])
    else:
        return data_request['data'][name]


def query_service(service, fields, name=None, filters=None):
    """
        Apply the given filters to a query of a model service given its name
        and the desired fields.
    """
    from nautilus.conventions import root_query
    return query_graphql_service(url='http://{}'.format(service_location_by_name(service)), name=name or root_query(service), fields=fields, filters=filters or {})


def query_api(model, fields, filters=None):
    """
        Perform the given query on the api gateway and turn the results.
        Use this function to avoid hard coding the name of the api gateway.
    """
    return query_service(api_gateway_name(), fields, filters, name=model)