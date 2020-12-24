# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ups/defaults.py
# Compiled at: 2014-08-02 22:39:18
from django.utils.translation import ugettext as _
from mezzanine.conf import register_setting
register_setting(name='UPS_CREDENTIALS', description='UPS credentials: username, password, \t\taccess license, shipper number', editable=False)
register_setting(name='UPS_SHIPMENT_ORIGIN', description='Address of the origin of the package', editable=False)