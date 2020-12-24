# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\core\dua.py
# Compiled at: 2015-04-22 12:21:41
"""
"""
import ssl, logging
from datetime import datetime
from ldap3 import RESULT_PROTOCOL_ERROR
from pyasn1.codec.ber import decoder, encoder
from ..protocol.rfc4511 import build_extended_response, build_ldap_result, build_ldap_message

class Dua(object):
    """
    Directory User Agent - a client actually connected to the DSA with an active transport
    """

    def __init__(self, user, reader, writer, dsa):
        self.user = user
        self.dsa = dsa
        self.connected_time = datetime.now()
        self.reader = reader
        self.writer = writer
        self.tls_started = False
        self.pending = {}

    def send(self, ldap_message):
        encoded_message = encoder.encode(ldap_message)
        self.writer.write(encoded_message)
        self.writer.drain()

    def abort(self, result_code=RESULT_PROTOCOL_ERROR, diagnostic_message=''):
        result = build_ldap_result(result_code, diagnostic_message=diagnostic_message)
        response = build_extended_response(result, '1.3.6.1.4.1.1466.20036')
        ldap_message = build_ldap_message(0, 'extendedResp', response)
        self.send(ldap_message)
        self.writer.close()

    def start_tls(self):
        if not self.tls_started:
            logging.debug('start_tls')
            ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(self.dsa.cert_file, keyfile=self.dsa.key_file, password=self.dsa.key_file_password)
            wrapped_socket = ssl_context.wrap_socket(self.writer.get_extra_info('socket'), server_side=True, do_handshake_on_connect=False)
            wrapped_socket.do_handshake(block=True)
            return True
        return False