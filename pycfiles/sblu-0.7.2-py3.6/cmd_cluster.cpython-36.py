# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/docking/cmd_cluster.py
# Compiled at: 2019-04-09 13:30:31
# Size of source mod 2**32: 3053 bytes
import click, numpy as np, json as _json

def cluster(pwrmsds, cluster_radius, min_clust_size, max_clusters):
    marked = set()
    cluster_indices = [set(np.where((row <= cluster_radius) & (row >= 0.0))[0]) for row in pwrmsds]
    cluster_centers = list()
    for _ in range(max_clusters):
        max_index = None
        max_size = 0
        for j, cluster in enumerate(cluster_indices):
            if j in marked:
                pass
            else:
                cluster_size = len(cluster)
                if cluster_size >= min_clust_size and cluster_size > max_size:
                    max_index = j
                    max_size = cluster_size

        if max_index is None:
            break
        cluster_centers.append(max_index)
        marked.update(cluster_indices[max_index])

    if len(cluster_centers) == 0:
        raise RuntimeError('Unable to find any clusters. Try increasing radius (currently {} A) or decreasing cluster size (currently {})'.format(cluster_radius, min_clust_size))
    final_cluster_assignments = pwrmsds[cluster_centers].argmin(axis=0)
    cluster_members = [[] for _ in range(len(cluster_centers))]
    s2 = set()
    for c in cluster_centers:
        s2 = s2 | cluster_indices[c]

    for i in sorted(s2):
        cluster_members[final_cluster_assignments[i]].append(int(i))

    return sorted((zip(cluster_centers, cluster_members)), key=(lambda x: len(x[1])),
      reverse=True)


@click.command('cluster', short_help='Cluster PIPER results.')
@click.argument('pwrmsds')
@click.option('-r', '--radius', default=9.0, type=(click.FLOAT))
@click.option('-s', '--min-cluster-size', default=10, type=(click.INT))
@click.option('-l', '--max-clusters', default=50, type=(click.INT))
@click.option('-o', '--output', type=click.File(mode='w'), default=(click.open_file('-', 'w')))
@click.option('--json/--no-json', default=False)
def cli(pwrmsds, radius, min_cluster_size, max_clusters, output, json):
    pwrmsds = np.loadtxt(pwrmsds)
    pwrmsds = pwrmsds.reshape(int(np.sqrt(len(pwrmsds))), -1)
    if not pwrmsds.shape[0] == pwrmsds.shape[1]:
        raise AssertionError
    else:
        assert np.allclose(pwrmsds, (pwrmsds.T), atol=0.02)
        clusters = cluster(pwrmsds, radius, min_cluster_size, max_clusters)
        if json:
            data = {'radius':radius,  'min_cluster_size':min_cluster_size, 
             'max_clusters':max_clusters, 
             'clusters':[{'center':center,  'members':members} for center, members in clusters]}
            _json.dump(data, output)
        else:
            print(('Radius\t{:f}'.format(radius)), file=output)
            for cluster_center, members in clusters:
                print(('Center {}'.format(cluster_center + 1)), file=output)
                for member in members:
                    print((member + 1), file=output)