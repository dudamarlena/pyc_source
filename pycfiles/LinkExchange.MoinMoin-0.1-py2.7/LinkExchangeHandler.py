# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/MoinMoin/action/LinkExchangeHandler.py
# Compiled at: 2011-05-12 16:28:31
from linkexchange.MoinMoin import support
from linkexchange.MoinMoin.support import moin_version

def status_msg(status):
    if status == 404:
        return 'Not found'
    else:
        if status == 200:
            return 'OK'
        return


def execute(pagename, request):
    cfg = request.cfg
    if moin_version < (1, 9):
        uri = request.form.get('uri', ['/'])[0]
    else:
        uri = request.values.get('uri', '/')
    try:
        platform = cfg.linkexchange_platform
    except AttributeError:
        support.configure(cfg)
        platform = cfg.linkexchange_platform

    lx_request = support.convert_request(request)
    lx_request.uri = uri
    lx_response = platform.handle_request(lx_request)
    if moin_version < (1, 6):
        from MoinMoin.util import MoinMoinNoFooter
        request.http_headers([
         'Status: %d %s' % (
          lx_response.status, status_msg(lx_response.status) or '')])
        request.setResponseCode(lx_request.status)
        request.http_headers([ '%s: %s' % (k, v) for k, v in lx_response.headers.items()
                             ])
        request.write(lx_response.body)
        raise MoinMoinNoFooter
    elif moin_version < (1, 9):
        headers = ['Status: %d %s' % (
          lx_response.status, status_msg(lx_response.status) or '')]
        headers.extend([ '%s: %s' % (k, v) for k, v in lx_response.headers.items()
                       ])
        request.emit_http_headers(headers)
        request.write(lx_response.body)
    else:
        request.status_code = lx_response.status
        for k, v in lx_response.headers.items():
            request.headers[k] = v

        request.write(lx_response.body)