# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marketplacecli/utils/org_utils.py
# Compiled at: 2016-06-03 07:47:35
__author__ = 'UShareSoft'
from marketplacecli.exceptions.UForgeException import UForgeException
from marketplacecli.utils import marketplace_utils

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

    except Exception as e:
        marketplace_utils.print_uforge_exception(e)

    if org is None and on_error_raise:
        raise UForgeException('Unable to find organization')
    return org