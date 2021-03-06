# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/annotate_db.py
# Compiled at: 2017-12-07 17:15:59
from __future__ import absolute_import, division, print_function
import logging, re
logger = logging.getLogger('STAR-SEQR')

def get_chimerdb(jxn, chimerdb3):
    chrom1, pos1, str1, chrom2, pos2, str2, repleft, repright = re.split(':', jxn)
    pos1 = int(pos1)
    pos2 = int(pos2)
    maxrep = max(10, int(max(int(repleft), int(repright))))
    chimerdb3.columns = ['c1', 's1', 'e1', 'c2', 's2', 'e2',
     'Fusion', 'Counts', 'strand1', 'strand2',
     'Source', 'Cancer', 'Features']
    subset_df = chimerdb3[((chimerdb3['c1'] == chrom1) & ((chimerdb3['s1'] >= pos1 - maxrep) & (chimerdb3['s1'] <= pos1 + maxrep)) & ((chimerdb3['c2'] == chrom2) & ((chimerdb3['s2'] >= pos2 - maxrep) & (chimerdb3['s2'] <= pos2 + maxrep))))]
    sum_count = ''
    if len(subset_df.index >= 1):
        sum_count = subset_df['Counts'].astype(int).sum()
    return (
     sum_count,
     (',').join(set(subset_df['Source'].astype(str))),
     (',').join(set(subset_df['Cancer'].astype(str))),
     (',').join(set(subset_df['Features'].astype(str))))


def get_fusioncancerdb(jxn, fuca):
    chrom1, pos1, str1, chrom2, pos2, str2, repleft, repright = re.split(':', jxn)
    pos1 = int(pos1)
    pos2 = int(pos2)
    maxrep = max(10, int(max(int(repleft), int(repright))))
    subset_df = fuca[((fuca['c1'] == chrom1) & ((fuca['s1'] >= pos1 - maxrep) & (fuca['s1'] <= pos1 + maxrep)) & ((fuca['c2'] == chrom2) & ((fuca['s2'] >= pos2 - maxrep) & (fuca['s2'] <= pos2 + maxrep))))]
    max_rate = ''
    if len(subset_df.index >= 1):
        max_rate = float(('{0:.2f}').format(subset_df['Rate'].astype(float).max()))
    return (
     max_rate,
     (',').join(set(subset_df['Methods'].astype(str))),
     (',').join(set(subset_df['Cancers'].astype(str))))