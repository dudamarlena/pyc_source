# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/create_test_files.py
# Compiled at: 2018-12-13 08:22:07
from tests.utils import create_and_write_both_type_of_functions
from tests.materials import Nickel, Argon

def create_nickel():
    ni = Nickel()
    create_and_write_both_type_of_functions(ni.lammps_gr_filename, ni.real_space_filename, ni.reciprocal_space_filename, **ni.kwargs)


def create_argon():
    ar = Argon()
    create_and_write_both_type_of_functions(ar.lammps_gr_filename, ar.real_space_filename, ar.reciprocal_space_filename, **ar.kwargs)


if __name__ == '__main__':
    create_nickel()
    create_argon()