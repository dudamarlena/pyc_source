# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/adipose_eqtl/process_adipose_eqtl.py
# Compiled at: 2019-11-14 14:46:58
# Size of source mod 2**32: 1121 bytes
import pandas as pd, sys
print('\n> Processing GWAS locus file...')
gwas_df = pd.read_csv('gwas_locus_column.txt', index_col=None, header=None)
gwas_locus_gene_dict = {}
for row in gwas_df.iloc[:, 0]:
    genes = row.split(';')
    for g in genes:
        gwas_locus_gene_dict[g] = gwas_locus_gene_dict.get(g, 0) + 1

print('\n> Processing cis eQTL file...')
cis_eqtl_df = pd.read_csv('cis_eqtl_column.txt', index_col=None, header=None)
cis_eqtl_gene_dict = {}
for gene in cis_eqtl_df.iloc[:, 0]:
    cis_eqtl_gene_dict[gene] = cis_eqtl_gene_dict.get(gene, 0) + 1

tmp_gwas_df = pd.Series(gwas_locus_gene_dict).to_frame('adipose_GWAS_locus')
tmp_eqtl_df = pd.Series(cis_eqtl_gene_dict).to_frame('adipose_cis_eQTL')
print(tmp_eqtl_df.shape)
full_df = pd.merge(tmp_gwas_df, tmp_eqtl_df, left_index=True, right_index=True, how='outer')
full_df.fillna(0, inplace=True)
full_df.reset_index(inplace=True)
full_df.columns.values[0] = 'Gene_Name'
print(full_df.head())
print(full_df.tail())
print(full_df.shape)
full_df.to_csv('adipose_eQTL.csv', index=False)