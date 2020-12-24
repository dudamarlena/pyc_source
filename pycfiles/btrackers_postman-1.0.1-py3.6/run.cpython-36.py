# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/run.py
# Compiled at: 2017-11-04 03:57:08
# Size of source mod 2**32: 2293 bytes
import argparse, importlib
from argparse import RawTextHelpFormatter
from btp.util import fetcher, postman
trackers = importlib.import_module('btp.util.trackers')
parser = argparse.ArgumentParser(prog='btp',
  formatter_class=RawTextHelpFormatter)
parser.add_argument('jsonrpc_url',
  metavar='jsonrpc_url',
  type=str,
  help='Target aria2 server jsonrpc url')
parser.add_argument('jsonrpc_token',
  metavar='jsonrpc_token',
  type=str,
  help='Target aria2 server jsonrpc token')
parser.add_argument('-i',
  '--index', metavar='index',
  choices=(range(len(trackers.TRACKERS_URL_LIST))),
  type=int,
  default=0,
  help='0 - trackers_best (DEFAULT)\n1 - trackers_all\n2 - trackers_all_udp\n3 - trackers_all_http\n4 - trackers_all_https\n5 - trackers_best_ip\n6 - trackers_all_ip\nMore detail: https://github.com/ngosang/trackerslist\n')
parser.add_argument('-p',
  '--proxy', metavar='proxy',
  type=str,
  help='Request proxy, http proxy or socks proxy likes: \nhttp://user:password@10.1.1.6:8080 or socks5://127.0.0.1:1086')

def main():
    try:
        args = parser.parse_args()
        url = trackers.get_trackers_url(args.index)
        try:
            content = fetcher.get_trackers_content(url, proxy=(args.proxy))
            if content:
                url_list = fetcher.parse_content(content)
                if not url_list:
                    print('Tracker urls empty, more detail: https://github.com/ngosang/trackerslist')
                else:
                    result = postman.push((args.jsonrpc_url), (args.jsonrpc_token), url_list, proxy=(args.proxy))
                    if result:
                        print('Success.')
                    else:
                        print('Failed to post urls to aria2 server.')
            else:
                print('Failed to get tracker urls from github.')
        except Exception as e:
            print('Exception, please try again later:\n    %s' % str(e))

    except:
        pass