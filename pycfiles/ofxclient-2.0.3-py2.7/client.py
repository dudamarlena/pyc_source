# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/ofxclient/client.py
# Compiled at: 2017-04-21 11:10:37
from __future__ import absolute_import
from __future__ import unicode_literals
try:
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

import logging, time
try:
    from urllib.parse import splittype, splithost
except ImportError:
    from urllib import splittype, splithost

import uuid
DEFAULT_APP_ID = b'QWIN'
DEFAULT_APP_VERSION = b'2500'
DEFAULT_OFX_VERSION = b'102'
LINE_ENDING = b'\r\n'

def ofx_uid():
    return str(uuid.uuid4().hex)


class Client:
    """This communicates with the banks via the OFX protocol

    :param institution: institution to connect to
    :type institution: :py:class:`ofxclient.Institution`
    :param id: client id (optional need for OFX version >= 103)
    :type id: string
    :param app_id: OFX app id
    :type app_id: string
    :param app_version: OFX app version
    :type app_version: string
    :param ofx_version: OFX spec version
    :type ofx_version: string
    """

    def __init__(self, institution, id=ofx_uid(), app_id=DEFAULT_APP_ID, app_version=DEFAULT_APP_VERSION, ofx_version=DEFAULT_OFX_VERSION):
        self.institution = institution
        self.id = id
        self.app_id = app_id
        self.app_version = app_version
        self.ofx_version = ofx_version
        self.cookie = 3

    def authenticated_query(self, with_message=None, username=None, password=None):
        """Authenticated query

        If you pass a 'with_messages' array those queries will be passed along
        otherwise this will just be an authentication probe query only.
        """
        u = username or self.institution.username
        p = password or self.institution.password
        contents = [
         b'OFX', self._signOn(username=u, password=p)]
        if with_message:
            contents.append(with_message)
        return LINE_ENDING.join([self.header(), _tag(*contents)])

    def bank_account_query(self, number, date, account_type, bank_id):
        """Bank account statement request"""
        return self.authenticated_query(self._bareq(number, date, account_type, bank_id))

    def credit_card_account_query(self, number, date):
        """CC Statement request"""
        return self.authenticated_query(self._ccreq(number, date))

    def brokerage_account_query(self, number, date, broker_id):
        return self.authenticated_query(self._invstreq(broker_id, number, date))

    def account_list_query(self, date=b'19700101000000'):
        return self.authenticated_query(self._acctreq(date))

    def post(self, query):
        i = self.institution
        logging.debug(b'posting data to %s' % i.url)
        logging.debug(b'---- request ----')
        logging.debug(query)
        garbage, path = splittype(i.url)
        host, selector = splithost(path)
        h = HTTPSConnection(host, timeout=60)
        if host == b'ofx.discovercard.com':
            h.putrequest(b'POST', selector, skip_host=True, skip_accept_encoding=True)
            h.putheader(b'Content-Type', b'application/x-ofx')
            h.putheader(b'Host', host)
            h.putheader(b'Content-Length', len(query))
            h.putheader(b'Connection', b'Keep-Alive')
            h.endheaders(query.encode())
        else:
            h.request(b'POST', selector, query, {b'Content-type': b'application/x-ofx', 
               b'Accept': b'*/*, application/x-ofx', 
               b'User-Agent': b'httpclient'})
        res = h.getresponse()
        response = res.read().decode(b'ascii', b'ignore')
        logging.debug(b'---- response ----')
        logging.debug(res.__dict__)
        logging.debug(response)
        res.close()
        return response

    def next_cookie(self):
        self.cookie += 1
        return str(self.cookie)

    def header(self):
        parts = [
         b'OFXHEADER:100',
         b'DATA:OFXSGML',
         b'VERSION:%d' % int(self.ofx_version),
         b'SECURITY:NONE',
         b'ENCODING:USASCII',
         b'CHARSET:1252',
         b'COMPRESSION:NONE',
         b'OLDFILEUID:NONE',
         b'NEWFILEUID:' + ofx_uid(),
         b'']
        return LINE_ENDING.join(parts)

    def _signOn(self, username=None, password=None):
        i = self.institution
        u = username or i.username
        p = password or i.password
        fidata = [_field(b'ORG', i.org)]
        if i.id:
            fidata.append(_field(b'FID', i.id))
        client_uid = b''
        if str(self.ofx_version) == b'103':
            client_uid = _field(b'CLIENTUID', self.id)
        return _tag(b'SIGNONMSGSRQV1', _tag(b'SONRQ', _field(b'DTCLIENT', now()), _field(b'USERID', u), _field(b'USERPASS', p), _field(b'LANGUAGE', b'ENG'), _tag(b'FI', *fidata), _field(b'APPID', self.app_id), _field(b'APPVER', self.app_version), client_uid))

    def _acctreq(self, dtstart):
        req = _tag(b'ACCTINFORQ', _field(b'DTACCTUP', dtstart))
        return self._message(b'SIGNUP', b'ACCTINFO', req)

    def _bareq(self, acctid, dtstart, accttype, bankid):
        req = _tag(b'STMTRQ', _tag(b'BANKACCTFROM', _field(b'BANKID', bankid), _field(b'ACCTID', acctid), _field(b'ACCTTYPE', accttype)), _tag(b'INCTRAN', _field(b'DTSTART', dtstart), _field(b'INCLUDE', b'Y')))
        return self._message(b'BANK', b'STMT', req)

    def _ccreq(self, acctid, dtstart):
        req = _tag(b'CCSTMTRQ', _tag(b'CCACCTFROM', _field(b'ACCTID', acctid)), _tag(b'INCTRAN', _field(b'DTSTART', dtstart), _field(b'INCLUDE', b'Y')))
        return self._message(b'CREDITCARD', b'CCSTMT', req)

    def _invstreq(self, brokerid, acctid, dtstart):
        req = _tag(b'INVSTMTRQ', _tag(b'INVACCTFROM', _field(b'BROKERID', brokerid), _field(b'ACCTID', acctid)), _tag(b'INCTRAN', _field(b'DTSTART', dtstart), _field(b'INCLUDE', b'Y')), _field(b'INCOO', b'Y'), _tag(b'INCPOS', _field(b'DTASOF', now()), _field(b'INCLUDE', b'Y')), _field(b'INCBAL', b'Y'))
        return self._message(b'INVSTMT', b'INVSTMT', req)

    def _message(self, msgType, trnType, request):
        return _tag(msgType + b'MSGSRQV1', _tag(trnType + b'TRNRQ', _field(b'TRNUID', ofx_uid()), _field(b'CLTCOOKIE', self.next_cookie()), request))


def _field(tag, value):
    return b'<' + tag + b'>' + value


def _tag(tag, *contents):
    return LINE_ENDING.join([b'<' + tag + b'>'] + list(contents) + [b'</' + tag + b'>'])


def now():
    return time.strftime(b'%Y%m%d%H%M%S', time.localtime())