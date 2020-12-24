# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnpsdk/communication.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, print_function, unicode_literals
import mimetypes, re, requests
from requests.auth import HTTPBasicAuth
from cnpsdk import utils
conf = utils.Configuration()
CNP_CONTENT_TYPE = b'application/com.vantivcnp.services-v2+xml'
CHARGEBACK_API_HEADERS = {b'Accept': CNP_CONTENT_TYPE, b'Content-Type': CNP_CONTENT_TYPE}
HTTP_ERROR_MESSAGE = b'Error with Https Request, Please Check Proxy and Url configuration'

def http_get_retrieval_request(url_suffix, config=conf):
    request_url = config.url + url_suffix
    try:
        http_response = requests.get(request_url, headers=CHARGEBACK_API_HEADERS, auth=HTTPBasicAuth(config.username, config.password))
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nGET request to:', request_url, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_retrieval_response(http_response)


def http_put_request(url_suffix, request_xml, config=conf):
    request_url = config.url + url_suffix
    request_xml = utils.obj_to_xml(request_xml)
    try:
        http_response = requests.put(request_url, headers=CHARGEBACK_API_HEADERS, auth=HTTPBasicAuth(config.username, config.password), data=request_xml)
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nPUT request to:', request_url, config)
    print_to_console(b'\nRequest :', request_xml, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_update_response(http_response)


def http_get_document_request(url_suffix, document_path, config=conf):
    request_url = config.url + url_suffix
    try:
        http_response = requests.get(request_url, auth=HTTPBasicAuth(config.username, config.password))
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nGET Request to:', request_url, config)
    validate_response(http_response)
    retrieve_file(http_response, document_path, config)


def http_delete_document_response(url_suffix, config=conf):
    request_url = config.url + url_suffix
    try:
        http_response = requests.delete(request_url, auth=HTTPBasicAuth(config.username, config.password))
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nDELETE request to:', request_url, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_document_response(http_response)


def http_post_document_request(url_suffix, document_path, config=conf):
    request_url = config.url + url_suffix
    try:
        data, content_type = get_file_content(document_path)
        http_response = requests.post(url=request_url, headers={b'Content-Type': content_type}, auth=HTTPBasicAuth(config.username, config.password), data=data)
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nPOST request to:', request_url, config)
    print_to_console(b'\nFile:', document_path, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_document_response(http_response)


def http_put_document_request(url_suffix, document_path, config=conf):
    request_url = config.url + url_suffix
    try:
        data, content_type = get_file_content(document_path)
        http_response = requests.put(url=request_url, headers={b'Content-Type': content_type}, auth=HTTPBasicAuth(config.username, config.password), data=data)
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nPUT request to:', request_url, config)
    print_to_console(b'\nFile:', document_path, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_document_response(http_response)


def http_get_document_list_request(url_suffix, config=conf):
    request_url = config.url + url_suffix
    try:
        http_response = requests.get(request_url, headers=CHARGEBACK_API_HEADERS, auth=HTTPBasicAuth(config.username, config.password))
    except requests.RequestException:
        raise utils.ChargebackError(HTTP_ERROR_MESSAGE)

    print_to_console(b'\nGET request to:', request_url, config)
    validate_response(http_response)
    print_to_console(b'\nResponse :', http_response.text, config)
    return utils.generate_document_response(http_response)


def validate_response(http_response, config=conf):
    """check the status code of the response
    :param http_response: http response generated
    :return: raises an exception
    """
    if http_response is None:
        raise utils.ChargebackError(b'There was an exception while fetching the response')
    content_type = http_response.headers._store[b'content-type'][1]
    if http_response.status_code != 200:
        if CNP_CONTENT_TYPE in content_type:
            error_response = utils.generate_error_response(http_response)
            print_to_console(b'\nResponse :', http_response.text, config)
            error_list, error_message = _generate_error_data(error_response)
            raise utils.ChargebackWebError(error_message, str(http_response.status_code), error_list)
        raise utils.ChargebackWebError(http_response, str(http_response.status_code))
    return


def _generate_error_data(error_response):
    error_list = error_response[b'errors'][b'error']
    error_message = b''
    prefix = b''
    for error in error_list:
        print(error)
        error_message += prefix + error
        prefix = b'\n'

    return (
     error_list, error_message)


def retrieve_file(http_response, document_path, config=conf):
    content_type = http_response.headers._store[b'content-type'][1]
    if CNP_CONTENT_TYPE in content_type:
        error_response = utils.generate_document_response(http_response)
        print_to_console(b'\nResponse :', http_response.text, config)
        error_message = str(error_response[b'responseMessage'])
        error_code = error_response[b'responseCode']
        raise utils.ChargebackDocumentError(error_message, error_code)
    elif content_type != b'image/tiff':
        raise utils.ChargebackWebError(http_response.text, str(http_response.status_code))
    else:
        with open(document_path, b'wb') as (f):
            for block in http_response.iter_content(1024):
                f.write(block)

        print_to_console(b'\nDocument saved at: ', document_path, config)


def get_file_content(path):
    with open(path, b'rb') as (f):
        data = f.read()
    content_type = mimetypes.guess_type(path)[0]
    return (data, content_type)


def neuter_xml(xml_string):
    xml_string = re.sub(b'<token>.*</token>', b'<token>****</token>', xml_string)
    xml_string = re.sub(b'<cardNumberLast4>.*</cardNumberLast4>', b'<cardNumberLast4>****</cardNumberLast4>', xml_string)
    return xml_string


def print_to_console(prefix_message, xml_string, config=conf):
    if config.print_xml:
        if config.neuter_xml:
            xml_string = neuter_xml(xml_string)
        print(prefix_message, xml_string)