# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/tools/visit_h5.py
# Compiled at: 2019-07-18 11:38:44
# Size of source mod 2**32: 5990 bytes
"""Visit h5py file"""
import sys, json, h5py, numpy as np, yaml
from opentea.noob.asciigraph import nob_asciigraph
from opentea.noob.noob import nob_get

class H5LookupError(Exception):
    __doc__ = ' Exception class for h5 lookup\n    '

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def ascii2string(ascii_list):
    """ Ascii to string conversion

        Parameters:
        -----------
        ascii_list : a list of string to be converted

        Returns:
        --------
        a string joining the list elements

    """
    return ''.join((chr(i) for i in ascii_list[:-1]))


def get_node_description(node):
    """Get number of elements in an array or
      value of a single-valued node.

    Parameters:
    -----------
    node : hdf5 node

    Returns:
    --------
    a value with a Python format
    None if data is not a singlevalued quantity
    """
    out = None
    value = node[()]
    shape = node.shape
    if np.prod(shape) == 1:
        if node.dtype in ('int8', ):
            out = np.char.array(ascii2string(value))[0]
        elif shape in (1, (1,)):
            if node.dtype in ('int32', 'int64'):
                out = int(value[0])
            elif node.dtype in ('float32', 'float64'):
                out = float(value[0])
    else:
        out = 'array of %s elements' % ' x '.join([str(k) for k in shape])
    return out


def log_hdf_node(node):
    """
    Build a dictionnary with the structure of a HDF5 node

    Parameters:
    -----------
    node : hdf5 node

    Returns:
    --------
    a dictionnary
    """
    out = dict()

    def extend_dict(dict_, address, attr):
        tmp = dict_
        for key in address[:]:
            if key not in tmp:
                tmp[key] = attr.copy()
            tmp = tmp[key]

    def visitor_func--- This code section failed: ---

 L.  84         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'log_hdf_node.<locals>.visitor_func.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'name'
                8  LOAD_METHOD              split
               10  LOAD_STR                 '/'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  STORE_FAST               'key_list'

 L.  85        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'node'
               24  LOAD_GLOBAL              h5py
               26  LOAD_ATTR                Dataset
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_FALSE    78  'to 78'

 L.  86        32  LOAD_GLOBAL              dict
               34  CALL_FUNCTION_0       0  '0 positional arguments'
               36  STORE_FAST               'attr'

 L.  87        38  LOAD_GLOBAL              str
               40  LOAD_FAST                'node'
               42  LOAD_ATTR                dtype
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  LOAD_FAST                'attr'
               48  LOAD_STR                 'dtype'
               50  STORE_SUBSCR     

 L.  88        52  LOAD_GLOBAL              get_node_description
               54  LOAD_FAST                'node'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  LOAD_FAST                'attr'
               60  LOAD_STR                 'value'
               62  STORE_SUBSCR     

 L.  89        64  LOAD_DEREF               'extend_dict'
               66  LOAD_DEREF               'out'
               68  LOAD_FAST                'key_list'
               70  LOAD_FAST                'attr'
               72  CALL_FUNCTION_3       3  '3 positional arguments'
               74  POP_TOP          
               76  JUMP_FORWARD         78  'to 78'
             78_0  COME_FROM            76  '76'
             78_1  COME_FROM            30  '30'

Parse error at or near `COME_FROM' instruction at offset 78_0

    node.visititems(visitor_func)
    return out


def hdf5_query_field(node, address):
    """Get the content of the adress

    Parameters:
    -----------
    node : hdf5 node
    address : the adress of the content to retrieve. Possible options:
                - String : key of the value to retrieve (e.g 'content')
                - String : A posix-like full address
                  (e.g 'full/address/to/content')
                - List : A list of adress stages, complete or not
                  (e.g ['full', 'address', 'to', 'content'] or, ['content'])
                - A list of lists : a list holding address stages, as it is
                  done for instance in h5py.
                  (e.g [['full'], ['address'], ['to'], ['content']]])

    Returns:
    --------
    content of the address
    """
    if isinstanceaddressstr:
        keys = address.split('/')
    else:
        if isinstanceaddresslist:
            if all([isinstanceitemstr for item in address]):
                keys = address
            else:
                keys = [item for sublist in address for item in sublist]
        else:
            msg = 'Unknown address %s !\n' % str(address)
            msg = msg + 'address should be a list of keys or a string'
            raise H5LookupError(msg)
    return nob_get(node, *keys, **{'failsafe': False})


def pprint_dict(dict_, style=None):
    """Pretty pring a dictionnary using yaml or json formatting"""
    if style == 'json':
        lines = json.dumps(dict_, indent=4)
    else:
        if style == 'yaml':
            lines = yaml.dump(dict_, default_flow_style=False)
        else:
            lines = nob_asciigraph(dict_)
            lines = lines.replace('dtype (str)', 'dtype')
            lines = lines.replace('value (str)', 'value')
            lines = lines.replace(' (dict)\n', '\n')
    print(lines)


def h5_node_to_dict(node):
    """Read hdf5 node values and structure into a dictionnary

        Parameters:
        ==========
        node : hdf5 node

        Returns:
        =======
        data_dict : a dictionnary holding the data
    """

    def _get_datasets(buf=None, data_dict=None, path_=''):
        if data_dict is None:
            data_dict = dict()
        for gname, group in buf.items():
            data_dict[gname] = dict()
            path = path_ + '/' + gname
            if not isinstancegrouph5py.Dataset:
                _get_datasets((buf[gname]), (data_dict[gname]), path_=path)
            elif buf[path][()].size >= 1:
                data_dict[gname] = buf[path][()]

        return data_dict

    data_dict = _get_datasets(node)
    return data_dict


def h5_datasets_names(node):
    """Get hdf5 node datasets names

        Parameters:
        ==========
        node : hdf5 node

        Returns:
        =======
        ds_names : a list of datasets names
    """
    ds_names = []
    for path, _ in _rec_h5_dataset_iterator(node):
        ds_names.append(path.split('/')[(-1)].strip())

    return ds_names


def _rec_h5_dataset_iterator(node, prefix=''):
    for key in node.keys():
        item = node[key]
        path = '{}/{}'.format(prefix, key)
        if isinstanceitemh5py.Dataset:
            yield (
             path, item)
        elif isinstanceitemh5py.Group:
            yield from _rec_h5_dataset_iteratoritempath


def visit_h5(h5_filename):
    """ Show hdf5 file components

        Parameters:
        ----------
        h5_filename : path to hdf5 file to inspect
    """
    with h5py.File(h5_filename) as (node):
        pprint_dict((log_hdf_node(node)), style='yaml')


if __name__ == '__main__':
    visit_h5(sys.argv[1])