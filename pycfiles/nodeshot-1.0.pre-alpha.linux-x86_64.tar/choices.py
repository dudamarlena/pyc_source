# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/services/models/choices.py
# Compiled at: 2014-09-02 11:45:33
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
LOGIN_TYPES = (
 (
  1, _('read-only')),
 (
  2, _('write')))
SERVICE_STATUS = (
 (
  1, _('up')),
 (
  2, _('down')),
 (
  3, _('not reachable')))
APPLICATION_PROTOCOLS = (
 ('http', 'http'),
 ('https', 'https'),
 ('ftp', 'FTP'),
 ('smb', 'Samba'),
 ('afp', 'AFP'),
 ('git', 'Git'))
TRANSPORT_PROTOCOLS = (
 ('tcp', 'TCP'),
 ('udp', 'UDP'))