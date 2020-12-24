# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\dinpy\_util.py
# Compiled at: 2011-10-22 22:09:08


def _import_builtins():
    from dao import builtin
    from dao.builtins.matcher import Matcher
    from dao.dinpy.dexpr import _BuiltinSymbol
    globls = globals()
    for name in globls:
        obj = globls[name]
        if not isinstance(obj, builtin.Builtin):
            del globls[name]
        if isinstance(obj, Matcher):
            continue
        else:
            globls[name] = _BuiltinSymbol(obj)


_import_builtins()