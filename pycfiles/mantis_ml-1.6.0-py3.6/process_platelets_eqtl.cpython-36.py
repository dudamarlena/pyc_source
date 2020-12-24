# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/platelets_eqtl/process_platelets_eqtl.py
# Compiled at: 2019-11-14 14:47:05
# Size of source mod 2**32: 402 bytes
import pandas as pd
input_file = '1-s2.0-S0002929716300428-mmc3.csv'
df = pd.read_csv(input_file)
df.eGene = df.eGene.str.replace('*', '')
print(df.head())
grouped_df = pd.DataFrame(df.groupby(by='eGene')['eQTL_pvalue'].count())
grouped_df.reset_index(inplace=True)
grouped_df.columns = ['Gene_Name', 'platelets_eQTL']
print(grouped_df.head())
grouped_df.to_csv('platelets_eQTL.csv', index=None)