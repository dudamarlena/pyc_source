# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/utils/org_utils.py
# Compiled at: 2017-03-01 08:38:06
import uforgecli_utils
from ussclicore.utils.printer import *

def org_get(api, name, on_error_raise=True):
    try:
        org = None
        if name is None:
            org = api.Orgs('default').Get()
            return org
        orgs = api.Orgs().Getall(None)
        for o in orgs.orgs.org:
            if o.name == name:
                org = o

    except Exception, e:
        uforgecli_utils.print_uforge_exception(e)

    if org is None and on_error_raise:
        raise Exception('Unable to find organization')
    return org