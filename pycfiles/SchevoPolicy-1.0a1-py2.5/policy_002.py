# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/test/test_policy/policy_002.py
# Compiled at: 2008-01-19 12:32:25
from schevopolicy.schema import *
schevopolicy.schema.prep(locals())
default = ALLOW

@allow_t.when("extent is db.Foo and t_name == 'create'")
def allow_t(db, context, extent, entity, t_name):
    return False