# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/common/messaging/utils.py
# Compiled at: 2016-12-18 15:26:05
# Size of source mod 2**32: 6178 bytes
"""
The utils module gathers all utility functions used in messaging

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import os, socket, platform, datetime, json, logging
from of import __release__, __copyright__
import requests, sys
from requests.cookies import RequestsCookieJar
from of.common.logging import write_to_log, EC_NOTIFICATION, SEV_DEBUG, SEV_FATAL, EC_SERVICE, SEV_ERROR, EC_COMMUNICATION
from of.common.messaging.factory import get_current_login
import requests, urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
__author__ = 'Nicklas Borjesson'

def make_log_prefix(_name):
    return _name + '(' + str(os.getpid()) + '):'


def sys_modules():
    result = []
    for curr_key in sys.modules.keys():
        result.append(curr_key)

    return result


def get_environment_data():

    def python_versions():
        _major, _minor, _release, _state, _build = sys.version_info
        return str(_major) + '.' + str(_minor) + '.' + str(_release) + ' ' + _state + ' build ' + str(_build)

    return {'hostname': socket.gethostname(), 
     'Optimal Framework': {'Version': __release__, 
                           'Copyright': __copyright__}, 
     
     'Python': {'Version': python_versions(), 
                'Modules': sys_modules()}, 
     
     'Platform': platform.system(), 
     'Processor': platform.processor(), 
     'SystemPid': os.getpid(), 
     'User': get_current_login()}


def write_dbg_info(_data):
    write_to_log(_data, _category=EC_NOTIFICATION, _severity=SEV_DEBUG)


def register_at_broker(_address, _type, _server, _username, _password, _log_prefix='', _verify_SSL=True):
    _log_prefix = make_log_prefix(_log_prefix)
    _data = {'credentials': {'usernamePassword': {'username': _username, 
                                          'password': _password}}, 
     
     'environment': get_environment_data(), 
     'peerType': _type, 
     'address': _address}
    write_dbg_info(_log_prefix + '[' + str(datetime.datetime.utcnow()) + '] Registering at broker API.')
    _headers = {'content-type': 'application/json'}
    _response = requests.post(_server + '/register', data=json.dumps(_data), auth=('user',
                                                                                   'pass'), headers=_headers, verify=_verify_SSL)
    if _response.status_code == 500:
        write_dbg_info(_log_prefix + 'Broker login failed with internal server error! Exiting.')
        return False
    else:
        if _response.status_code != 200:
            write_dbg_info(_log_prefix + 'Broker login failed with error + ' + str(_response.status_code) + '! Exiting.')
            return False
        _response_dict = _response.json()
        if _response_dict is not None:
            _data = _response_dict
            if 'session_id' in _data:
                write_dbg_info(_log_prefix + 'Got a session id:' + _data['session_id'])
                return _data
            write_to_log(_log_prefix + 'Broker login failed! Exiting.', _category=EC_SERVICE, _severity=SEV_ERROR)
            return False
        write_to_log(_log_prefix + 'Broker login failed! Exiting.', _category=EC_SERVICE, _severity=SEV_ERROR)
        return False


def call_api(_url, _session_id, _data, _timeout=None, _print_log=None, _verify_SSL=True):
    """

    :param _url:
    :param _session_id:
    :param _data:
    :param _timeout:
    :param _print_log: Do not call write to log
    :return:
    """

    def do_log(_error, _category=EC_NOTIFICATION, _severity=SEV_DEBUG):
        if _print_log:
            print(_error)
        else:
            write_to_log(_data, _category=_category, _severity=_severity)
        return _error

    _cookie_jar = RequestsCookieJar()
    _cookie_jar.set(name='session_id', value=_session_id, secure=True)
    _headers = {'content-type': 'application/json'}
    _response = requests.post(_url, data=json.dumps(_data), headers=_headers, timeout=_timeout, verify=_verify_SSL, cookies=_cookie_jar)
    _response_dict = None
    if _response.status_code != 200:
        do_log('Response code :' + str(_response.status_code))
        try:
            _response.raise_for_status()
        except Exception as e:
            raise Exception(do_log('Error in call_api:' + str(e), _category=EC_COMMUNICATION, _severity=SEV_ERROR))

    elif _response.content:
        try:
            _response_dict = _response.json()
        except Exception as e:
            do_log("response.content didn't contain JSON data", _category=EC_COMMUNICATION, _severity=SEV_ERROR)
            _response_dict = None

        if _response_dict is not None:
            return _response_dict
        else:
            do_log('Got an empty response from server:' + str(_response.content), _category=EC_COMMUNICATION, _severity=SEV_ERROR)
            return


def make_error(_code, _message):
    return {'error_code': _code, 
     'message': _message}


def message_is_none(_message, _property, _value):
    """
    If a property is unset, return value, otherwise the specified property

    :param _message: The message
    :param _property: The name of the property
    :param _value: The value
    :return: A value
    """
    if _property in _message:
        return _message[_property]
    else:
        return _value


class MultiprocessingLoggingHandler:
    level = 0
    debug_prefix = None

    def handle(self, _record):
        write_dbg_info(self.debug_prefix + ': ' + str(_record))

    def __init__(self, _log_prefix=None, _level=None):
        if _log_prefix is not None:
            self.debug_prefix = _log_prefix
        else:
            self.debug_prefix = 'No debug_prefix set'
        if _level is not None:
            self.level = _level
        else:
            self.level = logging.INFO