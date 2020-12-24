# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\main.py
# Compiled at: 2017-08-17 03:32:58
# Size of source mod 2**32: 1289 bytes
import logging
logging.basicConfig(level=(logging.INFO))
if __name__ == '__main__':
    from zhihu.models.zhihu import Zhihu
    zhihu = Zhihu()
    data = zhihu.send_message('请问怎么发私信呢', user_slug='zhijun-liu')
    print(data.content)