# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/noob/noob.py
# Compiled at: 2020-03-02 09:54:34
# Size of source mod 2**32: 8877 bytes
"""Nested object services.

A nested object is here:
 -nested dicts
 -nested lists
 -a mix of nested lists and nested dicts

An address is a list of strings and/or integers
giving a position in the nested object

Hereafter, the -address, complete or not- statement
refer to an address with potentially missing elements.

EXAMPLE:@
for a dict such as :
d["a"]["b"]["c"]["d"]["e"]["f"]
this the full address
[ ["a","b","c","d","e"] ]
can be found  with either:
nob_find(d, "a","b","c","d","e") (full path)
nob_find(d, "b","d","e") (partial path)
nob_find(d, "e") (only one hint )

"""
import copy, yaml

class NobReferenceError(Exception):
    __doc__ = 'TO BE ADDED'


def str_address(addr):
    """Return an address -key list- into a path-like string."""
    return '/'.join([str(i) for i in addr])


def nob_find(obj_, *keys):
    """Find all occurences matching a serie of keys in a nested object.

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    list of addresses matching the input address
    """
    if not keys:
        raise RuntimeError('No key provided..')
    target_key = keys[(-1)]
    matching_addresses = []

    def rec_findkey(obj_, target_key, path):
        if isinstance(obj_, dict):
            for key in obj_:
                if key == target_key:
                    matching_addresses.append(path + [key])
                rec_findkey(obj_[key], target_key, path + [key])

        if isinstance(obj_, list):
            for key, item in enumerate(obj_):
                if isinstance(item, dict):
                    if 'name' in item:
                        if key == item['name']:
                            matching_addresses.append(path + [key])
                rec_findkey(item, target_key, path + [key])

    rec_findkey(obj_, target_key, [])
    out = []
    for addr in matching_addresses:
        if all([clue in addr for clue in keys[:-1]]):
            out.append(addr)

    return out


def nob_find_unique(obj_, *keys):
    """Find a unique occurences of a key in a nested object.
    Raise exceptions if problems

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    one single address matching the input address
    """
    out = None
    error_found = False
    error_msg = str()
    matchlist = nob_find(obj_, *keys)
    keys_str = ' '.join([str(key) for key in [*keys]])
    if not matchlist:
        error_found = True
        error_msg = 'No match for keys -' + keys_str + '-'
    else:
        if len(matchlist) > 1:
            error_found = True
            match_err = [str_address(match) for match in matchlist]
            error_msg = 'Multiple match for key -' + keys_str + '-\n' + '\n'.join(match_err)
        else:
            out = matchlist[0]
    if error_found:
        raise NobReferenceError(error_msg)
    return out


def nob_node_exist(obj_, *keys):
    """ Test if one node exist in a nested object

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    boolean
    """
    try:
        nob_find_unique(obj_, *keys)
    except NobReferenceError:
        return False
    else:
        return True


def nob_get(obj_, *keys, failsafe=False):
    """Access a nested object by keys.

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not
    failsafe : what to do if the node is missing
        - False : raise an exception
        - True : return None is missing
                 return the shortes path is several matches

    Returns
    -------
    if points to a leaf:
        immutable, the value stored in the leaf
    if points to a node:
        mutable : the object (dict or list) found at this address
    """
    if failsafe:
        match = nob_find(obj_, *keys)
        if match:
            address = match[0]
        else:
            return
    else:
        address = nob_find_unique(obj_, *keys)
    tmp = obj_.copy()
    for key in address:
        tmp = tmp[key]

    return tmp


def unique_dict_key(dict_):
    """Return the only key of a single child dict."""
    keys = list(dict_.keys())
    if len(keys) != 1:
        raise ValueError(f"No unique key: {keys}")
    if not keys:
        raise ValueError('No child found')
    return keys[0]


def nob_get_only_child(obj_, *keys):
    """Return the only key of a single child dict."""
    dict_ = nob_get(obj_, *keys)
    if not isinstance(dict_, dict):
        raise ValueError('This is not a single child dictionnary')
    l_keys = list(dict_.keys())
    if not l_keys:
        raise ValueError('No child found')
    if len(l_keys) > 1:
        raise ValueError('Several child found')
    return l_keys[0]


def nob_set(obj_, value, *keys):
    """Assign a value to an object from a nested object.

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns
    -------
    change the object in argument (NOT STATELESS)
    """
    address = nob_find_unique(obj_, *keys)
    if address[:-1]:
        father = nob_get(obj_, *address[:-1])
    else:
        father = obj_
    father[address[(-1)]] = value


