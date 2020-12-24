# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/files/paramlist.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 4210 bytes
COMMON_CSRF_NAMES = ('CSRFName', 'CSRFToken', 'csrf_token', 'anticsrf', '__RequestVerificationToken',
                     'VerificationToken', 'form_build_id', 'nonce', 'authenticity_token',
                     'csrf_param', 'TransientKey', 'csrf', 'AntiCSURF', 'YII_CSRF_TOKEN',
                     'yii_anticsrf', '[_token]', '_csrf_token', 'csrfmiddlewaretoken',
                     'ccm_token', 'XOOPS_TOKEN_REQUEST', '_csrf', 'token', 'auth',
                     'hash', 'secret', 'verify')
COMMON_CSRF_HEADERS = ('CSRF-Token', 'XSRF-Token', 'X-CSRF-Token', 'X-XSRF-Token',
                       'X-CSRF-Header', 'X-XSRF-Header', 'X-CSRF-Protection')
EXCLUSIONS_LIST = ('logout', 'action=out', 'action=logoff', 'action=delete', 'UserLogout',
                   'osCsid', 'action=logout')
TOKEN_ERRORS = ('the required form field', 'token could not', 'invalid token', 'wrong',
                'error', 'not valid', 'please check your request', 'your browser did something unexpected',
                'csrfclearing your cookies', 'tampered token', 'null', 'unacceptable',
                'false', 'void', 'incorrect', 'inoperative', 'faulty', 'absurd',
                'inconsistent', 'not acceptable')