# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/h5hep/write.py
# Compiled at: 2019-03-29 14:18:25
# Size of source mod 2**32: 13906 bytes
import numpy as np, h5py as h5

def initialize():
    """ Creates an empty data dictionary

    Returns:

        **data** (dict): An empty data dictionary

    """
    data = {}
    data['groups'] = {}
    data['datasets_and_counters'] = {}
    data['list_of_counters'] = []
    data['groups']['_SINGLETON_'] = [
     'INDEX']
    data['datasets_and_counters']['_SINGLETON_'] = '_SINGLETON_/INDEX'
    data['list_of_counters'].append('_SINGLETON_/INDEX')
    data['_SINGLETON_/INDEX'] = []
    return data


def clear_event(data):
    """ Clears the data from the data dictionary - should the name of the function change?

    Args:
        **data** (dict): The dictionary to be cleared

    """
    for key in data.keys():
        if type(data[key]) == list:
            data[key].clear()
        else:
            if type(data[key]) == int:
                data[key] = 0
            else:
                if type(data[key]) == float:
                    data[key] = 0.0


def create_single_event(data):
    """ Creates an event dictionary that will be used to collect data and then
    packed into the the master data dictionary.

    Args:
        **data** (dict): Data dictionary that will hold all the data from the events.

    Returns:
        **event** (dict): The new event dictionary with keys and no event information

    """
    event = {}
    for k in data.keys():
        if k[-5:] == 'index':
            event[k] = data[k]
        else:
            if k in data['groups']['_SINGLETON_']:
                event[k] = None
            else:
                if k in data['list_of_counters']:
                    event[k] = 0
                else:
                    event[k] = data[k].copy()

    return event


def create_group(data, groupname, counter=None):
    """ Adds a group in the dictionary

    Args:
        **data** (dict): Dictionary to which the group will be added

        **groupname** (string): Name of the group to be added

        **counter** (string): Name of the counter key. None by default

    """
    keys = data.keys()
    keyfound = False
    for k in keys:
        if groupname == k:
            print('\x1b[1m%s\x1b[0m is already in the dictionary!' % groupname)
            keyfound = True
            break

    if keyfound == False:
        data['groups'][groupname] = []
        print('Adding group \x1b[1m%s\x1b[0m' % groupname)
        if counter is not None:
            data['groups'][groupname].append(counter)
            name = '%s/%s' % (groupname, counter)
            data['datasets_and_counters'][groupname] = name
            if name not in data['list_of_counters']:
                data['list_of_counters'].append(name)
            data[name] = []
            print('Adding a counter for \x1b[1m%s\x1b[0m as \x1b[1m%s\x1b[0m' % (groupname, counter))
        else:
            print('----------------------------------------------------')
            print('There is no counter to go with group \x1b[1m%s\x1b[0m' % groupname)
            print("Are you sure that's what you want?")
            print('-----------------------------------------------------')


def create_dataset(data, datasets, group=None, dtype=None):
    """ Adds a dataset to a group in a dictionary. If the group does not exist, it will be created.

    Args:
        **data** (dict): Dictionary that contains the group
        
        **datasets** (list): Dataset to be added to the group (This doesn't have to be a list)

        **group** (string): Name of group the dataset will be added to.  None by default

        **dtype** (type): The data type. None by default - I don't think this is every used 

    Returns:
        **-1**: If the group is None

    """
    keys = data.keys()
    if group is None:
        print('-----------------------------------------------')
        print('You need to assign this dataset(s) to a group!')
        print('Groups are not added')
        print('-----------------------------------------------')
        if type(datasets) != list:
            datasets = [
             datasets]
        for dataset in datasets:
            keyfound = False
            for k in data['groups']['_SINGLETON_']:
                if dataset == k:
                    print('\x1b[1m%s\x1b[0m is already in the dictionary!' % dataset)
                    keyfound = True

            if keyfound == False:
                print('Adding dataset \x1b[1m%s\x1b[0m to the dictionary as a SINGLETON.' % dataset)
                data['groups']['_SINGLETON_'].append(dataset)
                data[dataset] = []
                data['datasets_and_counters'][dataset] = '_SINGLETON_/INDEX'

        return 0
    else:
        keyfound = False
        for k in data['groups']:
            if group == k:
                keyfound = True

        if keyfound == False:
            print('Your group, \x1b[1m%s\x1b[0m is not in the dictionary yet!' % group)
            counter = 'n%s' % group
            print('Adding it, along with a counter of \x1b[1m%s\x1b[0m' % counter)
            create_group(data, group, counter=counter)
        if type(datasets) != list:
            datasets = [
             datasets]
        for dataset in datasets:
            keyfound = False
            name = '%s/%s' % (group, dataset)
            for k in keys:
                if name == k:
                    print('\x1b[1m%s\x1b[0m is already in the dictionary!' % name)
                    keyfound = True

            if keyfound == False:
                print('Adding dataset \x1b[1m%s\x1b[0m to the dictionary under group \x1b[1m%s\x1b[0m.' % (dataset, group))
                data[name] = []
                data['groups'][group].append(dataset)
                counter = data['datasets_and_counters'][group]
                data['datasets_and_counters'][name] = counter

        return 0


