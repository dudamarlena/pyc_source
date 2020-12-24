# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyppeteer/pyppeteer/errors.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 717 bytes
"""Exceptions for pyppeteer package."""
import asyncio

class PyppeteerError(Exception):
    __doc__ = 'Base exception for pyppeteer.'


class BrowserError(PyppeteerError):
    __doc__ = 'Exception raised from browser.'


class ElementHandleError(PyppeteerError):
    __doc__ = 'ElementHandle related exception.'


class NetworkError(PyppeteerError):
    __doc__ = 'Network/Protocol related exception.'


class PageError(PyppeteerError):
    __doc__ = 'Page/Frame related exception.'


class TimeoutError(asyncio.TimeoutError):
    __doc__ = 'Timeout Error class.'