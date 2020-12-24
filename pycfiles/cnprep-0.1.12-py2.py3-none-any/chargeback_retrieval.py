# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnpsdk/chargeback_retrieval.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, print_function, unicode_literals
from cnpsdk import utils, communication
conf = utils.Configuration()
SERVICE_ROUTE = b'/chargebacks'

def get_chargeback_by_case_id(case_id, config=conf):
    url_suffix = SERVICE_ROUTE + b'/' + case_id
    return communication.http_get_retrieval_request(url_suffix, config)


def get_chargebacks_by_token(token, config=conf):
    return _get_retrieval_response({b'token': token}, config)


def get_chargebacks_by_card_number(card_number, expiration_date, config=conf):
    return _get_retrieval_response({b'cardNumber': card_number, b'expirationDate': expiration_date}, config)


def get_chargebacks_by_arn(arn, config=conf):
    return _get_retrieval_response({b'arn': arn}, config)


def get_chargebacks_by_date(activity_date, config=conf):
    return _get_retrieval_response({b'date': activity_date}, config)


def get_chargebacks_by_financial_impact(activity_date, financial_impact, config=conf):
    return _get_retrieval_response({b'date': activity_date, b'financialOnly': financial_impact}, config)


def get_actionable_chargebacks(actionable, config=conf):
    return _get_retrieval_response({b'actionable': actionable}, config)


def _get_retrieval_response(parameters, config):
    url_suffix = SERVICE_ROUTE
    prefix = b'?'
    for name in parameters:
        url_suffix += prefix + name + b'=' + str(parameters[name])
        prefix = b'&'

    return communication.http_get_retrieval_request(url_suffix, config)