# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\algorithms\cluster_models.py
# Compiled at: 2017-12-25 10:34:32
# Size of source mod 2**32: 2066 bytes
from ..default import *
from .. import structure
from .basic import *
from ..statistics import stats_methods
from scipy.spatial.distance import cosine
from sklearn.cluster import KMeans

def clustering(self, n_clusters):

    def relabel(labels, centers):
        dis = [1 - cosine(centers[labels[0]], centers[j]) for j in range(n_clusters)]
        mapping = dict(zip(sorted((range(len(dis))), key=(lambda k: dis[k]), reverse=True), range(n_clusters)))
        new_labels = [mapping[i] for i in labels]
        new_centers = {mapping[ind]:center for ind, center in enumerate(centers)}
        return (new_labels, new_centers)

    def kmeans(data):
        condition_order = data.index.get_level_values('condition_group').unique()
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(data)
        labels = kmeans.predict(data)
        centers = kmeans.cluster_centers_.squeeze()
        new_labels, new_centers = relabel(labels, centers)
        clusterID = pd.Series(new_labels, index=(data.index)).unstack('time')
        clusterID = clusterID.reindex(condition_order)
        clusterID.name = data.name
        return clusterID

    @self.iter('average')
    def to_erp(case_raw_data):
        check_availability(case_raw_data, single_value_level=['condition_group', 'trial_group', 'channel_group'])
        return case_raw_data.mean(level=['condition_group', 'channel']).stack('time').unstack('channel')

    erp_collection = to_erp()
    clustering_data = [kmeans(erp_batch) for erp_batch in erp_collection]
    default_plot_params = dict(plot_type=['direct', 'heatmap'], color=sns.cubehelix_palette(light=0.95, as_cmap=True), cbar_values=(list(range(1, n_clusters + 1))), cbar_title='clusters', grid=True,
      style='darkgrid')
    return structure.Analyzed_data('Clustering', clustering_data, None, default_plot_params)


structure.Extracted_epochs.clustering = clustering