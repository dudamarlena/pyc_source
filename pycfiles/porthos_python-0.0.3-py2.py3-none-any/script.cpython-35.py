# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/porthole/script.py
# Compiled at: 2020-03-19 22:11:54
# Size of source mod 2**32: 1977 bytes
import sys, json, argparse
from . import server
from . import client
parser = argparse.ArgumentParser()
subParser = parser.add_subparsers(help='command to run. -h with command shows detailed options.', dest='command')
sP = subParser.add_parser('serve', help='host os info through http server.')
sP.add_argument('-host', dest='host', default='', help='host for service.')
sP.add_argument('-p', '-port', dest='port', default=8000, type=int, help='port for service.')
sP = subParser.add_parser('fetch', help='get os info from destination server.')
sP.add_argument('-d', '-destination', dest='url', help='target uri', required=True)
sP = subParser.add_parser('test', help='test expression with os info given from destination server.')
sP.add_argument('-d', '-destination', dest='url', required=True, help='target uri')
sP.add_argument('-e', '-expression', dest='expr', help='expression string')
sP.add_argument('-s', '-source', dest='src', help='expression source')
args = parser.parse_args()
if args.command == 'serve':
    server.serve(args.host, args.port)
    exit(0)
if args.command == 'fetch':
    print(json.dumps(client.fetch(args.url), indent=4))
    exit(0)
if args.command == 'test':
    if args.expr == None and args.src == None:
        print('Either opts -e (expression) or -s (source) is required.')
        exit(1)
    if args.expr != None and args.src != None:
        print('Only one opts -e (expression) or -s (source) is required.')
        exit(1)
    if args.expr != None:
        exp = args.expr
elif args.src != None:
    try:
        f = open(args.src, 'rb')
        exp = f.read().decode()
        print(exp)
    except Exception as error:
        print('Error reading file : ' + args.src)
        print(error)
        exit(1)

    ok, err = client.test(args.url, exp)
    if not ok:
        print(err)
    exit(not ok)