# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/todd/github/python-resolve-link/resolve_link/__init__.py
# Compiled at: 2015-07-07 19:11:05
import re, sys
try:
    from urlparse import urlsplit, urlunsplit
except ImportError:
    from urllib.parse import urlsplit, urlunsplit

TLD_REGEXP = '\\.([a-zA-Z]*?)$'
PY3 = sys.version_info[0] == 3
try:
    unicode
except NameError:

    def _is_unicode(x):
        return 0


else:

    def _is_unicode(x):
        return isinstance(x, unicode)


def resolve_link(src_url, target_url):
    """Resolve complete/partials URLs against canonical target URL

    :param str src_url: URL/partial URL to be resolving from
    :param str target_url: Canonical URL to try to match if on the same domain
    :returns str ret_val: Completed URL formatted via `urllib.parse`
    """
    encoding = None
    if _is_unicode(src_url):
        encoding = 'utf-8'
        src_url = src_url.encode(encoding)
    src_url_parts = urlsplit(src_url)
    if not src_url_parts.scheme:
        tmp_src_url = ('//{src_url}').format(src_url=src_url)
        tmp_src_url_parts = urlsplit(tmp_src_url)
        if tmp_src_url_parts.netloc and re.search(TLD_REGEXP, tmp_src_url_parts.netloc):
            src_url = tmp_src_url
            src_url_parts = tmp_src_url_parts
    src_url_dict = src_url_parts._asdict()
    if src_url_dict['path'] == '':
        src_url_dict['path'] = '/'
    if src_url_dict['scheme'] == '':
        target_url_parts = urlsplit(target_url)
        if src_url_dict['netloc']:
            if src_url_dict['netloc'] == target_url_parts.netloc:
                src_url_dict['scheme'] = target_url_parts.scheme
            else:
                src_url_dict['scheme'] = 'http'
        else:
            src_url_dict['scheme'] = target_url_parts.scheme
            src_url_dict['netloc'] = target_url_parts.netloc
    ret_url = urlunsplit((src_url_dict['scheme'], src_url_dict['netloc'], src_url_dict['path'],
     src_url_dict['query'], src_url_dict['fragment']))
    if encoding:
        ret_url = ret_url.decode(encoding)
    return ret_url