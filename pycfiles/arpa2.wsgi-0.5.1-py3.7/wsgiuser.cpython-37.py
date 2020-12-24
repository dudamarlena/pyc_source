# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/arpa2/wsgi/byoid/wsgiuser.py
# Compiled at: 2020-02-10 11:21:05
# Size of source mod 2**32: 8064 bytes
import re, base64, urllib.parse

def _chrs(fst, lst):
    return '[\\x%02x-\\x%02x]' % (fst, lst)


rex_tail = _chrs(128, 191)
rex_utf8_2 = _chrs(194, 223) + rex_tail
rex_utf8_3 = '(?:%s|%s|%s|%s)' % (
 _chrs(224, 224) + _chrs(160, 191) + rex_tail,
 _chrs(225, 236) + rex_tail + rex_tail,
 _chrs(237, 237) + _chrs(128, 159) + rex_tail,
 _chrs(238, 239) + rex_tail + rex_tail)
rex_utf8_4 = '(?:%s|%s|%s)' % (
 _chrs(240, 240) + _chrs(144, 191) + rex_tail + rex_tail,
 _chrs(241, 243) + rex_tail + rex_tail + rex_tail,
 _chrs(244, 244) + _chrs(128, 143) + rex_tail + rex_tail)
rex_utf8_xtra_char = '(?%s|%s|%s)' % (rex_utf8_2, rex_utf8_3, rex_utf8_4)
rex_char = '[\x80-ÿ]'
rex_string = '(?:(?:[a-zA-Z0-9]|%s)+)' % rex_char
rex_username = '(?:%s(?:[.]%s)*)' % (rex_string, rex_string)
rex_utf8_rtext = '(?:[a-zA-Z0-9]|%s)' % rex_char
rex_ldh_str = '(?:(?:%s|[-])*%s)' % (rex_utf8_rtext, rex_utf8_rtext)
rex_label = '(?:%s(?:%s)*)' % (rex_utf8_rtext, rex_ldh_str)
rex_realm = '(?:%s(?:[.]%s)+)' % (rex_label, rex_label)
rex_nai = '(?:%s(?:[@]%s)?|[@]%s)' % (rex_username, rex_realm, rex_realm)
re_nai = re.compile('^%s$' % rex_nai)
rex_tilde = '^/~([^/]*)(/.*|$)'
re_tilde = re.compile(rex_tilde)

def _curried_add_vary(outer_resp):

    def _add_vary(status, resphdrs):
        outer_resp(status, resphdrs)
        resphdrs.append(('Vary', 'User'))

    return _add_vary


def mismatch_app(environ, start_response):
    status = '400 Bad Request'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['You provided several server-side user resource that did not match:\n - User header as per draft-vanrein-http-unauth-user\n - Basic authentication user name\n - Path information format /~username\nPlease check that these match or talk to your server administrator\n']


class User(object):
    __doc__ = 'WSGI-User middleware filters HTTP traffic\n\t   to detect if the User header is present.\n\t   If it is, the escape-removed version of\n\t   the header is syntax checked and, when\n\t   accepted, the result is stored in the\n\t   LOCAL_USER environment variable.\n\t   \n\t   The syntax check defaults to the NAI, as\n\t   defined in RFC 7542, with an extra flag\n\t   to also permit empty strings, defaulting\n\t   to True.\n\t   \n\t   When a LOCAL_USER value is delivered, the\n\t   cache will be notified of possible influence\n\t   of the User header through Vary in the\n\t   response.\n\t'

    def __init__(self, inner_app, user_syntax=None, allow_empty=True, map_tilde=True, map_basic=True, map_basic_always=False, proxy_auth=False):
        """Instantiate WSGI-User middleware for
                   the given syntax for LOCAL_USER, where
                   the default is the NAI syntax.  Other
                   regexes can be supplied.  The additional
                   flag allow_empty stores empty values for
                   the User header in LOCAL_USER even when
                   the syntax does not accept it, as would
                   be the case with a NAI.  By default,
                   empty strings are allowed.  Note that
                   the User header may contain % escapes,
                   which are removed before any of this
                   processing takes place.  Also note
                   that URIs, which are one possible
                   source for the User header value, are
                   not constrained to UTF-8 but can send
                   general binary strings (which is why
                   the addition of a parser is healthy).
                """
        if user_syntax is None:
            user_syntax = re_nai
        else:
            if type(user_syntax) == str:
                user_syntax = re.compile(user_syntax)
        self.user_syntax = user_syntax
        self.allow_empty = allow_empty
        self.inner_app = inner_app
        self.map_tilde = map_tilde
        self.map_basic = map_basic or map_basic_always
        self.drop_passwd = map_basic_always
        self.basic_header = 'HTTP_PROXY_AUTHORIZATION' if proxy_auth else 'HTTP_AUTHORIZATION'

    def __call__(self, outer_env, outer_resp):
        """This function makes WSGI-User instances
                   callable, using the common WSGI pattern.
                """
        mismatch = False
        inner_env = outer_env
        inner_resp = outer_resp
        user = outer_env.get('HTTP_USER')
        local_user = None
        if user is None:
            pass
        elif ':' in user:
            pass
        else:
            local_user = urllib.parse.unquote(user)
            inner_resp = _curried_add_vary(outer_resp)
        if self.map_tilde:
            tm = re_tilde.match(outer_env['PATH_INFO'])
            if tm is not None:
                tilde_user, new_path = tm.groups()
                if new_path == '':
                    new_path = '/'
                inner_env['PATH_INFO'] = new_path
                if local_user is not None:
                    mismatch = local_user != tilde_user
                if self.user_syntax.match(tilde_user):
                    local_user = tilde_user
        if self.map_basic:
            if self.basic_header in outer_env:
                try:
                    basic = outer_env[self.basic_header]
                    assert basic[:6] == 'Basic '
                    resp = base64.b64decode(basic[6:])
                    resp = str(resp, 'utf-8')
                    basic_user, pwd = resp.split(':', 1)
                    if local_user is not None:
                        mismatch = local_user != basic_user
                    local_user = basic_user
                    if self.drop_passwd or pwd == '':
                        del inner_env[self.basic_header]
                except Exception as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

        if local_user is None:
            pass
        elif local_user == '':
            local_user = self.allow_empty or None
        else:
            if not self.user_syntax.match(local_user):
                local_user = None
            if local_user is None:
                inner_resp = outer_resp
            next_app = self.mismatch_app if mismatch else self.inner_app
            if local_user is not None:
                inner_env['LOCAL_USER'] = local_user
            return next_app(inner_env, inner_resp)