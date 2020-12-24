# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/re_statements.py
# Compiled at: 2017-04-24 18:24:00
# Size of source mod 2**32: 5277 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
http_header_name = '[^\x00-\x1e\x7f()<>@,;:\\\\"/\\[\\]?={} \t]+'.encode('us-ascii')
http_method_name = 'GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE'
http_path_alphabet = 'a-zA-Z0-9_\\-.~%:/?#\\[\\]@!$&\'()*+,;="'
http_path = '/[' + http_path_alphabet + ']*'
http_version = '0\\.9|1\\.0|1\\.1'
uri_query_alphabet = "a-zA-Z0-9\\-._~%!$&'()*+,;=:@/?"
uri_fragment_alphabet = "a-zA-Z0-9\\-._~%!$&'()*+,;=:@/?"
http_get_vars_selection = '\\?([' + uri_query_alphabet + ']+)(#[' + uri_fragment_alphabet + ']*)?$'
http_post_vars_selection = '([' + uri_query_alphabet + ']+)'
http_cookie_expires = '[a-zA-Z0-9 ,:-]+'
http_cookie_max_age = '[1-9][0-9]*'
http_cookie_domain = '[a-zA-Z\\-.0-9]+'
http_cookie_secure = '.*'
http_cookie_httponly = '.*'
wasp_presenter_name_alphabet = 'a-zA-Z0-9_.\\-'
wasp_presenter_name_selection = '([a-zA-Z][' + wasp_presenter_name_alphabet + ']*)'
wasp_route_uri_pattern_alphabet = http_path_alphabet + '\\{\\}\\\\'
wasp_route_arg_name = '[a-zA-Z][a-zA-Z0-9_]*'
wasp_route_arg_name_selection = '\\{(' + wasp_route_arg_name + ')\\}'
wasp_route_arg_value_alphabet = http_path_alphabet
for c in ['/', '?', ',', '#']:
    wasp_route_arg_value_alphabet = wasp_route_arg_value_alphabet.replace(c, '')

wasp_route_arg_value_selection = '([' + wasp_route_arg_value_alphabet + ']+)'
wasp_route_custom_arg_value_pattern = '[^"]'
wasp_route_custom_arg_selection = '(\\{(' + wasp_route_arg_name + ') *: *"(' + wasp_route_custom_arg_value_pattern + '+)"\\})'
wasp_route_import_pattern = '^\\s*([' + wasp_route_uri_pattern_alphabet + ']+) +=> +' + wasp_presenter_name_selection + '( +\\((.*)\\))?\\s*$'