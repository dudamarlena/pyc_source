# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload_friendly/test.py
# Compiled at: 2016-03-06 10:33:23
import os, json
from functools import wraps
from funkload import FunkLoadTestCase
from .cookie import CookieDict
SECTION_FUNKLOAD_FRIENDLY = 'funkload-friendly'

class TestCase(FunkLoadTestCase.FunkLoadTestCase):
    """funkload-friendly TestCase
    """
    result_directory = '.'
    log_directory = '.'
    session_id_key = 'sessionid'
    site_url = 'http://example.com'

    def __init__(self, methodName='runTest', options=None):
        super(TestCase, self).__init__(methodName, options)
        self.reset_cookie()
        self.session_id_key = self.conf_get(SECTION_FUNKLOAD_FRIENDLY, 'session_id_key', self.__class__.session_id_key, quiet=True)
        self.site_url = self.conf_get('main', 'url', self.__class__.site_url, quiet=True)

    def reset_cookie(self):
        self.cookie = CookieDict()

    def _connect(self, url, params, ok_codes, rtype, description, redirect=False, consumer=None):
        """Override FunkLoadTestCase._connect
        """
        if self.cookie:
            self.setHeader('Cookie', self.cookie.render_to_string())
        response = super(TestCase, self)._connect(url, params, ok_codes, rtype, description, redirect=redirect, consumer=consumer)
        for key, value in response.headers.items():
            if key.lower() == 'set-cookie':
                self.cookie.from_cookie_string(value)

        content_type_header = response.headers.get('content-type')
        if content_type_header:
            if ';' in content_type_header:
                content_type, charset_pair = content_type_header.split(';', 1)
                if '=' in charset_pair:
                    _key, charset = charset_pair.split('=', 1)
                else:
                    charset = None
            else:
                content_type = content_type_header
                charset = None
        else:
            content_type = charset = None
        response.content_type_header = content_type_header
        if content_type:
            response.content_type = content_type.strip()
        else:
            response.content_type = None
        response.charset = charset
        if response.content_type == 'application/json':
            response.data = json.loads(response.body)
        else:
            response.data = None
        return response

    def set_session_id(self, session_id):
        """Set session ID to cookie
        """
        self.cookie[self.session_id_key] = session_id

    def clear_session_id(self):
        """Clear session ID
        """
        return self.cookie.get(self.session_id_key)

    def conf_get(self, section, key, default=FunkLoadTestCase._marker, quiet=False):
        """Override FunkLoadTestCase.conf_get
        """
        if section == self.test_name and key == 'description':
            method = getattr(self, section, None)
            if method and hasattr(method, 'description'):
                return method.description.encode('utf-8')
        if section in ('ftest', 'bench'):
            if section == 'ftest':
                test_name = self.__class__.__name__.lower()
            else:
                test_name = self.test_name
            if key == 'result_path':
                result_directory = super(TestCase, self).conf_get(section, 'result_directory', default=self.result_directory, quiet=quiet)
                result_path = os.path.join(result_directory, ('{}.xml').format(test_name))
                return result_path
            if key == 'log_path':
                log_directory = super(TestCase, self).conf_get(section, 'log_directory', default=self.log_directory, quiet=quiet)
                log_to = os.path.join(log_directory, ('{}.log').format(test_name))
                return log_to
        return super(TestCase, self).conf_get(section, key, default=default, quiet=quiet)


def description(description):
    """Set description to test_method
    """

    def wrapper(func):

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        wrapped.description = description
        return wrapped

    return wrapper