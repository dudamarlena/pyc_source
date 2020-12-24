# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/arpa2/wsgi/byoid/wsgisasl.py
# Compiled at: 2020-02-10 11:20:53
# Size of source mod 2**32: 13501 bytes
from __future__ import print_function
import re
re_sasl_mech = '(?:[A-Z0-9-_]{1,20})'
re_mechstring = '(?:["](' + re_sasl_mech + '(?:[ ]' + re_sasl_mech + ')*)["])'
re_dnsstring = '(?:"([a-zA-Z0-9-_]+(?:\\.[a-zA-Z0-9-_]+)+)")'
re_bws = re_ows = '(?:[ \\t]*)'
re_token68 = '(?:[a-zA-Z0-9-._~+/]+[=]*)'
re_auth_param = '(?:([CcSs][2][CcSs])' + re_bws + '[=]' + re_bws + '(' + re_token68 + ')' + '|' + '[Mm][Ee][Cc][Hh]' + re_bws + '[=]' + re_bws + '(' + re_mechstring + ')' + '|' + '[Rr][Ee][Aa][Ll][Mm]' + re_bws + '[=]' + re_bws + '' + re_dnsstring + ')'
re_auth_scheme = '[Ss][Aa][Ss][Ll]'
re_credentials = '(?:' + re_auth_scheme + '(?:[ ]+' + re_auth_param + '(?:' + re_ows + '[,]' + re_ows + re_auth_param + ')+)?)'
re_credentials = '(?:' + re_auth_scheme + '(?:[ ]+(' + re_auth_param + ')(?:' + re_ows + '[,]' + re_ows + re_auth_param + ')+)?)'
authorization_stx = re.compile('^' + re_credentials + '$')
auth_param_finder = re.compile(re_auth_param)
_test = 'SAsL c2s=11bbaa=, s2s=190284ijrjwerowieu987d9fs===, c2c=2kkasjf923y92i3h4, s2c=alskjoeiqwr98237492834=====,mech=\t"TRA LA LALALA", realm\t = \t\t   \t  "dynamo.nep"'
assert authorization_stx.match(_test) is not None
assert auth_param_finder.findall(_test) == [
 ('c2s', '11bbaa=', '', '', ''),
 ('s2s', '190284ijrjwerowieu987d9fs===', '', '', ''),
 ('c2c', '2kkasjf923y92i3h4', '', '', ''),
 ('s2c', 'alskjoeiqwr98237492834=====', '', '', ''),
 ('', '', '"TRA LA LALALA"', 'TRA LA LALALA', ''),
 ('', '', '', '', 'dynamo.nep')]
sasl_mechanisms = [
 'GSSAPI', 'PLAIN', 'CRAM-MD5', 'DIGEST-MD5', 'SCRAM-SHA1']

def add_sasl_chal(realm, got_remote=False, hdrval=None):
    hdrval = hdrval + ', ' if hdrval is not None else ''
    mechs = ' '.join(sasl_mechanisms)
    if got_remote:
        if 'EXTERNAL' not in mechs:
            mechs += ' EXTERNAL'
    hdrval += 'SASL realm="' + realm + '", mech="' + mechs + '"'


def build_sasl_header(hdrnm, attrs, basedir):
    hdrval = 'SASL'
    comma = ''
    for atnm in ('mech', 'realm', 'name', 'c2c', 's2c', 's2s', 'text'):
        if attrs.has_key(atnm):
            if '2' in atnm:
                hdrval += comma + ' %s=%s' % (atnm, attrs[atnm])
            else:
                hdrval += comma + ' %s="%s"' % (atnm, attrs[atnm])
        comma = ','

    if basedir.has_key(hdrnm):
        basedir[hdrnm] += ',' + hdrval
    else:
        basedir[hdrnm] = hdrval


