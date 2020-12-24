# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/david/Documents/dev/environments/test_sentry/lib/python2.6/site-packages/sentry_redflash/__init__.py
# Compiled at: 2012-06-16 09:13:46
"""
sentry_redflash
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by David Szotten.
:license: MIT, see LICENSE for more details.
"""
try:
    VERSION = __import__('pkg_resources').get_distribution('sentry-redflash').version
except Exception, e:
    VERSION = 'unknown'