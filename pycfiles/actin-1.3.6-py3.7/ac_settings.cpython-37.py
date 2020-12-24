# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgsilva/Astrophysics/Packages/ACTIN/actin/actin_files/ac_settings.py
# Compiled at: 2019-12-19 06:04:43
# Size of source mod 2**32: 1713 bytes
from __future__ import print_function
from __future__ import division
import numpy as np

def init():
    global err
    global fnames
    global ftypes
    global instr
    global outkeys
    ftypes = {}
    ftypes['1d'] = [
     'S1D',
     's1d',
     'ADP',
     'rdb']
    ftypes['2d'] = [
     'S2D',
     'e2ds']
    ftypes['all'] = ftypes['1d'] + ftypes['2d']
    instr = [
     'HARPS',
     'HARPN',
     'ESPRESSO']
    fnames = {}
    fnames['data'] = 'data.rdb'
    fnames['log_data'] = 'log.txt'
    fnames['lines_data'] = 'lines.txt'
    fnames['ln_plt'] = '.pdf'
    fnames['time_plt'] = 'time.pdf'
    fnames['time_mlty_plt'] = 'time_mlty.pdf'
    outkeys = {}
    outkeys = [
     'obj', 'instr', 'obs_date', 'bjd', 'rv', 'rv_err', 'fwhm', 'fwhm_err', 'cont', 'cont_err', 'bis', 'bis_err', 'ccf_noise', 'median_snr', 'data_flg', 'bv', 'airmass', 'exptime', 'fits_file']
    err = {}
    err['ERROR'] = '*** ERROR:'


def preamble(version_file):
    __author__ = 'Joao Gomes da Silva'
    try:
        with open(version_file, 'r') as (file):
            version = file.read().splitlines()[0]
        print('\nACTIN {}'.format(version))
    except:
        print("*** WARNING | Unable to read 'VERSION' file.")
        version = 'Unknown'

    print('Instituto de Astrofisica e Ciencias do Espaco')
    print('Centro de Astrofisica da Universidade do Porto')
    print('Author:', __author__ + ',', 'Joao.Silva@astro.up.pt')
    return version