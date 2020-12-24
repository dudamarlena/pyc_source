# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/util/assorted.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki assorted utilities

TODO: overview

assorted should read "unsorted" ;-) TODO: Sort. Sort of. Ish. 
    
"""
import re
from turbogears import identity
from elementtree.ElementTree import Element

def attributes_from_dict(dict_):
    """initialize class instance from __init__ arguments

        Taken from Python Cookbook, 2nd edition, recipe 6.18 
        TODO: elaborate, license
        
    """
    self_ = dict_.pop('self')
    for (name, value) in dict_.iteritems():
        setattr(self_, name, value)


def save_add(val_1, val_2):
    """add to values, None being a neutral element to the addition
    
    parameters: val_1,
                val_2: two values to be added
    returns: val_1 + val_2 iff both aren't None, else the one, that isn't
             None, or None if both are None
    throws: whatever may be thrown by adding val_1 and val_2 if both aren't
            None
    
    """
    if val_2 is None:
        return val_1
    elif val_1 is None:
        return val_2
    else:
        return val_1 + val_2
    return


def add_element_contents(etree_1, etree_2, ret_type):
    """adds the content of to elementtree elements
    
    parameters: etree_1,
                etree_2:  two elementtree.ElementTree.Element instances
                ret_type: elementtype of the Element instance to be returned
    returns: new Element instance of type ret_type with the contents of 
             etree_1 and etree_2 concatenated. If any of the etree_n has a 
             .tail (i.e. text following the end tag), it (the tail) will be 
             ignored.

    """
    ret = Element(ret_type)
    if len(etree_1) == 0:
        ret.text = save_add(etree_1.text, etree_2.text)
        ret[:] = etree_2[:]
    else:
        last_sub = etree_1[(len(etree_1) - 1)]
        last_sub.tail = save_add(last_sub.tail, etree_2.text)
        ret.text = etree_1.text
        ret[:] = etree_1[:-1] + [last_sub] + etree_2[:]
    return ret


def check_for_permission(perm):
    """check for a permission explicitly"""
    if not (perm is None or perm in identity.current.permissions):
        raise identity.IdentityFailure, "don't have permission %s" % perm
    return