# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/brew/lib/python2.7/site-packages/sentry_notify_github_issues/__init__.py
# Compiled at: 2015-07-07 03:58:51
try:
    VERSION = __import__('pkg_resources').get_distribution('sentry-notify-github-issues').version
except Exception as e:
    VERSION = 'unknown'