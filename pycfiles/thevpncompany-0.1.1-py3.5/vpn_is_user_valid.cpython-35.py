# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/vpn_is_user_valid.py
# Compiled at: 2020-01-05 04:32:58
# Size of source mod 2**32: 4187 bytes
"""
Checks if the user is valid to use the VPN according to the central TheVPNCompany database.

The following environment variables customizes the behaviour of the scripts:
 - VPN_API_URL, the URL to the HTTP(S) server that contains the VPN application

 OpenVPN executes this script sending the information about the certificate and the Common Name (cn)
 that has connected. This common name is the user_id of TheVPNCompany, so an API call
 can confirm if the user has permission to access to the VPN services.

"""
import logging, os, sys, re
from .components.vpnapi import TheVPNCompanyClient
__author__ = 'Ruben Rubio Rey'
__version__ = '0.1.0'
__license__ = 'MIT'
log = logging.getLogger(__name__)
VPN_API_URL = os.getenv('VPN_API_URL', 'https://thevpncompany.com.au')
log.debug('VPN API SERVER: %s' % VPN_API_URL)
ENV = os.getenv('ENV', 'dev')
log.debug('Environment ENV: %s' % ENV)
if ENV is None or ENV != 'dev' and ENV != 'prod' and ENV != 'tests':
    log.error("You need to configure the ENV environment variable. Possible values: 'dev' for development and 'prod' for production.")
    exit(1)
if ENV == 'prod' or ENV == 'tests':
    logging.basicConfig(level=logging.WARN)
else:
    logging.basicConfig(level=logging.DEBUG, filename='/tmp/vpn_is_user_valid.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def main():
    """
    depth        -- The current certificate chain depth.  In a typical
                     bi-level chain, the root certificate will be at level
                     1 and the client certificate will be at level 0.
                     This script will be called separately for each level.
    x509         -- the X509 subject string as extracted by OpenVPN from
                    the client's provided certificate.

    Credits:  https://robert.penz.name/21/ovpncncheck-an-openvpn-tls-verify-script/
    """
    log.info('Starting Validation of User')
    depth, x509 = sys.argv[1:]
    log.debug('Input dept: %s' % depth)
    log.debug('Input x509: %s' % x509)
    if int(depth) == 0:
        log.debug('Depth is zero: %s' % depth)
        found = re.compile('CN=([0-9]+)').search(x509)
        log.debug('Found: %s')
        log.debug(found)
        if found:
            cn = found.group(1)
            log.debug('Client common name found: ' + cn)
            if check_user(cn):
                sys.exit(0)
        else:
            log.debug('CN Not found:')
        sys.exit(1)
    sys.exit(0)


def check_user(user_id) -> bool:
    """
        Process the creation of a single server. The request has the following format
        {
            "server_id":1236",          # application server id request
            "supplier_id":1,            # cloud supplier
            "location_code":"tor1",     # location's identifier in the cloud supplier
            "user_id":3                 # user who requested the creation of the server
        }
    """
    log.info('Processing request: %s' % user_id)
    vpn = TheVPNCompanyClient(url=VPN_API_URL, api_key='')
    return vpn.is_user_valid(user_id=str(user_id))


if __name__ == '__main__':
    main()