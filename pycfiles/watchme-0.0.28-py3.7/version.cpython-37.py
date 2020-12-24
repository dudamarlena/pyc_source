# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/version.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 1134 bytes
__version__ = '0.0.28'
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'watchme'
PACKAGE_URL = 'http://www.github.com/vsoch/watchme'
KEYWORDS = 'web, changes, cron, reproducible, version-control'
DESCRIPTION = 'reproducible monitoring client with exporters'
LICENSE = 'LICENSE'
INSTALL_REQUIRES = (
 (
  'python-crontab', {'min_version': '2.3.6'}),
 (
  'configparser', {'min_version': '3.5.3'}),
 (
  'requests', {'min_version': '2.21.0'}))
INSTALL_URLS_DYNAMIC = (
 (
  'beautifulsoup4', {'min_version': '4.6.0'}),
 (
  'lxml', {'min_version': '4.1.1'}))
INSTALL_PSUTILS = (
 (
  'psutil', {'min_version': '5.4.3'}),)
INSTALL_ALL = INSTALL_REQUIRES + INSTALL_PSUTILS + INSTALL_URLS_DYNAMIC
INSTALL_WATCHERS = INSTALL_REQUIRES + INSTALL_PSUTILS + INSTALL_URLS_DYNAMIC