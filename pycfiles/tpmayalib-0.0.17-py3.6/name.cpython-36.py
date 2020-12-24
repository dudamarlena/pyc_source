# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/name.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 7996 bytes
"""
Module that contains functions and classes related to names
"""
from __future__ import print_function, division, absolute_import
import logging, tpMayaLib as maya
from tpPyUtils import strings
from tpPyUtils import name as naming_utils
LOGGER = logging.getLogger()

class FindUniqueName(naming_utils.FindUniqueString, object):
    __doc__ = '\n    This class allows to find a name that does not clash with other names in the Maya scene\n    It will increment the last number in hte name\n    If no number is found, it will append a 1 to the end of the name\n    '

    def __init__(self, name):
        super(FindUniqueName, self).__init__(name)
        self.work_on_last_number = True

    def get_last_number(self, bool_value):
        """
        Sets to update last number to get unique name or not
        :param bool_value: bool
        """
        self.work_on_last_number = bool_value

    def _get_scope_list(self):
        """
        Internal function used to get the scope list for the increment string
        :return: list<str>
        """
        if maya.cmds.objExists(self.increment_string):
            return [self.increment_string]
        else:
            return list()

    def _format_string(self, number):
        """
        Internal function to get the unique name format
        :param number: int
        """
        if number == 0:
            number = 1
            self.increment_string = '{}_{}'.format(self.test_string, number)
        if number > 1:
            if self.work_on_last_number:
                self.increment_string = naming_utils.increment_last_number(self.increment_string)
            else:
                self.increment_string = naming_utils.increment_first_number(self.increment_string)

    def _get_number(self):
        """
        Internal function to get the number on the string that we want to make unique
        :return: int
        """
        if self.work_on_last_number:
            number = naming_utils.get_last_number(self.test_string)
        else:
            number = naming_utils.get_first_number(self.test_string)
        if number is None:
            return 0
        else:
            return number


def get_basename(obj, remove_namespace=True, remove_attribute=False):
    """
    Get the base name in a hierarchy name (a|b|c -> returns c)
    :param obj: str, name to get base name from
    :param remove_namespace: bool, Whether to remove or not namespace from the base name
    :param remove_attribute: bool, Whether to remove or not attribute from the base name
    :return: str
    """
    split_name = obj.split('|')
    base_name = split_name[(-1)]
    if remove_attribute:
        base_name_split = base_name.split('.')
        base_name = base_name_split[0]
    if remove_namespace:
        split_base_name = base_name.split(':')
        return split_base_name[(-1)]
    else:
        return base_name


def get_short_name(obj):
    """
    Returns short name of given Maya object
    :param obj: str
    :return: str
    """
    try:
        obj = obj.meta_node
    except Exception:
        pass

    node_names = maya.cmds.ls(obj, shortNames=True)
    if node_names:
        if len(node_names) == 1:
            return node_names[0]
        LOGGER.warning('Too many objects named "{}"'.format(obj))
        for i, o in enumerate(node_names):
            LOGGER.warning('    ' + '{0}: "{1}"'.format(i, o))

        raise ValueError('Get Node Short Name || More than one object with name {}'.format(obj))
    raise ValueError('Get Node Short Name || No object with name {} exists'.format(obj))


def get_long_name(obj):
    """
    Returns long name of given Maya object
    :param obj: str
    :return: str
    """
    try:
        obj = obj.meta_node
    except Exception:
        pass

    node_names = maya.cmds.ls(obj, l=True)
    if node_names:
        if len(node_names) == 1:
            return node_names[0]
        LOGGER.error('Too many objects named "{}"'.format(obj))
        for i, o in enumerate(node_names):
            LOGGER.error('    ' + '{0}: "{1}"'.format(i, o))

        raise ValueError('Get Node Long Name || More than one object with name {}'.format(obj))
    raise ValueError('Get Node Long Name || No object with name {} exists'.format(obj))


def get_reference_prefix(node=None):
    """
    Returns reference prefix is given node name has ne
    :param node: str, object to get reference prefix from
    :return: str
    """
    if maya.cmds.referenceQuery(node, isNodeReferenced=True):
        split_prefix = node.split(':')
        return ':'.join(split_prefix[:-1])
    else:
        return False


def is_unique(name):
    """
    Returns whether a name is unique or not in the scene
    :param name: str, name to check
    :return: bool
    """
    objs = maya.cmds.ls(name)
    count = len(objs)
    if count > 1:
        return False
    else:
        if count == 1:
            return True
        return True


def prefix_name(node, prefix, name, separator='_'):
    """
    Renames Maya node by adding given prefix to its name
    :param node: str, name of the Maya node we want to rename
    :param prefix: str, prefix to add to the name
    :param name: str, name of the node
    :param separator: str, separator used
    :return:  str, new node name
    """
    new_name = maya.cmds.rename(node, '{}{}{}'.format(prefix, separator, name))
    return new_name


def prefix_hierarchy(top_group, prefix):
    """
    Adds a prefix to all hierarchy objects
    :param top_group: str, name of the top node of the hierarchy
    :param prefix: str, prefix to add in front of top_group name and its children
    :return: list<str>, list with renamed hierarchy names including top_group
    """
    relatives = maya.cmds.listRelatives(top_group, ad=True, f=True)
    relatives.append(top_group)
    renamed = list()
    prefix = prefix.strip()
    for child in relatives:
        short_name = get_basename(child)
        new_name = maya.cmds.rename(child, '{}_{}'.format(prefix, short_name))
        renamed.append(new_name)

    renamed.reverse()
    return renamed


def pad_number(name):
    """
    Renames given node name with pad
    :param name: str, node name we want to pad
    :return: str
    """
    pad_name = naming_utils.pad_number(name=name)
    renamed = maya.cmds.rename(name, pad_name)
    return renamed


def find_unique_name(name, include_last_number=True):
    """
    Finds a unique name by adding a number to the end
    :param name: str, name to start from
    :param include_last_number: bool, Whether to include last number or not
    :return: str
    """
    if not maya.cmds.objExists(name):
        return name
    else:
        unique = FindUniqueName(name)
        unique.get_last_number(include_last_number)
        return unique.get()


def find_available_name(name, suffix=None, index=0, padding=0, letters=False, capital=False):
    """
    Recursively find a free name matching specified criteria
    @param name: str, Name to check if already exists in the scene
    @param suffix: str, Suffix for the name
    @param index: int, Index of the name
    @param padding: int, Padding for the characters/numbers
    @param letters: bool, True if we want to use letters when renaming multiple nodes
    @param capital: bool, True if we want letters to be capital
    """
    if not maya.cmds.objExists(name):
        return name
    else:
        if letters is True:
            letter = strings.get_alpha(index - 1, capital)
            test_name = '%s_%s' % (name, letter)
        else:
            test_name = '%s_%s' % (name, str(index).zfill(padding + 1))
        if suffix:
            test_name = '%s_%s' % (test_name, suffix)
        if maya.cmds.objExists(test_name):
            return find_available_name(name, suffix, index + 1, padding, letters, capital)
        return test_name


short = get_short_name
base = get_basename
long = get_long_name