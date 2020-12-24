# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mdgt\__main__.py
# Compiled at: 2016-10-17 15:19:20
# Size of source mod 2**32: 1796 bytes
import argparse
from .mdgt import consolePrint, jsonPrint, listProvs
from .provider import Provider
from .webserve import serve as webserve
parser = argparse.ArgumentParser()
parser.add_argument('provider', nargs='?', help='Which provider to use (or, the type of object to query).')
parser.add_argument('query', nargs='?', help='The query for the provider to consume.')
parser.add_argument('-p', '--providers', action='store_true', help='List available providers and exit.')
outputGroup = parser.add_mutually_exclusive_group()
outputGroup.add_argument('-c', '--console', action='store_true', help='Output console-formatted text (default).')
outputGroup.add_argument('-j', '--json', action='store_true', help='Output json.')
outputGroup.add_argument('-pd', '--provider-dir', nargs='?', const=None, help='Directory that contains provider files.')
outputGroup.add_argument('-w', '--webserver', nargs='?', const=8181, help='Start as a web server daemon on the                          specified port (default 8181).')
args = parser.parse_args()
if args.providers:
    listProvs()
else:
    if args.webserver:
        webserve(int(args.webserver))
    else:
        if not args.provider and not args.query:
            print('Provider and query required. See --help')
        else:
            if args.json:
                prov = Provider(args.provider, args._provider_dir)
                jsonPrint(prov.scrape(args.query))
            else:
                prov = Provider(args.provider, args.provider_dir)
                consolePrint(prov.scrape(args.query))