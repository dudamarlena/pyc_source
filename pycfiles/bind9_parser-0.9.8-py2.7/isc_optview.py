# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_optview.py
# Compiled at: 2019-11-22 14:50:37
"""
File: isc_optview.py

Clause: options, view

Title: Statements Used Only By options And view Clauses

Description: isc_optview contains all parse elements pertaining
             to both options and view (but not zones)

"""
from pyparsing import Group, Keyword, OneOrMore, Literal, CaselessLiteral, Combine, Optional, Word, alphanums, ZeroOrMore, ungroup
from bind9_parser.isc_utils import isc_boolean, semicolon, lbrack, rbrack, squote, dquote, number_type, name_type, minute_type, seconds_type, byte_type, parse_me, run_me, path_name, check_options, quoted_path_name, size_spec, exclamation
from bind9_parser.isc_aml import aml_nesting, aml_choices
from bind9_parser.isc_inet import ip4_addr, ip6_addr, inet_ip_port_keyword_and_number_element, inet_ip_port_keyword_and_wildcard_element
from bind9_parser.isc_zone import zone_name
from bind9_parser.isc_domain import quoted_domain_generic_fqdn, domain_generic_fqdn, rr_fqdn_w_absolute
optview_stmt_acache_cleaning_interval = Keyword('acache-cleaning-interval').suppress() - isc_boolean('acache_cleaning_interval') + semicolon
optview_stmt_acache_enable = Keyword('acache-enable').suppress() - isc_boolean('acache_enable') + semicolon
optview_stmt_additional_from_auth = Keyword('additional-from-auth').suppress() - isc_boolean('additional_from_auth') + semicolon
optview_stmt_additional_from_cache = Keyword('additional-from-cache').suppress() - isc_boolean('additional_from_cache') + semicolon
optview_stmt_allow_new_zones = Keyword('allow-new-zones').suppress() - isc_boolean('allow_new_zones') + semicolon
optview_stmt_allow_query_cache = (Keyword('allow-query-cache').suppress() - Group(aml_nesting(''))('allow_query_cache'))('')
optview_stmt_allow_query_cache_on = (Keyword('allow-query-cache-on').suppress() - Group(aml_nesting(''))('allow_query_cache_on'))('')
optview_stmt_allow_recursion = (Keyword('allow-recursion').suppress() - Group(aml_nesting(''))('allow-recursion'))('')
optview_stmt_allow_recursion_on = (Keyword('allow-recursion-on').suppress() - Group(aml_nesting(''))('allow-recursion-on'))('')
optview_attach_cache_name = name_type
optview_attach_cache_name.setName('<cache_name>')
optview_stmt_attach_cache = Keyword('attach-cache').suppress() - optview_attach_cache_name('attach_cache') + semicolon
optview_stmt_auth_nxdomain = Keyword('auth-nxdomain').suppress() - isc_boolean('auth_nxdomain') + semicolon
optview_stmt_cache_file = Keyword('cache-file').suppress() - path_name('cache_file') + semicolon
optview_stmt_check_dup_records = Keyword('check-dup-records').suppress() - check_options('check_dup_records') + semicolon
optview_stmt_check_integrity = Keyword('check-integrity').suppress() - isc_boolean('check_integrity') + semicolon
optview_stmt_check_mx = Keyword('check-mx').suppress() - check_options('check_mx') + semicolon
optview_stmt_check_mx_cname = Keyword('check-mx-cname').suppress() - check_options('check_mx_cname') + semicolon
optview_stmt_check_names = (Keyword('check-names').suppress() - Group((Literal('master')('') | Literal('primary')('') | Literal('slave')('') | Literal('secondary')('') | Literal('response')(''))('zone_type') + check_options('result_status'))('') + semicolon)('check_names')
optview_stmt_check_sibling = Keyword('check-sibling').suppress() + check_options('check_sibling') + semicolon
optview_stmt_check_spf = Keyword('check-spf').suppress() - check_options('check_spf') - semicolon
optview_stmt_check_srv_cname = Keyword('check-srv-cname').suppress() - check_options('check_srv_cname') + semicolon
optview_stmt_check_wildcard = Keyword('check-wildcard').suppress() - isc_boolean('check_wildcard') + semicolon
optview_stmt_cleaning_interval = Keyword('cleaning-interval').suppress() - minute_type('cleaning_interval') + semicolon
optview_stmt_disable_empty_zone = (Keyword('disable-empty-zone').suppress() - Group(zone_name('') | Combine(squote + zone_name + squote)('') | Combine(dquote + zone_name + dquote)(''))('') + semicolon)('disable_empty_zone')
optview_stmt_dnssec_accept_expired = Keyword('dnssec-accept-expired').suppress() - isc_boolean('dnssec_accept_expired') + semicolon
optview_stmt_dnssec_enable = Keyword('dnssec-enable').suppress() - isc_boolean('dnssec_enable') + semicolon
optview_stmt_dnssec_lookaside = (Keyword('dnssec-lookaside').suppress() - Group(Keyword('auto') | Keyword('no') | Group(rr_fqdn_w_absolute('rr_set') + Keyword('trust-anchor')('').suppress() + domain_generic_fqdn('prepend_key_name'))('trust_anchor_method'))('dnssec_lookaside') + semicolon)('')
optview_stmt_dnssec_must_be_secure = Keyword('dnssec-must-be-secure').suppress() - Group(rr_fqdn_w_absolute('domain') - isc_boolean('accept_secured_answers'))('dnssec_must_be_secure') + semicolon
optview_stmt_dnssec_validation = Keyword('dnssec-validation').suppress() - (Literal('auto') | isc_boolean)('dnssec_validation') + semicolon
dual_stack_servers_address_set = ((Group(ip4_addr('ip4_addr') + Optional(inet_ip_port_keyword_and_number_element)) ^ Group(ip6_addr('ip6_addr') + Optional(inet_ip_port_keyword_and_number_element)) ^ Group(quoted_domain_generic_fqdn('domain') + Optional(inet_ip_port_keyword_and_number_element))) + semicolon)('')
dual_stack_servers_address_series = Group(ZeroOrMore(dual_stack_servers_address_set(''))(''))('')
optview_stmt_dual_stack_servers = (Keyword('dual-stack-servers').suppress() - Group(Optional(inet_ip_port_keyword_and_number_element('')) + lbrack - dual_stack_servers_address_series('addrs') + rbrack)('dual_stack_servers') + semicolon)('')
soa_name_type = rr_fqdn_w_absolute
optview_stmt_empty_contact = (Keyword('empty-contact').suppress() - Group(soa_name_type('soa_contact_name') + semicolon)('empty_contact'))('')
optview_stmt_empty_zones_enable = Keyword('empty-zones-enable').suppress() - isc_boolean('empty_zones_enable') + semicolon
optview_stmt_fetch_glue = Keyword('fetch-glue').suppress() - isc_boolean('fetch_glue') + semicolon
optview_stmt_files = (Keyword('files').suppress() - Group((ungroup(number_type('')) | Literal('unlimited')('') | Keyword('default'))('files_count'))('files') + semicolon)('')
optview_stmt_heartbeat_interval = Keyword('heartbeat-interval').suppress() - minute_type('heartbeat_interval') + semicolon
optview_stmt_hostname = Keyword('hostname').suppress() - Group(Literal('none')('none') | quoted_domain_generic_fqdn('hostname')('name') | domain_generic_fqdn('hostname')('name'))('hostname') + semicolon
optview_stmt_lame_ttl = Keyword('lame-ttl').suppress() - number_type('lame_ttl') + semicolon
optview_stmt_managed_keys_directory = Keyword('managed-keys-directory').suppress() - quoted_path_name('managed_keys_directory') + semicolon
optview_stmt_max_cache_size = Keyword('max-cache-size').suppress() - size_spec('max_cache_size') + semicolon
optview_stmt_max_cache_ttl = Keyword('max-cache-ttl').suppress() - seconds_type('max_cache_ttl') + semicolon
optview_stmt_max_ncache_ttl = Keyword('max-ncache-ttl').suppress() - seconds_type('max_ncache_ttl') + semicolon
optview_stmt_minimal_responses = Keyword('minimal-responses').suppress() - isc_boolean('minimal_responses') + semicolon
optview_stmt_preferred_glue = Keyword('preferred-glue').suppress() - (CaselessLiteral('A') ^ CaselessLiteral('AAAA') ^ CaselessLiteral('none'))('preferred_glue') + semicolon
optview_stmt_query_source = (Keyword('query-source').suppress() - Group(Optional(Optional(Keyword('address').suppress() + (ip4_addr('ip4_addr') | Literal('*')('ip4_addr')))(''))('') + Optional(inet_ip_port_keyword_and_wildcard_element('')))('query_source') + semicolon)('')
optview_stmt_query_source_v6 = (Keyword('query-source-v6').suppress() - Group(Optional(Keyword('address').suppress() + (ip6_addr('ip6_addr') | Literal('*')('ip6_addr'))(''))('') + Optional(inet_ip_port_keyword_and_wildcard_element('')))('query_source_v6') + semicolon)('')
optview_rate_limit_options = ((Keyword('all-per-second').suppress() - Group(number_type('all_per_second'))(''))('') | (Keyword('errors-per-second').suppress() - Group(number_type('errors_per_second'))(''))('') | (Keyword('exempt-clients').suppress() + lbrack + OneOrMore(Group(exclamation('not') + aml_nesting | exclamation('not') + aml_choices + semicolon | aml_nesting | aml_choices + semicolon))(None)('') + rbrack)('') | (Keyword('ipv4-prefix-length').suppress() - Group(number_type('ipv4_prefix_length'))(''))('') | (Keyword('ipv6-prefix-length').suppress() - Group(number_type('ipv6_prefix_length'))(''))('') | (Keyword('log-only').suppress() - Group(isc_boolean('log_only'))(''))('') | (Keyword('min-table-size').suppress() - Group(number_type('min_table_size'))(''))('') | (Keyword('max-table-size').suppress() - Group(number_type('max_table_size'))(''))('') | (Keyword('nodata-per-second').suppress() - Group(number_type('nodata_per_second'))(''))('') | (Keyword('nxdomains-per-second').suppress() - Group(number_type('nxdomains_per_second'))(''))('') | (Keyword('qps-scale').suppress() - Group(number_type('qps_scale'))(''))('') | (Keyword('referrals-per-second').suppress() - Group(number_type('referrals_per_second'))(''))('') | (Keyword('responses-per-second').suppress() - Group(number_type('responses_per_second'))(''))('') | (Keyword('slip').suppress() - Group(number_type('slip'))(''))('') | (Keyword('responses-per-second').suppress() - Group(number_type('response_per_second'))(''))('') | (Keyword('slip').suppress() - Group(number_type('slip'))(''))('') | (Keyword('window').suppress() - Group(number_type('window'))(''))('')) + semicolon
optview_stmt_rate_limit = (Keyword('rate-limit').suppress() + lbrack + OneOrMore(optview_rate_limit_options)('rate_limit') + rbrack + semicolon)('')
optview_stmt_recursion = Keyword('recursion').suppress() - isc_boolean('recursion') + semicolon
optview_stmt_response_policy = (Keyword('response-policy').suppress() - (lbrack + OneOrMore(Group(Keyword('zone') + zone_name + (Keyword('policy').suppress() + (Literal('given') | Literal('disabled') | Literal('passthru') | Literal('drop') | Literal('nxdomain') | Literal('nodata') | (Literal('tcp-only').suppress() + quoted_path_name)('tcp_only') | (Literal('cname').suppress() + rr_fqdn_w_absolute)('cname'))('policy') | Keyword('recursive-only').suppress() - isc_boolean('recursive_only') | Keyword('max-policy-ttl').suppress() - seconds_type('max_policy_ttl') | Keyword('break-dnssec').suppress() + isc_boolean('break_dnssec') | Keyword('min-ns-dots').suppress() + number_type('min_ns_dots') | (Keyword('log').suppress() + isc_boolean)('log')))('') + semicolon)('') + rbrack)('response_policy') + semicolon)('')
optview_stmt_rfc2308_type1 = Keyword('rfc2308-type1').suppress() - isc_boolean('rfc2308_type1') + semicolon
optview_stmt_root_delegation_only = Keyword('root-delegation-only').suppress() - Optional(Keyword('exclude').suppress() + lbrack - Group(OneOrMore(domain_generic_fqdn('') + semicolon)('domains'))('root_delegation_only') + rbrack)('')('') + semicolon
optview_class_type = CaselessLiteral('HS') | CaselessLiteral('IN') | CaselessLiteral('CH') | CaselessLiteral('ANY')
optview_type_type = Word(alphanums + '-', max=16)
optview_ordering_type = Literal('fixed') | Literal('random') | Literal('cyclic')
optview_order_spec = Optional(Keyword('class').suppress() + optview_class_type('class'))('') + Optional(Keyword('type').suppress() + optview_type_type('type'))('') + Optional(Keyword('name').suppress() + quoted_domain_generic_fqdn('name'))('') + Keyword('order').suppress() + optview_ordering_type('order') + semicolon
optview_stmt_rrset_order = (Keyword('rrset-order').suppress() - (lbrack + OneOrMore(Group(optview_order_spec(''))(''))('') + rbrack)('rrset_order') + semicolon)('')
optview_stmt_sortlist = (Keyword('sortlist').suppress() - Group(aml_nesting(''))('sortlist'))('')
optview_statements_set = optview_stmt_acache_cleaning_interval | optview_stmt_acache_enable | optview_stmt_additional_from_auth | optview_stmt_additional_from_cache | optview_stmt_allow_new_zones | optview_stmt_allow_query_cache_on | optview_stmt_allow_query_cache | optview_stmt_allow_recursion_on | optview_stmt_allow_recursion | optview_stmt_attach_cache | optview_stmt_auth_nxdomain | optview_stmt_cache_file | optview_stmt_check_dup_records | optview_stmt_check_integrity | optview_stmt_check_mx_cname | optview_stmt_check_mx | optview_stmt_check_names | optview_stmt_check_sibling | optview_stmt_check_spf | optview_stmt_check_srv_cname | optview_stmt_check_wildcard | optview_stmt_cleaning_interval | optview_stmt_disable_empty_zone | optview_stmt_dnssec_accept_expired | optview_stmt_dnssec_enable | optview_stmt_dnssec_lookaside | optview_stmt_dnssec_must_be_secure | optview_stmt_dnssec_validation | optview_stmt_dual_stack_servers | optview_stmt_empty_contact | optview_stmt_empty_zones_enable | optview_stmt_fetch_glue | optview_stmt_files | optview_stmt_heartbeat_interval | optview_stmt_hostname | optview_stmt_lame_ttl | optview_stmt_managed_keys_directory | optview_stmt_max_cache_size | optview_stmt_max_cache_ttl | optview_stmt_max_ncache_ttl | optview_stmt_minimal_responses | optview_stmt_preferred_glue | optview_stmt_query_source_v6 | optview_stmt_query_source | optview_stmt_rate_limit | optview_stmt_recursion | optview_stmt_response_policy | optview_stmt_rfc2308_type1 | optview_stmt_root_delegation_only | optview_stmt_rrset_order | optview_stmt_sortlist
optview_statements_series = ZeroOrMore(optview_statements_set)