# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gpl/software/python/vegas/examples/cfcn_cython.pyxbld
# Compiled at: 2018-01-04 16:41:24
# Size of source mod 2**32: 347 bytes
import numpy as np

def make_ext(modname, pyxfilename):
    from distutils.extension import Extension
    return Extension(name=modname, sources=[
     pyxfilename, 'cfcn.c'],
      libraries=[],
      include_dirs=[
     np.get_include()])


def make_setup_args():
    return dict()