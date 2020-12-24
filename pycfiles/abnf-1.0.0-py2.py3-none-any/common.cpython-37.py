# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ctyfoxylos/personal/python/abnamrolib/abnamrolib/common.py
# Compiled at: 2019-12-09 07:15:14
# Size of source mod 2**32: 3882 bytes
__doc__ = '\nMain code for common.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
import logging
from dataclasses import dataclass
from requests import Session
from .abnamrolibexceptions import InvalidCookies
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '09-12-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'common'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

@dataclass
class Cookie:
    """Cookie"""
    domain: str
    flag: bool
    path: str
    secure: bool
    expiry: int
    name: str
    value: str

    def to_dict(self):
        """Returns the cookie as a dictionary.

        Returns:
            cookie (dict): The dictionary with the required values of the cookie

        """
        return {key:getattr(self, key) for key in ('domain', 'name', 'value', 'path')}


class CookieAuthenticator:
    """CookieAuthenticator"""

    def __init__(self, cookie_file):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.session = self._get_authenticated_session(cookie_file)

    def _get_authenticated_session(self, cookie_file):
        session = Session()
        try:
            cfile = open(cookie_file, 'rb')
        except FileNotFoundError:
            message = 'Could not open cookies file, either file does not exist or no read access.'
            raise InvalidCookies(message)

        session = self._load_text_cookies(session, cfile)
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0)Gecko/20100101 Firefox/67.0'})
        return session

    def _load_text_cookies(self, session, cookies_file):
        try:
            text = cookies_file.read().decode('utf-8')
            cookies = [Cookie(*line.strip().split()) for line in text.splitlines() if not line.strip().startswith('#') if line]
            for cookie in cookies:
                (session.cookies.set)(**cookie.to_dict())

        except Exception:
            self._logger.exception('Things broke...')
            message = 'Could not properly load cookie text file.'
            raise InvalidCookies(message)

        return session