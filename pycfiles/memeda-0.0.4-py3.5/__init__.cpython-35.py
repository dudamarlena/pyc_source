# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\memeda\__init__.py
# Compiled at: 2017-08-28 03:34:37
# Size of source mod 2**32: 306 bytes
from urllib.request import urlretrieve

def memeda():
    print('么么哒！(づ￣ 3￣)づ')


def dl(url):
    try:
        urlretrieve(url, url.split('/')[(-1)])
        print('{}下载完成！'.format(url))
    except:
        print('地址错误')