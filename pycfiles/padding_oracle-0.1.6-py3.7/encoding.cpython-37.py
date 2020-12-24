# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/padding_oracle/encoding.py
# Compiled at: 2020-03-27 12:18:07
# Size of source mod 2**32: 2019 bytes
"""
Copyright (c) 2020 Yuankui Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import base64, urllib.parse
from typing import Union
__all__ = [
 'base64_encode', 'base64_decode',
 'urlencode', 'urldecode',
 '_to_bytes', '_to_str']

def _to_bytes(data: Union[(str, bytes)]):
    if isinstance(data, str):
        data = data.encode()
    assert isinstance(data, bytes)
    return data


def _to_str(data):
    if isinstance(data, bytes):
        data = data.decode()
    else:
        if isinstance(data, str):
            pass
        else:
            data = str(data)
        return data


def base64_decode(data: Union[(str, bytes)]) -> bytes:
    data = _to_bytes(data)
    return base64.b64decode(data)


def base64_encode(data: Union[(str, bytes)]) -> str:
    data = _to_bytes(data)
    return base64.b64encode(data).decode()


def urlencode(data: Union[(str, bytes)]) -> str:
    data = _to_bytes(data)
    return urllib.parse.quote(data)


def urldecode(data: str) -> bytes:
    data = _to_str(data)
    return urllib.parse.unquote_plus(data)