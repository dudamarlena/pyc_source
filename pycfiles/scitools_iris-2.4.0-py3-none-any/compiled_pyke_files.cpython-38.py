# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/home/h05/itwl/projects/git/iris/build/lib/iris/fileformats/_pyke_rules/compiled_krb/compiled_pyke_files.py
# Compiled at: 2019-12-16 04:04:08
# Size of source mod 2**32: 417 bytes
from pyke import target_pkg
pyke_version = '1.1.1'
compiler_version = 1
target_pkg_version = 1
try:
    loader = __loader__
except NameError:
    loader = None
else:

    def get_target_pkg():
        return target_pkg.target_pkg(__name__, __file__, pyke_version, loader, {('', '', 'fc_rules_cf.krb'): [
                                       1576487047.954705, 'fc_rules_cf_fc.py']}, compiler_version)