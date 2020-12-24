# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jgsilva/Astrophysics/Packages/ACTIN/actin/actin_files/ac_config.py
# Compiled at: 2019-03-07 02:12:30
# Size of source mod 2**32: 4268 bytes
from __future__ import print_function
from __future__ import division
import os, sys, codecs

def read_conf(config_file, calc_index):
    """
    Reads data from config file and selects the lines needed for the
    selected indices.

    Parameters:
    -----------
    config_file : string
        Name of the configuration file with path.
    calc_index : list of strings
        List of index ids to be calculated selected from the indices provided in the configuration file.

    Returns:
    --------
    sel_lines : dictionary
        Dictionary containing the identification of the indices selected and
        the parameters of the spectral lines required for each index.

        Each key entry is a list of parameters where the list indices form the
        rows related to the same spectral line identified with the key 'ln_id'
        which is related to the spectral index identified by 'ind_id'.

        The returned keys are:

        ==========  ========================================================
        keys            Description
        ----------  --------------------------------------------------------
        ind_id          str : Index identification.
        ind_var         str : Variable assigned to a given line to be used in
                                the index equation. Ex: 'L1', 'L2', etc, for the core
                                lines, and 'R1', 'R2', etc, for reference lines.
        ln_id           str : Spectral line identification.
        ln_c            float : Constant to be multilied to the flux of the line.
        ln_ctr          float : Wavelength of the line centre [angstroms].
        ln_win          float : Bandpass around the line centre to be used in
                                the flux integration [angstroms].
        bandtype    str : Type of bandpass used to integrate flux.
        ==========  ========================================================
    """
    print()
    print('LOADING DATA FROM CONFIG FILE')
    print('-----------------------------')
    try:
        f = codecs.open(config_file, 'r', encoding='utf-8')
    except FileNotFoundError as fnf_err:
        try:
            print('*** ERROR: Config file not found:')
            print(fnf_err)
            print('***', config_file)
            sys.exit()
        finally:
            fnf_err = None
            del fnf_err

    except TypeError as ty_err:
        try:
            print("*** ERROR: Config file is not 'str'")
            print('***', ty_err)
            sys.exit()
        finally:
            ty_err = None
            del ty_err

    for line in f:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            break
        else:
            header = line

    columns = []
    for line in f:
        if not line.strip():
            continue
        line = line.strip()
        column = line.replace('\t\t', '\t')
        column = line.split()
        columns.append(column)

    f.close()
    lines = {}
    keys = header.split()
    for k in range(len(keys)):
        lines[keys[k]] = []
        for i in range(len(columns)):
            lines[keys[k]].append(columns[i][k])

    for k in range(len(lines)):
        for i, x in enumerate(lines[keys[k]]):
            try:
                lines[keys[k]][i] = float(x)
            except ValueError:
                pass

    sel_ind = calc_index
    for k in range(len(sel_ind)):
        if sel_ind[k] not in lines['ind_id']:
            sys.exit('*** ERROR: Index {} is not in the config file.'.format(sel_ind[k]))

    sel_lines = {}
    for i in range(len(keys)):
        sel_lines[keys[i]] = []

    rows = len(lines['ind_id'])
    for k in range(rows):
        if lines['ind_id'][k] in sel_ind:
            print(lines['ln_id'][k])
            for i in range(len(keys)):
                sel_lines[keys[i]].append(lines[keys[i]][k])

    return sel_lines