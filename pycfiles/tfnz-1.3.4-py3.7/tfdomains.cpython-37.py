# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfdomains.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 3126 bytes
import sys
from tfnz.cli import generic_cli, base_argparse

def main():
    parser = base_argparse('tfdomains')
    subparsers = parser.add_subparsers(title='commands', dest='command')
    p_list = subparsers.add_parser('list', help='list domains')
    p_token = subparsers.add_parser('prepare', help='receive a pre-claim token')
    p_token.add_argument('prepare_domain', metavar='my.com')
    p_create = subparsers.add_parser('claim', help='claim a domain')
    p_create.add_argument('claim_domain', metavar='my.com')
    p_global = subparsers.add_parser('global', help='make a domain global')
    p_global.add_argument('global_domain', metavar='my.com')
    p_private = subparsers.add_parser('private', help='make a domain private')
    p_private.add_argument('private_domain', metavar='my.com')
    p_release = subparsers.add_parser('release', help='release your claim')
    p_release.add_argument('release_domain', metavar='my.com')
    generic_cli(parser, {'list':list_dom,  'prepare':prepare,  'claim':claim,  'private':private, 
     'global':gbl,  'release':release})


def list_dom(location, args):
    for dom in location.endpoints.values():
        print(dom.domain)


def prepare(location, args):
    rtn = location.conn.send_blocking_cmd(b'prepare_domain', {'domain': args.prepare_domain})
    print('Put a DNS record on your domain: tf-token.%s, TXT=%s' % (
     args.prepare_domain, rtn.params['token'].decode()))
    print('...then run: tfdomains claim ' + args.prepare_domain)
    print('The request will time out (and become invalid) after six hours.')


def claim(location, args):
    location.conn.send_blocking_cmd(b'claim_domain', {'domain': args.claim_domain})
    print('Claimed successfully - you can remove the tf-token record from DNS')


def gbl(location, args):
    location.conn.send_blocking_cmd(b'make_domain_global', {'domain': args.global_domain})
    print('Domain made global, clients will need to re-attach to see the change')


def private(location, args):
    location.conn.send_blocking_cmd(b'make_domain_private', {'domain': args.private_domain})
    print('Domain made private, clients will need to re-attach to see the change but can no longer publish.')


def release(location, args):
    location.conn.send_blocking_cmd(b'release_domain', {'domain': args.release_domain})
    print('Released domain')


if __name__ == '__main__':
    main()