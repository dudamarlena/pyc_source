# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\restfns.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 2082 bytes
import requests

def do_get(endpoint, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    return requests.get(endpoint, headers=headers).json()


def do_get_next(endpoint, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    looping = True
    value_list = []
    vm_dict = {}
    while looping:
        get_return = requests.get(endpoint, headers=headers).json()
        if 'value' not in get_return:
            return get_return
        if 'nextLink' not in get_return:
            looping = False
        else:
            endpoint = get_return['nextLink']
        value_list += get_return['value']

    vm_dict['value'] = value_list
    return vm_dict


def do_delete(endpoint, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    return requests.delete(endpoint, headers=headers)


def do_patch(endpoint, body, access_token):
    headers = {'content-type':'application/json', 
     'Authorization':'Bearer ' + access_token}
    return requests.patch(endpoint, data=body, headers=headers)


def do_post(endpoint, body, access_token):
    headers = {'content-type':'application/json', 
     'Authorization':'Bearer ' + access_token}
    return requests.post(endpoint, data=body, headers=headers)


def do_put(endpoint, body, access_token):
    headers = {'content-type':'application/json', 
     'Authorization':'Bearer ' + access_token}
    return requests.put(endpoint, data=body, headers=headers)