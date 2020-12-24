# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opendxl/viji/opendxl-console/dxlconsole/util.py
# Compiled at: 2019-06-07 18:26:01
NO_RESULT_JSON = '{response:{status:0,startRow:0,endRow:0,totalRows:0,data:[]}}'

def create_sc_response_wrapper():
    """
    Creates a wrapper object containing the standard fields required by SmartClient responses

    :return: an initial SmartClient response wrapper
    """
    response_wrapper = {'response': {}}
    response = response_wrapper['response']
    response['status'] = 0
    response['startRow'] = 0
    response['endRow'] = 0
    response['totalRows'] = 0
    response['data'] = []
    return response_wrapper


def create_sc_error_response(error_message):
    """
    Creates an error response for the SmartClient UI with the given message

    :param error_message: The error message
    :return: The SmartClient response in dict form
    """
    response_wrapper = create_sc_response_wrapper()
    response = response_wrapper['response']
    response['status'] = -1
    response['data'] = error_message
    return response