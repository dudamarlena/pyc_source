# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/main.py
# Compiled at: 2019-09-30 08:43:54
# Size of source mod 2**32: 5417 bytes
import argparse, sys, os, glob, numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.datasets import make_blobs
from cluster_drug_discovery.methods import kmeans, dbscan, agglomerative
import cluster_drug_discovery.input_preprocess as ce
import cluster_drug_discovery.visualization.plots as pl
from sklearn import cluster, datasets, mixture
import AdaptivePELE.utilities as utilities
from AdaptivePELE.analysis import splitTrajectory, simulationToCsv

def add_args(parser):
    parser.add_argument('algorithm', type=str, help='cluster algorithm to use')
    parser.add_argument('--nclust', type=int, help='n_cluster', default=5)
    return parser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clusterization algorithm with analysis techniques')
    parser = add_args(parser)
    args = parser.parse_args()
    pele_sim = '/data/JJ/IL17A/63O_inducefit/output/'
    pele_path = os.path.join(pele_sim, '*/*.pdb')
    residue = '63O'
    limit_structs = 1
    trajectory_basename = 'run_trajectory_'
    top = '/data/JJ/IL17A/63O_inducefit/IL17A_4HR9_complex_processed.pdb'
    pdb_files = glob.glob(pele_path)
    feat_ext = ce.CoordinatesExtractor(pdb_files, [residue], 20)
    if os.path.exists('extracted_feature.txt'):
        X = np.loadtxt('extracted_feature.txt')
    else:
        X, samples = feat_ext.retrieve_coords()
        np.savetxt('extracted_feature.txt', X)
    cluster = agglomerative.AgglomerativeAlg(X, nclust=6)
    y_pred = cluster.run()
    silhouette_values = silhouette_samples(X, y_pred)
    idx = np.argsort(silhouette_values)[::-1]
    try:
        samples[idx]
    except NameError:
        raise NameError('Remove previously generated extracted_feature.txt file and run again')

    for i in range(0, cluster.nclust):
        output_structs = 0
        for clust, sample, silh in zip(y_pred[idx], samples[idx], silhouette_values[idx]):
            print(sample.epoch, clust, sample.traj)
            if output_structs < limit_structs:
                if clust == i:
                    if pele_path[-3:] == 'pdb':
                        topology = None
                        filename = 'path{}.{}.{}.cluster{}.pdb'.format(sample.epoch, trajectory_basename, sample.traj, i)
                        trajectory = os.path.join(pele_sim, '{}/{}{}.pdb'.format(sample.epoch, trajectory_basename, sample.traj))
                        snapshots = utilities.getSnapshots(trajectory, topology=topology, use_pdb=False)
                        with open(filename, 'w') as (fw):
                            fw.write(snapshots[(sample.model - 1)])
                if pele_path[-3:] == 'xtc':
                    topology = top
                    filename = 'path{}.{}.{}.cluster{}.pdb'.format(sample.epoch, trajectory_basename, sample.traj, i)
                    trajectory = os.path.join(pele_sim, '{}/{}{}.xtc'.format(sample.epoch, trajectory_basename, sample.traj))
                    splitTrajectory.main('', [trajectory], topology, [sample.model], template=filename, use_pdb=False)
                output_structs += 1