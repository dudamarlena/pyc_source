# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ganesh/work/silota-python/silota/helpers.py
# Compiled at: 2013-11-30 16:18:07
from dateutil.parser import parse as parse_datetime

def is_collection(obj):
    """Tests if an object is a collection."""
    col = getattr(obj, '__getitem__', False)
    val = False if not col else True
    if isinstance(obj, basestring):
        val = False
    return val


def to_python(obj, in_dict, str_keys=None, date_keys=None, int_keys=None, object_map=None, bool_keys=None, dict_keys=None, **kwargs):
    """Extends a given object for API Consumption.

    :param obj: Object to extend.
    :param in_dict: Dict to extract data from.
    :param string_keys: List of in_dict keys that will be extracted as strings.
    :param date_keys: List of in_dict keys that will be extrad as datetimes.
    :param object_map: Dict of {key, obj} map, for nested object results.
    """
    d = dict()
    if str_keys:
        for in_key in str_keys:
            d[in_key] = in_dict.get(in_key)

    if date_keys:
        for in_key in date_keys:
            in_date = in_dict.get(in_key)
            if in_date:
                try:
                    out_date = parse_datetime(in_date)
                except TypeError as e:
                    raise e
                    out_date = None

            else:
                out_date = None
            d[in_key] = out_date

    if int_keys:
        for in_key in int_keys:
            if in_dict is not None and in_dict.get(in_key) is not None:
                d[in_key] = int(in_dict.get(in_key))

    if bool_keys:
        for in_key in bool_keys:
            if in_dict.get(in_key) is not None:
                d[in_key] = bool(in_dict.get(in_key))

    if dict_keys:
        for in_key in dict_keys:
            if in_dict.get(in_key) is not None:
                d[in_key] = dict(in_dict.get(in_key))

    if object_map:
        for k, v in object_map.items():
            if in_dict.get(k):
                d[k] = v.new_from_dict(in_dict.get(k))

    obj.__dict__.update(d)
    obj.__dict__.update(kwargs)
    return obj