# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/common/diff.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 9491 bytes
"""
    Helper library for QAL diff operations.
     
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details. 

"""
import difflib

def diff_strings(_a, _b):
    result = '---------- String A-----------\n'
    result += _a + '\n'
    result += '---------- String B-----------\n'
    result += _b + '\n'
    result += '---------- Diff between A and B-----------\n' + '\n'
    for line in difflib.context_diff(_a, _b):
        result += line

    return result


def diff_files(_file_a, _file_b):
    _f_a = open(_file_a, 'r')
    _f_b = open(_file_b, 'r')
    _a = _f_a.read()
    _b = _f_b.read()
    _f_a.close()
    _f_b.close()
    return diff_strings(_a=_a, _b=_b)


def cmp_key_columns(_left, _right, _key_columns):
    """
    This functions compares the columns in the specified key fields only and returns data usable in a </=/>-comparer
    """
    for _curr_key_column in _key_columns:
        if _left[_curr_key_column] < _right[_curr_key_column]:
            return -1
        if _left[_curr_key_column] > _right[_curr_key_column]:
            return 1

    return 0


def match_all_columns(_left, _right):
    """Match all columns in two arrays, return false if they differ anywhere.
    
    :param array _left: The left array
    :param array _right: The right array
    
    .. note::
        This function is a *little bit* tailored to QAL needs. 
        The left column *has* to be used for column iteration, since _right might have extra columns for references
        to underlying structures that should not be compared.
    """
    for _curr_column in range(0, len(_left)):
        if _left[_curr_column] != _right[_curr_column]:
            return False

    return True


def compare(_left, _right, _key_columns, _full):
    """ The compare function takes two structurally identical 2-dimensional matrices,
        _left and _right, matches them using the columns in _key_colums,
        and returns a tuple of the results.
        
        :param 2d-array _left: The left matrix
        :param 2d-array _right: The right matrix
        :param array _key_columns: An array with the key columns
        :param bool _full: If the _full parameter is True, also the values in the rows are compared, and the third         result, _different is populated with a list of rows where the values differ.
        
        
        :return array _missing_left: rows present in _right, but not in _left
        :return array _missing_right: rows present in _left, but not in _right
        :return array _difference: rows that by keys are present in _left and _right, but differ with in rows
        :return 2d-array _right_s: The _right matrix, but sorted by keys, often useful when one wants to continue             massaging the data.
        
        .. note::
            The results are not in original order, but sorted by their keys.
    """
    _missing_left = []
    _missing_right = []
    _difference = []
    try:
        if len(_key_columns) == 1:
            _left_s = sorted(_left, key=lambda d: d[_key_columns[0]])
            _right_s = sorted(_right, key=lambda d: d[_key_columns[0]])
        else:
            if len(_key_columns) == 2:
                _left_s = sorted(_left, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]]))
                _right_s = sorted(_right, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]]))
            else:
                if len(_key_columns) == 3:
                    _left_s = sorted(_left, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]], d[_key_columns[2]]))
                    _right_s = sorted(_right, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]], d[_key_columns[2]]))
                else:
                    if len(_key_columns) == 0:
                        raise Exception('Error in compare, at least one key column is required.')
                    else:
                        raise Exception('Err..sorry, only 3 key columns are supported currently, too tired to make it dynamic. :-)')
    except TypeError as e:
        if str(e).find('TypeError: unorderable types'):
            raise Exception('There seem to be data of different types in the same column.\nPerhaps data need to be cast to some common data type, for example string. \nError:' + str(e))
        else:
            raise Exception(str(e))

    _left_idx = _right_idx = 0
    _left_len = len(_left_s)
    _right_len = len(_right_s)
    while _left_idx < _left_len and _right_idx < _right_len:
        _cmp_res = cmp_key_columns(_left_s[_left_idx], _right_s[_right_idx], _key_columns)
        if _cmp_res < 0:
            _missing_right.append([_left_idx, _right_idx, _left_s[_left_idx]])
            _left_idx += 1
        elif _cmp_res > 0:
            _missing_left.append([_left_idx, _right_idx, _right_s[_right_idx]])
            _right_idx += 1
        else:
            if _full is True and match_all_columns(_left_s[_left_idx], _right_s[_right_idx]) is not True:
                _difference.append([_left_idx, _right_idx, _left_s[_left_idx], _right_s[_right_idx]])
            _left_idx += 1
            _right_idx += 1

    if _left_idx < _left_len:
        for _curr_item in _left_s[_left_idx:_left_len]:
            _missing_right.append([_left_idx, _left_idx, _curr_item])

    if _right_idx < _right_len:
        for _curr_item in _right_s[_right_idx:_right_len]:
            _missing_left.append([_right_idx, _right_idx, _curr_item])

    return (
     _missing_left, _missing_right, _difference, _right_s)


def diff_to_text(_missing_left, _missing_right, _different):
    """Creates a textual representation of the differences
    
        .. note::
            Not implemented.
    
    """
    _diff_text = ''
    raise Exception('diff_to_text is not implemented')


class DictDiffer(object):
    __doc__ = '\n    Calculate the difference between two dictionaries as:\n    (1) items added\n    (2) items removed\n    (3) keys same in both but changed values\n    (4) keys same in both and unchanged values\n\n    '

    def __init__(self, current_dict, past_dict):
        """
        Compares two dicts

        :param current_dict: The correct dict
        :param past_dict: The old dict

        """
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [set(d.keys()) for d in (current_dict, past_dict)]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        """
        A list of added items

        """
        return self.current_keys - self.intersect

    def removed(self):
        """
        Returns a list of removed items

        """
        return self.past_keys - self.intersect

    def changed(self):
        """
        Returns a list of changed items

        """
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """
        Returns a list of unchanged items

        """
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

    @staticmethod
    def compare_documents(_old, _new):
        _changes = []
        _differ = DictDiffer(_new, _old)
        for _property in _differ.added():
            _changes.append({'action': 'added', 'attribute': _property, 'before': None, 'after': _new[_property]})

        for _property in _differ.removed():
            _changes.append({'action': 'removed', 'attribute': _property, 'before': _old[_property], 'after': None})

        for _property in _differ.changed():
            _changes.append({'action': 'changed', 'attribute': _property, 'before': _old[_property], 'after': _new[_property]})

        return _changes

    @staticmethod
    def pretty_print_diff(_changes):
        for _curr_diff in _changes:
            print('Attribute : ' + str(_curr_diff['attribute']) + ', action : ' + str(_curr_diff['action']) + '\nBefore : ' + str(_curr_diff['before']) + '\nAfter :  ' + str(_curr_diff['after']))