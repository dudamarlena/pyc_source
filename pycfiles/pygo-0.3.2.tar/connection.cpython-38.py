# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyGnuTLS/connection.py
# Compiled at: 2020-04-24 09:24:19
# Size of source mod 2**32: 18185 bytes
__doc__ = 'GNUTLS connection support'
__all__ = [
 'X509Credentials',
 'TLSContext',
 'TLSContextServerOptions',
 'ClientSession',
 'ServerSession',
 'ServerSessionFactory']
from time import time
from socket import GNUTLS_SHUT_RDWR as SOCKET_SHUT_RDWR
from _ctypes import PyObj_FromPtr
from ctypes import c_char_p, POINTER, c_uint, c_void_p, string_at, c_size_t, byref, cast, create_string_buffer
from PyGnuTLS.crypto import X509Identity, X509Certificate
from PyGnuTLS.errors import CertificateAuthorityError, CertificateError, CertificateExpiredError, CertificateRevokedError, CertificateSecurityError, RequestedDataNotAvailable, GNUTLSError
from PyGnuTLS.library.constants import GNUTLS_A_BAD_CERTIFICATE, GNUTLS_A_CERTIFICATE_EXPIRED, GNUTLS_A_CERTIFICATE_REVOKED, GNUTLS_A_INSUFFICIENT_SECURITY, GNUTLS_AL_FATAL, GNUTLS_A_UNKNOWN_CA, GNUTLS_CERT_INSECURE_ALGORITHM, GNUTLS_CERT_INVALID, GNUTLS_CERT_REQUEST, GNUTLS_CERT_REVOKED, GNUTLS_CERT_SIGNER_NOT_CA, GNUTLS_CERT_SIGNER_NOT_FOUND, GNUTLS_CLIENT, GNUTLS_CRD_CERTIFICATE, GNUTLS_CRT_X509, GNUTLS_NAME_DNS, GNUTLS_SERVER, GNUTLS_SHUT_RDWR, GNUTLS_X509_FMT_DER
from PyGnuTLS.library.types import gnutls_certificate_credentials_t, gnutls_session_t, gnutls_certificate_retrieve_function, gnutls_priority_t, gnutls_x509_crt_t
from PyGnuTLS.library.functions import gnutls_alert_send, gnutls_bye, gnutls_certificate_allocate_credentials, gnutls_certificate_free_credentials, gnutls_certificate_get_peers, gnutls_certificate_server_set_request, gnutls_certificate_set_retrieve_function, gnutls_certificate_set_verify_limits, gnutls_certificate_set_x509_key, gnutls_certificate_set_x509_trust, gnutls_certificate_type_get, gnutls_certificate_verify_peers2, gnutls_cipher_get, gnutls_cipher_get_name, gnutls_compression_get, gnutls_compression_get_name, gnutls_credentials_clear, gnutls_credentials_set, gnutls_deinit, gnutls_handshake, gnutls_handshake_set_private_extensions, gnutls_init, gnutls_kx_get, gnutls_kx_get_name, gnutls_mac_get, gnutls_mac_get_name, gnutls_priority_deinit, gnutls_priority_init, gnutls_priority_set_direct, gnutls_protocol_get_name, gnutls_protocol_get_version, gnutls_record_get_direction, gnutls_record_recv, gnutls_record_send, gnutls_server_name_get, gnutls_server_name_set, gnutls_session_get_ptr, gnutls_session_set_ptr, gnutls_set_default_priority, gnutls_transport_set_ptr

@gnutls_certificate_retrieve_function
def _retrieve_certificate(c_session, req_ca_dn, nreqs, pk_algos, pk_algos_length, retr_st):
    session = PyObj_FromPtr(gnutls_session_get_ptr(c_session))
    identity = session.credentials.select_server_identity(session)
    retr_st.contents.deinit_all = 0
    if identity is None:
        retr_st.contents.ncerts = 0
    else:
        retr_st.contents.ncerts = 1
        retr_st.contents.cert_type = GNUTLS_CRT_X509
        retr_st.contents.cert.x509.contents = identity.cert._c_object
        retr_st.contents.key.x509 = identity.key._c_object
    return 0


