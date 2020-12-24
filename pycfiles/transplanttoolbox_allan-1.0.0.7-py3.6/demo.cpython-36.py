# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/transplanttoolbox_allan/demo.py
# Compiled at: 2018-04-04 17:12:13
# Size of source mod 2**32: 2186 bytes
from __future__ import division, print_function, absolute_import
import argparse, sys, logging
from pkgutil import get_data
import os, re, requests, operator, glob
__author__ = 'Gragert Lab'
__copyright__ = 'Gragert Lab'
__license__ = 'gpl3'
allele_to_ag_dict = {}
population_allele_frequencies = {}
allele_frequencies = {}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNOS_conversion_table_filename = os.path.join(BASE_DIR, 'transplanttoolbox_allan/UNOS_conversion_table_with_rules.csv')
UNOS_conversion_table_file = open(UNOS_conversion_table_filename, 'r')
race_list = [
 'AAFA', 'AFA', 'CAU', 'HIS', 'NAM', 'AFB', 'AINDI', 'API',
 'AISC', 'ALANAM', 'AMIND', 'CARB', 'CARHIS', 'CARIBI',
 'EURCAU', 'FILII', 'HAWI', 'JAPI', 'KORI', 'MENAFC', 'MSWHIS', 'NCHI', 'SCAHIS', 'SCAMB', 'SCSEAI', 'VIET']
for pop in race_list:
    file = BASE_DIR + '/transplanttoolbox_allan/freqs_6loc/' + pop + '.ARS.freqs'
    freq_file = open(file, 'r')
    for line in freq_file:
        if line.startswith('Haplo'):
            continue
        else:
            line_split = line.split(',')
            allele_list = line_split[0]
            count = line_split[1]
            haplotype_frequency = line_split[2]
            allele_split = allele_list.split('~')
            for allele in allele_split:
                allele = allele.rstrip('g')
                key = pop + '%' + allele
                if key in population_allele_frequencies:
                    population_allele_frequencies[key] += float(haplotype_frequency)
                else:
                    population_allele_frequencies[key] = float(haplotype_frequency)