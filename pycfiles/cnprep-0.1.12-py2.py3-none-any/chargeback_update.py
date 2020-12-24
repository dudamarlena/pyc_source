# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnpsdk/chargeback_update.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, print_function, unicode_literals
from cnpsdk import fields_chargeback, utils, communication
conf = utils.Configuration()
SERVICE_ROUTE = b'/chargebacks'

def assign_case_to_user(case_id, user_id, note, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'ASSIGN_TO_USER'
    request_body.assignedTo = user_id
    request_body.note = note
    return _get_update_response(case_id, request_body, config)


def add_note_to_case(case_id, note, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'ADD_NOTE'
    request_body.note = note
    return _get_update_response(case_id, request_body, config)


def assume_liability(case_id, note, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'MERCHANT_ACCEPTS_LIABILITY'
    request_body.note = note
    return _get_update_response(case_id, request_body, config)


def represent_case(case_id, note, representment_amount=None, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'MERCHANT_REPRESENT'
    request_body.note = note
    request_body.representedAmount = representment_amount
    return _get_update_response(case_id, request_body, config)


def respond_to_retrieval_request(case_id, note, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'MERCHANT_RESPOND'
    request_body.note = note
    return _get_update_response(case_id, request_body, config)


def request_arbitration(case_id, note, config=conf):
    request_body = fields_chargeback.chargebackUpdateRequest()
    request_body.activityType = b'MERCHANT_REQUESTS_ARBITRATION'
    request_body.note = note
    return _get_update_response(case_id, request_body, config)


def _get_update_response(parameter_value1, request_body, config):
    url_suffix = SERVICE_ROUTE + b'/' + str(parameter_value1)
    return communication.http_put_request(url_suffix, request_body, config)