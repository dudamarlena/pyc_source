# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/qrcode_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 1200 bytes
"""
@author = super_fazai
@File    : qrcode_utils.py
@connect : superonesfazai@gmail.com
"""
from requests import get
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
__all__ = [
 'decode_qrcode']

def decode_qrcode(img_url=None, img_path=None, headers=None):
    """
    二维码内容解码
    :param img_url: 二维码地址
    :param img_path: 本地图片路径
    :return:
    """
    if not img_url is not None:
        assert img_path is not None, 'img_url or img_path都为None, 赋值异常!'
    elif img_url is not None:
        decode_result = decode(Image.open(BytesIO(get(url=img_url, headers=headers).content)))
    else:
        if img_path is not None:
            decode_result = decode(Image.open(img_path))
        else:
            raise AssertionError
    return str((decode_result[0].data), encoding='utf-8')