# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/xc8_symbols.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pymomo.hex8 import symbols

def build_symbols(target, source, env):
    symtab = symbols.XC8SymbolTable(str(source[0]))
    symtab.generate_h_file(str(target[0]))
    symtab.generate_stb_file(str(target[1]))


_build_sym_h = SCons.Builder.Builder(action=build_symbols)

def generate(env):
    env['BUILDERS']['build_symbols'] = _build_sym_h


def exists(env):
    return 1