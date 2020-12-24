# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/in_web/process_inweb_data.py
# Compiled at: 2019-11-14 14:47:00
# Size of source mod 2**32: 1261 bytes
import pandas as pd, sys
df = pd.read_csv('inweb_pairwise_gene_interactions.tsv', sep='\t')
print(df.shape)
rev_df = df[['gene_right', 'gene_left', 'source']]
rev_df.columns = ['gene_left', 'gene_right', 'source']
full_df = pd.concat([df, rev_df], axis=0)
full_df.reset_index(drop=True, inplace=True)
print(full_df.shape)
print(full_df[0:3])
print(full_df[612996:612999])
experim_df = full_df.loc[full_df['source'] == 'experimental interaction detection', :]
agg_experim_df = pd.DataFrame(experim_df.groupby('gene_left')['gene_right'].apply(list))
agg_experim_df.columns = ['interacting_genes']
agg_experim_df.index.name = 'Gene_Name'
agg_experim_df.reset_index(inplace=True)
print(agg_experim_df.head())
print(agg_experim_df.shape)
agg_experim_df.to_csv('experimental_pairwise_interactions.tsv', sep='\t', index=None)
inferred_df = full_df.loc[full_df['source'] == 'inference', :]
agg_inferred_df = pd.DataFrame(inferred_df.groupby('gene_left')['gene_right'].apply(list))
agg_inferred_df.columns = ['interacting_genes']
agg_inferred_df.index.name = 'Gene_Name'
agg_inferred_df.reset_index(inplace=True)
print(agg_inferred_df.shape)
print(agg_inferred_df.head())
agg_inferred_df.to_csv('inferred_pairwise_interactions.tsv', sep='\t', index=None)