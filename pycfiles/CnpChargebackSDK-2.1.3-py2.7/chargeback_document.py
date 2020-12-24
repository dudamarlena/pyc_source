# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnpsdk/chargeback_document.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, print_function, unicode_literals
from cnpsdk import utils, communication
conf = utils.Configuration()
SERVICE_ROUTE = b'/services/chargebacks'

def upload_document(case_id, document_path, config=conf):
    document_id = document_path.split(b'/')[(-1)]
    url_suffix = SERVICE_ROUTE + b'/upload/' + str(case_id) + b'/' + str(document_id)
    return communication.http_post_document_request(url_suffix, document_path, config=config)


def retrieve_document(case_id, document_id, document_path, config=conf):
    url_suffix = SERVICE_ROUTE + b'/retrieve/' + str(case_id) + b'/' + str(document_id)
    communication.http_get_document_request(url_suffix, document_path, config=config)


def replace_document(case_id, document_id, document_path, config=conf):
    url_suffix = SERVICE_ROUTE + b'/replace/' + case_id + b'/' + document_id
    return communication.http_put_document_request(url_suffix, document_path, config=config)


def delete_document(case_id, document_id, config=conf):
    url_suffix = SERVICE_ROUTE + b'/delete/' + str(case_id) + b'/' + str(document_id)
    return communication.http_delete_document_response(url_suffix, config=config)


def list_documents(case_id, config=conf):
    url_suffix = SERVICE_ROUTE + b'/list/' + str(case_id)
    return communication.http_get_document_list_request(url_suffix, config=config)