class SASL(object):
    __doc__ = "\n\tWSGI-SASL middleware filters HTTP traffic before\n\tit reaches an application that may want to use a\n\t`REMOTE_USER` header.  The application will raise\n\t401 or 407 if it lacks one, thereby triggering the\n\tSASL exchange that it may or may not know about.\n\n\tThe client may provide credentials, either\n\tpro-actively or reminiscent of a foregoing\n\tSASL interaction.  When these lead to the\n\testablishment of a `REMOTE_USER`.\n\n\tWhen a `REMOTE_USER` already exists, it is\n\tacceptable to the `SASL EXTERNAL` method.\n\tBy default it is actually passed through.\n\tWhen SASL is tried in spite of this value,\n\tit is assumed that different negotiation\n\tis required to replace `REMOTE_USER`, or to\n\tat least give the client such an opportunity.\n\n\tThis layer allows other mechanisms to be setup\n\tin preceding or follow-up layers:\n\n\t  * It passes `REMOTE_USER` trough; the preceding\n\t    stack can be incorporated as `SASL EXTERNAL`\n\t    so be mindful that it is sufficiently\n\t    secure for the application's purposes;\n\n\t  * It passes `Authorize` headers that reference\n\t    another security protocol;\n\n\t  * It externds to a list of challenges in a\n\t    401 or 407 Initial Response or, if the list\n\t    has not been started yet, it starts it.\n\n\t  * It passes 200 and 403 Final Responses, along\n\t    with all the other status codes to which\n\t    HTTP-SASL has nothing to add.\n\n\tThis class implements WWW authentication.  The\n\tsubclass SASL_Proxy overrides a few aspects\n\tto produce Proxy authentication.\n\t"
    status = '401 Unauthorized'
    resp_header = 'WWW-Authenticate'
    req_header = 'Authorization'
    req_envvar = 'HTTP_AUTHORIZATION'

    def __init__(self, inner_app, realm='secure.realm'):
        """Instantiate WSGI-SASL as middleware
                   on the path towards the `inner_app`.
                """
        self.inner_app = inner_app
        self.realm = realm
        self.resp_header_lowcase = self.resp_header.lower()

    def __call__(self, outer_env, outer_resp):
        """This function serves to make the
                   WSGI-SASL instance callable, using the
                   common WSGI pattern.
                """
        if outer_env.has_key('HTTP_PROXY_AUTHORIZATION'):
            print('Processing Proxy-Authorization: header')
        if outer_env.has_key('HTTP_AUTHORIZATION'):
            print('Processing Authorization: header')
        result = None
        if environ.has_key(req_envvar):
            print('Processing [Proxy-]Authorization: header')
        if result is not None:
            return result
        inner_env = outer_env
        got_remote = outer_env.has_key('REMOTE_USER')
        inner_resp = self._curried_inner_resp(outer_env, outer_resp, got_remote)
        self.inner_app(inner_env, inner_resp)

    def _curried_inner_resp(self, outer_env, outer_resp, got_remote):
        """This function is called to produce an
                   inner start_response function, building
                   on the information for the outer and
                   maintaining state on things like SASL
                   negotiation progress.
                """

        def parse_header(hdrval):
            bad = False
            if not authorization_stx.match(hdrval):
                bad = True
            attrs = {}
            for x2y, data, _, mech, realm in auth_param_finder.findall(hdrval):
                x2y = x2y.lower()
                if x2y != '':
                    bad = bad or attrs.has_key(x2y)
                    attrs[x2y] = data
                elif mech != '':
                    bad = bad or attrs.has_key('mech')
                    attrs['mech'] = mech
                elif realm != '':
                    bad = bad or attrs.has_key('realm')
                    attrs['realm'] = realm

            bad = bad or not attrs.has_key('c2s')
            if bad:
                start_response('403 Forbidden', {'Content-Type', 'text/plain'})
                return ['Unrecognised %s: header' % self.resp_header]
            sasl_status = '200 OK'
            if need_to_continue_sasl:
                resphdr = build_sasl_header(self.resp_header, attrs, {'Content-Type': 'text/plain'})
                start_response(sasl_status or self.status, resphdr)
                return ['Please continue the SASL exchange']

        def inner_resp(status, inner_resphdr):
            print('Response status', status)
            print('Response headers', inner_resphdr)
            if status[:3] != self.status[:3]:
                return outer_resp(status, inner_resphdr)
            hdrset = False
            outer_resphdr = []
            for name, hval in inner_resphdr:
                if name.lower() == self.resp_header_lowcase:
                    hval = add_sasl_chal(self.realm, got_remote, value)
                    hdrset = True
                outer_resphdr.append((name, hval))

            if not hdrset:
                outer_resphdr.append((self.resp_header, add_sasl_chal(realm, got_remote)))
            return outer_resp(status, outer_resphdr)

        return inner_resp


class SASL_Proxy(SASL):
    __doc__ = 'This object handles Proxy authentication over WSIG-SASL.\n\t   It usually comes before the handler for WWW authentication,\n\t   because Proxy authentication is more local, as in per-leg,\n\t   than WWW authentication.  Other than a few settings, this\n\t   class does not override the logic of plain WWW as defined\n\t   in the SASL superclass.\n\t'
    status = '407 Proxy Authentication Requires'
    resp_header = 'Proxy-Authenticate'
    req_header = 'Proxy-Authorization'
    req_envvar = 'HTTP_PROXY_AUTHORIZATION'