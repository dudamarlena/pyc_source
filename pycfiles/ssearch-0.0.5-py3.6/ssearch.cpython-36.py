# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ssearch/ssearch.py
# Compiled at: 2019-03-07 09:59:19
# Size of source mod 2**32: 2777 bytes
import sys
from hashlib import md5
import requests, uuid, argparse, re

class Language:
    ch = '中文'


class Bcolors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def fm(s):
    """
    clear rich text
    :param s:
    :return:
    """
    return re.sub('<.*?>', '', s)


def search(text):
    print('{}using sougou translate search [{}] ...{}'.format(Bcolors.HEADER, text, Bcolors.ENDC))
    url = 'https://fanyi.sogou.com/reventondc/translate'
    _from = 'auto'
    to = 'zh-CHS'
    s = md5('{}{}{}{}'.format(_from, to, text, 'b33bf8c58706155663d1ad5dba4192dc').encode()).hexdigest()
    param = {'from':_from,  'to':to, 
     'client':'pc', 
     'fr':'browser_pc', 
     'text':text, 
     'useDetect':'on', 
     'useDetectResult':'on', 
     'needQc':1, 
     'uuid':str(uuid.uuid4()), 
     'oxford':'on', 
     'isReturnSugg':'on', 
     's':s}
    resp = requests.post(url=url, data=param).json()
    detect = resp.get('detect', {}).get('language')
    sys.stdout.write('\x1b[F')
    sys.stdout.write('\x1b[K')
    print(Bcolors.OKGREEN)
    print('{0: >10} : {1}'.format('text', resp.get('translate', {}).get('text')))
    print('{0: >10} : {1}'.format('dit', resp.get('translate', {}).get('dit')))
    d = resp.get('dictionary')
    if d:
        for item in d['content']:
            phonetic = item.get('phonetic', [])
            if isinstance(phonetic, list):
                for p in phonetic:
                    print('{0: >10} : {1}'.format(p['type'], p['text']))

            for u in item.get('usual', []):
                print('{0: >10} : {1}'.format(u['pos'], fm(' '.join(u['values']))))

    if detect == Language.ch:
        if d:
            for item in d['content']:
                cat = item.get('category', [])
                for c in cat:
                    for sense in c['sense']:
                        print('{:>10} : {}'.format('sense', sense['description']))

    print('')


def main():
    parser = argparse.ArgumentParser(description='search tool')
    parser.add_argument('text', nargs='?', help='search content')
    parser.add_argument('-e', nargs='+', help='search engineer')
    args = parser.parse_args()
    if args.text:
        search(args.text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()