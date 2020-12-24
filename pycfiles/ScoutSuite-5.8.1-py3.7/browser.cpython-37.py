# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/base/configs/browser.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 3377 bytes
import copy
from ScoutSuite.core.console import print_exception

def combine_paths(path1, path2):
    path = path1
    for p in path2:
        if p == '..':
            del path[-1]
        else:
            path.append(p)

    return path


def get_object_at(object, path, attribute_name=None):
    """
    Get arbitrary object given a dictionary and path (list of keys).

    :param object:
    :param path:
    :param attribute_name:
    :return:
    """
    o = object
    try:
        for p in path:
            if type(o) is dict:
                o = o[p]
            else:
                o = getattr(o, p)

        if attribute_name:
            if type(o) is dict:
                return o[attribute_name]
            return getattr(o, attribute_name)
        else:
            return o
    except Exception as e:
        try:
            raise Exception
        finally:
            e = None
            del e


def get_value_at(all_info, current_path, key, to_string=False):
    """
    Get value located at a given path.

    :param all_info:        All of the services' data
    :param current_path:    The value of the `path` variable defined in the finding file
    :param key:             The key that is being requested
    :param to_string:       Whether or not the returned value should be casted as a string
    :return:                The value in `all_info` indicated by the `key` in `current_path`
    """
    keys = key.split('.')
    if keys[(-1)] == 'id':
        target_obj = current_path[(len(keys) - 1)]
    else:
        if key == 'this':
            target_path = current_path
        else:
            if '.' in key:
                target_path = []
                for i, key in enumerate(keys):
                    if key == 'id':
                        target_path.append(current_path[i])
                    elif key == '' and i < len(current_path) and current_path[i].isdigit():
                        target_path.append(int(current_path[i]))
                    else:
                        target_path.append(key)

                if len(keys) > len(current_path):
                    target_path = target_path + keys[len(target_path):]
            else:
                target_path = copy.deepcopy(current_path)
                target_path.append(key)
        target_obj = all_info
        for p in target_path:
            try:
                if type(target_obj) == list and type(target_obj[0]) == dict:
                    target_obj = target_obj[int(p)]
                else:
                    if type(target_obj) == list and type(p) == int:
                        target_obj = target_obj[p]
                    else:
                        if type(target_obj) == list and p.isdigit():
                            target_obj = target_obj[int(p)]
                        else:
                            if type(target_obj) == list:
                                target_obj = p
                            else:
                                if p == '':
                                    pass
                                else:
                                    target_obj = target_obj[p]
            except Exception as e:
                try:
                    print_exception(e, additional_details={'current_path': current_path})
                finally:
                    e = None
                    del e

    if to_string:
        return str(target_obj)
    return target_obj