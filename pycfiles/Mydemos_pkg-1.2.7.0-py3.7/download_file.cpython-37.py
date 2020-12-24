# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\download_file.py
# Compiled at: 2020-05-04 22:32:16
# Size of source mod 2**32: 168 bytes


def download(g, n):
    import requests
    f = requests.get(g)
    with open(n, 'wb') as (p):
        for c in r.iter_content(chunk_size=1024):
            p.write(c)