# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mete/beta_lookuptable_builder.py
# Compiled at: 2013-10-23 21:36:48
"""Grow the beta lookup table

Command line usage:
Call the following command from the directory with the pickled lookup table
python beta_dictionary_builder.py S_min S_max N_min N_max

"""
import mete, sys
if __name__ == '__main__':
    S_min = int(sys.argv[1])
    S_max = int(sys.argv[2])
    N_min = int(sys.argv[3])
    N_max = int(sys.argv[4])
    mete.build_beta_dict(S_min, S_max, N_max, N_min=N_min)