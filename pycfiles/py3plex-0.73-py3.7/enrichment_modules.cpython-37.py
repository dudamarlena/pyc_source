# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/enrichment_modules.py
# Compiled at: 2019-12-03 00:25:58
# Size of source mod 2**32: 7746 bytes
from scipy.stats import fisher_exact
import multiprocessing as mp, random
from statsmodels.sandbox.stats.multicomp import multipletests
from collections import defaultdict, Counter
from ..term_parsers import parse_gaf_file, read_termlist, read_topology_mappings, read_uniprot_GO
import pandas as pd, numpy as np, logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

def calculate_pval(term, alternative='two-sided'):
    """
    Parallel kernel for computation of p vals. All partitions are considered with respect to agiven GO term! Counts in a given partition are compared to population.

    """
    query_term = term[0]
    query_term_count_population = term[1]
    inside_local = 0
    outside_local = 0
    for x in _partition_entries:
        terms = _map_term_database[x]
        if query_term in terms:
            inside_local += 1
        else:
            outside_local += 1

    if _normalize_by_comsize:
        query_term_count_population = int(query_term_count_population / _number_of_communities)
    elif inside_local > 1:
        query_counts = [
         inside_local - 1, query_term_count_population]
    else:
        query_counts = [
         inside_local, query_term_count_population]
    pop_counts = [
     outside_local, _number_of_all_annotated - query_term_count_population]
    p_value = fisher_exact([query_counts, pop_counts], alternative=alternative)[1]
    return p_value


def multiple_test_correction(input_dataset):
    """
    Multiple test correction. Given a dataset with corresponding significance levels, perform MTC.
    """
    from statsmodels.sandbox.stats.multicomp import multipletests
    pvals = defaultdict(list)
    with open(input_dataset) as (ods):
        for line in ods:
            try:
                component, term, pval = line.split()
                pvals[component].append((term, pval))
            except:
                pass

    logging.info('Component_by_size PFAM_term pvalue')
    for key, values in pvals.items():
        tmpP = [float(val[1]) for val in values]
        termN = [val[0] for val in values]
        significant, pvals, sidak, bonf = multipletests(tmpP, method='hs', is_sorted=False, returnsorted=False)
        output = zip(termN, significant, pvals, tmpP)
        for term, significant, pval, tmp in output:
            if significant == True:
                print(key, term, significant, tmp, pval)


def parallel_enrichment(term):
    """
    A simple kernel for parallel computation of p-values. (assuming independence of experiments)
    """
    pval = calculate_pval((_term_database[term]), alternative=_alternative)
    return {'observation':_partition_name,  'term':_term_database[term][0],  'pval':pval}


def compute_enrichment(term_dataset, term_database, topology_map, all_counts, whole_term_list=False, pvalue=0.05, multitest_method='fdr_bh', alternative='two-sided', intra_community=False):
    """
    The main method for computing the enrichment of a subnetwork. This work in parallel and also offers methods for multiple test correction.
    """
    global _alternative
    global _map_term_database
    global _normalize_by_comsize
    global _number_of_all_annotated
    global _number_of_communities
    global _partition_entries
    global _partition_name
    global _term_database
    if whole_term_list:
        tvals = (set.union)(*[x for x in topology_map.values()])
        topology_map = {}
        topology_map['1_community'] = tvals
    _alternative = alternative
    _number_of_all_annotated = all_counts
    _term_database = {en:x for en, x in enumerate(term_database.items())}
    _map_term_database = term_dataset
    _number_of_communities = len(topology_map)
    _normalize_by_comsize = intra_community
    if intra_community:
        _number_of_all_annotated = int(_number_of_all_annotated / _number_of_communities)
    finalFrame = pd.DataFrame()
    for k, v in topology_map.items():
        logging.info('Computing enrichment for partition {}'.format(k))
        _partition_name = k
        _partition_entries = v
        ncpu = 2
        n = len(term_database)
        step = ncpu
        jobs = [range(n)[i:i + step] for i in range(0, n, step)]
        tmpframe = pd.DataFrame(columns=['observation', 'term', 'pval'])
        results = [parallel_enrichment(x) for x in range(n)]
        tmpframe = tmpframe.append(results, ignore_index=True)
        if multitest_method == 'raw':
            tmpframe = tmpframe[(tmpframe['pval'] < pvalue)]
        else:
            significant, p_adjusted, sidak, bonf = multipletests((tmpframe['pval']), method=multitest_method, is_sorted=False, returnsorted=False, alpha=pvalue)
            tmpframe['corrected_pval_' + multitest_method] = pd.Series(p_adjusted)
            tmpframe['significant'] = pd.Series(significant)
            tmpframe = tmpframe[(tmpframe['significant'] == True)]
        finalFrame = finalFrame.append(tmpframe, ignore_index=True)

    return finalFrame


def fet_enrichment_generic(term_dataset, term_database, all_counts, topology_map):
    """
    A generic enrichment method useful for arbitrary partition enrichment (CBSSD baseline).

    term_dataset = defaultdict(list) of node:[a1..an] mappings
    term_datset = Counter object of individual annotation occurrences
    all_counts = number of all annotation occurences

    """
    significant_results = compute_enrichment(term_dataset, term_database, topology_map, all_counts, whole_term_list=False)
    return significant_results


def fet_enrichment_terms(partition_mappings, annotation_mappings, alternative='two-sided', intra_community=False, pvalue=0.1, multitest_method='fdr_bh'):
    """
    This is the most generic enrichment process.
    """
    term_dataset, term_database, all_counts = read_uniprot_GO(annotation_mappings)
    topology_map = read_topology_mappings(partition_mappings)
    significant_results = compute_enrichment(term_dataset, term_database, topology_map, all_counts, whole_term_list=False, alternative=alternative, intra_community=intra_community, pvalue=pvalue, multitest_method=multitest_method)
    return significant_results


def fet_enrichment_uniprot(partition_mappings, annotation_mappings):
    """
    This is a pre-designed wrapper for uniprot-like annotation.
    """
    term_dataset, term_database, all_counts = read_uniprot_GO(annotation_mappings)
    topology_map = read_topology_mappings(partition_mappings)
    significant_results = compute_enrichment(term_dataset, term_database, topology_map, all_counts, whole_term_list=False)
    return significant_results


if __name__ == '__main__':
    pass