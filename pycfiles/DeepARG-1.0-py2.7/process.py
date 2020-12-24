# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/argdb/process.py
# Compiled at: 2018-12-06 14:22:32
import json, utils
path = '/Users/gustavoarango/Documents/projects/ARGdb/db/'
metadata = json.load(open(path + 'metadata_with_multilabels.json'))
clusters = json.load(open(path + 'CLUSTERS.csv.json'))
alignments = json.load(open(path + 'alignment.tsv.json'))
iden = 90
DB = {}
for cluster in clusters:
    cluster_stats = utils.consensus_type(clusters[cluster], metadata, alignments)
    DB.update(utils.cluster_annotation(cluster_stats, 90, 1e-10, metadata))

vari = 'AnFactor'
from collections import Counter
Counter([ DB[i][vari] for i in DB ])
json.dump(DB, open(path + 'ANNOTATION_FULL2.json', 'w'))