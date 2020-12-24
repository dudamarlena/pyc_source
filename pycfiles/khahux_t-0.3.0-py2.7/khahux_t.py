# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bin/khahux_t.py
# Compiled at: 2019-11-11 05:20:29
from __future__ import print_function
import json, sys
try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

URL = 'http://fanyi.youdao.com/openapi.do'
KEY = 1132608537
KEYFROM = 'khahux'
CODE_MSG_MAP = {20: '要翻译的文本过长', 
   30: '无法进行有效的翻译', 
   40: '不支持的语言类型', 
   50: '无效的key', 
   60: '无词典结果，仅在获取词典结果生效'}

def get_translate(q):
    url = URL
    param = {'keyfrom': KEYFROM, 
       'key': KEY, 
       'type': 'data', 
       'doctype': 'json', 
       'version': '1.1', 
       'q': q}
    url += '?' + urlencode(param)
    req = Request(url)
    res = urlopen(req)
    return json.loads(res.read().decode('utf-8'))


def show_json(json_data):
    error_code = json_data.get('errorCode')
    if error_code != 0:
        return print(('\n    [\x1b[1;32;40m{}\x1b[0m]{}\n        ').format(error_code, CODE_MSG_MAP.get(error_code)))
    else:
        query = json_data.get('query')
        translations = json_data.get('translation')
        print()
        print(('    [{}]: \x1b[1;32;40m{}\x1b[0m').format(query, ('\x1b[1;31;40m; \x1b[0m').join(translations)))
        basic = json_data.get('basic')
        if basic and isinstance(basic, dict):
            phonetic = basic.get('phonetic', None)
            uk = basic.get('uk-phonetic', None)
            us = basic.get('us-phonetic', None)
            explains = basic.get('explains', [])
            print(('    [phonetic]{}; [us]\x1b[1;32;40m{}\x1b[0m; [uk]{}').format(phonetic, uk, us))
            print()
            print('    ' + ('\x1b[1;31;40m; \x1b[0m').join(explains))
            print()
        web = json_data.get('web')
        if web and isinstance(web, list):
            for item in web:
                print(('    {0}: {1}').format(item['key'], ('\x1b[1;31;40m; \x1b[0m').join(item['value'])))

        print()
        return


def main():
    if not len(sys.argv) > 1 or len(sys.argv) == 2 and sys.argv[1] == '--help':
        return print('\n    Usage:\n    \x1b[1;32;40mkhahux_t\x1b[0m <word>\n        ')
    q = (' ').join(sys.argv[1:])
    json_data = get_translate(q)
    show_json(json_data)


if __name__ == '__main__':
    main()