# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_options.py
# Compiled at: 2019-11-22 14:50:27
"""
File: isc_options.py

Clause: options

Title: Statements Used Only By 'options' Clause

Description: Various 'options' statement that is used
             only by 'options' clause.
"""
from pyparsing import Group, Keyword, OneOrMore, Optional, Word, ZeroOrMore, OneOrMore, Combine, Literal
from bind9_parser.isc_utils import lbrack, rbrack, semicolon, size_spec, name_type, path_name, number_type, seconds_type, isc_boolean, fqdn_name, key_id, krb5_principal_name, exclamation, quoted_path_name, squote, dquote
from bind9_parser.isc_inet import ip_port, inet_dscp_port_keyword_and_number_element, inet_ip_port_keyword_and_number_element
from bind9_parser.isc_domain import domain_generic_fqdn, domain_charset_alphanums_dash_underscore, domain_fqdn, quoted_domain_generic_fqdn
from bind9_parser.isc_aml import aml_nesting, aml_choices
options_stmt_acache_cleaning_interval = Keyword('acache-cleaning-interval').suppress() - seconds_type('acache_cleaning_interval') + semicolon
options_stmt_acache_enable = Keyword('acache-enable').suppress() - isc_boolean('acache-enable') + semicolon
options_stmt_answer_cookie = Keyword('answer-cookie').suppress() - isc_boolean('answer-cookie') + semicolon
options_stmt_automatic_interface_scan = Keyword('automatic-interface-scan').suppress() - isc_boolean('automatic_interface_scan') + semicolon
options_ip_port_list = ip_port + semicolon
options_ip_port_series = OneOrMore(options_ip_port_list)('options_ip_port_series_OneOrMore')
options_stmt_avoid_v4_udp_ports = Keyword('avoid-v4-udp-ports').suppress() + lbrack + options_ip_port_series('avoid_v4_udp_ports') + rbrack + semicolon
options_stmt_avoid_v4_udp_ports.setName('avoid-v4-udp-ports { port; ... };')
options_stmt_avoid_v6_udp_ports = Keyword('avoid-v6-udp-ports').suppress() + lbrack + options_ip_port_series('avoid_v6_udp_ports') + rbrack + semicolon
options_stmt_avoid_v6_udp_ports.setName('avoid-v6-udp-ports { port; ... };')
options_stmt_bindkeys_file = Keyword('bindkeys-file').suppress() - quoted_path_name('bindkeys_file') + semicolon
options_stmt_blackhole = Keyword('blackhole').suppress() + Group(aml_nesting(''))('blackhole')
options_stmt_cache_file = Keyword('cache-file').suppress() + quoted_path_name('cache_file') + semicolon
options_stmt_coresize = Keyword('coresize').suppress() - size_spec('coresize') + semicolon
options_stmt_datasize = Keyword('datasize').suppress() - size_spec('datasize') + semicolon
options_stmt_deallocate_on_exit = Keyword('deallocate-on-exit').suppress() - isc_boolean('deallocate_on_exit') + semicolon
options_stmt_deny_answer_addresses = Keyword('deny-answer-addresses').suppress() + Group(lbrack + ZeroOrMore(Group(exclamation('not') + aml_nesting | exclamation('not') + aml_choices + semicolon | aml_nesting | aml_choices + semicolon))(None)('aml') + rbrack + Optional(Keyword('except-from') + lbrack - name_type + semicolon + rbrack) + semicolon)('deny_answer_addresses')
options_stmt_deny_answer_addresses.setName('deny-answer-addresses [ except-from { <name>; } ];')
options_stmt_deny_answer_aliases = Keyword('deny-answer-aliases').suppress() + Group(lbrack - OneOrMore(Group(name_type('name') + semicolon)) + rbrack + Optional(Keyword('except-from').suppress() + lbrack + Group(name_type('name') + semicolon) + rbrack))('deny_answer_aliases') + semicolon
options_stmt_directory = Keyword('directory').suppress() - quoted_path_name('directory') + semicolon
options_stmt_disable_algorithms = (Keyword('disable-algorithms').suppress() + Group(domain_generic_fqdn('domain_name') + lbrack + OneOrMore(Word(domain_charset_alphanums_dash_underscore, max=63)('') + semicolon)('algorithm_list') + rbrack) + semicolon)('disable_algorithms')
options_stmt_disable_ds_digests = (Keyword('disable-ds-digests').suppress() + Group(domain_generic_fqdn + lbrack + OneOrMore(Word(domain_charset_alphanums_dash_underscore, max=63) + semicolon)('digest_list') + rbrack) + semicolon)('disable_ds_digests')
options_stmt_dscp = inet_dscp_port_keyword_and_number_element
options_stmt_dump_file = Keyword('dump-file').suppress() - quoted_path_name('dump_file') + semicolon
options_stmt_fake_iquery = Keyword('fake-iquery').suppress() - isc_boolean('fake_iquery') + semicolon
options_stmt_flush_zones_on_shutdown = Keyword('flush-zones-on-shutdown').suppress() - isc_boolean('flush_zones_on_shutdown') + semicolon
options_stmt_has_old_clients = Keyword('has-old-clients').suppress() - isc_boolean('has_old_clients') + semicolon
options_stmt_hostname_statistics = Keyword('hostname-statistics').suppress() - isc_boolean('hostname_stiatistics') + semicolon
options_stmt_hostname_statistics_max = Keyword('hostname-statistics-max').suppress() - isc_boolean('hostname_stiatistics_max') + semicolon
options_stmt_interface_interval = Keyword('interface-interval').suppress() - number_type('interface_interval') + semicolon
options_stmt_listen_on = (Keyword('listen-on').suppress() + Group(Optional(inet_ip_port_keyword_and_number_element) - aml_nesting))('listen_on')
options_stmt_listen_on_v6 = (Keyword('listen-on-v6').suppress() + Group(Optional(inet_ip_port_keyword_and_number_element) - aml_nesting))('listen_on_v6')
options_stmt_lock_file = Keyword('lock-file').suppress() - quoted_path_name('lock_file') + semicolon
options_stmt_match_mapped_addresses = Keyword('match-mapped-addresses').suppress() - isc_boolean('match_mapped_addresses') + semicolon
options_stmt_max_rsa_exponent_size = Keyword('max-rsa-exponent-size').suppress() - number_type('max_rsa_exponent_size') + semicolon
options_stmt_memstatistics = Keyword('memstatistics').suppress() - isc_boolean('memstatistics') + semicolon
options_stmt_memstatistics_file = Keyword('memstatistics-file').suppress() - quoted_path_name('memstatistics_file') + semicolon
options_stmt_multiple_cnames = Keyword('multiple-cnames').suppress() - isc_boolean('multiple_cnames_boolean') + semicolon
options_stmt_named_xfer = Keyword('named-xfer').suppress() - path_name('named_xfer_path_name') + semicolon
options_stmt_pid_file = Keyword('pid-file').suppress() - quoted_path_name('pid_file_path_name') + semicolon
options_stmt_port = inet_ip_port_keyword_and_number_element + semicolon
options_stmt_prefetch = Keyword('prefetch').suppress() + Group(number_type('expiry_ttl') + Optional(seconds_type('threshold_ttl')))('prefetch') + semicolon
options_stmt_querylog = Keyword('querylog').suppress() - isc_boolean('querylog_boolean') + semicolon
options_stmt_random_device = Keyword('random-device').suppress() - quoted_path_name('random_device_path_name') + semicolon
options_stmt_recursing_file = Keyword('recursing-file').suppress() - quoted_path_name('recursing_file_path_name') + semicolon
options_stmt_recursive_clients = Keyword('recursive-clients').suppress() - number_type('recursive_clients') + semicolon
options_stmt_resolver_query_timeout = Keyword('resolver-query-timeout').suppress() - seconds_type('resolver_query_timeout') + semicolon
options_stmt_secroots_file = Keyword('secroots-file').suppress() - quoted_path_name('secroots_file_path_name') + semicolon
options_stmt_serial_query_rate = Keyword('serial-query-rate').suppress() - number_type('serial_query_rate') + semicolon
options_stmt_server_id_name = fqdn_name('server_id_fqdn_name')
options_stmt_server_id_name.setName('<server_id_string>')
options_stmt_server_id = Keyword('server-id').suppress() - (quoted_domain_generic_fqdn | options_stmt_server_id_name('server_id_name'))('server_id_name') + semicolon
options_stmt_session_keyalg = Keyword('session-keyalg').suppress() - name_type('session_keyalg_name') + semicolon
options_stmt_session_keyname = Keyword('session-keyname').suppress() - key_id('session_keyname_name') + semicolon
options_stmt_session_keyfile = Keyword('session-keyfile').suppress() - quoted_path_name('session_keyfile_path_name') + semicolon
options_stmt_stacksize = Keyword('stacksize').suppress() - size_spec('stacksize') + semicolon
options_stmt_statistics_file = Keyword('statistics-file').suppress() - quoted_path_name('statistics_file_path_name') + semicolon
options_stmt_tcp_clients = Keyword('tcp-clients').suppress() - number_type('tcp_clients') + semicolon
options_tcp_listen_queue = Keyword('tcp-listen-queue').suppress() - number_type('tcp_listen_queue') + semicolon
options_tkey_dhkey_tag = number_type
options_tkey_dhkey_tag.setName('<key_tag>')
options_stmt_tkey_dhkey = (Keyword('tkey-dhkey').suppress() - Group(quoted_domain_generic_fqdn('host_name') - options_tkey_dhkey_tag('key_tag')) + semicolon)('tkey_dhkey')
options_stmt_tkey_domain = Keyword('tkey-domain').suppress() - quoted_domain_generic_fqdn('tkey_domain') + semicolon
options_stmt_tkey_gssapi_credential = (Keyword('tkey-gssapi-credential').suppress() + Group(Combine(squote + krb5_principal_name + squote)('') | Combine(dquote + krb5_principal_name + dquote)(''))('tkey_gssapi_credential') + semicolon)('')
options_stmt_tkey_gssapi_keytab = Keyword('tkey-gssapi-keytab').suppress() - quoted_path_name('tkey_gssapi_keytab_path_name') + semicolon
options_stmt_transfers_in = Keyword('transfers-in').suppress() - number_type('transfers_in') + semicolon
options_stmt_transfers_out = Keyword('transfers-out').suppress() - number_type('transfers_out') + semicolon
options_stmt_transfers_per_ns = Keyword('transfers-per-ns').suppress() - number_type('transfers_per_ns') + semicolon
options_version_string = path_name
options_version_string.setName('<version_string>')
options_stmt_version = Keyword('version').suppress() - options_version_string('version_string') + semicolon
options_multiple_stmt_disable_ds_digests = ZeroOrMore(options_stmt_disable_ds_digests)('disable_ds_digests')
options_multiple_stmt_disable_algorithms = ZeroOrMore(options_stmt_disable_algorithms)('disable_algorithms')
options_multiple_stmt_listen_on = ZeroOrMore(options_stmt_listen_on)('listen_on')
options_multiple_stmt_listen_on_v6 = ZeroOrMore(options_stmt_listen_on_v6)('listen_on')
options_multiple_stmt_tkey_dhkey = ZeroOrMore(options_stmt_tkey_dhkey)('tkey_dhkey')
options_statements_set = options_stmt_acache_cleaning_interval | options_stmt_acache_enable | options_stmt_answer_cookie | options_stmt_automatic_interface_scan | options_stmt_avoid_v4_udp_ports | options_stmt_avoid_v6_udp_ports | options_stmt_bindkeys_file | options_stmt_blackhole | options_stmt_cache_file | options_stmt_coresize | options_stmt_datasize | options_stmt_deallocate_on_exit | options_stmt_deny_answer_addresses | options_stmt_deny_answer_aliases | options_stmt_directory | options_stmt_dscp | options_stmt_dump_file | options_stmt_fake_iquery | options_stmt_flush_zones_on_shutdown | options_stmt_has_old_clients | options_stmt_hostname_statistics_max | options_stmt_hostname_statistics | options_stmt_interface_interval | options_stmt_match_mapped_addresses | options_stmt_max_rsa_exponent_size | options_stmt_memstatistics | options_stmt_memstatistics_file | options_stmt_multiple_cnames | options_stmt_named_xfer | options_stmt_pid_file | options_stmt_port | options_stmt_prefetch | options_stmt_querylog | options_stmt_random_device | options_stmt_recursing_file | options_stmt_recursive_clients | options_stmt_resolver_query_timeout | options_stmt_secroots_file | options_stmt_serial_query_rate | options_stmt_server_id | options_stmt_session_keyalg | options_stmt_session_keyfile | options_stmt_session_keyname | options_stmt_stacksize | options_stmt_statistics_file | options_stmt_tcp_clients | options_stmt_tkey_domain | options_stmt_tkey_gssapi_credential | options_stmt_tkey_gssapi_keytab | options_stmt_transfers_in | options_stmt_transfers_out | options_stmt_transfers_per_ns | options_stmt_version | options_stmt_disable_algorithms | options_stmt_disable_ds_digests | options_stmt_listen_on_v6 | options_stmt_listen_on | options_stmt_tkey_dhkey
options_statements_series = ZeroOrMore(options_statements_set)