# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_mapclassify/geobricks_mapclassify/core/classify.py
# Compiled at: 2015-04-07 08:39:12
import numpy
from pysal.esda import mapclassify

def get_ranges(data):
    if 'ranges' in data and data['ranges'] is not None:
        data['ranges'].append(data['ranges'][(len(data['ranges']) - 1)])
        return data['ranges']
    else:
        return classify_values(get_data_values(data), data['intervals'], data['classificationtype'])
        return


def get_data_values(data):
    data_values = []
    for d in data['joindata']:
        for key in d:
            if isinstance(d[key], basestring):
                d[key] = float(d[key])
            data_values.append(d[key])

    if 'doublecounting' in data and data['doublecounting']:
        return data_values
    else:
        return list(set(data_values))


def classify_values(values, intervals, classification_type):
    intervals = intervals if intervals <= len(values) else len(values)
    values = numpy.array(values)
    classification_type = classification_type.lower()
    if classification_type == 'jenks_caspall':
        return classify_jenks_caspall(values, intervals)
    if classification_type == 'jenks_caspall_forced':
        return classify_jenks_caspall_forced(values, intervals)
    if classification_type == 'natural_breaks':
        return classify_natural_breaks(values, intervals)
    if classification_type == 'quantile':
        return classify_quantile(values, intervals)
    if classification_type == 'equal_interval':
        return classify_equal_interval(values, intervals)
    if classification_type == 'percentiles':
        return classify_percentiles(values)


def classify_jenks_caspall(values, intervals):
    result = mapclassify.Jenks_Caspall(values, intervals)
    return result.bins


def classify_jenks_caspall_forced(values, intervals):
    result = mapclassify.Jenks_Caspall_Forced(values, intervals)
    return result.bins


def classify_natural_breaks(values, intervals):
    result = mapclassify.natural_breaks(values, intervals)
    return result


def classify_quantile(values, intervals):
    result = mapclassify.quantile(values, intervals)
    return result


def classify_percentiles(values):
    result = mapclassify.Percentiles(values)
    return result.bins


def classify_equal_interval(values, intervals):
    result = mapclassify.Equal_Interval(values, intervals)
    return result.bins