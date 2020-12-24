# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/kd100/kd100.py
# Compiled at: 2019-04-03 13:23:52
from __future__ import print_function, unicode_literals
try:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode

import os, json, random, argparse
GUESS = b'http://m.kuaidi100.com/autonumber/auto?{0}'
QUERY = b'http://m.kuaidi100.com/query?{0}'
FAKE_UA = b'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

def format_info(data):
    res = (b'code: {nu: <20} company: {com: <15} is checked: {ischeck}\n').format(**data)
    res += b'=' * 65 + b'\n'
    res += (b'{0: ^21}|{1: ^44}\n').format(b'time', b'content')
    for item in data[b'data']:
        res += b'-' * 65 + b'\n'
        res += (b'{time: ^21}| {context}\n').format(**item)

    res += b'=' * 65 + b'\n'
    return res


def kd100_query(code, output=None, quite=False, company=None):
    params = urlencode({b'num': code})
    guess_url = GUESS.format(params)
    if company is None:
        res = json.loads(urlopen(guess_url).read().decode(b'utf-8'))
        possible_company_name = [ company[b'comCode'] for company in res ]
    else:
        possible_company_name = [
         str(company)]
    if not quite:
        print(b'Possible company:', (b', ').join(possible_company_name))
    for company_name in possible_company_name:
        if not quite:
            print(b'Try', company_name, b'...', end=b'')
        params = urlencode({b'type': company_name, 
           b'postid': code, 
           b'id': 1, 
           b'valicode': b'', 
           b'temp': random.random()})
        req = Request(QUERY.format(params), headers={b'Referer': guess_url, 
           b'User-Agent': FAKE_UA})
        res = json.loads(urlopen(req).read().decode(b'utf-8'))
        if res[b'message'] == b'ok':
            if not quite:
                print(b'Done.\n')
            table = format_info(res)
            if output:
                with open(output, b'wb') as (f):
                    f.write(table.encode(b'utf-8'))
                if not quite:
                    print(b'Result saved to [' + os.path.abspath(output) + b'].')
            else:
                print(table)
            break
        elif not quite:
            print(b'Failed.')
    else:
        print(b'\nNo result.')

    return


def main():
    parser = argparse.ArgumentParser(description=b'query express info use kuaidi100 api')
    parser.add_argument(b'-c', b'--code', type=str, help=b'express code')
    parser.add_argument(b'-p', b'--company', type=str, default=None, help=b'express company, will auto guess company if not provided')
    parser.add_argument(b'-o', b'--output', help=b'output file')
    parser.add_argument(b'-q', b'--quite', help=b'be quite', action=b'store_true', default=False)
    args = parser.parse_args()
    express_code = args.code
    if express_code is None:
        while True:
            try:
                express_code = input(b'Input your express code: ' if not args.quite else b'')
                break
            except ValueError:
                if not args.quite:
                    print(b'Please input a number')

    kd100_query(express_code, args.output, args.quite, args.company)
    return


if __name__ == b'__main__':
    main()