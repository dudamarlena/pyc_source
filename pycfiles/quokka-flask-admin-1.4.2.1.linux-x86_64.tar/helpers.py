# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/model/helpers.py
# Compiled at: 2016-06-26 14:14:34


def prettify_name(name):
    """
        Prettify pythonic variable name.

        For example, 'hello_world' will be converted to 'Hello World'

        :param name:
            Name to prettify
    """
    return name.replace('_', ' ').title()


def get_mdict_item_or_list(mdict, key):
    """
        Return the value for the given key of the multidict.

        A werkzeug.datastructures.multidict can have a single
        value or a list of items. If there is only one item,
        return only this item, else the whole list as a tuple

        :param mdict: Multidict to search for the key
        :type mdict: werkzeug.datastructures.multidict
        :param key: key to look for
        :return: the value for the key or None if the Key has not be found
    """
    if hasattr(mdict, 'getlist'):
        v = mdict.getlist(key)
        if len(v) == 1:
            value = v[0]
            if value == '':
                value = None
            return value
        if len(v) == 0:
            return
        return tuple(v)
    return