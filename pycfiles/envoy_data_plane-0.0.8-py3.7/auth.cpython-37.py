# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/auth.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 18856 bytes
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional
import betterproto
from envoy_data_plane.envoy.api.v2 import core
from envoy_data_plane.envoy.type import matcher
from envoy_data_plane.google import protobuf

class TlsParametersTlsProtocol(betterproto.Enum):
    TLS_AUTO = 0
    TLSv1_0 = 1
    TLSv1_1 = 2
    TLSv1_2 = 3
    TLSv1_3 = 4


@dataclass
class TlsParameters(betterproto.Message):
    tls_minimum_protocol_version = betterproto.enum_field(1)
    tls_minimum_protocol_version: 'TlsParametersTlsProtocol'
    tls_maximum_protocol_version = betterproto.enum_field(2)
    tls_maximum_protocol_version: 'TlsParametersTlsProtocol'
    cipher_suites = betterproto.string_field(3)
    cipher_suites: List[str]
    ecdh_curves = betterproto.string_field(4)
    ecdh_curves: List[str]


@dataclass
class PrivateKeyProvider(betterproto.Message):
    __doc__ = '\n    BoringSSL private key method configuration. The private key methods are\n    used for external (potentially asynchronous) signing and decryption\n    operations. Some use cases for private key methods would be TPM support and\n    TLS acceleration.\n    '
    provider_name = betterproto.string_field(1)
    provider_name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class TlsCertificate(betterproto.Message):
    __doc__ = '[#next-free-field: 7]'
    certificate_chain = betterproto.message_field(1)
    certificate_chain: core.DataSource
    private_key = betterproto.message_field(2)
    private_key: core.DataSource
    private_key_provider = betterproto.message_field(6)
    private_key_provider: 'PrivateKeyProvider'
    password = betterproto.message_field(3)
    password: core.DataSource
    ocsp_staple = betterproto.message_field(4)
    ocsp_staple: core.DataSource
    signed_certificate_timestamp = betterproto.message_field(5)
    signed_certificate_timestamp: List[core.DataSource]


@dataclass
class TlsSessionTicketKeys(betterproto.Message):
    keys = betterproto.message_field(1)
    keys: List[core.DataSource]


@dataclass
class CertificateValidationContext(betterproto.Message):
    __doc__ = '[#next-free-field: 10]'
    trusted_ca = betterproto.message_field(1)
    trusted_ca: core.DataSource
    verify_certificate_spki = betterproto.string_field(3)
    verify_certificate_spki: List[str]
    verify_certificate_hash = betterproto.string_field(2)
    verify_certificate_hash: List[str]
    verify_subject_alt_name = betterproto.string_field(4)
    verify_subject_alt_name: List[str]
    match_subject_alt_names = betterproto.message_field(9)
    match_subject_alt_names: List[matcher.StringMatcher]
    require_ocsp_staple = betterproto.message_field(5,
      wraps=(betterproto.TYPE_BOOL))
    require_ocsp_staple: Optional[bool]
    require_signed_certificate_timestamp = betterproto.message_field(6,
      wraps=(betterproto.TYPE_BOOL))
    require_signed_certificate_timestamp: Optional[bool]
    crl = betterproto.message_field(7)
    crl: core.DataSource
    allow_expired_certificate = betterproto.bool_field(8)
    allow_expired_certificate: bool


@dataclass
class CommonTlsContext(betterproto.Message):
    __doc__ = '\n    TLS context shared by both client and server TLS contexts. [#next-free-\n    field: 9]\n    '
    tls_params = betterproto.message_field(1)
    tls_params: 'TlsParameters'
    tls_certificates = betterproto.message_field(2)
    tls_certificates: List['TlsCertificate']
    tls_certificate_sds_secret_configs = betterproto.message_field(6)
    tls_certificate_sds_secret_configs: List['SdsSecretConfig']
    validation_context = betterproto.message_field(3,
      group='validation_context_type')
    validation_context: 'CertificateValidationContext'
    validation_context_sds_secret_config = betterproto.message_field(7,
      group='validation_context_type')
    validation_context_sds_secret_config: 'SdsSecretConfig'
    combined_validation_context = betterproto.message_field(8,
      group='validation_context_type')
    combined_validation_context: 'CommonTlsContextCombinedCertificateValidationContext'
    alpn_protocols = betterproto.string_field(4)
    alpn_protocols: List[str]


@dataclass
class CommonTlsContextCombinedCertificateValidationContext(betterproto.Message):
    default_validation_context = betterproto.message_field(1)
    default_validation_context: 'CertificateValidationContext'
    validation_context_sds_secret_config = betterproto.message_field(2)
    validation_context_sds_secret_config: 'SdsSecretConfig'


@dataclass
class UpstreamTlsContext(betterproto.Message):
    common_tls_context = betterproto.message_field(1)
    common_tls_context: 'CommonTlsContext'
    sni = betterproto.string_field(2)
    sni: str
    allow_renegotiation = betterproto.bool_field(3)
    allow_renegotiation: bool
    max_session_keys = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    max_session_keys: Optional[int]


@dataclass
class DownstreamTlsContext(betterproto.Message):
    __doc__ = '[#next-free-field: 7]'
    common_tls_context = betterproto.message_field(1)
    common_tls_context: 'CommonTlsContext'
    require_client_certificate = betterproto.message_field(2,
      wraps=(betterproto.TYPE_BOOL))
    require_client_certificate: Optional[bool]
    require_sni = betterproto.message_field(3,
      wraps=(betterproto.TYPE_BOOL))
    require_sni: Optional[bool]
    session_ticket_keys = betterproto.message_field(4,
      group='session_ticket_keys_type')
    session_ticket_keys: 'TlsSessionTicketKeys'
    session_ticket_keys_sds_secret_config = betterproto.message_field(5,
      group='session_ticket_keys_type')
    session_ticket_keys_sds_secret_config: 'SdsSecretConfig'
    session_timeout = betterproto.message_field(6)
    session_timeout: timedelta


@dataclass
class SdsSecretConfig(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    sds_config = betterproto.message_field(2)
    sds_config: core.ConfigSource


@dataclass
class Secret(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    tls_certificate = betterproto.message_field(2, group='type')
    tls_certificate: 'TlsCertificate'
    session_ticket_keys = betterproto.message_field(3,
      group='type')
    session_ticket_keys: 'TlsSessionTicketKeys'
    validation_context = betterproto.message_field(4,
      group='type')
    validation_context: 'CertificateValidationContext'