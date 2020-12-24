# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/h5hep/read.py
# Compiled at: 2019-03-21 01:29:55
# Size of source mod 2**32: 6609 bytes
import h5py as h5, numpy as np

def load(filename=None, verbose=False, desired_datasets=None, subset=None):
    """ Reads all, or a subset of the data, from the HDF5 file to fill a data dictionary.
    Returns an empty dictionary to be filled later with select events.

    Args:
        **filename** (string): Name of the input file
        
        **verbose** (boolean): True if debug output is required

        **desired_datasets** (list): Datasets to be read from input file

        **subset** (int): Number of events to be read from input file

    Returns:
        **ourdata (dict): Selected data from HDF5 file
        
        **event** (dict): An empty event dictionary to be filled by individual events

    """
    f = None
    if filename != None:
        f = h5.File(filename, 'r+')
    else:
        print("No filename passed in! Can't open file.\n")
        return
    ourdata = {}
    ourdata['datasets_and_counters'] = {}
    ourdata['datasets_and_indices'] = {}
    ourdata['list_of_counters'] = []
    ourdata['all_datasets'] = []
    ourdata['nentries'] = f.attrs['nentries']
    if subset is not None:
        if type(subset) == int:
            subset = (
             0, subset)
        ourdata['nentries'] = subset[1] - subset[0]
    event = {}
    dc = f['datasets_and_counters']
    for vals in dc:
        counter = vals[1].decode()
        index = '%s_INDEX' % counter
        ourdata['datasets_and_counters'][vals[0].decode()] = counter
        ourdata['datasets_and_indices'][vals[0].decode()] = index
        ourdata['list_of_counters'].append(vals[1].decode())
        ourdata['all_datasets'].append(vals[0].decode())
        ourdata['all_datasets'].append(vals[1].decode())

    ourdata['list_of_counters'] = np.unique(ourdata['list_of_counters']).tolist()
    ourdata['all_datasets'] = np.unique(ourdata['all_datasets']).tolist()
    sg = f['_SINGLETONGROUP_'][0]
    decoded_string = sg[1].decode()
    vals = decoded_string.split('__:__')
    vals.remove('INDEX')
    ourdata['_SINGLETON_'] = vals
    entries = ourdata['all_datasets']
    if desired_datasets is not None:
        if type(desired_datasets) != list:
            desired_datasets = list(desired_datasets)
        i = len(entries) - 1
        while i >= 0:
            entry = entries[i]
            is_dropped = True
            for desdat in desired_datasets:
                if desdat in entry:
                    is_dropped = False
                    break

            if is_dropped == True:
                print('Not reading out %s from the file....' % entry)
                entries.remove(entry)
            i -= 1

    if verbose == True:
        print('Datasets and counters:')
        print(ourdata['datasets_and_counters'])
        print('\nDatasets and indices:')
        print(ourdata['list_of_counters'])
    print('Building the indices...')
    for name in ourdata['list_of_counters']:
        if subset is not None:
            ourdata[name] = f[name][subset[0]:subset[1]]
        else:
            ourdata[name] = f[name][:]
        indexname = '%s_INDEX' % name
        index = np.zeros((len(ourdata[name])), dtype=int)
        start = 0
        nentries = len(index)
        for i in range(0, nentries):
            index[i] = start
            nobjs = ourdata[name][i]
            start = index[i] + nobjs

        ourdata[indexname] = index

    print('Built the indices!')
    for name in entries:
        counter = None
        if name not in ourdata['list_of_counters']:
            counter = ourdata['datasets_and_counters'][name]
        if verbose == True:
            print(f[name])
        data = f[name]
        if type(data) == h5.Dataset:
            datasetname = name
            if subset is not None:
                ourdata[datasetname] = data[subset[0]:subset[1]]
            else:
                ourdata[datasetname] = data[:]
            event[datasetname] = None
            if verbose == True:
                print(data)

    f.close()
    print('Data is read in and input file is closed.')
    return (
     ourdata, event)


def unpack(event, data, n=0):
    """ Fills the event dictionary with selected events.

    Args:

        **event** (dict): Event dictionary to be filled

        **data** (dict): Data dictionary used to fill the event dictionary

    """
    keys = event.keys()
    for key in keys:
        if key in data['list_of_counters'] or key in data['_SINGLETON_']:
            event[key] = data[key][n]
        else:
            if 'INDEX' not in key:
                indexkey = data['datasets_and_indices'][key]
                numkey = data['datasets_and_counters'][key]
                if len(data[indexkey]) > 0:
                    index = data[indexkey][n]
                if len(data[numkey]) > 0:
                    nobjs = data[numkey][n]
                    event[key] = data[key][index:index + nobjs]


def get_nentries(filename):
    """ Get the number of entries in the file.

    """
    f = h5.File(filename, 'r+')
    a = f.attrs
    if a.__contains__('nentries'):
        nentries = a.get('nentries')
        f.close()
        return nentries
    else:
        print('\nFile does not contain the attribute, "nentries"\n')
        f.close()
        return