class _ServerNameIdentities(dict):
    """_ServerNameIdentities"""

    def __init__(self, identities):
        dict.__init__(self)
        for identity in identities:
            self.add(identity)

    def add(self, identity):
        for name in identity.cert.alternative_names.dns:
            self[name.lower()] = identity

        for ip in identity.cert.alternative_names.ip:
            self[ip] = identity

        subject = identity.cert.subject
        if subject.CN is not None:
            self[subject.CN.lower()] = identity

    def get(self, server_name, default=None):
        server_name = server_name.lower()
        if server_name in self:
            return self[server_name]
        for name in (n for n in self if n.startswith('*.')):
            suffix = name[1:]
            if server_name.endswith(suffix) and '.' not in server_name[:-len(suffix)]:
                return self[name]
            return default


class X509Credentials(object):

    def __new__(cls, *args, **kwargs):
        c_object = gnutls_certificate_credentials_t()
        gnutls_certificate_allocate_credentials(byref(c_object))
        instance = object.__new__(cls)
        instance._X509Credentials__deinit = gnutls_certificate_free_credentials
        instance._c_object = c_object
        return instance

    def __init__(self, cert=None, key=None, trusted=[], crl_list=[], identities=[]):
        """Credentials contain a X509 certificate, a private key, a list of trusted CAs and a list of CRLs (all optional).
        An optional list of additional X509 identities can be specified for applications that need more that one identity"""
        if cert and key:
            gnutls_certificate_set_x509_key(self._c_object, byref(cert._c_object), 1, key._c_object)
        elif (cert, key) != (None, None):
            raise ValueError('Specify neither or both the certificate and private key')
        gnutls_certificate_set_retrieve_function(self._c_object, _retrieve_certificate)
        self._max_depth = 5
        self._max_bits = 8200
        self._type = GNUTLS_CRD_CERTIFICATE
        self._cert = cert
        self._key = key
        self._identities = tuple(identities)
        self._trusted = ()
        self.add_trusted(trusted)
        self.crl_list = crl_list
        self.server_name_identities = _ServerNameIdentities(identities)
        if cert:
            if key:
                self.server_name_identities.add(X509Identity(cert, key))

    def __del__(self):
        self._X509Credentials__deinit(self._c_object)

    def add_trusted(self, trusted):
        size = len(trusted)
        if size > 0:
            ca_list = (gnutls_x509_crt_t * size)(*[cert._c_object for cert in trusted])
            gnutls_certificate_set_x509_trust(self._c_object, cast(byref(ca_list), POINTER(gnutls_x509_crt_t)), size)
            self._trusted = self._trusted + tuple(trusted)

    @property
    def cert(self):
        return self._cert

    @property
    def key(self):
        return self._key

    @property
    def identities(self):
        return self._identities

    @property
    def trusted(self):
        return self._trusted

    def _get_crl_list(self):
        return self._crl_list

    def _set_crl_list(self, crl_list):
        self._crl_list = tuple(crl_list)

    crl_list = property(_get_crl_list, _set_crl_list)
    del _get_crl_list
    del _set_crl_list

    def _get_max_verify_length(self):
        return self._max_depth

    def _set_max_verify_length(self, max_depth):
        gnutls_certificate_set_verify_limits(self._c_object, self._max_bits, max_depth)
        self._max_depth = max_depth

    max_verify_length = property(_get_max_verify_length, _set_max_verify_length)
    del _get_max_verify_length
    del _set_max_verify_length

    def _get_max_verify_bits(self):
        return self._max_bits

    def _set_max_verify_bits(self, max_bits):
        gnutls_certificate_set_verify_limits(self._c_object, max_bits, self._max_depth)
        self._max_bits = max_bits

    max_verify_bits = property(_get_max_verify_bits, _set_max_verify_bits)
    del _get_max_verify_bits
    del _set_max_verify_bits

    def check_certificate(self, cert, cert_name='certificate'):
        """Verify activation, expiration and revocation for the given certificate"""
        now = time()
        if cert.activation_time > now:
            raise CertificateExpiredError('%s is not yet activated' % cert_name)
        if cert.expiration_time < now:
            raise CertificateExpiredError('%s has expired' % cert_name)
        for crl in self.crl_list:
            crl.check_revocation(cert, cert_name=cert_name)

    def select_server_identity(self, session):
        """Select which identity the server will use for a given session. The default selection algorithm uses
        the server name extension. A subclass can overwrite it if a different selection algorithm is desired."""
        server_name = session.server_name
        if server_name is not None:
            return self.server_name_identities.get(server_name)
        if self.cert:
            if self.key:
                return self
        return


