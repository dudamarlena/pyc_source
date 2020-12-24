# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/embedding_visualization/embedding_tools.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1533 bytes
try:
    from MulticoreTSNE import MulticoreTSNE as TSNE
    import multiprocessing as mp
    parallel_tsne = True
except ImportError:
    try:
        from sklearn.manifold import TSNE
        parallel_tsne = False
    except:
        pass

import pandas as pd, numpy as np

def get_2d_coordinates_tsne(multinet, output_format='json', verbose=True):
    embedding = multinet.embedding
    X = embedding[0]
    indices = embedding[1]
    if verbose:
        multinet.monitor('Doing the TSNE reduction to 2 dimensions!')
    elif parallel_tsne:
        X_embedded = TSNE(n_components=2, n_jobs=(mp.cpu_count())).fit_transform(X)
    else:
        X_embedded = TSNE(n_components=2).fit_transform(X)
    dfr = pd.DataFrame(X_embedded, columns=['dim1', 'dim2'])
    dfr['node_names'] = [n for n in multinet.get_nodes()]
    dfr['node_codes'] = indices
    if output_format == 'json':
        return dfr.to_json(orient='records')
    if output_format == 'dataframe':
        return dfr
    if output_format == 'pos_dict':
        output_dict = {}
        for index, row in dfr.iterrows():
            output_dict[row['node_names']] = (
             row['dim1'], row['dim2'])

        return output_dict
    return


def layout_positions_to_json(position_dict):
    outlist = []
    for k, v in position_dict.items():
        outlist.append({node_names: k, dim1: v[0], dim2: v[1]})

    return outlist