# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/human_protein_atlas/collapse_rna_expression.py
# Compiled at: 2019-11-14 14:46:56
# Size of source mod 2**32: 711 bytes
from sys import argv, exit
import pandas as pd
input_file = argv[1]
df = pd.read_csv(input_file, sep='\t')
print(df.head())
target_col = 'ProteinAtlas_RNA_expression_TMP'
dupl_genes = [
 'ARL14EPL', 'BTBD8', 'C2orf61', 'COG8', 'HIST1H3D', 'LYNX1', 'MATR3', 'PRSS50', 'RABGEF1', 'SCO2', 'SDHD', 'TXNRD3NB']
print(df.loc[df.Gene_Name.isin(dupl_genes)])
df = df.groupby('Gene_Name').sum()
df['Gene_Name'] = df.index.copy()
df = df[['Gene_Name', target_col]]
print(df.loc[df.Gene_Name.isin(dupl_genes)])
out_file = input_file.replace('.tmp', '')
df.to_csv(out_file, sep='\t', index=None)