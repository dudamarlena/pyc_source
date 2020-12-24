# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: filepath.py
# Compiled at: 2018-06-01 20:07:45
"""
Created on Tue May 29 16:51:23 2018

@author: whe3
"""
import os, json
RequiredFilePath = '/Work_progress/FunctionRegion_Crispr/Test/RequiredFiles'
OutputDir = '/Work_progress/FunctionRegion_Crispr/Test/Output'
Inputfile = os.path.join(RequiredFilePath, 'DataSet_V2.csv')
Datafile = os.path.join(RequiredFilePath, 'DomainScreenDataset.csv')
excelfile = os.path.join(RequiredFilePath, 'score2.xlsx')
domain_file = os.path.join(RequiredFilePath, 'pfam_genomic_position.txt')
exons_dic_file = os.path.join(RequiredFilePath, 'exons_dict')
ac_file = os.path.join(RequiredFilePath, 'Acetylation_site.txt')
me_file = os.path.join(RequiredFilePath, 'Methylation_site.txt')
po_file = os.path.join(RequiredFilePath, 'Phosphorylation_site.txt')
ub_file = os.path.join(RequiredFilePath, 'Ubiquitination_site.txt')
exons_dic = json.loads(open(exons_dic_file).read())
cell_list = [
 'NCI.H1299', 'RKO', 'DLD1']
size_list = ['10', '20', '30', '40', '50']