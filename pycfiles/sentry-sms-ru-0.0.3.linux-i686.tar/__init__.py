# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/noname/.virtualenvs/sentry/lib/python2.7/site-packages/sentry_sms_ru/__init__.py
# Compiled at: 2013-06-06 03:48:12
try:
    VERSION = __import__('pkg_resources').get_distribution(__name__).version
except Exception as e:
    VERSION = 'Unknown'