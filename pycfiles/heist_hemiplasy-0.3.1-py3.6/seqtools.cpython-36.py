# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/heist/seqtools.py
# Compiled at: 2020-04-19 12:04:38
# Size of source mod 2**32: 16222 bytes
from itertools import zip_longest
from Bio.Phylo.Consensus import _BitString
from Bio import Phylo
import io, re
resultss = 0

def grouper(iterable, n, fillvalue=None):
    """
    Utility function
    """
    args = [
     iter(iterable)] * n
    return zip_longest(*args, **{'fillvalue': fillvalue})


def cluster(d):
    """
    Utility function
    """
    clusters = {}
    for key, val in d.items():
        clusters.setdefault(val, []).append(key)

    return clusters


def getSisters(tree, t='g'):
    """Some nasty regex to get pairs of sister taxa
    (only at terminal branches)"""
    if t == 's':
        l = re.findall('\\(([1-9][0-9]|\\d),([1-9][0-9]|\\d)\\)', tree)
    else:
        l = re.findall('\\(([1-9][0-9]|\\d):\\d\\.\\d\\d\\d,([1-9][0-9]|\\d):\\d\\.\\d\\d\\d\\)', tree)
    return l


def checkEqual(lst):
    """
    Utility function
    """
    return lst[1:] == lst[:-1]


def readSeqs(seqs, ntaxa, speciesPattern, nodes, batch, prefix, breaks=0):
    """
    Reads in sequences, determines if gene tree site pattern matches species tree
    site pattern. Returns indices of those which do.
    """
    indices = []
    c = cluster(speciesPattern)
    shouldMatch1 = c[0]
    shouldMatch2 = c[1]
    counts = [0, 0]
    tmpFocal = open(prefix + '.focaltrees.tmp', 'w')
    index = 0
    iii = 0
    p = ntaxa + nodes
    with open(seqs, 'rU') as (f):
        block = []
        tax = []
        for lines in f:
            if iii < p:
                l = lines.replace('\n', '').split()
                if l[1] in ('A', 'T', 'C', 'G'):
                    tax.append(l[0])
                    block.append(l[1])
                    iii += 1
            else:
                if iii == p:
                    iii = 0
                    assert len(block) == ntaxa + nodes
                    pattern = {}
                    for x, line in enumerate(block):
                        pattern[str(tax[x])] = str(line)

                    block = []
                    tax = []
                    levels = set()
                    for key, val in pattern.items():
                        if int(key) in range(1, ntaxa + 1):
                            levels.add(val)

                    if len(levels) == 2:
                        a = []
                        for taxa in shouldMatch1:
                            a.append(pattern[str(taxa)])

                        if checkEqual(a):
                            b = []
                            for taxa in shouldMatch2:
                                b.append(pattern[str(taxa)])

                            if checkEqual(b):
                                if b[0] != pattern[str(ntaxa + 1)]:
                                    indices.append(index + 1)
                                    tmpFocal.write(' 10 1\n')
                                    for k, v in pattern.items():
                                        tmpFocal.write(k + '\t' + v + '\n')

                                    if index < breaks:
                                        counts[0] += 1
                                    else:
                                        counts[1] += 1
                    index += 1

    tmpFocal.close()
    return (indices, counts)


def readSeqs2(seqs, ntaxa, speciesPattern, nodes, batch, prefix, breaks=[]):
    """
    Reads in sequences, determines if gene tree site pattern matches species tree
    site pattern. Returns indices of those which do.
    """
    indices = []
    c = cluster(speciesPattern)
    shouldMatch1 = c[0]
    shouldMatch2 = c[1]
    if len(breaks) != 0:
        counts = [
         0] * len(breaks)
    else:
        counts = [
         0]
    tmpFocal = open(prefix + '.focaltrees.tmp', 'w')
    index = 0
    with open(seqs, 'rU') as (f):
        for lines in grouper(f, ntaxa + nodes + 1, ''):
            assert len(lines) == ntaxa + nodes + 1
            pattern = {}
            for x, line in enumerate(lines):
                if x != 0:
                    l = line.replace('\n', '').split()
                    pattern[str(l[0])] = str(l[1])

            levels = set()
            for key, val in pattern.items():
                if int(key) in range(1, ntaxa + 1):
                    levels.add(val)

            if len(levels) == 2:
                a = []
                for taxa in shouldMatch1:
                    a.append(pattern[str(taxa)])

                if checkEqual(a):
                    b = []
                    for taxa in shouldMatch2:
                        b.append(pattern[str(taxa)])

                    if checkEqual(b):
                        if b[0] != pattern[str(ntaxa + 1)]:
                            indices.append(index)
                            for y in lines:
                                tmpFocal.write(y)

                            if len(breaks) != 0:
                                tree_class = 0
                                for i, breakpoint in enumerate(breaks):
                                    if i != 0:
                                        if index <= breakpoint:
                                            if index > breaks[(i - 1)]:
                                                tree_class = i
                                        elif index <= breakpoint:
                                            tree_class = i

                                counts[tree_class] += 1
                            else:
                                counts[0] += 1
            index += 1

    tmpFocal.close()
    return (
     indices, counts)


