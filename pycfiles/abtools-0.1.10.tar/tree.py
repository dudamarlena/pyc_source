# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryanbriney/git/abtools/abtools/phylogeny/tree.py
# Compiled at: 2016-06-09 17:12:18
import os, subprocess as sp, ete2

def make_tree(alignment, timepoints, delimiter, is_aa, scale, branch_vert_margin, fontsize, show_name, tree_orientation, show_scale=False):
    """
    Builds a tree file (using FastTree) from a sequence alignment in FASTA format

    Input
    path to a FASTA-formatted sequence alignment

    Output
    path to a Newick-formatted tree file
    """
    tree = alignment.replace('_aligned.aln', '_tree.nw')
    tree = fast_tree(alignment, tree, is_aa)
    make_figure(tree, timepoints, delimiter, scale, branch_vert_margin, fontsize, show_name, tree_orientation, show_scale=show_scale)


def fast_tree(alignment, tree, is_aa, show_output=False):
    if is_aa:
        ft_cmd = ('fasttree {} > {}').format(alignment, tree)
    else:
        ft_cmd = ('fasttree -nt {} > {}').format(alignment, tree)
    ft = sp.Popen(ft_cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    stdout, stderr = ft.communicate()
    if show_output:
        print ft_cmd
        print stdout
        print stderr
    return tree


def make_figure(tree, timepoints, delimiter, scale, branch_vert_margin, fontsize, show_name, tree_orientation, show_scale=False):
    fig = tree.replace('_tree.nw', '_tree.pdf')
    orders = {tp.name:tp.order for tp in timepoints}
    colors = {tp.name:tp.color for tp in timepoints}
    if show_name == 'none':
        show_name = []
    if show_name == 'all':
        show_name = [
         'mab', 'root', 'input']
    else:
        if show_name == 'no-root':
            show_name = [
             'input', 'mab']
        elif type(show_name) in [str, unicode]:
            show_name = [
             show_name]
        t = ete2.Tree(tree)
        t.set_outgroup(t & 'root')
        for node in t.traverse():
            earliest = get_earliest_leaf(node.get_leaf_names(), orders, delimiter)
            color = colors[earliest]
            node_type = get_node_type(node.name)
            style = ete2.NodeStyle()
            style['size'] = 0
            style['vt_line_width'] = 1.0
            style['hz_line_width'] = 1.0
            style['vt_line_color'] = color
            style['hz_line_color'] = color
            style['vt_line_type'] = 0
            style['hz_line_type'] = 0
            if node_type in show_name:
                if node_type in ('mab', 'input'):
                    name = ' ' + delimiter.join(node.name.split(delimiter)[1:])
                else:
                    name = ' ' + node.name
                tf = ete2.TextFace(name)
                tf.fsize = fontsize
                node.add_face(tf, column=0)
                style['fgcolor'] = '#000000'
            node.set_style(style)

    t.dist = 0
    ts = ete2.TreeStyle()
    ts.orientation = tree_orientation
    ts.show_leaf_name = False
    if scale:
        ts.scale = int(scale)
    if branch_vert_margin:
        ts.branch_vertical_margin = float(branch_vert_margin)
    ts.show_scale = False
    t.ladderize()
    t.render(fig, tree_style=ts)


def get_node_type(node_name):
    if node_name == 'root':
        return 'root'
    if node_name.startswith('mab'):
        return 'mab'
    if node_name == 'NoName':
        return 'inner'
    return 'input'


def get_earliest_leaf(leaves, order, delimiter):
    counts = {}
    for leaf in leaves:
        tp = leaf.split(delimiter)[0]
        counts[tp] = counts[tp] + 1 if tp in counts else 1

    total = sum(counts.values())
    if 'root' in counts:
        return 'root'
    timepoints = sorted(counts.keys(), key=lambda x: order[x])
    for tp in timepoints:
        if 100.0 * counts[tp] / total >= 5:
            return tp