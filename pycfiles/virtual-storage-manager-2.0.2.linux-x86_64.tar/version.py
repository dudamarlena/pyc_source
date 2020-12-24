# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/version.py
# Compiled at: 2016-06-13 14:11:03
from vsm.openstack.common import version as common_version
VSM_VENDOR = 'OpenStack Foundation'
VSM_PRODUCT = 'OpenStack Vsm'
VSM_PACKAGE = None
loaded = False
version_info = common_version.VersionInfo('vsm')
version_string = version_info.version_string
release_string = version_info.release_string