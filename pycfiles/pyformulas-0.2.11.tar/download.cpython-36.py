# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Joseph\Anaconda3-new\Lib\site-packages\pyformulas\_formulas\download.py
# Compiled at: 2018-03-18 15:02:56
# Size of source mod 2**32: 1109 bytes


def download(url, out_path=None, get_headers=False, get_body=None):
    from urllib.request import urlopen
    try:
        if all([protocol not in url[:8] for protocol in ('http://', 'https://')]):
            try_url = 'http://' + url
            result = urlopen(try_url)
            if result.getcode() != 200:
                try_url = 'https://' + url
                result = urlopen(try_url)
        else:
            result = urlopen(url)
        _headers, _body = bytes(result.headers), result.read()
    except:
        raise ConnectionError(-1, 'Could not access url', url)

    ret = bytes()
    if get_headers:
        ret += _headers
    else:
        if get_body is None:
            get_body = True
    if get_body:
        ret += _body
    if out_path is not None:
        with open(out_path, 'wb') as (file):
            file.write(ret)
    if len(ret) == 0:
        ret = None
    return ret