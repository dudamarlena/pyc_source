# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/clusteringModels.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 8657 bytes
from bokeh.io import gridplot
from sklearn import cluster
from sklearn.neighbors import kneighbors_graph, KernelDensity
import numpy as np, pandas as pd, time
from . import sklearnUtils as sku
from . import plotter
from . import utils

class StarKMeans(cluster.KMeans):
    pass


def is_cluster(dataframe, model_type='dbscan', batch_size=2):
    if model_type == 'dbscan':
        model_obj = cluster.DBSCAN(eps=0.2)
    else:
        if model_type == 'MiniBatchKMeans':
            assert batch_size, 'Batch size mandatory'
            model_obj = cluster.MiniBatchKMeans(n_clusters=batch_size)
    model_obj.fit(X)
    return model_obj.cluster_centers_


def cluster_analyze(dataframe, name='', **kwargs):
    plots = list()
    clustering_names = [
     'MiniBatchKMeans', 'AffinityPropagation', 'MeanShift',
     'SpectralClustering', 'Ward', 'AgglomerativeClustering',
     'DBSCAN', 'Birch', 'bgmm']
    X = sku.feature_scale_or_normalize(dataframe, dataframe.columns)
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)
    connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
    connectivity = 0.5 * (connectivity + connectivity.T)
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
    two_means = cluster.MiniBatchKMeans(n_clusters=2)
    ward = cluster.AgglomerativeClustering(n_clusters=2, linkage='ward', connectivity=connectivity)
    spectral = cluster.SpectralClustering(n_clusters=2, eigen_solver='arpack',
      affinity='nearest_neighbors')
    dbscan = cluster.DBSCAN(eps=0.2)
    affinity_propagation = cluster.AffinityPropagation(damping=0.9, preference=(-200))
    average_linkage = cluster.AgglomerativeClustering(linkage='average',
      affinity='cityblock',
      n_clusters=2,
      connectivity=connectivity)
    birch = cluster.Birch(n_clusters=2)
    bgmm_args = {'weight_concentration_prior_type':'dirichlet_process',  'n_components':5, 
     'reg_covar':0,  'init_params':'random',  'max_iter':1500, 
     'mean_precision_prior':0.8}
    bgmm = (utils.get_model_obj)(*('bgmm', ), **bgmm_args)
    clustering_algorithms = [two_means, affinity_propagation, ms, spectral, ward,
     average_linkage, dbscan, birch, bgmm]
    for model_name, algorithm in zip(clustering_names, clustering_algorithms):
        t0 = time.time()
        algorithm.fit(X)
        t1 = time.time()
        if hasattr(algorithm, 'labels_'):
            print('According to %s there are %d clusters' % (name, len(set(algorithm.labels_))))
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)
        plot_data = np.c_[(X, y_pred)]
        columns = list(dataframe.columns) + ['classes']
        new_df = pd.DataFrame(data=plot_data, columns=columns)
        s_plot = plotter.scatterplot(new_df, (columns[0]), (columns[1]), plttitle=('%s: %s' % (name, model_name)),
          groupCol='classes')
        plots.append(s_plot)
        if hasattr(algorithm, 'cluster_centers_'):
            print('According to %s there are %d clusters' % (name, len(algorithm.cluster_centers_)))
            centers = pd.DataFrame(algorithm.cluster_centers_)
            for i, c in enumerate(algorithm.cluster_centers_):
                plotter.mtext(s_plot, (c[0]), (c[1]), ('%s' % str(i)), text_color='red')

    grid = gridplot(list(utils.chunks(plots, size=2)))
    plotter.show(grid)


def silhouette_analyze(dataframe, cluster_type='KMeans', n_clusters=None):
    """
    Plot silhouette analysis plot of given data and cluster type across different  cluster sizes
    # from here Silhouette analysis --http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
    """
    from sklearn.metrics import silhouette_samples, silhouette_score
    import matplotlib.cm as cm, numpy as np, collections
    if not n_clusters:
        n_clusters = range(2, 8, 2)
    elif not isinstance(n_clusters, collections.Iterable):
        raise AssertionError('n_clusters must be an iterable object')
    dataframe = dataframe.as_matrix()
    cluster_scores_df = pd.DataFrame(columns=['cluster_size', 'silhouette_score'])
    for j, clusternum in enumerate(n_clusters):
        if cluster_type != 'bgmm':
            clusterer = utils.get_model_obj(cluster_type, n_clusters=clusternum)
        else:
            clusterer = utils.get_model_obj(cluster_type, n_components=(2 * cluster))
        if cluster_type not in ('KMeans', 'spectral', 'bgmm', 'birch', 'dbscan'):
            cluster_labels = clusterer.fit(dataframe)
        else:
            if cluster_type == 'bgmm':
                clusterer.fit(dataframe)
                cluster_labels = set(clusterer.predict(dataframe))
            else:
                cluster_labels = clusterer.fit_predict(dataframe)
            if len(set(cluster_labels)) > 1:
                silhouette_avg = silhouette_score(dataframe, cluster_labels)
                cluster_scores_df.loc[j] = [clusternum, silhouette_avg]
                print('For clusters =', clusternum, 'The average silhouette_score is :', silhouette_avg)
            else:
                print('No cluster found with cluster no:%d and algo type: %s' % (clusternum, cluster_type))
                continue
        dataframe = pd.DataFrame(dataframe)
        cols = list(dataframe.columns)
        dataframe['predictions'] = pd.Series(cluster_labels)
        s_plot = plotter.scatterplot(dataframe, (cols[0]),
          (cols[1]), groupCol='predictions',
          xlabel='Feature space for 1st feature',
          ylabel='Feature space for 2nd feature',
          plttitle='Visualization of the clustered data')
        if hasattr(clusterer, 'cluster_centers_'):
            for i, c in enumerate(clusterer.cluster_centers_):
                plotter.mtext(s_plot, (c[0]), (c[1]), ('%s' % str(i)), text_color='red')

        plotter.show(s_plot)

    plotter.show(plotter.lineplot(cluster_scores_df, xcol='cluster_size', ycol='silhouette_score'))


def som_analyze(dataframe, mapsize, algo_type='som'):
    import sompy
    som_factory = sompy.SOMFactory()
    data = dataframe.as_matrix()
    if not isinstance(mapsize, tuple):
        raise AssertionError('Mapsize must be a tuple')
    else:
        sm = som_factory.build(data, mapsize=mapsize, normalization='var', initialization='pca')
        if algo_type == 'som':
            sm.train(n_job=6, shared_memory='no', verbose='INFO')
            v = sompy.mapview.View2DPacked(50, 50, 'test', text_size=8)
            v.show(sm, what='codebook', cmap='jet', col_sz=6)
            v.show(sm, what='cluster', cmap='jet', col_sz=6)
            h = sompy.hitmap.HitMapView(10, 10, 'hitmap', text_size=8, show_text=True)
            h.show(sm)
        else:
            if algo_type == 'umatrix':
                u = sompy.umatrix.UMatrixView(50, 50, 'umatrix', show_axis=True, text_size=8, show_text=True)
                UMAT = u.build_u_matrix(som, distance=1, row_normalized=False)
                u.show(som, distance2=1, row_normalized=False, show_data=True, contooor=False, blob=False)
            else:
                raise 'Unknown SOM algorithm type'