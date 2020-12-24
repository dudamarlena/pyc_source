# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ipfspinsteem/__init__.py
# Compiled at: 2018-04-27 18:18:46
# Size of source mod 2**32: 3127 bytes
import argparse, ipfspinsteem.strings as s
from ipfspinsteem.ipfspinsteem2 import Steem, Parser, IPFS
import ipfsapi
parser = argparse.ArgumentParser(description='Extracts IPFS Hashes to Dtube/Dsound, creates an IPFS Object and pins it to an IPFS node.')
parser.add_argument('url', type=str, nargs='+', help='Dtube Video-Url. Example: account/permlink')
parser.add_argument('--api', dest='api', default='127.0.0.1', help='IPFS API IP. Default:127.0.0.1')
parser.add_argument('--port', dest='port', type=int, default=5001, help='API Port. Default:5001')
parser.add_argument('--exclude', dest='exclude', nargs='+', help='Exclude something. Example: videohash')
parser.add_argument('--object', dest='object', action='store_true', help='Will wrap all hashes to a single IPFS Object.')
parser.add_argument('--no-pin', dest='nopin', action='store_true', help='Will not pin anything to IPFS')
parser.add_argument('--quiet', dest='quiet', action='store_true', help='Will only print hash(es) and nothing else when successfully finnished.')
args = parser.parse_args()

def main():
    """
        Connect to IPFS and Steem api.
        """
    ipfs = IPFS(args.api, args.port)
    steem = Steem(steemd_nodes=None)
    try:
        parser = Parser()
        info = parser.parseURL(urls=(args.url))
    except ValueError:
        print('Invalid URL. Aborted')
        exit(0)

    try:
        hashes = steem.getHashesByContentList(info)
    except SyntaxError:
        print('SyntaxError. Probablly unavailable user and/or permlink. Aborted')
        exit(0)
    except KeyboardInterrupt:
        print('Interrupted by user')

    if hashes is None:
        print('No hashes found')
        exit(0)
    opts = {s.donotadd: args.exclude}
    hashes = Steem.removeInvalid(hashes, opts)
    liste = []
    for h in hashes:
        for e in h[s.permlinks]:
            for q in e:
                for p in q[s.links]:
                    if args.quiet == False:
                        print('extracted', h[s.user], '/', q[s.permlink], '/', p[s.Name], '/', p[s.Hash])
                    if args.object == False:
                        liste.append(p[s.Hash])

    if args.object == True:
        try:
            obj = (
             ipfs.createNewSingleObject(hashes),)
        except KeyboardInterrupt:
            print('interrupted by user')
            exit(0)

        liste.append(obj[0])
        if args.quiet == False:
            print('created object', obj[0])
    if args.nopin == False:
        try:
            ipfs.pin(liste)
            if args.quiet == False:
                for i in liste:
                    print('pinned', i, 'recursively')

            else:
                for i in liste:
                    print(i)

        except ipfsapi.exceptions.DecodingError as e:
            print('pinning failed')
            print(e)
        except KeyboardInterrupt:
            print('Pinning Interrupted by user')

    if args.object == True:
        if args.quiet == True:
            print(liste[0])