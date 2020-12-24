# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/graph.py
# Compiled at: 2014-10-03 15:18:32
import bct, numpy as np, scipy.io as sio
from collections import OrderedDict
from traits.api import HasTraits, Str, Any, List
from traitsui.api import View, Item, TabularEditor
from traitsui.tabular_adapter import TabularAdapter

class StatisticsDisplay(HasTraits):
    name = Str
    stat = Any
    display_chart = Any

    def __init__(self, name, stat, labels, **kwargs):
        super(HasTraits, self).__init__(**kwargs)
        self.name = name
        if np.size(stat) == 1:
            self.stat = stat
            self.display_chart = np.array((('', '%.3f' % stat),))
        elif np.size(stat) != len(labels):
            raise ValueError('Size of graph statistic inconsistent')
        else:
            nr_labels = len(labels)
            self.stat = stat.reshape((nr_labels, 1))
            self.display_chart = np.append(np.reshape(labels, (nr_labels, 1)), np.reshape(map(lambda nr: '%.3f' % nr, stat), (nr_labels, 1)), axis=1)

    traits_view = View(Item('display_chart', editor=TabularEditor(adapter=TabularAdapter(columns=['', '']), editable=False, show_titles=True), height=300, width=225, show_label=False))


def calculate_modules(adj):
    ci, _ = bct.modularity_louvain_und(adj)
    ci2, _ = bct.modularity_finetune_und(adj, ci=ci)
    return ci2


def do_summary(adj, mods, opts):
    stats = OrderedDict()
    for opt in opts:
        if opt in ('modularity', 'participation coefficient', 'within-module degree') and mods is None:
            import cvu_utils as util
            raise util.CVUError('Need Modules')

    for opt in opts:
        stats.update({opt: do_opt(adj, mods, opt)})

    return stats


def do_opt(adj, mods, option):
    if option == 'global efficiency':
        return bct.efficiency_wei(adj)
    if option == 'local efficiency':
        return bct.efficiency_wei(adj, local=True)
    if option == 'average strength':
        return bct.strengths_und(adj)
    if option == 'clustering coefficient':
        return bct.clustering_coef_wu(adj)
    if option == 'eigenvector centrality':
        return bct.eigenvector_centrality_und(adj)
    if option == 'binary kcore':
        return bct.kcoreness_centrality_bu(adj)[0]
    if option == 'modularity':
        return bct.modularity_und(adj, mods)[1]
    if option == 'participation coefficient':
        return bct.participation_coef(adj, mods)
    if option == 'within-module degree':
        return bct.module_degree_zscore(adj, mods)