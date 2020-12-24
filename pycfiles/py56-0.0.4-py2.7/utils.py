# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/py56/utils.py
# Compiled at: 2014-11-04 17:04:59
import base64

class NoAds:
    """
    # 功能:从url得到ID
    """

    @staticmethod
    def getUrlId(url):
        if 'http' not in url:
            id = NoAds.flvDeId(url)
        elif 'v=' in url:
            id = url.strip().split('v=')[1]
            id = id.replace('.html', '')
            id = NoAds.flvDeId(id)
        elif 'v_' in url:
            id = url.strip().split('v_')[1]
            id = id.replace('.html', '')
            id = NoAds.flvDeId(id)
        elif 'vid-' in url:
            id = url.strip().split('vid-')[1]
            id = id.replace('.html', '')
            id = NoAds.flvDeId(id)
        elif '.html' in url:
            id = url.strip().split('/id')[1]
            id = id.replace('.html', '')
        else:
            id = url.strip().split('id=')[1]
            id = id.split('&')
            id = id[0]
        return id

    @staticmethod
    def flvDeId(id):
        if str(id).isdigit():
            return id
        else:
            return int(base64.b64decode(id))