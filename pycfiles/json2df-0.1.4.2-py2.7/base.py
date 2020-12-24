# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/json2df/base.py
# Compiled at: 2018-01-01 09:49:28
import ast, pandas as pd
from collections import defaultdict
import itertools
from time import time, ctime

def unpack_one_layer_list(data):
    return list(itertools.chain.from_iterable(data))


def flatten_dict(data, layers=1, split_sign='.', drop_deeper=False):
    for _ in range(layers):
        data = [ (isinstance(v, dict) or k, v) if 1 else [ (str(k) + split_sign + str(k2), v2) for k2, v2 in v.items() ] for k, v in data.items() ]
        data = [ item for sublist in data for item in sublist if isinstance(sublist, list) ] + [ y for y in data if not isinstance(y, list) ]
        data = dict(data)

    if drop_deeper:
        data = {k:v for k, v in data.items() if not isinstance(v, dict) or isinstance(v, list) if not isinstance(v, dict) or isinstance(v, list)}
    return data


def unpack_dict(dictionary, layer=1, keep_deeper=True, split_sign='.'):
    for count in range(layer):
        tmp = []
        for i in dictionary.items():
            if type(i[(-1)]) != dict:
                tmp.append(i)
            else:
                for j in i[(-1)].items():
                    tmp.append((str(i[0]) + split_sign + str(j[0]), j[(-1)]))

            dictionary = dict(tmp)

    if not keep_deeper:
        tmp = []
        for k in dictionary.items():
            if type(k[(-1)]) != dict:
                tmp.append(k)

        dictionary = tmp
    return dict(dictionary)


def series2df(Series, layer=2, split_sign='_'):
    """expect pass a series that each row is string formated Json data with the same structure"""
    try:
        Series.columns
        Series = Series.iloc[:, 0]
    except:
        pass

    def _helper(x, layer=2):
        try:
            return flatten_dict(ast.literal_eval(x), layers=layer, split_sign=split_sign)
        except:
            try:
                return flatten_dict(x, layers=layer, split_sign=split_sign)
            except:
                return x

    df = pd.DataFrame(Series.apply(_helper).tolist())
    return df


def doc(docstring):

    def document(func):
        func.__doc__ = docstring
        return func

    return document


class LoadFile(object):
    """Object load data from json/ csv &txt/ excel file, inherit using Pandas pd.read_* : 
      kind = 'json', kind = 'csv', or kind = 'excel'
      check instance.doc to read the doc for load_data"""

    def __init__(self, kind='json'):
        if kind == 'json':
            self._load = pd.read_json
        elif kind == 'csv':
            self._load = pd.read_csv
        else:
            self._load = pd.read_excel
        self.doc = self._load.__doc__
        print 'choose file type: ' + kind + '\n please use instance.load_data(path) to load data'

    def load_data(self, path, *args, **kwargs):
        """see print instance.doc, e.g. cat=LoadFile(kind='excel')
          read how to use cat.load_data, exec: print (cat.doc)"""
        self.df = self._load(path, *args, **kwargs)
        self.series = self.df.iloc[:, 0]
        print 'Success! file length: ' + str(self.df.shape[0])

    def convert(self, layer=2, split_sign='_', *args, **kwargs):
        """convert data to DataFrame"""
        return series2df(self.series, *args, **kwargs)

    def doc(self, docstring):

        def document(func):
            func.__doc__ = docstring
            return func

        return document