# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tgext/subform/config.py
# Compiled at: 2013-01-29 22:57:48
from tgext.admin import AdminConfig
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.subform.controller import SubformController

class TgSubformAdminConfig(TGAdminConfig):
    DefaultControllerConfig = SubformController


class SubformAdminConfig(AdminConfig):
    DefaultControllerConfig = SubformController