class TLSContextServerOptions(object):

    def __init__(self, certificate_request=GNUTLS_CERT_REQUEST):
        self.certificate_request = certificate_request


class TLSContext(object):

    def __init__(self, credentials, session_parameters=None, server_options=None):
        self.credentials = credentials
        self.session_parameters = session_parameters
        self.server_options = server_options or 

    @property
    def session_parameters(self):
        return self.__dict__.get('session_parameters')

    @session_parameters.setter
    def session_parameters(self, value):
        priority = gnutls_priority_t()
        try:
            gnutls_priority_init(byref(priority), value, None)
        except GNUTLSError:
            raise ValueError('invalid session parameters: %s' % value)
        else:
            gnutls_priority_deinit(priority)
        self.__dict__['session_parameters'] = value


class Session(object):
    """Session"""
    session_type = None

    def __new__(cls, *args, **kwargs):
        if cls is Session:
            raise RuntimeError('Session cannot be instantiated directly')
        instance = object.__new__(cls)
        instance._Session__deinit = gnutls_deinit
        instance._c_object = gnutls_session_t()
        return instance

    def __init__(self, socket, context):
        gnutls_init(byref(self._c_object), self.session_type)
        gnutls_session_set_ptr(self._c_object, id(self))
        gnutls_set_default_priority(self._c_object)
        gnutls_priority_set_direct(self._c_object, context.session_parameters, None)
        gnutls_transport_set_ptr(self._c_object, socket.fileno())
        gnutls_handshake_set_private_extensions(self._c_object, 1)
        self.socket = socket
        self.credentials = context.credentials

    def __del__(self):
        self._Session__deinit(self._c_object)

    def __getattr__(self, name):
        return getattr(self.socket, name)

    def _get_credentials(self):
        return self._credentials

    def _set_credentials(self, credentials):
        gnutls_credentials_clear(self._c_object)
        gnutls_credentials_set(self._c_object, credentials._type, cast(credentials._c_object, c_void_p))
        self._credentials = credentials

    credentials = property(_get_credentials, _set_credentials)
    del _get_credentials
    del _set_credentials

    @property
    def protocol(self):
        return gnutls_protocol_get_name(gnutls_protocol_get_version(self._c_object))

    @property
    def kx_algorithm(self):
        return gnutls_kx_get_name(gnutls_kx_get(self._c_object))

    @property
    def cipher(self):
        return gnutls_cipher_get_name(gnutls_cipher_get(self._c_object))

    @property
    def mac_algorithm(self):
        return gnutls_mac_get_name(gnutls_mac_get(self._c_object))

    @property
    def compression(self):
        return gnutls_compression_get_name(gnutls_compression_get(self._c_object))

    @property
    def peer_certificate(self):
        if gnutls_certificate_type_get(self._c_object) != GNUTLS_CRT_X509:
            return
        list_size = c_uint()
        cert_list = gnutls_certificate_get_peers(self._c_object, byref(list_size))
        if list_size.value == 0:
            return
        cert = cert_list[0]
        return X509Certificate(string_at(cert.data, cert.size), GNUTLS_X509_FMT_DER)

    @property
    def interrupted_while_writing(self):
        """True if an operation was interrupted while writing"""
        return gnutls_record_get_direction(self._c_object) == 1

    @property
    def interrupted_while_reading(self):
        """True if an operation was interrupted while reading"""
        return gnutls_record_get_direction(self._c_object) == 0

    def handshake(self):
        gnutls_handshake(self._c_object)

    def send(self, data):
        data = str(data)
        if not data:
            return 0
        return gnutls_record_send(self._c_object, data, len(data))

    def sendall(self, data):
        size = len(data)
        while size > 0:
            sent = self.send(data[-size:])
            size -= sent

    def recv(self, limit):
        data = create_string_buffer(limit)
        size = gnutls_record_recv(self._c_object, data, limit)
        return data[:size]

    def send_alert(self, exception):
        alertdict = {CertificateError: GNUTLS_A_BAD_CERTIFICATE, 
         CertificateAuthorityError: GNUTLS_A_UNKNOWN_CA, 
         CertificateSecurityError: GNUTLS_A_INSUFFICIENT_SECURITY, 
         CertificateExpiredError: GNUTLS_A_CERTIFICATE_EXPIRED, 
         CertificateRevokedError: GNUTLS_A_CERTIFICATE_REVOKED}
        alert = alertdict.get(exception.__class__)
        if alert:
            gnutls_alert_send(self._c_object, GNUTLS_AL_FATAL, alert)

    def bye(self, how=GNUTLS_SHUT_RDWR):
        gnutls_bye(self._c_object, how)

    def shutdown(self, how=SOCKET_SHUT_RDWR):
        self.socket.shutdown(how)

    def close(self):
        self.socket.close()

    def verify_peer(self):
        status = c_uint()
        gnutls_certificate_verify_peers2(self._c_object, byref(status))
        status = status.value
        if status & GNUTLS_CERT_INVALID:
            raise CertificateError('peer certificate is invalid')
        elif status & GNUTLS_CERT_SIGNER_NOT_FOUND:
            raise CertificateAuthorityError('peer certificate signer not found')
        elif status & GNUTLS_CERT_SIGNER_NOT_CA:
            raise CertificateAuthorityError('peer certificate signer is not a CA')
        elif status & GNUTLS_CERT_INSECURE_ALGORITHM:
            raise CertificateSecurityError('peer certificate uses an insecure algorithm')
        elif status & GNUTLS_CERT_REVOKED:
            raise CertificateRevokedError('peer certificate was revoked')


