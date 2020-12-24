# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/sztal/code/python/pybdm/pybdm/ctmdata/__init__.py
# Compiled at: 2019-09-22 08:46:03
# Size of source mod 2**32: 971 bytes
__doc__ = "Resources submodule with reference dataset containing\nprecomputed approximated algorithmic complexity values for\nsimple objects based on *Coding Theorem Method*\n(see :doc:`theory`).\n\nAll datasets' names use the following naming scheme: ``ctm-bX-dY``.\n\nDatasets\n--------\n:``ctm-b2-d12.pkl``:\n    Binary strings of length from 1 to 12.\n:``ctm-b4-d12.pkl``:\n    4-symbols strings of length from 1 to 12.\n:``ctm-b5-d12.pkl``:\n    5-symbols strings of length from 1 to 12.\n:``ctm-b6-d12.pkl``:\n    6-symbols strings of length from 1 to 12.\n:``ctm-b9-d12.pkl``:\n    9-symbols strings of length from 1 to 12.\n:``ctm-b2-d4x4.pkl``:\n    Square binary matrices of width from 1 to 4.\n"
CTM_DATASETS = {'CTM-B2-D12': 'ctm-b2-d12.pkl.gz', 
 'CTM-B4-D12': 'ctm-b4-d12.pkl.gz', 
 'CTM-B5-D12': 'ctm-b5-d12.pkl.gz', 
 'CTM-B6-D12': 'ctm-b6-d12.pkl.gz', 
 'CTM-B9-D12': 'ctm-b9-d12.pkl.gz', 
 'CTM-B2-D4x4': 'ctm-b2-d4x4.pkl.gz'}