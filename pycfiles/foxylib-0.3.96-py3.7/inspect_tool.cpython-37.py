# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/native/inspect/inspect_tool.py
# Compiled at: 2020-02-07 17:13:58
# Size of source mod 2**32: 353 bytes
import inspect
from foxylib.tools.collections.collections_tool import l_singleton2obj

class InspectTool:

    @classmethod
    def variable2name(cls, var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        l = [var_name for var_name, var_val in callers_local_vars if var_val is var]
        return l_singleton2obj(l)