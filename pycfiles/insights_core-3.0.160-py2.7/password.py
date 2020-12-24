# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/password.py
# Compiled at: 2019-05-16 13:41:33
from .. import parser
from ..parsers.pam import PamDConf
from insights.specs import Specs

@parser(Specs.password_auth)
class PasswordAuthPam(PamDConf):
    """Parsing for `/etc/pam.d/password-auth`. """
    pass