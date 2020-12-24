# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/omim/process_edited_genemap2.py
# Compiled at: 2019-11-14 14:47:00
# Size of source mod 2**32: 1201 bytes
import pandas as pd
df = pd.read_csv('genemap2.edited.collapsed.txt', sep='\t')
print(df.head())
print(df.shape)
print('\nAnnotation has AD:')
ad_df = df.loc[df.Annotation.str.contains('AD'), :]
pd.Series(ad_df['Approved_Symbol'].unique()).to_csv('AD_genes.txt', index=False)
print(ad_df.shape)
print('\nAnnotation has AR:')
ar_df = df.loc[df.Annotation.str.contains('AR'), :]
pd.Series(ar_df['Approved_Symbol'].unique()).to_csv('AR_genes.txt', index=False)
print(ar_df.shape)
print('\nAnnotation has AD but not AR:')
ad_only_df = df.loc[df.Annotation.str.contains('AD'), :]
ad_only_df = ad_only_df.loc[~df.Annotation.str.contains('AR'), :]
pd.Series(ad_only_df['Approved_Symbol'].unique()).to_csv('AD_only_genes.txt', index=False)
print(ad_only_df.shape)
print('\nAnnotation has AR but not AD:')
ar_only_df = df.loc[df.Annotation.str.contains('AR'), :]
ar_only_df = ar_only_df.loc[~df.Annotation.str.contains('AD'), :]
pd.Series(ar_only_df['Approved_Symbol'].unique()).to_csv('AR_only_genes.txt', index=False)
print(ar_only_df.shape)