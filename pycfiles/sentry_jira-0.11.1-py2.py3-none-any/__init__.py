# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/getsentry/sentry-jira/sentry_jira/__init__.py
# Compiled at: 2016-06-02 14:44:05
try:
    VERSION = __import__('pkg_resources').get_distribution('sentry-jira').version
except Exception as e:
    VERSION = 'over 9000'