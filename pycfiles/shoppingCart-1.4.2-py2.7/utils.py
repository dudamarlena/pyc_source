# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/shoppingCart/utils.py
# Compiled at: 2015-08-10 04:44:00


def id_from_object(object):
    """
    :return: Id of object or object itself.
    """
    if not isinstance(object, (int, str)):
        object = getattr(object, 'id', object)
    return object


def get_dict_of_ids(object_dict):
    """
    :return: Dict of ids of object dict.
    """
    keys, values = [], []
    for key, value in object_dict.items():
        keys.append(id_from_object(key))
        if isinstance(value, dict):
            for k, v in value.items():
                values.append({id_from_object(k): v})

        else:
            values.append(id_from_object(value))

    return dict(zip(keys, values))


def get_list_of_ids(object_list):
    """
    :return: List of ids of object list.
    """
    return [ id_from_object(value) for value in object_list ]