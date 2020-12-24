# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\t\builtins\control.py
# Compiled at: 2011-11-06 20:23:40
from dao.env import ModuleEnvironment
from dao.term import var
from dao.builtin import collocet_builtins_to_module
from dao.t.builtins.globalenv import global_env
from dao.builtins.control import *
control = ModuleEnvironment({}, None)
global_env[var('control')] = control
collocet_builtins_to_module(globals(), global_env, control)