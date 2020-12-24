# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/pyppeteer/pyppeteer/command.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 385 bytes
"""Commands for Pyppeteer."""
import logging
from pyppeteer.chromium_downloader import check_chromium, download_chromium

def install() -> None:
    """Download chromium if not install."""
    if not check_chromium():
        download_chromium()
    else:
        logging.getLogger(__name__).warning('chromium is already installed.')