def getTrees(treefile, matchlist):
    """
    Returns list of trees at indices obtained from readSeqs
    """
    focal_trees = []
    trees = open(treefile, 'r')
    i = 0
    for line in trees:
        l = line.replace('\n', '')
        if len(l) > 3:
            i += 1
            if i in matchlist:
                focal_trees.append(l)

    trees.close()
    return (
     focal_trees, 0)


def _bitstrs(tree):
    bitstrs = set()
    term_names = [term.name for term in tree.get_terminals()]
    term_names.sort()
    for clade in tree.get_nonterminals():
        clade_term_names = [term.name for term in clade.get_terminals()]
        boolvals = [name in clade_term_names for name in term_names]
        bitstr = _BitString(''.join(map(str, map(int, boolvals))))
        bitstrs.add(bitstr)

    return bitstrs


def rev(sis):
    """Utility function"""
    return (
     sis[1], sis[0])


def compareToSpecies(tree1, tree2, spp_sisters=None):
    """Compares tree topologies. Will first check if sister taxa in the species tree are also sister 
    in the gene tree, returning false at the first non-shared occurence. If all sister taxa are present,
    it will calculate a bitstring distance with Biopython Phylo."""
    if spp_sisters == None:
        spp_sisters = getSisters(tree1)
    sisters = getSisters(tree2)
    top = bool
    for s in sisters:
        if s not in spp_sisters:
            if rev(s) not in spp_sisters:
                return False

    tree1 = tree1.replace(';', '')
    tree2 = tree2.replace(';', '')
    tree1 = Phylo.read(io.StringIO(tree1), 'newick')
    tree2 = Phylo.read(io.StringIO(tree2), 'newick')
    term_names1 = [term.name for term in tree1.get_terminals()]
    term_names2 = [term.name for term in tree2.get_terminals()]
    if set(term_names1) != set(term_names2):
        return False
    else:
        if _bitstrs(tree1) == _bitstrs(tree2):
            return True
        return False


def propDiscordant(focal_trees, species_tree):
    """
    Original function
    Determines the proportion of focal_trees (which have the same site pattern as the
    species tree) which are discordant (i.e. have a different topology)
    """
    i = 0
    countDis = 0
    disc_g = []
    conc_g = []
    spp_sisters = getSisters(species_tree, 's')
    for i, tree in enumerate(focal_trees):
        r = call(species_tree, tree, spp_sisters, i)
        if r[0] == 1:
            disc_g.append(r[1])
            countDis += 1
        else:
            if r[0] == 0:
                conc_g.append(r[1])

    try:
        return (
         [
          countDis, len(focal_trees), countDis / len(focal_trees)],
         disc_g,
         conc_g)
    except ZeroDivisionError:
        return (
         [
          countDis, len(focal_trees), 0.0], disc_g, conc_g)


def call(species_tree, tree, spp_sisters, i):
    """Function to make parallel calling easier"""
    if compareToSpecies(species_tree, tree, spp_sisters) is False:
        return [1, i]
    else:
        return [
         0, i]


def parse_seqgen(seqfile, ntaxa, mask):
    """
    Parses seq-gen file. Returns a list of ordered 
    taxon-allele pairs for each tree.   
    """
    lines = []
    with open(seqfile) as (seqs):
        for line in seqs:
            if re.match('\\w', line):
                lines.append(str.strip(line))

    lines = [lines[i].replace('\t', ' ') for i in range(len(lines))]
    trees = [lines[i:i + ntaxa * 2 - 1] for i in range(0, len(lines), ntaxa * 2 - 1)]
    return [trees[i] for i in mask]


