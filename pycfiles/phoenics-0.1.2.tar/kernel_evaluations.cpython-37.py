# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/BayesianNetwork/kernel_evaluations.pyxbld
# Compiled at: 2019-11-24 12:43:13
# Size of source mod 2**32: 358 bytes
__author__ = 'Florian Hase'

def make_ext(modname, pyxfilename):
    from distutils.extension import Extension
    ext = Extension(name=modname,
      sources=[
     pyxfilename])
    return ext


def make_setup_args():
    return dict(script_args=['--verbose'])