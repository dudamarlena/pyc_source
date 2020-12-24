# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/interfaces.py
# Compiled at: 2012-01-12 18:16:00
from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IKannelDataSourceInfo(IBasicDataSourceInfo):
    secure = schema.Boolean(title=_t('Use SSL'))
    password = schema.Password(title=_t('Kannel Admin Password'))
    port = schema.Text(title=_t('Kannel Server Port'))
    timeout = schema.Int(title=_t('Connection Timeout (seconds)'))