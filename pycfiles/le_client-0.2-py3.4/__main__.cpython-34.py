# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/__main__.py
# Compiled at: 2016-07-21 15:09:47
# Size of source mod 2**32: 4004 bytes
import argparse, urllib.parse, re, os, os.path, sys
from .request import CertificateRequest
from .keys import ECKeyFile, RemoteKey
from .utils import openssl
from . import get_certificate

def run():
    env_key = os.environ.get('ACME_ACCOUNT_KEY', None)
    prog = sys.argv[0]
    if prog.endswith('__main__.py'):
        prog = 'python -m {}'.format(__package__)
    parser = argparse.ArgumentParser(description='Obtains a TLS certificate', prog=prog)
    parser.add_argument('--key', required=env_key is None, help="A PEM-encoded file with account private key or URL of a Chatelain service. If starts with '@' then it's a path to a one-liner text file that contains such value. Optional if ACME_ACCOUNT_KEY environment variable is present.")
    parser.add_argument('--register', default=False, action='store_true', help='Make sure account key is registered.')
    parser.add_argument('--webroot', required=True, help='A path template with {} in place of domain name')
    parser.add_argument('--no-www', dest='no_www', default=False, action='store_true', help="Strip 'www.' prefix for http-01 webroot path")
    parser.add_argument('--csr', help='CSR file', required=True)
    parser.add_argument('--out', help='Output filename. If not specified, certificate will be written to stdout.')
    parser.add_argument('--only-exp', dest='only_exp', default=None, type=int, metavar='DAYS', help='If output file is specified and already exist, only request a new certificate if output is expiring in a given number of days from now.')
    args = parser.parse_args()
    if args.key is None:
        args.key = env_key
    if args.key.startswith('@'):
        with open(args.key[1:], 'rU') as (f):
            args.key = f.readline().strip()
    if re.match('^https?://', args.key):
        url = urllib.parse.urlsplit(args.key)
        if url.username is not None and url.password is not None:
            credentials = (
             url.username, url.password)
            url = url._replace(netloc=url.netloc.split('@', 1)[1])
        else:
            credentials = None
        url = urllib.parse.urlunsplit(url)
        key = RemoteKey(url, credentials=credentials)
    else:
        key = ECKeyFile(args.key)
    if args.only_exp is not None:
        if os.path.exists(args.out):
            try:
                openssl('x509', '-checkend', str(86400 * args.only_exp), '-noout', '-in', args.out)
                return 3
            except IOError as e:
                pass

    csr = CertificateRequest(args.csr)
    cert = get_certificate(key, csr, args.webroot, register=args.register, no_www=args.no_www)
    if args.out is not None:
        with open(args.out, 'w') as (f):
            f.write(cert)
    else:
        print(cert)
    return 0


if __name__ == '__main__':
    exit(run())