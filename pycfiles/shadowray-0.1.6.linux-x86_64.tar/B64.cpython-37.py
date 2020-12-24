# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/common/B64.py
# Compiled at: 2019-06-22 10:44:10
# Size of source mod 2**32: 243 bytes
import base64

def decode(text):
    n = len(text)
    missing_padding = 4 - n % 4
    if missing_padding:
        text += '=' * missing_padding
    text = bytes(text, encoding='utf8')
    return str((base64.b64decode(text)), encoding='utf8')