class ClientSession(Session):
    session_type = GNUTLS_CLIENT

    def __init__(self, socket, context, server_name=None):
        Session.__init__(self, socket, context)
        self._server_name = None
        if server_name is not None:
            self.server_name = server_name

    def _get_server_name(self):
        return self._server_name

    def _set_server_name(self, server_name):
        gnutls_server_name_set(self._c_object, GNUTLS_NAME_DNS, c_char_p(server_name), len(server_name))
        self._server_name = server_name

    server_name = property(_get_server_name, _set_server_name)
    del _get_server_name
    del _set_server_name


class ServerSession(Session):
    session_type = GNUTLS_SERVER

    def __init__(self, socket, context):
        Session.__init__(self, socket, context)
        if context.server_options.certificate_request is not None:
            gnutls_certificate_server_set_request(self._c_object, context.server_options.certificate_request)

    @property
    def server_name--- This code section failed: ---

 L. 492         0  LOAD_GLOBAL              c_size_t
                2  LOAD_CONST               256
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'data_length'

 L. 493         8  LOAD_GLOBAL              create_string_buffer
               10  LOAD_FAST                'data_length'
               12  LOAD_ATTR                value
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'data'

 L. 494        18  LOAD_GLOBAL              c_uint
               20  CALL_FUNCTION_0       0  ''
               22  STORE_FAST               'hostname_type'

 L. 495        24  LOAD_GLOBAL              range
               26  LOAD_CONST               65536
               28  CALL_FUNCTION_1       1  ''
               30  GET_ITER         
               32  FOR_ITER            184  'to 184'
               34  STORE_FAST               'i'

 L. 496        36  SETUP_FINALLY        68  'to 68'

 L. 497        38  LOAD_GLOBAL              gnutls_server_name_get

 L. 498        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _c_object

 L. 498        44  LOAD_FAST                'data'

 L. 498        46  LOAD_GLOBAL              byref
               48  LOAD_FAST                'data_length'
               50  CALL_FUNCTION_1       1  ''

 L. 498        52  LOAD_GLOBAL              byref
               54  LOAD_FAST                'hostname_type'
               56  CALL_FUNCTION_1       1  ''

 L. 498        58  LOAD_FAST                'i'

 L. 497        60  CALL_FUNCTION_5       5  ''
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        162  'to 162'
             68_0  COME_FROM_FINALLY    36  '36'

 L. 500        68  DUP_TOP          
               70  LOAD_GLOBAL              RequestedDataNotAvailable
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    92  'to 92'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 501        82  POP_EXCEPT       
               84  POP_TOP          
               86  JUMP_ABSOLUTE       184  'to 184'
               88  POP_EXCEPT       
               90  JUMP_FORWARD        162  'to 162'
             92_0  COME_FROM            74  '74'

 L. 502        92  DUP_TOP          
               94  LOAD_GLOBAL              MemoryError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   160  'to 160'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 503       106  LOAD_FAST                'data_length'
              108  DUP_TOP          
              110  LOAD_ATTR                value
              112  LOAD_CONST               1
              114  INPLACE_ADD      
              116  ROT_TWO          
              118  STORE_ATTR               value

 L. 504       120  LOAD_GLOBAL              create_string_buffer
              122  LOAD_FAST                'data_length'
              124  LOAD_ATTR                value
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'data'

 L. 505       130  LOAD_GLOBAL              gnutls_server_name_get

 L. 506       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _c_object

 L. 506       136  LOAD_FAST                'data'

 L. 506       138  LOAD_GLOBAL              byref
              140  LOAD_FAST                'data_length'
              142  CALL_FUNCTION_1       1  ''

 L. 506       144  LOAD_GLOBAL              byref
              146  LOAD_FAST                'hostname_type'
              148  CALL_FUNCTION_1       1  ''

 L. 506       150  LOAD_FAST                'i'

 L. 505       152  CALL_FUNCTION_5       5  ''
              154  POP_TOP          
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM            98  '98'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM            90  '90'
            162_2  COME_FROM            66  '66'

 L. 508       162  LOAD_FAST                'hostname_type'
              164  LOAD_ATTR                value
              166  LOAD_GLOBAL              GNUTLS_NAME_DNS
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   174  'to 174'

 L. 509       172  JUMP_BACK            32  'to 32'
            174_0  COME_FROM           170  '170'

 L. 510       174  LOAD_FAST                'data'
              176  LOAD_ATTR                value
              178  ROT_TWO          
              180  POP_TOP          
              182  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 86


class ServerSessionFactory(object):

    def __init__(self, socket, context, session_class=ServerSession):
        if not issubclass(session_class, ServerSession):
            raise TypeError('session_class must be a subclass of ServerSession')
        self.socket = socket
        self.context = context
        self.session_class = session_class

    def __getattr__(self, name):
        return getattr(self.socket, name)

    def bind(self, address):
        self.socket.bind(address)

    def listen(self, backlog):
        self.socket.listen(backlog)

    def accept(self):
        new_sock, address = self.socket.accept()
        session = self.session_class(new_sock, self.context)
        return (
         session, address)

    def shutdown(self, how=SOCKET_SHUT_RDWR):
        self.socket.shutdown(how)

    def close(self):
        self.socket.close()