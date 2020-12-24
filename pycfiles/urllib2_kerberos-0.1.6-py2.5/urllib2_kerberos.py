# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/urllib2_kerberos.py
# Compiled at: 2008-07-11 12:28:23
import re, logging, sys, urllib2 as u2, kerberos as k

def getLogger():
    log = logging.getLogger('http_kerberos_auth_handler')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


log = getLogger()

class AbstractKerberosAuthHandler:
    """auth handler for urllib2 that does Kerberos HTTP Negotiate Authentication
    """

    def negotiate_value(self, headers):
        """checks for "Negotiate" in proper auth header
        """
        authreq = headers.get(self.auth_header, None)
        if authreq:
            rx = re.compile('(?:.*,)*\\s*Negotiate\\s*([^,]*),?', re.I)
            mo = rx.search(authreq)
            if mo:
                return mo.group(1)
            else:
                log.debug('regex failed on: %s' % authreq)
        else:
            log.debug('%s header not found' % self.auth_header)
        return

    def __init__(self):
        self.retried = 0
        self.context = None
        return

    def generate_request_header(self, req, headers, neg_value):
        self.retried += 1
        log.debug('retry count: %d' % self.retried)
        host = req.get_host()
        log.debug('req.get_host() returned %s' % host)
        (tail, sep, head) = host.rpartition(':')
        domain = tail if tail else head
        (result, self.context) = k.authGSSClientInit('HTTP@%s' % domain)
        if result < 1:
            log.warning('authGSSClientInit returned result %d' % result)
            return
        log.debug('authGSSClientInit() succeeded')
        result = k.authGSSClientStep(self.context, neg_value)
        if result < 0:
            log.warning('authGSSClientStep returned result %d' % result)
            return
        log.debug('authGSSClientStep() succeeded')
        response = k.authGSSClientResponse(self.context)
        log.debug('authGSSClientResponse() succeeded')
        return 'Negotiate %s' % response

    def authenticate_server(self, headers):
        neg_value = self.negotiate_value(headers)
        if neg_value is None:
            log.critical('mutual auth failed. No negotiate header')
            return
        result = k.authGSSClientStep(self.context, neg_value)
        if result < 1:
            log.critical('mutual auth failed: authGSSClientStep returned result %d' % result)
        return

    def clean_context(self):
        if self.context is not None:
            log.debug('cleaning context')
            k.authGSSClientClean(self.context)
            self.context = None
        return

    def http_error_auth_reqed(self, host, req, headers):
        neg_value = self.negotiate_value(headers)
        if neg_value is not None:
            if not self.retried > 0:
                return self.retry_http_kerberos_auth(req, headers, neg_value)
            else:
                return
        else:
            self.retried = 0
        return

    def retry_http_kerberos_auth(self, req, headers, neg_value):
        try:
            try:
                neg_hdr = self.generate_request_header(req, headers, neg_value)
                if neg_hdr is None:
                    log.debug('neg_hdr was None')
                    return
                req.add_unredirected_header(self.authz_header, neg_hdr)
                resp = self.parent.open(req)
                self.authenticate_server(resp.info())
                return resp
            except k.GSSError, e:
                log.critical('GSSAPI Error: %s/%s' % (e[0][0], e[1][0]))
                return

        finally:
            self.clean_context()
            self.retried = 0

        return


class ProxyKerberosAuthHandler(u2.BaseHandler, AbstractKerberosAuthHandler):
    """Kerberos Negotiation handler for HTTP proxy auth
    """
    authz_header = 'Proxy-Authorization'
    auth_header = 'proxy-authenticate'
    handler_order = 480

    def http_error_407(self, req, fp, code, msg, headers):
        log.debug('inside http_error_407')
        host = req.get_host()
        retry = self.http_error_auth_reqed(host, req, headers)
        self.retried = 0
        return retry


class HTTPKerberosAuthHandler(u2.BaseHandler, AbstractKerberosAuthHandler):
    """Kerberos Negotiation handler for HTTP auth
    """
    authz_header = 'Authorization'
    auth_header = 'www-authenticate'
    handler_order = 480

    def http_error_401(self, req, fp, code, msg, headers):
        log.debug('inside http_error_401')
        host = req.get_host()
        retry = self.http_error_auth_reqed(host, req, headers)
        self.retried = 0
        return retry


def test():
    log.setLevel(logging.DEBUG)
    log.info('starting test')
    opener = u2.build_opener()
    opener.add_handler(HTTPKerberosAuthHandler())
    resp = opener.open(sys.argv[1])
    print dir(resp), resp.info(), resp.code


if __name__ == '__main__':
    test()