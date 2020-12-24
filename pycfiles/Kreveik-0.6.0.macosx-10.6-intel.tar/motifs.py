# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/family/motifs.py
# Compiled at: 2012-09-09 23:45:49
"""
family.motifs module
====================
Houses functions concerning motif extraction from a Family.

Functions
---------
    motif_freqs: extracts motifs and their frequencies.
    exclusive_motif_freqs: WIP
    
"""

def motif_freqs(family, degree, exclusive=False, sorting=False, **kwargs):
    """
    Returns a list of motifs of the family.
    
    Takes every single individual of a family, extracts motif frequencies of every single one
    of them (Check network.motif.motif_freqs() function), accumulating with each individual.
    When supplied with a motiflist, this function only searches for the motifs within the list.
    If there isn't any motiflist supplied, then the function generates all possible motifs with
    a specified number of nodes, and resumes calculation.
    
    Args:
    ----
    
        family: The family in which motif frequencies will be extracted.
        degree: the number of nodes of motifs in question.
        sorting: if True, will sort the returned list of motif frequencies.
        motiflist: an optional argument, that if supplied, the search for motifs will be 
        limited with that particular list. 
    """
    from kreveik import network
    import copy, logging
    if 'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        if exclusive == True:
            returned_motifs = network.motif.exclusive_conn_motifs(degree)[:]
        else:
            returned_motifs = network.motif.all_conn_motifs(degree)[:]
        logging.info('Computing motif frequencies of the family')
        for networkf in family:
            returned_motifs = network.motif.motif_freqs(networkf, degree, motiflist=returned_motifs)

    if sorting:
        return sorted(returned_motifs, key=lambda returned_motifs: returned_motifs[1], reverse=True)
    else:
        return returned_motifs


def relative_motif_freqs(network_family, degree, sorting=False, **kwargs):
    """
    """
    from kreveik import network
    import copy, logging, numpy as num
    if 'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        returned_motifs = network.motif.all_conn_motifs(degree)[:]
    logging.info('Computing relative motif frequencies of the family')
    family_motifs = motif_freqs(network_family, degree, motiflist=returned_motifs)[:]
    motif_counts = num.array([ [family_motifs[i][1]] for i in range(len(family_motifs)) ])
    relative_freqs = []
    for i in range(len(family_motifs)):
        relative_freqs.append([family_motifs[i][0], float(family_motifs[i][1]) / motif_counts.sum()])

    return num.array(relative_freqs)


def exclusive_motif_freqs(family, degree):
    """
    Work in Progress
    """
    from kreveik import network
    import copy, logging
    motifs = network.motif.exclusive_conn_motifs(degree)[:]
    for networkf in family:
        logging.info('Computing motif frequencies of the network' + str(networkf) + '.')
        returned_motifs = network.motif.motif_freqs(networkf, degree, exclusive=True)
        for i in range(len(motifs)):
            motifs[i][1] = motifs[i][1] + returned_motifs[i][1]

    return motifs


__all__ = [
 motif_freqs, exclusive_motif_freqs]