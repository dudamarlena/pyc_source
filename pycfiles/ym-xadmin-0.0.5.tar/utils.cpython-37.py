# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\utils.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 518 bytes
from django.template.context import RequestContext

def get_context_dict(context):
    """
     Contexts in django version 1.9+ must be dictionaries. As xadmin has a legacy with older versions of django,
    the function helps the transition by converting the [RequestContext] object to the dictionary when necessary.
    :param context: RequestContext
    :return: dict
    """
    if isinstance(context, RequestContext):
        ctx = context.flatten()
    else:
        ctx = context
    return ctx