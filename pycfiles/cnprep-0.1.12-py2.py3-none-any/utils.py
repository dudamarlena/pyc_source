# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnpsdk/utils.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, print_function, unicode_literals
import json, os, pyxb, xmltodict
from cnpsdk import fields_chargeback
from . import version

class Configuration(object):
    """Setup Configuration variables.

    Attributes:
        user (Str): authentication.user
        password (Str): authentication.password
        merchant_id (Str): The unique string to identify the merchant within the system.
        url (Str): Url for server.
        proxy (Str): Https proxy server address. Must start with "https://"
        print_xml (Str): Whether print request and response xml
    """
    VERSION = version.VERSION
    RELEASE = version.RELEASE
    _CONFIG_FILE_PATH = os.path.join(os.environ[b'CNP_CHARGEBACK_SDK_CONFIG'], b'.cnp_chargeback_sdk.conf') if b'CNP_CHARGEBACK_SDK_CONFIG' in os.environ else os.path.join(os.path.expanduser(b'~'), b'.cnp_chargeback_sdk.conf')

    def __init__(self, conf_dict=dict()):
        attr_dict = {b'username': b'', 
           b'password': b'', 
           b'merchant_id': b'', 
           b'url': b'http://www.testvantivcnp.com/sandbox/new', 
           b'proxy': b'', 
           b'print_xml': False, 
           b'neuter_xml': False}
        for k in attr_dict:
            setattr(self, k, attr_dict[k])

        try:
            with open(self._CONFIG_FILE_PATH, b'r') as (config_file):
                config_json = json.load(config_file)
                for k in attr_dict:
                    if k in config_json and config_json[k]:
                        setattr(self, k, config_json[k])

        except:
            pass

        if conf_dict:
            for k in conf_dict:
                if k in attr_dict:
                    setattr(self, k, conf_dict[k])
                else:
                    raise ChargebackError(b'"%s" is NOT an attribute of conf' % k)

    def save(self):
        """Save Class Attributes to .cnp_chargeback_sdk.conf

        Returns:
            full path for configuration file.

        Raises:
            IOError: An error occurred
        """
        with open(self._CONFIG_FILE_PATH, b'w') as (config_file):
            json.dump(vars(self), config_file)
        return self._CONFIG_FILE_PATH


def obj_to_xml(obj):
    """Convert object to xml string without namespaces

    Args:
        obj: Object

    Returns:
        Xml string

    Raises:
        pyxb.ValidationError
    """
    try:
        xml = obj.toxml(b'utf-8')
    except pyxb.ValidationError as e:
        raise ChargebackError(e.details())

    xml = xml.replace(b'ns1:', b'')
    xml = xml.replace(b':ns1', b'')
    return xml


def generate_retrieval_response(http_response, return_format=b'dict'):
    return convert_to_format(http_response.text, b'chargebackRetrievalResponse', return_format)


def generate_update_response(http_response, return_format=b'dict'):
    return convert_to_format(http_response.text, b'chargebackUpdateResponse', return_format)


def generate_document_response(http_response, return_format=b'dict'):
    return convert_to_format(http_response.text, b'chargebackDocumentUploadResponse', return_format)


def generate_error_response(http_response, return_format=b'dict'):
    return convert_to_format(http_response.text, b'errorResponse', return_format)


def convert_to_format(http_response, response_type, return_format=b'dict'):
    return_format = return_format.lower()
    if return_format == b'xml':
        response_xml = http_response.text
        return response_xml
    else:
        if return_format == b'object':
            return convert_to_obj(http_response.text)
        return convert_to_dict(http_response, response_type)


def convert_to_obj(xml_response):
    return fields_chargeback.CreateFromDocument(xml_response)


def convert_to_dict(xml_response, response_type):
    response_dict = xmltodict.parse(xml_response)[response_type]
    if response_dict[b'@xmlns'] != b'':
        _create_lists(response_dict)
        return response_dict
    raise ChargebackError(b'Invalid Format')


def _create_lists(response_dict):
    if b'chargebackCase' in response_dict:
        _create_list(b'chargebackCase', response_dict)
        for case in response_dict[b'chargebackCase']:
            if b'activity' in case:
                _create_list(b'activity', case)

    if b'errors' in response_dict:
        _create_list(b'error', response_dict[b'errors'])


def _create_list(element_key, container):
    element_value = container[element_key]
    if element_value != b'' and not isinstance(element_value, list):
        container[element_key] = [
         element_value]


class ChargebackError(Exception):

    def __init__(self, message):
        self.message = message


class ChargebackWebError(Exception):

    def __init__(self, message, code, error_list=None):
        self.message = message
        self.code = code
        self.error_list = error_list


class ChargebackDocumentError(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code