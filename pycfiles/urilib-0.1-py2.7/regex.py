# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/urilib/regex.py
# Compiled at: 2011-08-25 23:29:20
pct_encoded = '%[0-9a-fA-F]{2}'
unreserved = '[\\w.~-]'
sub_delims = "[!$&\\'()*+,;=]"
gen_delims = '[:/?#[\\]@]'
reserved = '(?:%s|%s)' % (sub_delims, gen_delims)
pchar = '(?:%s|%s|%s|:|@)' % (unreserved, pct_encoded, sub_delims)
query = '(?:%s|/|[?])*' % pchar
fragment = '(?:%s|/|[?])*' % pchar
segment = '(?:%s)*' % pchar
segment_nz = '(?:%s)+' % pchar
segment_nz_nc = '(?:%s|%s|%s|@)+' % (unreserved, pct_encoded, sub_delims)
path_abempty = '(?:/%s)*' % segment
path_absolute = '(?:/(?:%s(?:/%s)*)*' % (segment_nz, segment)
path_noscheme = '(?:%s(?:/%s)*)' % (segment_nz_nc, segment)
path_rootless = '(?:%s(?:/%s)*' % (segment_nz, segment)
path_empty = ''
path = '%s|%s|%s|%s|%s' % (path_abempty, path_absolute, path_noscheme,
 path_rootless, path_empty)
dec_octet = '\\d{1,3}'
hexdigit = '[0-9a-fA-F]'
h16 = '%s{4}' % hexdigit
ipv4_address = '%s\\.%s\\.%s\\.%s' % (dec_octet, dec_octet, dec_octet, dec_octet)
ls32 = '(?:%s:%s|%s)' % (h16, h16, ipv4_address)
ipv6_part = '(?:%s:)' % h16
ipv6_address = '(?:%s{6}%s' % (ipv6_part, ls32)
ipvfuture = ''
ip_literal = '\\[(?:%s|%s)\\]' % (ipv6_address, ipvfuture)
reg_name = '(?:%s|%s|%s)' % (unreserved, pct_encoded, sub_delims)
userinfo = '(?:%s|%s|%s|:)' % (unreserved, pct_encoded, sub_delims)
host = '(?:%s|%s|%s)' % (ip_literal, ipv4_address, reg_name)
port = '\\d'
scheme = '(?:[^\\W\\d_](?:[^\\W_]|[+.\\-])*)'
authority = '(?:%s@)?%s(?::%s)?' % (userinfo, host, port)
hier_part = '(?://%s%s|%s|%s|%s)' % (authority, path_abempty, path_absolute,
 path_noscheme, path_empty)
uri = '%s:%s(?:[?]%s)(?:[#]%s)' % (scheme, hier_part, query, fragment)
relative_part = '//%s%s|%s|%s|%s' % (authority, path_abempty, path_absolute,
 path_noscheme, path_empty)
relative_ref = '%s(?:%s)?(?:%s)?' % (relative_part, query, fragment)
uri_reference = '(?:%s)|(?:%s)' % (uri, relative_ref)
absolute_uri = '%s:%s(?:[?]%s)' % (scheme, hier_part, query)
simple_uri_regex = '^(([^:/?#]+):)?((//([^/?#]*))?([^?#]*))?(\\?([^#]*))?(#(.*))?'