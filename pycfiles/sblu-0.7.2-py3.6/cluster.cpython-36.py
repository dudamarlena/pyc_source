# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cluster.py
# Compiled at: 2019-04-09 13:30:31
# Size of source mod 2**32: 1149 bytes
import re, json as _json

def read_clusters_stream_text(stream):
    cluster_data = {'radius':None, 
     'min_cluster_size':None, 
     'max_clusters':None, 
     'clusters':[]}
    cluster = {'center':-1, 
     'members':[]}
    for line in stream:
        line_ = line.rstrip()
        if re.match('^Radius', line_):
            cluster_data['radius'] = float(line_.split()[1])
        else:
            if re.match('^Center', line_):
                if cluster['center'] != -1:
                    cluster_data['clusters'].append(cluster)
                cluster = {'center':int(line_.split()[1]) - 1, 
                 'members':[]}
            else:
                if re.match('^[0-9]+$', line_):
                    cluster['members'].append(int(line_) - 1)
                else:
                    raise ValueError('Unexpected line in clusterfile.')

    cluster_data['clusters'].append(cluster)
    return cluster_data


def read_clusters(filepath):
    with open(filepath, 'r') as (f):
        try:
            clusters_data = _json.load(f)
        except ValueError:
            f.seek(0)
            clusters_data = read_clusters_stream_text(f)

        return clusters_data