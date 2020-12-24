# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/gtex/RNASeq/process_gtex_rnaseq_data.py
# Compiled at: 2019-11-14 14:46:56
# Size of source mod 2**32: 1681 bytes
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 150)
disease_search_term = 'Kidney'
hgnc_genes_series = pd.read_csv('../../exac-broadinstitute/all_hgnc_genes.txt', header=None).loc[:, 0]
full_df = pd.read_csv('GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_median_tpm.gct', sep='\t')
full_df.head()
full_df.shape
disease_cols = [c for c in full_df.columns if disease_search_term in c]
disease_cols
df = full_df[(['Gene_Name', 'gene_id'] + disease_cols)]
df.head()
df.Gene_Name.unique().shape
df.loc[(df.Gene_Name == 'PKD2')]
agg_df = df.groupby('Gene_Name').agg('sum')
agg_df.head()
agg_df.shape
total_tissue_expr = 'GTEx_' + disease_search_term + '_TPM_expression'
sum_df = pd.DataFrame(agg_df.sum(axis=1))
sum_df.columns = [total_tissue_expr]
sum_df = sum_df.reindex(hgnc_genes_series)
sum_df.fillna(0, inplace=True)
sum_df.sort_values(by=total_tissue_expr, inplace=True)
sum_df.reset_index(inplace=True)
sum_df.columns.values[0] = 'Gene_Name'
sum_df.head()
print('Median:', sum_df.median())
sum_df.describe()
tissue_rank = 'GTEx_' + disease_search_term + '_Expression_Rank'
sum_df[tissue_rank] = sum_df.index
sum_df.loc[(sum_df[total_tissue_expr] < int(sum_df[total_tissue_expr].median()), tissue_rank)] = 0
sum_df.describe()
sum_df.tail()
sum_df.to_csv((disease_search_term + '_GTEx_expression_features.tsv'), sep='\t', index=None)