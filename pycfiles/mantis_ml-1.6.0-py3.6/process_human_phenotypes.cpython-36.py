# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/HPO/process_human_phenotypes.py
# Compiled at: 2019-11-14 14:46:57
# Size of source mod 2**32: 950 bytes
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 80)
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
all_df = pd.read_csv('ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt', sep='\t')
all_df.head()
all_df.shape
freq_df = pd.read_csv('ALL_SOURCES_FREQUENT_FEATURES_genes_to_phenotype.txt', sep='\t')
freq_df.head()
freq_df.shape
df = freq_df.copy()
df.head()
pattern = re.compile('kidney|[^(ad)]renal|nephro|eGFR|dialysis', re.IGNORECASE)
df = df[df['HPO-Term-Name'].str.contains(pattern)]
df.shape
len(df['entrez-gene-symbol'].unique())
disease_related_df = pd.DataFrame({'Gene_Name':df['entrez-gene-symbol'].unique(),  'known_CKD_gene':1})
disease_related_df.head()
disease_related_df.shape
disease_related_df.to_csv('Known_CKD_genes.tsv', sep='\t', index=None)