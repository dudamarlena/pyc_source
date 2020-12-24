# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/s3iotools-project/s3iotools/tests/io_dataframe.py
# Compiled at: 2019-05-19 22:48:53
import os, pandas as pd
df_customers = pd.read_csv(os.path.join(os.path.dirname(__file__), 'customers.tsv'), sep='\t', encoding='utf8')