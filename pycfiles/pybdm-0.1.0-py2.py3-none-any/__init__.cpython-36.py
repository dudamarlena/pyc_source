# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sztal/code/python/pybdm/pybdm/ctmdata/__init__.py
# Compiled at: 2019-09-22 08:46:03
# Size of source mod 2**32: 971 bytes
"""Resources submodule with reference dataset containing
precomputed approximated algorithmic complexity values for
simple objects based on *Coding Theorem Method*
(see :doc:`theory`).

All datasets' names use the following naming scheme: ``ctm-bX-dY``.

Datasets
--------
:``ctm-b2-d12.pkl``:
    Binary strings of length from 1 to 12.
:``ctm-b4-d12.pkl``:
    4-symbols strings of length from 1 to 12.
:``ctm-b5-d12.pkl``:
    5-symbols strings of length from 1 to 12.
:``ctm-b6-d12.pkl``:
    6-symbols strings of length from 1 to 12.
:``ctm-b9-d12.pkl``:
    9-symbols strings of length from 1 to 12.
:``ctm-b2-d4x4.pkl``:
    Square binary matrices of width from 1 to 4.
"""
CTM_DATASETS = {'CTM-B2-D12':'ctm-b2-d12.pkl.gz', 
 'CTM-B4-D12':'ctm-b4-d12.pkl.gz', 
 'CTM-B5-D12':'ctm-b5-d12.pkl.gz', 
 'CTM-B6-D12':'ctm-b6-d12.pkl.gz', 
 'CTM-B9-D12':'ctm-b9-d12.pkl.gz', 
 'CTM-B2-D4x4':'ctm-b2-d4x4.pkl.gz'}