# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/canonicalize/centroid.py
# Compiled at: 2015-02-12 17:33:58
import numpy
from affinegap import normalizedAffineGapDistance as comparator

def getCentroid(attribute_variants, comparator):
    """ 
    Takes in a list of attribute values for a field,
    evaluates the centroid using the comparator,
    & returns the centroid (i.e. the 'best' value for the field)
    """
    n = len(attribute_variants)
    distance_matrix = numpy.zeros([n, n])
    for i in range(0, n):
        for j in range(0, i):
            distance = comparator(attribute_variants[i], attribute_variants[j])
            distance_matrix[(i, j)] = distance_matrix[(j, i)] = distance

    average_distance = distance_matrix.mean(0)
    min_dist_indices = numpy.where(average_distance == average_distance.min())[0]
    if len(min_dist_indices) > 1:
        centroid = breakCentroidTie(attribute_variants, min_dist_indices)
    else:
        centroid_index = min_dist_indices[0]
        centroid = attribute_variants[centroid_index]
    return centroid


def breakCentroidTie(attribute_variants, min_dist_indices):
    """
    Finds centroid when there are multiple values w/ min avg distance 
    (e.g. any dupe cluster of 2) right now this selects the first among a set of 
    ties, but can be modified to break ties in strings by selecting the longest string
    """
    return attribute_variants[min_dist_indices[0]]


def getCanonicalRep(record_cluster):
    """
    Given a list of records within a duplicate cluster, constructs a canonical representation
    of the cluster by finding canonical values for each field
    """
    canonical_rep = {}
    for key in record_cluster[0].keys():
        key_values = []
        for record in record_cluster:
            if record[key]:
                key_values.append(record[key])

        if key_values:
            canonical_rep[key] = getCentroid(key_values, comparator)
        else:
            canonical_rep[key] = ''

    return canonical_rep