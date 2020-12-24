# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/output/to_json.py
# Compiled at: 2019-02-01 07:35:06
import json, datetime, codecs

def myconverter(o):
    """function to serialise datetime"""
    if isinstance(o, datetime.datetime):
        return o.__str__()


def write_to_file(data, path):
    """Export extracted fields to json

    Appends .json to path if missing and generates json file in specified directory, if not then in root

    Parameters
    ----------
    data : dict
        Dictionary of extracted fields
    path : str
        directory to save generated json file

    Notes
    ----
    Do give file name to the function parameter path.

    Examples
    --------
        >>> from ninvoice2data.output import to_json
        >>> to_json.write_to_file(data, "/exported_json/invoice.json")
        >>> to_json.write_to_file(data, "invoice.json")

    """
    if path.endswith('.json'):
        filename = path
    else:
        filename = path + '.json'
    with codecs.open(filename, 'w', encoding='utf-8') as (json_file):
        for line in data:
            try:
                line['date'] = line['date'].strftime('%d/%m/%Y')
            except:
                print 'toJSON ignoring date format'

        print type(json)
        print json
        json.dump(data, json_file, indent=4, sort_keys=True, default=myconverter, ensure_ascii=False)