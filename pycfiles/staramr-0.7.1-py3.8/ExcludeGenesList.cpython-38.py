# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/databases/exclude/ExcludeGenesList.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 799 bytes
from os import path
import pandas as pd

class ExcludeGenesList:
    DEFAULT_EXCLUDE_FILE = path.join(path.dirname(__file__), 'data', 'genes_to_exclude.tsv')

    def __init__(self, file=DEFAULT_EXCLUDE_FILE):
        self._data = pd.read_csv(file, sep='\t')

    def tolist(self):
        """
        Converts the exclude genes data to a list.
        :return: A list with genes to exclude.
        """
        return self._data['#gene_id'].tolist()

    @classmethod
    def get_default_exclude_file(cls):
        """
        Get the default file containing the list of genes to exclude.
        :return: The default file containing the list of genes to exclude.
        """
        return cls.DEFAULT_EXCLUDE_FILE