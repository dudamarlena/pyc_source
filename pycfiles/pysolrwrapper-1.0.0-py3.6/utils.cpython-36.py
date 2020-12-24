# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysolrwrapper/utils.py
# Compiled at: 2019-01-19 06:14:25
# Size of source mod 2**32: 1642 bytes


def convert_result(results: {}):
    tmp = {}
    tmp['num_shown'] = len(results['response']['docs'])
    tmp['num_found'] = results['response']['numFound']
    hl = results['highlighting'] if 'highlighting' in results else {}
    docs = results['response']['docs']
    tmp['docs'] = convert_docs(docs, hl)
    if 'facet_counts' in results:
        tmp['facet_fields'] = {}
        for res in results['facet_counts']['facet_fields']:
            tmp['facet_fields'][res] = convert_array_to_dict(results['facet_counts']['facet_fields'][res])

    return tmp


def convert_docs(array: [], high: {}):
    tmp = []
    for row in array:
        new_row = {}
        for key, val in row.items():
            if key != '_version_':
                hl = high.get(row['concept_id'])
                if hl != None:
                    if key in hl:
                        new_row[key] = format_high(val, high.get(row['concept_id'])[key])
                new_row[key] = val

        tmp.append(new_row)

    return tmp


def format_high(orig, replace):
    import typing
    if len(replace) == 0:
        return orig
    else:
        if isinstance(orig, typing.List):
            return replace
        return replace[0]


def convert_array_to_dict(array: []):
    tmp = []
    for idx, val in enumerate(array):
        if idx % 2:
            res = {}
            res[key] = val
            tmp.append(res)
        else:
            key = val

    return tmp


def convert_pandas(dic: {}):
    import pandas as pd
    return pd.DataFrame.from_dict(dic)


def escape_edismax(query: str):
    return query