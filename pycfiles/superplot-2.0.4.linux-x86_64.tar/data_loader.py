# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/data_loader.py
# Compiled at: 2017-08-19 22:58:02
r"""
This module contains code for:

- Opening and processing a \\*.txt data file.
- Opening and processing an \\*.info information file.
- Using the \\*.info file to label the data.
"""
import warnings, pandas as pd

def load(info_file, data_file):
    r"""
    Read data from \*.info file and \*.txt file.

    :param data_file: Name of \*.txt file
    :type data_file: string
    :param info_file: Name of \*.info file
    :type info_file: string

    :returns: Dictionary with chain's labels and array of data
    :rtype: dict (labels), array (data)
    """
    if not data_file:
        raise RuntimeWarning('Must specify a *.txt data file')
    data = _read_data_file(data_file)
    labels = _read_info_file(info_file)
    _label_chain(data, labels)
    return (
     labels, data)


def _read_data_file(file_name, fill=0.0):
    r"""
    Read \*.txt file into an array.

    :param file_name: Name of \*.txt file
    :type file_name: string
    :param fill: Fill value for problematic data entries
    :type fill: float

    :returns: Data as an array, with first index as column number
    :rtype: numpy.array
    """

    def safe_float(entry):
        r"""
        :param entry: String from \*.txt file
        :type entry: str

        :returns: Float of argument
        :rtype: float
        """
        try:
            return float(entry)
        except ValueError:
            warnings.warn(('{} filled with {}').format(entry, fill))
            return fill

    with open(file_name) as (file_):
        n_cols = len(file_.readline().split())
    converters = dict.fromkeys(range(n_cols), safe_float)
    data_frame = pd.read_csv(file_name, header=None, sep='\\s+', engine='c', converters=converters, na_filter=False)
    data_frame = data_frame.transpose()
    data_array = data_frame.values.astype('float64')
    return data_array


def _read_info_file(file_name):
    """
    Read labels from a SuperBayeS-style *.info file into a dictionary.

    .. warning::
        SuperBayeS index begins at 1 and misses posterior weight and
        chi-squared. We begin at index 0 and include posterior weight and
        chi-squared. Thus, we add 1 to SuperBayeS indexes.

    :param file_name: Name of *.info file
    :type file_name: string

    :returns: Labels of columns in *.txt file
    :rtype: dict
    """
    labels = {0: '$p_i$', 1: '$\\chi^2$'}
    if file_name is None:
        warnings.warn('No *.info file for labels')
        return labels
    else:
        with open(file_name, 'rb') as (info_file):
            for line in info_file:
                line = line.strip()
                if line.startswith('lab'):
                    line = line.lstrip('lab')
                    words = line.split('=')
                    index = int(words[0]) + 1
                    name = str(words[1])
                    labels[index] = name

        return labels


def _label_chain(data, labels):
    """
    Check if labels match data. If they don't, add data indicies to the list
    of labels.

    .. warning::
        This alters labels in place.

    :param data: Data chain, to match arguments with
    :type data: numpy.array
    :param info: Labels for data chain
    :type info: dict
    """
    for index in range(len(data)):
        if not labels.get(index):
            warnings.warn('Labels did not match data. Missing labels are integers.')
            labels[index] = str(index)