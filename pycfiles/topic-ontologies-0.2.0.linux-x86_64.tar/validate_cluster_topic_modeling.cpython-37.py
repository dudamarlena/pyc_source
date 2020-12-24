# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/disk1/anaconda3/lib/python3.7/site-packages/topic_modeling/validate_cluster_topic_modeling.py
# Compiled at: 2020-02-24 12:17:43
# Size of source mod 2**32: 435 bytes
import pandas as pd
path_df_cluster_argument_vectors = '/mnt/disk1/topic-ontologies/args-me/argument-vectors-debatepedia-esa-corpus-args-me-cluster.csv'
path_df_local_argument_vectors = '/mnt/disk1/topic-ontologies/args-me/argument-vectors-debatepedia-esa-corpus-args-me-local.csv'
df_cluster = pd.read_pickle(path_df_cluster_argument_vectors)
df_local = pd.read_pickle(path_df_local_argument_vectors)
print(df_cluster)
print(df_local)