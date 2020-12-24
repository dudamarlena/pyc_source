# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/policy/twitabit_policy_001.py
# Compiled at: 2008-01-19 12:54:35
from schevopolicy.schema import *
schevopolicy.schema.prep(locals())
default = ALLOW

@allow_t.when("entity in db.User and context != entity and t_name == 'change_password'")
def allow_t(db, context, extent, entity, t_name):
    return False


@allow_t.when("entity in db.User and context != entity and t_name == 'change_status'")
def allow_t(db, context, extent, entity, t_name):
    return False