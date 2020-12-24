# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/pyppeteer/pyppeteer/util.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 856 bytes
"""Utility functions."""
import gc, socket
from typing import Dict, Optional
from pyppeteer.chromium_downloader import check_chromium, chromium_executable
from pyppeteer.chromium_downloader import download_chromium
__all__ = [
 'check_chromium',
 'chromium_executable',
 'download_chromium',
 'get_free_port',
 'merge_dict']

def get_free_port() -> int:
    """Get free port."""
    sock = socket.socket()
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    del sock
    gc.collect()
    return port


def merge_dict(dict1: Optional[Dict], dict2: Optional[Dict]) -> Dict:
    """Merge two dictionaries into new one."""
    new_dict = {}
    if dict1:
        new_dict.update(dict1)
    if dict2:
        new_dict.update(dict2)
    return new_dict