# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/champ/PartitionEnsemble.py
# Compiled at: 2019-05-22 09:04:07
# Size of source mod 2**32: 51512 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from future.utils import iteritems
import gzip, sys, os, re
from .champ_functions import get_intersection
from .champ_functions import PolyArea
from .champ_functions import min_dist_origin
from .champ_functions import point_comparator
from .champ_functions import get_number_of_communities
from .champ_functions import get_expected_edges
from .champ_functions import get_expected_edges_ml
from .champ_functions import get_sum_internal_edges
from .plot_domains import plot_2d_domains
from .plot_domains import plot_multiplex_community as plot_multilayer_pd
import matplotlib.lines as mlines, matplotlib.pyplot as plt, matplotlib.patheffects as path_effects, matplotlib.colors as mc, matplotlib.colorbar as mcb
from matplotlib import rc
import igraph as ig, pandas as pd, numpy as np, h5py, copy, sklearn.metrics as skm, warnings, logging
logging.basicConfig(format=':%(asctime)s:%(levelname)s:%(message)s', level=(logging.INFO))
import seaborn as sbn
iswin = os.name == 'nt'
is_py3 = sys.version_info >= (3, 0)
try:
    import cpickle as pickle
except ImportError:
    import pickle

class PartitionEnsemble(object):
    """PartitionEnsemble"""

    def __init__(self, graph=None, interlayer_graph=None, layer_vec=None, listofparts=None, name='unnamed_graph', maxpt=None, min_com_size=5):
        if not interlayer_graph is None:
            if not layer_vec is not None:
                raise AssertionError('Layer_vec must be supplied for multilayer graph')
        self._hdf5_file = None
        self.int_edges = np.array([])
        self.exp_edges = np.array([])
        self.int_inter_edges = np.array([])
        self.resolutions = np.array([])
        self.couplings = np.array([])
        self.numcoms = np.array([])
        self.orig_mods = np.array([])
        self.numparts = 0
        self.graph = graph
        self.interlayer_graph = interlayer_graph
        self.layer_vec = layer_vec
        self.ismultilayer = self.layer_vec is not None
        self._min_com_size = min_com_size
        self.maxpt = maxpt
        self._partitions = np.array([])
        self._uniq_coeff_indices = None
        self._uniq_partition_indices = None
        self._twin_partitions = None
        self._sim_mat = None
        self._mu = None
        if listofparts != None:
            self.add_partitions(listofparts, maxpt=(self.maxpt))
        self.name = name

    def get_adjacency(self, intra=True):
        """
                Calc adjacency representation if it exists
                :param intra: return intralayer adjacency.  If false returns interlayer adj.
                :return: self.adjacency
sub
                """
        if intra:
            if 'adjacency' not in self.__dict__:
                if 'intra_adjacency' not in self.__dict__:
                    if 'weight' in self.graph.edge_attributes():
                        self.intra_adj = self.graph.get_adjacency(type=(ig.GET_ADJACENCY_BOTH), attribute='weight')
                    else:
                        self.intra_adj = self.graph.get_adjacency(type=(ig.GET_ADJACENCY_BOTH))
                    self.adjacency = self.intra_adj
            self.adjacency = np.array(self.adjacency.data)
            return self.adjacency
        else:
            if not self.ismultilayer:
                raise ValueError('Cannot get interedge adjacency from single layer graph')
            if 'inter_adj' not in self.__dict__:
                if 'weight' in self.interlayer_graph.edge_attributes():
                    self.inter_adj = self.interlayer_graph.get_adjacency(type=(ig.GET_ADJACENCY_BOTH), attribute='weight')
                else:
                    self.inter_adj = self.interlayer_graph.get_adjacency(type=(ig.GET_ADJACENCY_BOTH))
            self.inter_adj = np.array(self.inter_adj.data)
            return self.inter_adj

    def calc_internal_edges(self, memvec, intra=True):
        """
                Uses igraph Vertex Clustering representation to calculate internal edges.  see          :meth:`louvain_ext.get_expected_edges`

                :param memvec: membership vector for which to calculate the internal edges.
                :param intra: boolean indicating whether to calculate intralayer edges that are                 internal (True) or interlayer edges that are internal to communities (False).
                :type memvec: list

                :return:

                """
        if intra:
            partobj = ig.VertexClustering(graph=(self.graph), membership=memvec)
            weight = 'weight' if 'weight' in self.graph.edge_attributes() else None
        else:
            if not self.ismultilayer:
                raise ValueError('Cannot get calculate internal interlayer edges from single layer graph')
            partobj = ig.VertexClustering(graph=(self.interlayer_graph), membership=memvec)
            weight = 'weight' if 'weight' in self.interlayer_graph.edge_attributes() else None
        return get_sum_internal_edges(partobj=partobj, weight=weight)

    def calc_expected_edges(self, memvec):
        """
                Uses igraph Vertex Clustering representation to calculate expected edges for            each layer within the graph.
                :meth:`louvain_ext.get_expected_edges`

                :param memvec: membership vector for which to calculate the expected edges
                :type memvec: list
                :return: expected edges under null
                :rtype: float

                """
        partobj = ig.VertexClustering(graph=(self.graph), membership=memvec)
        weight = 'weight' if 'weight' in self.graph.edge_attributes() else None
        if self.ismultilayer:
            Phat = get_expected_edges_ml(partobj, (self.layer_vec), weight=weight)
        else:
            Phat = get_expected_edges(partobj, weight=weight, directed=(self.graph.is_directed()))
        return Phat

    def __getitem__(self, item):
        """
                List of paritions in the PartitionEnsemble object can be indexed directly

                :param item: index of partition for direct access
                :type item: int
                :return: self.partitions[item]
                :rtype:  membership vector of community for partition
                """
        return self.partitions[item]

    class _PartitionOnFile:

        def __init__(self, file=None):
            self._hdf5_file = file

        def __getitem__(self, item):
            with h5py.File(self._hdf5_file, 'r') as (openfile):
                try:
                    return openfile['_partitions'].__getitem__(item)
                except TypeError:
                    return openfile['_partitions'].__getitem__(list(item))

        def __len__(self):
            with h5py.File(self._hdf5_file, 'r') as (openfile):
                return openfile['_partitions'].shape[0]

        def __str__(self):
            return '%d partitions saved on %s' % (len(self), self._hdf5_file)

    @property
    def min_com_size(self):
        return self._min_com_size

    @min_com_size.setter
    def min_com_size(self, value):
        """when the minimum com size is updated, we want to go back through
                and recalculate the number of communities in each partition"""
        self._min_com_size = value
        for i in range(len(self.partitions)):
            self.numcoms[i] = get_number_of_communities((self.partitions[i]), min_com_size=(self._min_com_size))

    @property
    def partitions(self):
        """Type/value of partitions is defined at time of access. If the PartitionEnsemble         has an associated hdf5 file (PartitionEnsemble.hdf5_file), then partitions will be              read and added to on the file, and not as an object in memory."""
        if self._hdf5_file is not None:
            return PartitionEnsemble._PartitionOnFile(file=(self._hdf5_file))
        else:
            return self._partitions

    @property
    def hdf5_file(self):
        """Default location for saving/loading PartitionEnsemble if hdf5 format is used.  When this is set         it will automatically resave the PartitionEnsemble into the file specified."""
        return self._hdf5_file

    @hdf5_file.setter
    def hdf5_file(self, value):
        """Set new value for hdf5_file and automatically save to this file."""
        self._hdf5_file = value
        self.save()

    def _check_lengths(self):
        """
                check all state variables for equal length.  Will use length of partitions stored               in the hdf5 file if this is set for the PartitionEnsemble.  Otherwise just uses                 internal lists.

                :return: boolean indicating states varaible lengths are equal

                """
        if self._hdf5_file is not None:
            with h5py.File(self._hdf5_file) as (openfile):
                if openfile['_partitions'].shape[0] == len(self.int_edges):
                    if openfile['_partitions'].shape[0] == len(self.resolutions):
                        if openfile['_partitions'].shape[0] == len(self.exp_edges):
                            return True
                return False
        elif self.partitions.shape[0] == len(self.int_edges) and self.partitions.shape[0] == len(self.resolutions) and self.partitions.shape[0] == len(self.exp_edges):
            if self.ismultilayer:
                if self.partitions.shape[0] == len(self.int_inter_edges):
                    if self.partitions.shape[0] == len(self.couplings):
                        return True
                return False
            else:
                return True
        else:
            return False

    def _combine_partitions_hdf5_files(self, otherfile):
        assert self._hdf5_file != otherfile, 'Cannot combine a partition ensemble file with itself'
        if self._hdf5_file is None or otherfile is None:
            raise IOError('PartitionEnsemble does not have hdf5 file currently defined')
        with h5py.File(self._hdf5_file, 'a') as (myfile):
            with h5py.File(otherfile, 'r') as (file_2_add):
                attributes = [
                 '_partitions', 'resolutions', 'orig_mods', 'int_edges', 'exp_edges', 'numcoms']
                if self.ismultilayer:
                    attributes += ['couplings', 'int_inter_edges']
                for attribute in attributes:
                    cshape = myfile[attribute].shape
                    oshape = file_2_add[attribute].shape
                    if len(cshape) == 1:
                        assert len(oshape) == 1, 'attempting to combine objects of different dimensions'
                        newshape = (cshape[0] + oshape[0],)
                        myfile[attribute][cshape[0]:cshape[0] + newshape[0]] = file_2_add[attribute]
                    else:
                        assert cshape[1] == oshape[1], 'attempting to combine objects of different dimensions'
                        newshape = (cshape[0] + oshape[0], cshape[1])
                        myfile[attribute].resize(newshape)
                        print(newshape, myfile[attribute].shape)
                        print(oshape, file_2_add[attribute].shape)
                        myfile[attribute][cshape[0]:cshape[0] + newshape[0], :] = file_2_add[attribute]

    def _append_partitions_hdf5_file(self, partitions):
        """

                :param partitions: list of partitions (in dictionary) to add to the PartitionEnsemble.

                :type partitions: dict

                """
        with h5py.File(self._hdf5_file, 'a') as (openfile):
            orig_shape = openfile['_partitions'].shape
            attributes = ['_partitions', 'resolutions', 'orig_mods', 'int_edges', 'exp_edges', 'numcoms']
            if self.ismultilayer:
                attributes += ['couplings', 'int_inter_edges']
            for attribute in attributes:
                cshape = openfile[attribute].shape
                if len(cshape) == 1:
                    openfile[attribute].resize((cshape[0] + len(partitions),))
                else:
                    openfile[attribute].resize((cshape[0] + len(partitions), cshape[1]))

            for i, part in enumerate(partitions):
                cind = orig_shape[0] + i
                openfile['_partitions'][cind] = np.array(part['partition'])
                if 'resolution' in part:
                    self.resolutions = np.append(self.resolutions, part['resolution'])
                    openfile['resolutions'][cind] = part['resolution']
                else:
                    self.resolutions = np.append(self.resolutions, None)
                    openfile['resolutions'][cind] = None
                if 'int_edges' in part:
                    self.int_edges = np.append(self.int_edges, part['int_edges'])
                    openfile['int_edges'][cind] = part['int_edges']
                else:
                    cint_edges = self.calc_internal_edges(part['partition'])
                    self.int_edges = np.append(self.int_edges, cint_edges)
                    openfile['int_edges'][cind] = cint_edges
                if 'exp_edges' in part:
                    self.exp_edges = np.append(self.exp_edges, part['exp_edges'])
                    openfile['exp_edges'][cind] = part['exp_edges']
                else:
                    cexp_edges = self.calc_expected_edges(part['partition'])
                    self.exp_edges = np.append(self.exp_edges, cexp_edges)
                    openfile['exp_edges'][cind] = cexp_edges
                if 'orig_mod' in part:
                    self.orig_mods = np.append(self.orig_mods, part['orig_mod'])
                    openfile['orig_mods'][cind] = part['orig_mod']
                else:
                    if self.resolutions[(-1)] is not None:
                        corigmod = self.int_edges[(-1)] - self.resolutions[(-1)] * self.exp_edges
                        self.orig_mods = np.append(self.orig_mods, corigmod)
                        openfile['orig_mods'][cind] = corigmod
                    else:
                        openfile['orig_mods'][cind] = None
                        self.orig_mods = np.append(self.orig_mods, None)
                if self.ismultilayer:
                    if 'int_inter_edges' in part:
                        self.int_inter_edges = np.append(self.int_inter_edges, part['int_inter_edges'])
                        openfile['int_inter_edges'][cind] = part['int_inter_edges']
                    else:
                        cint_inter_edges = self.calc_internal_edges((part['partition']), intra=False)
                        self.int_edges = np.append(self.int_inter_edges, cint_inter_edges)
                        openfile['int_inter_edges'][cind] = cint_inter_edges
                    if 'coupling' in part:
                        self.couplings = np.append(self.couplings, part['coupling'])
                        openfile['couplings'][cind] = part['coupling']
                    else:
                        self.couplings = np.append(self.couplings, None)
                        openfile['couplings'][cind] = None

            self.numparts = openfile['_partitions'].shape[0]
        assert self._check_lengths()

    def add_partitions(self, partitions, maxpt=None):
        """
                Add additional partitions to the PartitionEnsemble object. Also adds the number of              communities for each.  In the case where PartitionEnsemble was openned from a file, we          just appended these and the other values onto each of the files.  Partitions are not kept               in object, however the other partitions values are.

                :param partitions: list of partitions to add to the PartitionEnsemble
                :type partitions: dict,list

                """
        if not hasattr(partitions, '__iter__'):
            partitions = [
             partitions]
        else:
            if self._hdf5_file is not None:
                self._append_partitions_hdf5_file(partitions)
            else:
                for part in partitions:
                    if len(self._partitions) == 0:
                        self._partitions = np.array([part['partition']])
                    else:
                        self._partitions = np.append((self._partitions), [part['partition']], axis=0)
                    if 'resolution' in part:
                        self.resolutions = np.append(self.resolutions, part['resolution'])
                    else:
                        self.resolutions = np.append(self.resolutions, None)
                    if 'int_edges' in part:
                        self.int_edges = np.append(self.int_edges, part['int_edges'])
                    else:
                        cint_edges = self.calc_internal_edges(part['partition'])
                        self.int_edges = np.append(self.int_edges, cint_edges)
                    if 'exp_edges' in part:
                        self.exp_edges = np.append(self.exp_edges, part['exp_edges'])
                    else:
                        cexp_edges = self.calc_expected_edges(part['partition'])
                        self.exp_edges = np.append(self.exp_edges, cexp_edges)
                    if 'orig_mod' in part:
                        self.orig_mods = np.append(self.orig_mods, part['orig_mod'])
                    else:
                        if self.resolutions[(-1)] is not None:
                            self.orig_mods = np.append(self.orig_mods, self.int_edges[(-1)] - self.resolutions[(-1)] * self.exp_edges)
                        else:
                            self.orig_mods = np.append(self.orig_mods, None)
                    if self.ismultilayer:
                        if 'coupling' in part:
                            self.couplings = np.append(self.couplings, part['coupling'])
                        else:
                            self.couplings = np.append(self.couplings, None)
                        if 'int_inter_edges' in part:
                            self.int_inter_edges = np.append(self.int_inter_edges, part['int_inter_edges'])
                        else:
                            cint_inter_edges = self.calc_internal_edges((part['partition']), intra=False)
                            self.int_inter_edges = np.append(self.int_inter_edges, cint_inter_edges)
                    self.numcoms = np.append(self.numcoms, get_number_of_communities((part['partition']), min_com_size=(self._min_com_size)))
                    assert self._check_lengths()
                    self.numparts = len(self.partitions)

        self.apply_CHAMP(maxpt=(self.maxpt))
        self.sim_mat

    def get_champ_gammas(self):
        """
                Return the first coordinate for each range in the dominante domain, sorted by increasing gamma
                :return: sorted list
                """
        allgams = sorted(set([pt[0] for pts in self.ind2doms.values() for pt in pts]))
        return allgams

    def get_broadedst_domains(self, n=None):
        r"""
                Return the starting $\gamma$ for the top n domains by the length of the domain          (i.e. $\gamma_{i+1}-\gamma_{i}$) as well as the length of the domain and the index
                in ind2doms dict

                :param n: number of top starting values to return
                :return: list of n tuples  : [ ($\gamma$ values,length domain, champ index) , ( ) , ... ]
                """
        if not self.ismultilayer:
            out_df = pd.DataFrame(columns=['start_gamma', 'end_gamma', 'width', 'ind'])
            for k, pts in self.ind2doms.items():
                cind = out_df.shape[0]
                width = pts[1][0] - pts[0][0]
                out_df.loc[(cind, ['start_gamma', 'end_gamma', 'width', 'ind'])] = (pts[0][0], pts[1][0], width, k)

            out_df.sort_values(by='width', ascending=False, inplace=True)
            if n is not None:
                return out_df.iloc[:n, :]
            return out_df
        else:
            if n is None:
                n = 4
            all_areas = map(lambda x: PolyArea(x), self.ind2doms.values())
            top_n = np.argpartition(all_areas, -1 * n)[-1 * n:]
            top_n = [ind[1] for ind in sorted(list((zip(all_areas[top_n], top_n)), (lambda x: x[0]), reverse=True))]
            return self.ind2doms.values()[top_n]

    def get_partition_dictionary(self, ind=None):
        """
                Get dictionary representation of partitions with the following keys:

                        'partition','resolution','orig_mod','int_edges','exp_edges'

                :param ind: optional indices of partitions to return.  if not supplied all partitions will be returned.
                :type ind: int, list
                :return: list of dictionaries

                """
        if ind is not None:
            if not hasattr(ind, '__iter__'):
                ind = [
                 ind]
        else:
            ind = range(len(self.partitions))
        outdicts = []
        for i in ind:
            cdict = {'partition':self.partitions[i],  'int_edges':self.int_edges[i], 
             'exp_edges':self.exp_edges[i], 
             'resolution':self.resolutions[i], 
             'orig_mod':self.orig_mods[i]}
            if self.ismultilayer:
                cdict['coupling'] = self.couplings[i]
                cdict['int_inter_edges'] = self.int_inter_edges[i]
            outdicts.append(cdict)

        return outdicts

    def _offset_keys_new_dict(self, indict):
        offset = self.numparts
        newdict = {k + offset:val for k, val in indict.items()}
        return newdict

    def merge_ensemble(self, otherEnsemble, new=True):
        """
                Combine to PartitionEnsembles.  Checks for concordance in the number of vertices.               Assumes that internal ordering on the graph nodes for each is the same.

                :param otherEnsemble: otherEnsemble to merge
                :param new: create a new PartitionEnsemble object? Otherwise partitions will be loaded into             the one of the original partition ensemble objects (the one with more partitions in the first place).
                :type new: bool
                :return:  PartitionEnsemble reference with merged set of partitions

                """
        if not self.graph.vcount() == otherEnsemble.graph.vcount():
            raise ValueError('PartitionEnsemble graph vertex counts do not match')
        elif self.ismultilayer != otherEnsemble.ismultilayer:
            raise ValueError('ParitionEnsembles must both be sinlge layer or both be multilayer')
        else:
            if self.ismultilayer:
                if self.interlayer_graph.vcount() != otherEnsemble.interlayer_graph.vcount():
                    raise ValueError('PartitionEnsemble interlayer_graph vertex counts do not match')
            if new:
                newEnsemble = copy.deepcopy(self)
                attributes = ['_partitions', 'resolutions', 'orig_mods', 'int_edges', 'exp_edges', 'numcoms']
                if self.ismultilayer:
                    attributes += ['couplings', 'int_inter_edges']
                for attribute in attributes:
                    newEnsemble.__dict__[attribute] = np.concatenate([newEnsemble.__dict__[attribute], otherEnsemble.__dict__[attribute]])

                newEnsemble.ind2doms = {}
                newEnsemble.ind2doms.update(self.ind2doms)
                newEnsemble.ind2doms.update(self._offset_keys_new_dict(otherEnsemble.ind2doms))
                newEnsemble.apply_CHAMP(subset=(list(newEnsemble.ind2doms)))
                return newEnsemble
            if self._hdf5_file is not None:
                if self._hdf5_file == otherEnsemble._hdf5_file:
                    warnings.warn('Partitions are stored on the same file.  returning self', UserWarning)
                    return self
        if self.numparts < otherEnsemble.numparts:
            return otherEnsemble.merge_ensemble(self, new=False)
        else:
            if self._hdf5_file is not None:
                if otherEnsemble.hdf5_file is not None:
                    self._combine_partitions_hdf5_files(otherEnsemble.hdf5_file)
                    self.open(self._hdf5_file)
                    return self
            self.ind2doms.update(self._offset_keys_new_dict(otherEnsemble.ind2doms))
            self.add_partitions(otherEnsemble.get_partition_dictionary())
            self.apply_CHAMP(subset=(list(self.ind2doms)), maxpt=(self.maxpt))
            return self

    def get_coefficient_array(self, subset=None):
        """
                Create array of coefficents for each partition.
                :param subset: subset of partitions to create the coefficient array for
                :return: np.array with coefficents for each of the partions

                """
        if subset is None:
            subset = range(self.numparts)
        else:
            if not self.ismultilayer:
                for i, ind in enumerate(subset):
                    if i == 0:
                        outlist = np.array([
                         [self.int_edges[ind],
                          self.exp_edges[ind]]])
                    else:
                        outlist = np.append(outlist,
                          [
                         [
                          self.int_edges[ind],
                          self.exp_edges[ind]]],
                          axis=0)

            else:
                for i, ind in enumerate(subset):
                    if i == 0:
                        outlist = np.array([
                         [self.int_edges[ind],
                          self.exp_edges[ind],
                          self.int_inter_edges[ind]]])
                    else:
                        outlist = np.append(outlist,
                          [
                         [
                          self.int_edges[ind],
                          self.exp_edges[ind],
                          self.int_inter_edges[ind]]],
                          axis=0)

        return outlist

    @property
    def unique_coeff_indices(self):
        if self._uniq_coeff_indices is None:
            self._uniq_coeff_indices = self.get_unique_coeff_indices()
            return self._uniq_coeff_indices

    @property
    def unique_partition_indices(self):
        if self._uniq_partition_indices is None:
            self._twin_partitions, self._uniq_partition_indices = self._get_unique_twins_and_partition_indices()
        return self._uniq_partition_indices

    @property
    def twin_partitions(self):
        """
                We define twin partitions as those that have the same coefficients but are different partitions.                To find these we look for the diffence in the partitions with the same coefficients.

                :return: List of groups of the indices of partitions that have the same coefficient but                 are non-identical.
                :rtype: list of list (possibly empty if no twins)
                """
        if self._twin_partitions is None:
            self._twin_partitions, self._uniq_partition_indices = self._get_unique_twins_and_partition_indices()
        return self._twin_partitions

    @property
    def sim_mat(self):
        if self._sim_mat is None:
            sim_mat = np.zeros((len(self.ind2doms), len(self.ind2doms)))
            keys = [x[0] for x in sorted((self.ind2doms.items()), key=(lambda x: x[1][0][0]))]
            for i in range(len(keys)):
                for j in range(i, len(keys)):
                    ind1 = keys[i]
                    ind2 = keys[j]
                    partition1 = self.partitions[ind1]
                    partition2 = self.partitions[ind2]
                    sim_mat[i][j] = skm.adjusted_mutual_info_score(partition1, partition2)
                    sim_mat[j][i] = sim_mat[i][j]

            self._sim_mat = sim_mat
        return self._sim_mat

    @property
    def mu(self):
        """total intralayer edges (and inter if is multilayer)"""
        if self._mu is None:
            self._mu = self.graph.ecount()
            if self.ismultilayer:
                self._mu += self.interlayer_graph.ecount()
        return self._mu

    def get_unique_coeff_indices(self):
        r""" Get the indices for the partitions with unique coefficient              :math:`\hat{A}=\sum_{ij}A_{ij}`                 :math:`\hat{P}=\sum_{ij}P_{ij}`

                 Note that for each replicated partition we return the index of one (the earliest in the list)           the replicated

                :return: the indices of unique coeficients
                :rtype: np.array
                """
        _, indices = np.unique((self.get_coefficient_array()), return_index=True, axis=0)
        return indices

    def _reindex_part_array(self, part_array):
        """we renumber partitions labels to ensure that each goes from number 0,1,2,...
                in order to compare.

                :param part_array:
                :type part_array:
                :return: relabeled array
                :rtype:
                """
        out_array = np.zeros(part_array.shape)
        for i in range(part_array.shape[0]):
            clabdict = {}
            for j in range(part_array.shape[1]):
                clabdict[part_array[i][j]] = clabdict.get(part_array[i][j], len(clabdict))

            for j in range(part_array.shape[1]):
                out_array[i][j] = clabdict[part_array[i][j]]

        return out_array

    def _get_unique_twins_and_partition_indices(self, reindex=True):
        """
                Returns the (possibly empty) list of twin partitions and the list of unique partitions.

                :param reindex: if True, will reindex partitions that it is comparing to ensure they are unique under           permutation.
                :return: list of twin partition (can be empty), list of indicies of unique partitions.
                :rtype: list,np.array
                """
        uniq, index, reverse, counts = np.unique((self.get_coefficient_array()), return_index=True,
          return_counts=True,
          return_inverse=True,
          axis=0)
        ind2keep = index[np.where(counts == 1)[0]]
        twin_inds = []
        for ind in np.where(counts > 1)[0]:
            revinds = np.where(reverse == ind)[0]
            parts2comp = self.partitions[np.where(reverse == ind)[0]]
            if reindex:
                reindexed_parts2comp = self._reindex_part_array(parts2comp)
            else:
                reindexed_parts2comp = parts2comp
            _, curpart_inds = np.unique(reindexed_parts2comp, axis=0, return_index=True)
            if len(curpart_inds) > 1:
                twin_inds.append(revinds[curpart_inds])
            ind2keep = np.append(ind2keep, revinds[curpart_inds])

        np.sort(ind2keep)
        return (
         twin_inds, ind2keep)

    def get_unique_partition_indices(self, reindex=True):
        """
           This returns the indices for the partitions who are unique.  This could be larger than the
           indices for the unique coeficient since multiple partitions can give rise to the same coefficient.      In practice this has been very rare.  This function can take sometime for larger network with many      partitions since it reindex the partitions labels to ensure they aren't permutations of each other.

           :param reindex: if True, will reindex partitions that it is comparing to ensure they are unique under           permutation.
           :return: list of twin partition (can be empty), list of indicies of unique partitions.
           :rtype: list,np.array
           """
        _, uniq_inds = self._get_unique_twins_and_partition_indices(reindex=reindex)
        return uniq_inds

    def apply_CHAMP(self, subset=None, maxpt=None):
        """
                Apply CHAMP to the partition ensemble.

                :param maxpt: maximum domain threshhold for included partition.  I.e            partitions with a domain greater than maxpt will not be included in pruned              set
                :param subset: subset of partitions to apply CHAMP to.  This is useful in merging               two sets because we only need to apply champ to the combination of the two
                :type maxpt: int

                """
        if subset is None:
            self.ind2doms = get_intersection((self.get_coefficient_array()), max_pt=maxpt)
        else:
            cind2doms = get_intersection(self.get_coefficient_array(subset=subset), max_pt=maxpt)
            self.ind2doms = {subset[k]:val for k, val in cind2doms.items()}

    def get_CHAMP_indices(self):
        """
                Get the indices of the partitions that form the pruned set after application of                 CHAMP

                :return: list of indices of partitions that are included in the prune set               sorted by their domains of dominance
                :rtype: list

                """
        if not self.ismultilayer:
            inds = list(zip(self.ind2doms.keys(), [val[0][0] for val in self.ind2doms.values()]))
            inds.sort(key=(lambda x: x[1]))
        else:
            inds = list(zip(self.ind2doms.keys(), [min_dist_origin(val) for val in self.ind2doms.values()]))
            inds.sort(key=(lambda x: x[0]), cmp=(lambda x, y: point_comparator(x, y)))
        return [ind[0] for ind in inds]

    def get_CHAMP_partitions(self):
        """Return the subset of partitions that form the outer envelop.
                :return: List of partitions in membership vector form of the paritions
                :rtype: list

                """
        inds = self.get_CHAMP_indices()
        return [self.partitions[i] for i in inds]

    def _write_graph_to_hd5f_file(self, file, compress=4, intra=True):
        """
                Write the internal graph to hd5f file saving the edge lists, the edge properties, and the               vertex properties all as subgroups.  We only save the edges, and the vertex and node attributes

                :param file: openned h5py.File
                :type file: h5py.File
                :return: reference to the File
                """
        if not intra:
            if not self.ismultilayer:
                raise AssertionError('Cannot save interlayer graph to file because graph is not multilayer')
        keyname = 'graph' if intra else 'interlayer_graph'
        if keyname in file.keys():
            del file[keyname]
        grph = file.create_group(keyname)
        graph2save = self.graph if intra else self.interlayer_graph
        grph.create_dataset('directed', data=(int(graph2save.is_directed())))
        grph.create_dataset('num_nodes', data=(int(graph2save.vcount())))
        grph.create_dataset('edge_list', data=(np.array([e.tuple for e in graph2save.es])),
          compression='gzip',
          compression_opts=compress)
        edge_atts = grph.create_group('edge_attributes')
        for attrib in graph2save.edge_attributes():
            if is_py3 and type(graph2save.vs[attrib][0]) is str:
                dt = h5py.special_dtype(vlen=str)
                cdata = np.array([x.encode('utf8') for x in graph2save.es[attrib]])
                edge_atts.create_dataset(attrib, data=cdata, dtype=dt,
                  compression='gzip',
                  compression_opts=compress)
            else:
                edge_atts.create_dataset(attrib, data=(np.array(graph2save.es[attrib])),
                  compression='gzip',
                  compression_opts=compress)

        node_atts = grph.create_group('node_attributes')
        for attrib in graph2save.vertex_attributes():
            if is_py3:
                if type(graph2save.vs[attrib][0]) is str:
                    dt = h5py.special_dtype(vlen=str)
                    cdata = np.array([x.encode('utf8') for x in graph2save.vs[attrib]])
                    node_atts.create_dataset(attrib, data=cdata,
                      dtype=dt,
                      compression='gzip',
                      compression_opts=compress)
            else:
                node_atts.create_dataset(attrib, data=(np.array(graph2save.vs[attrib])),
                  compression='gzip',
                  compression_opts=compress)

        return file

    def _read_graph_from_hd5f_file(self, file, intra=True):
        """
                Load self.graph from hd5f file.  Sets self.graph as new igraph created from edge list           and attributes stored in the file.

                :param file: Opened hd5f file that contains the edge list, edge attributes, and                 node attributes stored in the hierarchy as PartitionEnsemble._write_graph_to_hd5f_file.
                :param intra: read the intralayer connections graph (if false reads the interlayer_graph)
                :type file: h5py.File

                """
        if intra:
            grph = file['graph']
            directed = bool(grph['directed'].value)
            num_nodes = grph['num_nodes'].value
            self.graph = ig.Graph(n=num_nodes).TupleList((grph['edge_list']), directed=directed)
            for attrib in grph['edge_attributes'].keys():
                self.graph.es[attrib] = grph['edge_attributes'][attrib][:]

            for attrib in grph['node_attributes'].keys():
                self.graph.vs[attrib] = grph['node_attributes'][attrib][:]

        else:
            grph = file['interlayer_graph']
            num_nodes = grph['num_nodes'].value
            directed = bool(grph['directed'].value)
            self.interlayer_graph = ig.Graph(n=num_nodes).TupleList((grph['edge_list']), directed=directed)
            for attrib in grph['edge_attributes'].keys():
                self.interlayer_graph.es[attrib] = grph['edge_attributes'][attrib][:]

            for attrib in grph['node_attributes'].keys():
                self.interlayer_graph.vs[attrib] = grph['node_attributes'][attrib][:]

    def save(self, filename=None, dir='.', hdf5=True, compress=9):
        r"""
                Use pickle or h5py to store representation of PartitionEnsemble in compressed file.  When called                if object has an assocated hdf5_file, this is the default file written to.  Otherwise objected          is stored using pickle.

                :param filename: name of file to write to.  Default is created from name of ParititonEnsemble\:                         "%s_PartEnsemble_%d" %(self.name,self.numparts)
                :param hdf5: save the PartitionEnsemble object as a hdf5 file.  This is                 very useful for larger partition sets, especially when you only need to work            with the optimal subset.  If object has hdf5_file attribute saved               this becomes the default
                :type hdf5: bool
                :param compress: Level of compression for partitions in hdf5 file.  With less compression, files take           longer to write but take up more space.  9 is default.
                :type compress: int [0,9]
                :param dir: directory to save graph in.  relative or absolute path.  default is working dir.
                :type dir: str
                """
        if filename is None:
            if hdf5:
                if self._hdf5_file is None:
                    filename = '%s_PartEnsemble_%d.hdf5' % (self.name, self.numparts)
                    filename = os.path.join(dir, filename)
                else:
                    filename = self._hdf5_file
            else:
                filename = '%s_PartEnsemble_%d.gz' % (self.name, self.numparts)
        else:
            if hdf5:
                filename = os.path.join(dir, filename)
                with h5py.File(filename, 'w') as (outfile):
                    for k, val in iteritems(self.__dict__):
                        if k == 'graph':
                            self._write_graph_to_hd5f_file(outfile, compress=compress)
                        elif k == 'interlayer_graph':
                            if self.__dict__[k] is not None:
                                self._write_graph_to_hd5f_file(outfile, compress=compress, intra=False)
                        elif isinstance(val, dict):
                            indgrp = outfile.create_group(k)
                            for ind, dom in iteritems(val):
                                indgrp.create_dataset((str(ind)), data=dom, compression='gzip', compression_opts=compress)

                        elif isinstance(val, str):
                            outfile.create_dataset(k, data=val)
                        elif isinstance(val, pd.DataFrame):
                            grp = outfile.create_group(k)
                            cvalues = val.values
                            rows = val.index
                            columns = val.columns
                            rshape = list(rows.shape)
                            rshape[0] = None
                            rshape = tuple(rshape)
                            cshape = list(rows.shape)
                            cshape[0] = None
                            cshape = tuple(cshape)
                            grp.create_dataset('values', cvalues)
                            grp.create_dataset('index', data=rows, maxshape=rshape, compression='gzip',
                              compression_opts=compress)
                            grp.create_dataset('index', data=columns, maxshape=cshape, compression='gzip',
                              compression_opts=compress)
                        elif hasattr(val, '__len__'):
                            data = np.array(val)
                            cshape = list(data.shape)
                            cshape[0] = None
                            cshape = tuple(cshape)
                            try:
                                cdset = outfile.create_dataset(k, data=data, maxshape=cshape, compression='gzip',
                                  compression_opts=compress)
                            except TypeError:
                                dt = h5py.special_dtype(vlen=str)
                                data = np.array([str(x).encode('utf8') for x in data])
                                cdset = outfile.create_dataset(k, data=data, maxshape=cshape, compression='gzip',
                                  compression_opts=compress,
                                  dtype=dt)

                        else:
                            if val is not None:
                                cdset = outfile.create_dataset(k, data=val)

                self._hdf5_file = filename
            else:
                with gzip.open(os.path.join(dir, filename), 'wb') as (fh):
                    pickle.dump(self, fh)
        return filename

    def save_graph(self, filename=None, dir='.', intra=True):
        """
                Save a copy of the graph with each of the optimal partitions stored as vertex attributes                in graphml compressed format.  Each partition is attribute names part_gamma where gamma is              the beginning of the partitions domain of dominance.  Note that this is seperate from the information           about the graph that is saved within the hdf5 file along side the partions.

                :param filename: name of file to write out to.  Default is self.name.graphml.gz or              :type filename: str
                :param dir: directory to save graph in.  relative or absolute path.  default is working dir.
                :type dir: str
                """
        if not intra:
            if not self.multlayer:
                raise AssertionError('cannot save interlayer edges if graph is not multilayered')
        if filename is None:
            if intra:
                filename = self.name + '.graphml.gz'
            else:
                filename = self.name + 'interlayer.graphml.gz'
        outgraph = self.graph.copy() if intra else self.interlayer_graph.copy()
        for ind in self.get_CHAMP_indices():
            part_name = 'part_%.3f' % self.ind2doms[ind][0][0]
            outgraph.vs[part_name] = self.partitions[ind]

        outgraph.write_graphmlz(os.path.join(dir, filename))
        return filename

    def _load_datafame_from_hdf5_file(self, file, key):
        values = file[key]['values'][:]
        index = file[key]['index'][:]
        columns = file[key]['columns'][:]
        outdf = pd.DataFrame(values, index=index, columns=columns)
        return outdf

    def open(self, filename):
        """
                Loads pickled PartitionEnsemble from file.

                :param file:  filename of pickled PartitionEnsemble Object

                :return: writes over current instance and returns the reference

                """
        try:
            with h5py.File(filename, 'r') as (infile):
                self._read_graph_from_hd5f_file(infile, intra=True)
                if infile['ismultilayer'].value:
                    self._read_graph_from_hd5f_file(infile, intra=False)
                for key in infile.keys():
                    if key != 'graph' and key != '_partitions' and key != 'interlayer_graph':
                        if key == 'ind2doms':
                            self.ind2doms = {}
                            for ind in infile[key]:
                                self.ind2doms[int(ind)] = infile[key][ind][:]

                        else:
                            try:
                                carray = infile[key][:]
                                if re.search('object', str(infile[key][:].dtype)):
                                    new_array = []
                                    for x in carray:
                                        try:
                                            new_array.append(eval(infile[key][:][0]))
                                        except ValueError:
                                            new_array.append(x)

                                    carray = np.array(new_array)
                                    self.__dict__[key] = carray
                                else:
                                    self.__dict__[key] = infile[key][:]
                            except ValueError:
                                self.__dict__[key] = infile[key].value

            self._hdf5_file = filename
            return self
        except IOError:
            with gzip.open(filename, 'rb') as (fh):
                opened = pickle.load(fh)
            openedparts = opened.get_partition_dictionary()
            self.__init__((opened.graph), listofparts=openedparts)
            return self

    def _sub_tex(self, str):
        new_str = re.sub('\\$', '', str)
        new_str = re.sub('\\\\ge', '>=', new_str)
        new_str = re.sub('\\\\', '', new_str)
        return new_str

    def _remove_tex_legend(self, legend):
        for text in legend.get_texts():
            text.set_text(self._sub_tex(text.get_text()))

        return legend

    def _remove_tex_axes(self, axes):
        axes.set_title(self._sub_tex(axes.get_title()))
        axes.set_xlabel(self._sub_tex(axes.get_xlabel()))
        axes.set_ylabel(self._sub_tex(axes.get_ylabel()))
        return axes

    def plot_modularity_mapping(self, ax=None, downsample=2000, champ_only=False, legend=True, no_tex=True):
        r"""

                Plot a scatter of the original modularity vs gamma with the modularity envelope super imposed.          Along with communities vs :math:`\gamma` on a twin axis.  If no orig_mod values are stored in the               ensemble, just the modularity envelope is plotted.  Depending on the backend used to render plot                the latex in the labels can cause error.  If you are getting RunTime errors when showing or saving              the plot, try setting no_tex=True

                :param ax: axes to draw the figure on.
                :type ax: matplotlib.Axes
                :param champ_only: Only plot the modularity envelop represented by the CHAMP identified subset.
                :type champ_only: bool
                :param downsample: for large number of runs, we down sample the scatter for the number of communities           and the original partition set.  Default is 2000 randomly selected partitions.
                :type downsample: int
                :param legend: Add legend to the figure.  Default is true
                :type legend: bool
                :param no_tex: Use latex in the legends.  Default is true.  If error is thrown on plotting try setting          this to false.
                :type no_tex: bool
                :return: axes drawn upon
                :rtype: matplotlib.Axes

                """
        if not not self.ismultilayer:
            raise AssertionError('plot_modularity_mapping is for the single layer case.  For multilayer please use plot_2d_modularity_domains')
        else:
            if ax == None:
                f = plt.figure()
                ax = f.add_subplot(111)
            else:
                if not no_tex:
                    rc('text', usetex=True)
                else:
                    rc('text', usetex=False)
                if downsample:
                    if downsample <= len(self.partitions):
                        rand_ind = np.random.choice((range(len(self.partitions))), size=downsample)
                else:
                    rand_ind = range(len(self.partitions))
                allgams = [self.resolutions[ind] for ind in rand_ind]
                allcoms = [self.numcoms[ind] for ind in rand_ind]
                if not champ_only and self.orig_mods[0] is not None:
                    allmods = [self.orig_mods[ind] for ind in rand_ind]
                    ax.set_ylim([np.min(allmods) - 100, np.max(allmods) + 100])
                    mk1 = ax.scatter(allgams, allmods, color='red',
                      marker='.',
                      alpha=0.6,
                      s=10,
                      label='modularity',
                      zorder=2)
                champ_inds = self.get_CHAMP_indices()
                gammas = [self.ind2doms[ind][0][0] for ind in champ_inds]
                mods = [self.ind2doms[ind][0][1] for ind in champ_inds]
                champ_coms = [self.numcoms[ind] for ind in champ_inds]
                mk5 = ax.plot(gammas, mods, ls='--', color='green', lw=3, zorder=3)
                mk5 = mlines.Line2D([], [], color='green', ls='--', lw=3)
                mk2 = ax.scatter(gammas, mods, marker='v', color='blue', s=200, zorder=4)
                ax.set_ylabel('modularity')
                a2 = ax.twinx()
                a2.grid('off')
                sct2 = a2.scatter(allgams, allcoms, marker='^', color='#91AEC1', alpha=1,
                  label=('\\# communities ($\\ge %d$ nodes)' % self._min_com_size),
                  zorder=1)
                mk3 = a2.scatter([], [], marker='^', color='#91AEC1', alpha=1, label=('\\# communities ($\\ge %d$)' % self._min_com_size),
                  zorder=1,
                  s=20)
                stp = a2.step(gammas, champ_coms, color='#004F2D', where='post', path_effects=[
                 path_effects.SimpleLineShadow(alpha=0.5), path_effects.Normal()])
                mk4 = mlines.Line2D([], [], color='#004F2D', lw=2, path_effects=[
                 path_effects.SimpleLineShadow(alpha=0.5), path_effects.Normal()])
                a2.set_ylabel('\\# communities ($\\ge 5$ nodes)')
                ax.set_zorder(a2.get_zorder() + 1)
                ax.patch.set_visible(False)
                ax.set_xlim(xmin=0, xmax=(max(allgams)))
                if champ_only:
                    leg_set = [
                     mk3, mk2, mk4, mk5]
                    leg_text = ['\\# communities ($\\ge %d $ nodes)' % self._min_com_size, 'transitions,$\\gamma$',
                     '\\# communities ($\\ge %d$ nodes) optimal' % self._min_com_size, 'convex hull of $Q(\\gamma)$']
                else:
                    leg_set = [
                     mk1, mk3, mk2, mk4, mk5]
                    leg_text = ['modularity', '\\# communities ($\\ge %d $ nodes)' % self._min_com_size, 'transitions,$\\gamma$',
                     '\\# communities ($\\ge %d$ nodes) optimal' % self._min_com_size, 'convex hull of $Q(\\gamma)$']
                if legend:
                    l = ax.legend(leg_set, leg_text,
                      bbox_to_anchor=[
                     0.5, 0.87],
                      loc='center',
                      frameon=True,
                      fontsize=14)
                    l.get_frame().set_fill(False)
                    l.get_frame().set_ec('k')
                    l.get_frame().set_linewidth(1)
                    if no_tex:
                        l = self._remove_tex_legend(l)
            if no_tex:
                a2 = self._remove_tex_axes(a2)
                ax = self._remove_tex_axes(ax)
        return ax

    def plot_2d_modularity_domains(self, ax=None, col=None):
        """Handle to call plot_domains.plot_2d_domains

                :param ax: matplotlib.Axes on which to plot the figure.
                :param col:
                :return:
                """
        return plot_2d_domains((self.ind2doms), ax=ax, col=col)

    def plot_multiplex_communities(self, ind, ax=None):
        """
                This only works well if the network is multiplex.  Plots the square with
                each layer representing a column
                :return: matplotlib.Axes
                """
        assert self.ismultilayer, 'Can only plot with multilayer PartitionEnsemble'
        return plot_multilayer_pd((self.partitions[ind]), (self.layer_vec), ax=ax, cmap=None)

    def plot_2d_modularity_domains_with_AMI(self, true_part, ax=None, cmap=None, colorbar_ax=None):
        """

                :param true_part:
                :param ax:
                :param cmap: color map withwhich to depcit the AMI of the partions with the t
                :param colorbar_ax: In case a color bar is desired the user can provide a seperate axes         on which to plot the color bar.
                :return:
                """
        nmis = []
        if cmap is None:
            cmap = sbn.cubehelix_palette(as_cmap=True)
        cnorm = mc.Normalize(vmin=0, vmax=1.0)
        for ind in self.ind2doms:
            nmis.append(skm.adjusted_mutual_info_score(self.partitions[ind], true_part))

        colors = list(map(lambda x: cmap(cnorm(x)), nmis))
        a = self.plot_2d_modularity_domains(ax=ax, col=colors)
        if colorbar_ax is not None:
            cb1 = mcb.ColorbarBase(colorbar_ax, cmap=cmap, norm=cnorm,
              orientation='vertical')
        return a