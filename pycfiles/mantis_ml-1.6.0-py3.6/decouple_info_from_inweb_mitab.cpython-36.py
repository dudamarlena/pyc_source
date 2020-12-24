# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/in_web/decouple_info_from_inweb_mitab.py
# Compiled at: 2019-11-14 14:47:00
# Size of source mod 2**32: 718 bytes
import pandas as pd, re, sys
input_file = 'InBio_Map_core_2016_09_12/core.psimitab'
df = pd.read_csv(input_file, sep='\t', header=None)
df.dropna(subset=[4], inplace=True)
df.dropna(subset=[5], inplace=True)
cols_of_interest = [
 4, 5, 6]
df = df[cols_of_interest]
df['gene_left'] = [v[1] for v in df[4].str.split(':|\\(', 0).tolist()]
df['gene_right'] = [v[1] for v in df[5].str.split(':|\\(', 0).tolist()]
df['source'] = [v[1] for v in df[6].str.split('\\(|\\)', 0).tolist()]
print(df.head())
df = df[['gene_left', 'gene_right', 'source']]
df.to_csv('inweb_pairwise_gene_interactions.tsv', sep='\t', index=None)