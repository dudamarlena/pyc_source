# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smtphealth/main.py
# Compiled at: 2013-09-09 14:59:22
import sys
from optparse import OptionParser
import pkg_resources
from . import SmtpHealthCheck

def main():
    version = pkg_resources.require('smtp-health-check')[0].version
    description = 'Connects to a remote SMTP server, verifying that it responds with a banner code\nthat indicates a healthy system (e.g. 220). Each step of the connection may be\ntimed. The output of this health check shows the results of the check, and the\nlength of time taken by each piece of the operation.\n'
    op = OptionParser(usage='%prog [options] <host>', version=version, description=description)
    op.add_option('-p', '--port', type='int', metavar='NUM', default=25, help='The port to connect to, default %default.')
    op.add_option('-s', '--ssl', action='store_true', default=False, help='Initiate an SSL handshake before getting the banner.')
    op.add_option('-d', '--dns-timeout', type='int', metavar='SEC', default=10, help='The DNS lookup failure timeout, default %default.')
    op.add_option('-c', '--connect-timeout', type='int', metavar='SEC', default=10, help='The connection failure timeout, default %default.')
    op.add_option('-e', '--ssl-timeout', type='int', metavar='SEC', default=10, help='The SSL handshake failure timeout, default %default.')
    op.add_option('-b', '--banner-timeout', type='int', metavar='SEC', default=10, help='The banner failure timeout, default %default.')
    options, extra = op.parse_args()
    if len(extra) < 1:
        op.error('At least one host must be provided.')
    check = SmtpHealthCheck(dns_timeout=options.dns_timeout, connect_timeout=options.connect_timeout, ssl_timeout=options.ssl_timeout, banner_timeout=options.banner_timeout)
    for host in extra:
        check.run(host, options.port, options.ssl)
        return check.output(sys.stdout)