def pack--- This code section failed: ---

 L. 238         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'event'
                4  LOAD_ATTR                keys
                6  CALL_FUNCTION_0       0  '0 positional arguments'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'keys'

 L. 240        12  SETUP_LOOP          204  'to 204'
               14  LOAD_FAST                'keys'
               16  GET_ITER         
               18  FOR_ITER            202  'to 202'
               20  STORE_FAST               'key'

 L. 243        22  LOAD_FAST                'key'
               24  LOAD_STR                 'datasets_and_counters'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     18  'to 18'
               30  LOAD_FAST                'key'
               32  LOAD_STR                 'groups'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_TRUE     18  'to 18'
               38  LOAD_FAST                'key'
               40  LOAD_STR                 'list_of_counters'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    48  'to 48'

 L. 244        46  CONTINUE             18  'to 18'
               48  ELSE                     '200'

 L. 247        48  LOAD_FAST                'key'
               50  LOAD_STR                 '_SINGLETON_/INDEX'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    72  'to 72'

 L. 248        56  LOAD_FAST                'data'
               58  LOAD_FAST                'key'
               60  BINARY_SUBSCR    
               62  LOAD_ATTR                append
               64  LOAD_CONST               1
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  POP_TOP          

 L. 249        70  CONTINUE             18  'to 18'

 L. 253        72  LOAD_GLOBAL              type
               74  LOAD_FAST                'event'
               76  LOAD_FAST                'key'
               78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  LOAD_GLOBAL              list
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   126  'to 126'

 L. 254        88  LOAD_FAST                'event'
               90  LOAD_FAST                'key'
               92  BINARY_SUBSCR    
               94  STORE_FAST               'value'

 L. 255        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'value'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  LOAD_CONST               0
              104  COMPARE_OP               >
              106  POP_JUMP_IF_FALSE   200  'to 200'

 L. 256       108  LOAD_FAST                'data'
              110  LOAD_FAST                'key'
              112  DUP_TOP_TWO      
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'value'
              118  INPLACE_ADD      
              120  ROT_THREE        
              122  STORE_SUBSCR     

 L. 265       124  CONTINUE             18  'to 18'

 L. 268       126  LOAD_FAST                'key'
              128  LOAD_FAST                'data'
              130  LOAD_STR                 'groups'
              132  BINARY_SUBSCR    
              134  LOAD_STR                 '_SINGLETON_'
              136  BINARY_SUBSCR    
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   182  'to 182'

 L. 269       142  LOAD_FAST                'event'
              144  LOAD_FAST                'key'
              146  BINARY_SUBSCR    
              148  LOAD_CONST               None
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   200  'to 200'

 L. 270       154  LOAD_GLOBAL              print
              156  LOAD_STR                 '\n\x1b[1m%s\x1b[0m is part of the SINGLETON group and is expected to have a value for each event.'
              158  LOAD_FAST                'key'
              160  BINARY_MODULO    
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_TOP          

 L. 271       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'However it is None...exiting.\n'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  POP_TOP          

 L. 272       174  LOAD_GLOBAL              exit
              176  CALL_FUNCTION_0       0  '0 positional arguments'
              178  POP_TOP          
              180  JUMP_BACK            18  'to 18'
              182  ELSE                     '200'

 L. 274       182  LOAD_FAST                'data'
              184  LOAD_FAST                'key'
              186  BINARY_SUBSCR    
              188  LOAD_ATTR                append
              190  LOAD_FAST                'event'
              192  LOAD_FAST                'key'
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  POP_TOP          
            200_0  COME_FROM           152  '152'
            200_1  COME_FROM           106  '106'
              200  JUMP_BACK            18  'to 18'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP       12  '12'

