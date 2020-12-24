# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/TSCons.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 1309 bytes
from os import path
from SCons.Builder import Builder
from six.moves import map

def scons_env(env, add=''):
    opath = path.dirname(path.abspath('$TARGET'))
    lstr = 'thrift --gen cpp -o ' + opath + ' ' + add + ' $SOURCE'
    cppbuild = Builder(action=lstr)
    env.Append(BUILDERS={'ThriftCpp': cppbuild})


def gen_cpp(env, dir, file):
    scons_env(env)
    suffixes = ['_types.h', '_types.cpp']
    targets = map(lambda s: 'gen-cpp/' + file + s, suffixes)
    return env.ThriftCpp(targets, dir + file + '.thrift')