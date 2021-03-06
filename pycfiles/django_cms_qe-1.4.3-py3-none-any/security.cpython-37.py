# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/security.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 4415 bytes
"""
Big goal is to have this library secure, so it has by default those main settings
ready:

 * Used HTTPS with HSTS with all subdomains (but no preload).
 * Session cookie is secure and readable by HTTP only.
 * Page can be used in iframe only on the same domain (turn on only because of Django CMS).
 * CSP header to not allow any not trusted content.
 * XSS-protection header to not allow run any script submitted by form.
 * Content-type: nosniff header to not allow run any page or script uploaded as a file.
 * Use CSRF to not allow make dangerous post request outside of the page.
 * :ref:`Save password very securely by latest best algorithm
   <django:auth_password_storage>`.
 * Use password validators to allow at least 8 characters which should not be
   user name, common password or all numeric.
 * Use ``django-axes`` to limit authorization (after 5 attempts is username and IP banned
   for one hour, can be changed by custom configuration).

Tip: when you want to just test page without final configuration, it's good to temporally
disable CSP header in your config (actually - just report but don't block):

.. code-block:: python

    CSP_REPORT_ONLY = True

If your test environment do not run with SSL, then you should turn it off:

.. code-block:: python

    META_SITE_PROTOCOL = 'http'
    SESSION_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

If your website is behind proxy, you have to set Django AXES to properly limit brute-force
authorization by one of those options (more about that in `documentation
<https://django-axes.readthedocs.io/en/latest/configuration.html>`_:

.. code-block:: python

    AXES_REVERSE_PROXY_HEADER = 'header'
    AXES_NUM_PROXIES = 1

"""
from typing import List
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
CSP_DEFAULT_SRC = ("'self'", )
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", '*.googleapis.com',
                  '*.gstatic.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", '*.googleapis.com')
CSP_FONT_SRC = ("'self'", 'data:', 'fonts.gstatic.com')
CSP_IMG_SRC = ("'self'", 'data:', '*.googleapis.com', '*.gstatic.com')
CSP_CONNECT_SRC = ("'self'", '*.django-cms.org', 'raw.githubusercontent.com/divio')
CSP_FRAME_SRC = ("'self'", 'https:')
CSP_REPORT_URI = '/csp-report'
CSRF_FAILURE_VIEW = 'cms_qe.views.errors.handler403'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS = []
CSRF_USE_SESSIONS = True
AUTH_PASSWORD_VALIDATORS = [
 {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator', 
  'OPTIONS':{'min_length': 8}},
 {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
PASSWORD_HASHERS = [
 'django.contrib.auth.hashers.Argon2PasswordHasher',
 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
 'django.contrib.auth.hashers.BCryptPasswordHasher']
AXES_LOGIN_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = 'cms_qe/auth/locked.html'
AXES_DISABLE_ACCESS_LOG = False
AXES_DISABLE_SUCCESS_ACCESS_LOG = True