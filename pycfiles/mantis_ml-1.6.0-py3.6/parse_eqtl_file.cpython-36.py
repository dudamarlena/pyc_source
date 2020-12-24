# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mantis_ml/data/exSNP/parse_eqtl_file.py
# Compiled at: 2019-11-14 14:47:09
# Size of source mod 2**32: 640 bytes
from sys import argv, exit
import pandas as pd
input_file = argv[1]
disease = argv[2]
eqtl_hits_per_gene = dict()
cnt = 0
with open(input_file) as (fh):
    for line in fh:
        if cnt == 0:
            cnt += 1
        else:
            line = line.rstrip()
            vals = line.split('\t')
            genes = vals[3].split('/')
            for g in genes:
                eqtl_hits_per_gene[g] = eqtl_hits_per_gene.get(g, 0) + 1

df = pd.DataFrame.from_dict(pd.Series(eqtl_hits_per_gene))
df.reset_index(inplace=True)
df.columns = ['Gene_Name', disease + '_eQTL_hits']
print(df.head())
df.to_csv((disease + '_eQTL_hits.csv'), index=False)