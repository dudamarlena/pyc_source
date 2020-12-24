# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/whitlam/home/users/uqdparks/git/unitem/unitem/defaults.py
# Compiled at: 2017-08-18 13:07:59
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
CHECKM_BAC_MS = os.path.join(file_dir, 'checkm_ms', 'bacteria.ms')
CHECKM_AR_MS = os.path.join(file_dir, 'checkm_ms', 'archaea.ms')
CHECKM_BAC_DIR = 'checkm_bac'
CHECKM_AR_DIR = 'checkm_ar'
BINNING_METHOD_DIR = 'binning_methods'
MARKER_GENE_TABLE = 'marker_gene_table.tsv'
GENOME_QUALITY_TABLE = 'genome_quality.tsv'