Parse error at or near `POP_BLOCK' instruction at offset 202


def convert_list_and_key_to_string_data(datalist, key):
    """ Converts data dictionary to a string

    Args:
        **datalist** (list): A list to be saved as a string.

    Returns:
        **key** (string): We will assume that this will be unpacked as a dictionary,
                      and this will be the key for the list in that dictionary.

    """
    a = np.string_(key)
    mydataset = []
    b = np.string_('')
    nvals = len(datalist)
    for i, val in enumerate(datalist):
        b += np.string_(val)
        if i < nvals - 1:
            b += np.string_('__:__')

    mydataset.append([a, b])
    return mydataset


def convert_dict_to_string_data(dictionary):
    """ Converts data dictionary to a string

    Args:
        **dictionary** (dict): Dictionary to be converted to a string

    Returns:
        **mydataset** (string): String representation of the dataset

    """
    keys = dictionary.keys()
    nkeys = len(keys)
    mydataset = []
    for i, key in enumerate(keys):
        a = np.string_(key)
        b = np.string_(dictionary[key])
        mydataset.append([a, b])

    return mydataset


def write_to_file(filename, data, comp_type=None, comp_opts=None, force_single_precision=True):
    """ Writes the selected data to an h5hep file

    Args:
        **filename** (string): Name of output file

        **data** (dictionary): Data to be written into output file

        **comp_type** (string): Type of compression

        **force_single_precision** (boolean): True if data should be written in single precision

    Returns:
        **hdoutfile** (h5hep): File to which the data has been written 

    """
    hdoutfile = h5.File(filename, 'w')
    groups = data['groups'].keys()
    mydataset = convert_dict_to_string_data(data['datasets_and_counters'])
    dset = hdoutfile.create_dataset('datasets_and_counters', data=mydataset,
      dtype='S256',
      compression=comp_type,
      compression_opts=comp_opts)
    mydataset = convert_list_and_key_to_string_data(data['groups']['_SINGLETON_'], '_SINGLETONGROUP_')
    dset = hdoutfile.create_dataset('_SINGLETONGROUP_', data=mydataset,
      dtype='S256',
      compression=comp_type,
      compression_opts=comp_opts)
    for group in groups:
        hdoutfile.create_group(group)
        hdoutfile[group].attrs['counter'] = np.string_(data['datasets_and_counters'][group])
        datasets = data['groups'][group]
        for dataset in datasets:
            name = None
            if group == '_SINGLETON_':
                if dataset is not 'INDEX':
                    name = dataset
            else:
                name = '%s/%s' % (group, dataset)
            x = data[name]
            if type(x) == list:
                x = np.array(x)
            if force_single_precision == True:
                if x.dtype == np.float64:
                    x = x.astype(np.float32)
            hdoutfile.create_dataset(name, data=x, compression=comp_type, compression_opts=comp_opts)

    counters = data['list_of_counters']
    nentries = -1
    prevcounter = None
    for i, countername in enumerate(counters):
        ncounter = len(data[countername])
        print('%-32s has %-12d entries' % (countername, ncounter))
        if i > 0:
            if ncounter != nentries:
                print('-------- WARNING -----------')
                print('%s and %s have differing numbers of entries!' % (countername, prevcounter))
                print('-------- WARNING -----------')
        if nentries < ncounter:
            nentries = ncounter
        prevcounter = countername

    hdoutfile.attrs['nentries'] = nentries
    hdoutfile.close()
    return hdoutfile