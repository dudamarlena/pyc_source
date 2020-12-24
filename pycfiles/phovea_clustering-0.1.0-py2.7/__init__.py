# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_clustering/__init__.py
# Compiled at: 2017-04-05 09:54:14


def phovea(registry):
    """
  register extension points
  :param registry:
  """
    registry.append('clustering', 'caleydo-clustering-kmeans', 'phovea_clustering.clustering_kmeans', {})
    registry.append('clustering', 'caleydo-clustering-hierarchical', 'phovea_clustering.clustering_hierarchical', {})
    registry.append('clustering', 'caleydo-clustering-affinity', 'phovea_clustering.clustering_affinity', {})
    registry.append('clustering', 'caleydo-clustering-fuzzy', 'phovea_clustering.clustering_fuzzy', {})
    registry.append('namespace', 'caleydo-clustering', 'phovea_clustering.clustering_api', {'namespace': '/api/clustering'})


def phovea_config():
    """
  :return: file pointer to config file
  """
    from os import path
    here = path.abspath(path.dirname(__file__))
    config_file = path.join(here, 'config.json')
    if path.exists(config_file):
        return config_file
    else:
        return