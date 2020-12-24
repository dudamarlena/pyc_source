# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_inet.py
# Compiled at: 2019-11-22 14:50:14
"""
File: isc_inet.py

Element: inet

Title: Elements that covers Internet

Description: Provides inet-related grammar in PyParsing engine
             for ISC-configuration style

"""
from pyparsing import Word, nums, Combine, Group, pyparsing_common, ZeroOrMore, Literal, Keyword, ungroup, OneOrMore, Optional
from bind9_parser.isc_utils import semicolon, squote, dquote

def ip4_subnet_range_check(strg, loc, toks):
    """
    s = the original string being parsed
    loc = the location of the matching substring
    toks = a list of the matched tokens, packaged as a ParseResults object
    """
    value = int(toks[0])
    if value < 1 or value > 31:
        print 'IPv4 subnet is out of range: %d' % value
        print 'strg: %s' % strg
        print 'loc: %s' % loc
    return


dotted_decimal = Combine(Word(nums, max=3) + Literal('.') + Word(nums, max=3) + Literal('.') + Word(nums, max=3) + Literal('.') + Word(nums, max=3))
ip4_addr = pyparsing_common.ipv4_address
ip4_addr.setName('<ip4_addr>')
ip4s_subnet = Word(nums, min=1, max=2)
ip4s_subnet.setName('<ip4_or_ip4_subnet>')
ip4s_prefix = Combine(ip4_addr + '/' - ip4s_subnet)
ip4s_prefix.setName('<ip4subnet>')
ip6_addr = pyparsing_common.ipv6_address
ip6_addr.setName('<ip6_addr>')
ip46_addr = ip4_addr | ip6_addr
ip46_addr.setName('<ip46_addr>')
ip46_addr_or_prefix = ip4s_prefix | ip4_addr | ip6_addr
ip46_addr_or_prefix.setName('ip4^ip6^ip4/s')
ip_port = Word(nums).setParseAction(lambda toks: int(toks[0]), max=5)
ip_port.setName('<ip_port>')
inet_ip_port_keyword_and_number_element = (Keyword('port').suppress() - ip_port('ip_port'))('')
ip46_addr_and_port_list = (ip46_addr('addr') + Optional(inet_ip_port_keyword_and_number_element) + semicolon)('ip46_addr_port')('')
inet_ip_port_keyword_and_wildcard_element = Keyword('port').suppress() - (ip_port('ip_port_w') | Literal('*')('ip_port_w'))('')
dscp_port = Word(nums).setParseAction(lambda toks: int(toks[0]), max=3)
dscp_port.setName('<dscp_port>')
inet_dscp_port_keyword_and_number_element = (Keyword('dscp').suppress() + dscp_port('dscp_port'))('')
charset_wildcard = '*'
charset_wildcard_squotable = '*"'
charset_wildcard_dquotable = "*'"
wildcard_base = Literal(charset_wildcard)
wildcard_squoted = Combine(squote + Literal(charset_wildcard) + squote)
wildcard_dquoted = Combine(dquote + Literal(charset_wildcard) + dquote)
wildcard_name = wildcard_squoted | wildcard_dquoted | wildcard_base
ip4_addr_or_wildcard = wildcard_name | ip4_addr
ip6_addr_or_wildcard = wildcard_name | ip6_addr
ip46_addr_or_wildcard = wildcard_name | ip4_addr | ip6_addr
ip46_addr_or_wildcard.setName('<ip_addr_or_wildcard>')
ip46_addr_prefix_or_wildcard = wildcard_name | ip4s_prefix | ip4_addr | ip6_addr
ip46_addr_prefix_or_wildcard.setName('<ip46_addr_prefix_or_wildcard>')
ip4_addr_list = Group(ip4_addr + semicolon)
ip46_addr_list = Group(ip46_addr + semicolon)
ip4s_prefix_list = ip4s_prefix + semicolon
ip6_addr_list = ip6_addr + semicolon
ip4_addr_list_series = Group(ip4_addr_list + ZeroOrMore(ip4_addr_list))
ip46_addr_list_series = OneOrMore(ungroup(ip46_addr_list))
ip4s_prefix_list_series = Group(ip4s_prefix_list + ZeroOrMore(ip4s_prefix_list))
ip6_addr_list_series = Group(ip6_addr_list + ZeroOrMore(ip6_addr_list))
ip_addr_list = ip46_addr_or_prefix + semicolon
ip_addr_semicolon_series = Group(ip_addr_list + ZeroOrMore(ip_addr_list))