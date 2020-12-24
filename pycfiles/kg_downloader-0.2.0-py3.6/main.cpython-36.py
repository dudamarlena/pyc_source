# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kg_downloader\main.py
# Compiled at: 2019-11-25 18:35:39
# Size of source mod 2**32: 736 bytes
from kg_downloader.util import api
from kg_downloader.util import kg_cmder

def main():
    url, loc = kg_cmder.parse_cmd()
    pre_info = api.analyse(url)
    result = []
    if not pre_info:
        print('URL invalid.')
        exit(-1)
    else:
        if pre_info['flag'] in ('personal', 'play'):
            result_set = api.fetch_data(url, pre_info)
            print('[+] Construct metadata successful!')
            if api.confirm(loc, result_set):
                for key, val in result_set.items():
                    result.append(api.download_song(key, val, loc, 1024))

                print('[+] Report:\n%s' % result)
            else:
                api.save_session(result_set)
        else:
            exit(-2)


if __name__ == '__main__':
    main()