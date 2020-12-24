# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\t\builtins\globalenv.py
# Compiled at: 2011-11-10 02:08:10
from dao.env import GlobalEnvironment
global_env = GlobalEnvironment({})
from dao.base import is_subclass
from dao.term import var

def collocet_builtins_to_module(globls, global_env, module):
    for (name, obj) in globls.items():
        if isinstance(obj, Command):
            try:
                symbol = obj.symbol
            except:
                try:
                    symbol = obj.name
                except:
                    symbol = name

            else:
                v = var(symbol)
                module[v] = obj
                try:
                    is_global = obj.is_global
                except:
                    is_global = False
                else:
                    if is_global:
                        global_env[v] = obj