def nob_del(obj_, *keys, verbose=False):
    """ Delete all matchinf addresses in the nested object.
    Not a deletion in place, only the output argument is cropped.

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns
    -------
    obj_ : nested object without the matching keys
    """
    address_do_del = nob_find(obj_, *keys)
    if verbose:
        log = 'Will delete :\n'
        for addr in address_do_del:
            log += '    ' + str_address(addr) + '\n'

        print(log)

    def rec_delete_items(nob_in, curr_addr=None):
        nob_out = None
        if curr_addr is not None:
            pass
        else:
            curr_addr = list()
        if isinstance(nob_in, dict):
            nob_out = dict()
            for key in nob_in:
                next_addr = [
                 *curr_addr, key]
                if next_addr not in address_do_del:
                    nob_out[key] = rec_delete_items(nob_in[key], next_addr)
                else:
                    if verbose:
                        print('removing', str_address(next_addr))

        else:
            if isinstance(nob_in, list):
                nob_out = list()
                for i, list_item in enumerate(nob_in):
                    next_addr = [
                     *curr_addr, i]
                    if next_addr not in address_do_del:
                        nob_out.append(rec_delete_items(list_item, next_addr))
                    else:
                        if verbose:
                            print('removing', str_address(next_addr))

            else:
                nob_out = nob_in
        return nob_out

    nob_out = rec_delete_items(obj_)
    return nob_out


def nob_pprint(obj_, max_lvl=None):
    """ return a pretty print of a nested object.
    yaml.dump() in use for the display

    Parameters :
    ------------
    obj_ : nested object
    max_lvel : optional :  maximum nber of levels to show

    Output :
    --------
    out : string showing the nested_object structure
    """
    yamlstr = None
    if max_lvl is None:
        yamlstr = yaml.dump(obj_, default_flow_style=False)
    else:

        def rec_copy(obj_, lvl):
            out = None
            if lvl == 0:
                out = '(...)'
            else:
                if isinstance(obj_, dict):
                    out = {}
                    for key in obj_:
                        out[key] = rec_copy(obj_[key], lvl - 1)

                else:
                    if isinstance(obj_, list):
                        out = []
                        for elmt in obj_:
                            out.append(rec_copy(elmt, lvl - 1))

                    else:
                        out = obj_
            return out

        out = rec_copy(obj_, max_lvl)
        yamlstr = yaml.dump(out, default_flow_style=False)
    return yamlstr


def nob_merge_agressive--- This code section failed: ---

 L. 320         0  LOAD_GLOBAL              copy
                2  LOAD_METHOD              deepcopy
                4  LOAD_FAST                'base_obj'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'merged_obj'

 L. 322        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'obj_to_add'
               14  LOAD_GLOBAL              dict
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_FALSE    96  'to 96'

 L. 323        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'merged_obj'
               24  LOAD_GLOBAL              dict
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_FALSE    90  'to 90'

 L. 324        30  SETUP_LOOP           94  'to 94'
               32  LOAD_FAST                'obj_to_add'
               34  GET_ITER         
               36  FOR_ITER             86  'to 86'
               38  STORE_FAST               'key'

 L. 325        40  LOAD_FAST                'key'
               42  LOAD_FAST                'merged_obj'
               44  COMPARE_OP               not-in
               46  POP_JUMP_IF_FALSE    62  'to 62'

 L. 326        48  LOAD_FAST                'obj_to_add'
               50  LOAD_FAST                'key'
               52  BINARY_SUBSCR    
               54  LOAD_FAST                'merged_obj'
               56  LOAD_FAST                'key'
               58  STORE_SUBSCR     
               60  JUMP_BACK            36  'to 36'
             62_0  COME_FROM            46  '46'

 L. 328        62  LOAD_GLOBAL              nob_merge_agressive
               64  LOAD_FAST                'merged_obj'
               66  LOAD_FAST                'key'
               68  BINARY_SUBSCR    

 L. 329        70  LOAD_FAST                'obj_to_add'
               72  LOAD_FAST                'key'
               74  BINARY_SUBSCR    
               76  CALL_FUNCTION_2       2  '2 positional arguments'
               78  LOAD_FAST                'merged_obj'
               80  LOAD_FAST                'key'
               82  STORE_SUBSCR     
               84  JUMP_BACK            36  'to 36'
               86  POP_BLOCK        
               88  JUMP_ABSOLUTE       100  'to 100'
             90_0  COME_FROM            28  '28'

 L. 331        90  LOAD_FAST                'obj_to_add'
               92  STORE_FAST               'merged_obj'
             94_0  COME_FROM_LOOP       30  '30'
               94  JUMP_FORWARD        100  'to 100'
             96_0  COME_FROM            18  '18'

 L. 333        96  LOAD_FAST                'obj_to_add'
               98  STORE_FAST               'merged_obj'
            100_0  COME_FROM            94  '94'

 L. 335       100  LOAD_FAST                'merged_obj'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 94_0