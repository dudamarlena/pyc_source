# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/exac-broadinstitute/cnv/process_exac_cnv_table.py
# Compiled at: 2019-11-14 14:46:44
# Size of source mod 2**32: 692 bytes
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 80)
df = pd.read_csv('exac-final-cnv.gene.scores071316', sep=' ')
df.head()
df.drop(['gene', 'chr', 'start', 'end'], axis=1, inplace=True)
df.head()
agg_df = df.groupby('gene_symbol').mean()
agg_df.loc[(agg_df.flag >= 0.5, 'flag')] = 1
agg_df.loc[(agg_df.flag < 0.5, 'flag')] = 0
agg_df.columns = 'ExAC_' + agg_df.columns
agg_df.insert(0, 'Gene_Name', agg_df.index)
agg_df.head()
agg_df.to_csv('ExAC_CNV_features.tsv', sep='\t', index=None)