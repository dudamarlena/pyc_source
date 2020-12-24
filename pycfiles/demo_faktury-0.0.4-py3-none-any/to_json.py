# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\to_json.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 1298 bytes
import json, datetime, codecs

def myconverter(o):
    """function to serialise datetime"""
    if isinstance(o, datetime.datetime):
        return o.__str__()


def write_to_file(data, path, date_format='%Y-%m-%d'):
    """Export extracted fields to json

    Appends .json to path if missing and generates json file in specified directory, if not then in root

    Parameters
    ----------
    data : dict
        Dictionary of extracted fields
    path : str
        directory to save generated json file
    date_format : str
        Date format used in generated file

    Notes
    ----
    Do give file name to the function parameter path.
    """
    if path.endswith('.json'):
        filename = path
    else:
        filename = path + '.json'
    with codecs.open(filename, 'w', encoding='utf-8') as (json_file):
        for line in data:
            for k, v in line.items():
                if k.startswith('date') or k.endswith('date'):
                    line[k] = v.strftime(date_format)

        print(type(json))
        print(json)
        json.dump(data,
          json_file,
          indent=4,
          sort_keys=True,
          default=myconverter,
          ensure_ascii=False)