def count_mutations(tree, ntaxa):
    """
    Takes pairs of taxa/nodes and alleles,
    and returns the number of mutations that
    happened along the tree. Pairs must be ordered
    in same way as seq-gen output.
    """
    labels = [int(tree[i].split()[0]) for i in range(len(tree))]
    alleles = [tree[i].split()[1] for i in range(len(tree))]
    root = ntaxa + 1
    comparisons = []
    current_taxon = 1
    mutations = 0
    while current_taxon <= ntaxa:
        for i in range(len(labels)):
            if labels[i] > root and labels[(i - 1)] >= root and labels[i] == labels[(i - 1)] + 1:
                if [
                 labels[i],
                 labels[(i - 1)]] not in comparisons:
                    if alleles[i] != alleles[(i - 1)]:
                        mutations += 1
                        comparisons.append([labels[i], labels[(i - 1)]])
                    else:
                        comparisons.append([labels[i], labels[(i - 1)]])
            elif labels[i] > root and labels[(i - 2)] >= root and labels[i] == labels[(i - 2)] + 1:
                if [
                 labels[i],
                 labels[(i - 2)]] not in comparisons:
                    if alleles[i] != alleles[(i - 2)]:
                        mutations += 1
                        comparisons.append([labels[i], labels[(i - 2)]])
                    else:
                        comparisons.append([labels[i], labels[(i - 2)]])
            elif labels[i] > root and labels[(i - 3)] >= root and labels[i] == labels[(i - 3)] + 1:
                if [
                 labels[i],
                 labels[(i - 3)]] not in comparisons:
                    if alleles[i] != alleles[(i - 3)]:
                        mutations += 1
                        comparisons.append([labels[i], labels[(i - 3)]])
                    else:
                        comparisons.append([labels[i], labels[(i - 3)]])
            elif labels[i] > root and labels[(i - 4)] >= root and labels[i] == labels[(i - 4)] + 2:
                if [
                 labels[i],
                 labels[(i - 4)]] not in comparisons:
                    if alleles[i] != alleles[(i - 4)]:
                        mutations += 1
                        comparisons.append([labels[i], labels[(i - 4)]])
                    else:
                        comparisons.append([labels[i], labels[(i - 4)]])
            else:
                if labels[i] == current_taxon:
                    if labels[(i - 1)] >= root:
                        if alleles[i] != alleles[(i - 1)]:
                            mutations += 1
                    else:
                        if labels[(i - 2)] >= root:
                            if alleles[i] != alleles[(i - 2)]:
                                mutations += 1
                        current_taxon += 1

    return mutations


def get_interesting(trees, nderived, ntaxa):
    """
    This function uses count_mutations to
    pull out all the "interesting" cases of
    incongruence. For now, these are cases
    where the number of mutations is greater
    than 1 but less than the number of derived
    taxa.
    """
    interesting = []
    for index, tree in enumerate(trees):
        if count_mutations(tree, ntaxa) > 1 and count_mutations(tree, ntaxa) < nderived:
            interesting.append(tree)

    return interesting


def summarize_interesting(tree, ntaxa):
    """
    Summarizes the mutations that have occurred
    on the given tree.
    """
    labels = [int(tree[i].split()[0]) for i in range(len(tree))]
    alleles = [tree[i].split()[1] for i in range(len(tree))]
    root = ntaxa + 1
    current_taxon = 1
    ancestral_allele = alleles[labels.index(root)]
    summary = []
    while current_taxon <= ntaxa:
        for i in range(len(labels)):
            if labels[i] == current_taxon:
                if alleles[i] == ancestral_allele:
                    current_taxon += 1
                elif alleles[i] != ancestral_allele:
                    if labels[(i - 1)] >= root:
                        if alleles[i] != alleles[(i - 1)]:
                            summary.append((str(labels[i]), 1, str(0)))
                        else:
                            summary.append((str(labels[i]), 0, str(labels[(i - 1)])))
                    else:
                        if labels[(i - 2)] >= root:
                            if alleles[i] != alleles[(i - 2)]:
                                summary.append((str(labels[i]), 1, str(0)))
                            else:
                                summary.append((str(labels[i]), 0, str(labels[(i - 2)])))
                        current_taxon += 1

    return summary


def sum_counts_by_tree(counts):
    newcounts = [
     0] * len(counts[0])
    for batch in counts:
        for i, c in enumerate(batch):
            newcounts[i] += c

    return newcounts