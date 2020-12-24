# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cyberj/src/python/vtenv2.6/lib/python2.6/site-packages/signature/settings.py
# Compiled at: 2011-06-14 07:22:27
"""
From django-pki - Copyright (C) 2010 Daniel Kerwin <django-pki@linuxaddicted.de>

http://github.com/dkerwin/django-pki

This program and entire repository is free software; you can
redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software
Foundation; either version 2 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; If not, see <http://www.gnu.org/licenses/>.
"""
import os
from django.conf import settings
PKI_APP_DIR = os.path.abspath(os.path.dirname(__file__))
PKI_DIR = getattr(settings, 'PKI_DIR', os.path.join(PKI_APP_DIR, 'PKI'))
PKI_OPENSSL_BIN = getattr(settings, 'PKI_OPENSSL_BIN', '/usr/bin/openssl')
PKI_OPENSSL_CONF = getattr(settings, 'PKI_OPENSSL_CONF', os.path.join(PKI_APP_DIR, 'openssl.cnf'))
PKI_OPENSSL_TEMPLATE = getattr(settings, 'PKI_OPENSSL_TEMPLATE', 'pki/openssl.conf.in')
JQUERY_URL = getattr(settings, 'JQUERY_URL', 'pki/jquery-1.3.2.min.js')
PKI_LOG = getattr(settings, 'PKI_LOG', os.path.join(PKI_DIR, 'pki.log'))
PKI_LOGLEVEL = getattr(settings, 'PKI_LOGLEVEL', 'debug')
ADMIN_MEDIA_PREFIX = getattr(settings, 'ADMIN_MEDIA_PREFIX')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
PKI_BASE_URL = getattr(settings, 'PKI_BASE_URL', '')
PKI_SELF_SIGNED_SERIAL = getattr(settings, 'PKI_SELF_SIGNED_SERIAL', 0)
PKI_DEFAULT_COUNTRY = getattr(settings, 'PKI_DEFAULT_COUNTRY', 'DE')