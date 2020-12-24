# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/metadata.py
# Compiled at: 2019-06-10 07:54:07
# Size of source mod 2**32: 8487 bytes
"""
A metadata to manage indexes.
"""
from typing import List, Optional, Tuple
import pandas as pd
from databricks import koalas as ks
IndexMap = Tuple[(str, Optional[str])]

class Metadata(object):
    __doc__ = '\n    Manages column names and index information.\n\n    :ivar _data_columns: list of the Spark field names to be seen as columns in Koalas DataFrame.\n    :ivar _index_map: list of pair holding the Spark field names for indexes,\n                       and the index name to be seen in Koalas DataFrame.\n\n    .. note:: this is an internal class. It is not supposed to be exposed to users and users\n        should not directly access to it.\n\n    Metadata represents the index information for a DataFrame it belongs to. For instance,\n    if we have a Koalas DataFrame as below, Pandas DataFrame does not store the index as columns.\n\n    >>> kdf = ks.DataFrame({\n    ...     \'A\': [1, 2, 3, 4],\n    ...     \'B\': [5, 6, 7, 8],\n    ...     \'C\': [9, 10, 11, 12],\n    ...     \'D\': [13, 14, 15, 16],\n    ...     \'E\': [17, 18, 19, 20]}, columns = [\'A\', \'B\', \'C\', \'D\', \'E\'])\n    >>> kdf  # doctest: +NORMALIZE_WHITESPACE\n       A  B   C   D   E\n    0  1  5   9  13  17\n    1  2  6  10  14  18\n    2  3  7  11  15  19\n    3  4  8  12  16  20\n\n    However, all columns including index column are also stored in Spark DataFrame internally\n    as below.\n\n    >>> kdf.to_spark().show()  # doctest: +NORMALIZE_WHITESPACE\n    +-----------------+---+---+---+---+---+\n    |__index_level_0__|  A|  B|  C|  D|  E|\n    +-----------------+---+---+---+---+---+\n    |                0|  1|  5|  9| 13| 17|\n    |                1|  2|  6| 10| 14| 18|\n    |                2|  3|  7| 11| 15| 19|\n    |                3|  4|  8| 12| 16| 20|\n    +-----------------+---+---+---+---+---+\n\n    In order to fill this gap, the current metadata is used by mapping Spark\'s internal column\n    to Koalas\' index. See the method below:\n\n    * `data_columns` represents non-indexing columns\n\n    * `index_columns` represents internal index columns\n\n    * `columns` represents all columns\n\n    * `index_names` represents the external index name\n\n    * `index_map` is zipped pairs of `index_columns` and `index_names`\n\n    >>> metadata = kdf._metadata\n    >>> metadata.data_columns\n    [\'A\', \'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_columns\n    [\'__index_level_0__\']\n    >>> metadata.columns\n    [\'__index_level_0__\', \'A\', \'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_names\n    [None]\n    >>> metadata.index_map\n    [(\'__index_level_0__\', None)]\n\n    In case that index is set to one of the existing column as below:\n\n    >>> kdf1 = kdf.set_index("A")\n    >>> kdf1  # doctest: +NORMALIZE_WHITESPACE\n       B   C   D   E\n    A\n    1  5   9  13  17\n    2  6  10  14  18\n    3  7  11  15  19\n    4  8  12  16  20\n\n    >>> kdf1.to_spark().show()  # doctest: +NORMALIZE_WHITESPACE\n    +---+---+---+---+---+\n    |  A|  B|  C|  D|  E|\n    +---+---+---+---+---+\n    |  1|  5|  9| 13| 17|\n    |  2|  6| 10| 14| 18|\n    |  3|  7| 11| 15| 19|\n    |  4|  8| 12| 16| 20|\n    +---+---+---+---+---+\n\n    >>> metadata = kdf1._metadata\n    >>> metadata.data_columns\n    [\'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_columns\n    [\'A\']\n    >>> metadata.columns\n    [\'A\', \'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_names\n    [\'A\']\n    >>> metadata.index_map\n    [(\'A\', \'A\')]\n\n    In case that index becomes a multi index as below:\n\n    >>> kdf2 = kdf.set_index("A", append=True)\n    >>> kdf2  # doctest: +NORMALIZE_WHITESPACE\n         B   C   D   E\n      A\n    0 1  5   9  13  17\n    1 2  6  10  14  18\n    2 3  7  11  15  19\n    3 4  8  12  16  20\n\n    >>> kdf2.to_spark().show()  # doctest: +NORMALIZE_WHITESPACE\n    +-----------------+---+---+---+---+---+\n    |__index_level_0__|  A|  B|  C|  D|  E|\n    +-----------------+---+---+---+---+---+\n    |                0|  1|  5|  9| 13| 17|\n    |                1|  2|  6| 10| 14| 18|\n    |                2|  3|  7| 11| 15| 19|\n    |                3|  4|  8| 12| 16| 20|\n    +-----------------+---+---+---+---+---+\n\n    >>> metadata = kdf2._metadata\n    >>> metadata.data_columns\n    [\'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_columns\n    [\'__index_level_0__\', \'A\']\n    >>> metadata.columns\n    [\'__index_level_0__\', \'A\', \'B\', \'C\', \'D\', \'E\']\n    >>> metadata.index_names\n    [None, \'A\']\n    >>> metadata.index_map\n    [(\'__index_level_0__\', None), (\'A\', \'A\')]\n    '

    def __init__(self, data_columns: List[str], index_map: Optional[List[IndexMap]]=None) -> None:
        """ Create a new metadata to manage column fields and index fields and names.

        :param data_columns: list of string
                              Field names to appear as columns.
        :param index_map: list of string pair
                           Each pair holds the index field name which exists in Spark fields,
                           and the index name.
        """
        assert all((isinstance(col, str) for col in data_columns))
        if not index_map is None:
            assert all((isinstance(index_field, str) and (index_name is None or isinstance(index_name, str)) for index_field, index_name in index_map))
        self._data_columns = data_columns
        self._index_map = index_map or []

    @property
    def data_columns(self) -> List[str]:
        """ Returns the managed column field names. """
        return self._data_columns

    @property
    def index_columns(self) -> List[str]:
        """ Returns the managed index field names. """
        return [index_column for index_column, _ in self._index_map]

    @property
    def columns(self) -> List[str]:
        """ Return all the field names including index field names. """
        index_columns = self.index_columns
        return index_columns + [column for column in self._data_columns if column not in index_columns]

    @property
    def index_map(self) -> List[IndexMap]:
        """ Return the managed index information. """
        return self._index_map

    @property
    def index_names(self) -> List[Optional[str]]:
        """ Return the managed index names. """
        return [index_name for _, index_name in self._index_map]

    def copy(self, data_columns: Optional[List[str]]=None, index_map: Optional[List[IndexMap]]=None) -> 'Metadata':
        """ Copy the metadata.

        :param data_columns: the new column field names. If None, then the original ones are used.
        :param index_map: the new index information. If None, then the original one is used.
        :return: the copied metadata.
        """
        if data_columns is None:
            data_columns = self._data_columns
        if index_map is None:
            index_map = self._index_map
        return Metadata(data_columns=(data_columns.copy()), index_map=(index_map.copy()))

    @staticmethod
    def from_pandas(pdf: pd.DataFrame) -> 'Metadata':
        """ Create a metadata from pandas DataFrame.

        :param pdf: :class:`pd.DataFrame`
        :return: the created metadata
        """
        data_columns = [str(col) for col in pdf.columns]
        index = pdf.index
        index_map = []
        if isinstance(index, pd.MultiIndex):
            if index.names is None:
                index_map = [('__index_level_{}__'.format(i), None) for i in range(len(index.levels))]
            else:
                index_map = [('__index_level_{}__'.format(i) if name is None else name, name) for i, name in enumerate(index.names)]
        else:
            index_map = [
             (
              index.name if index.name is not None else '__index_level_0__', index.name)]
        return Metadata(data_columns=data_columns, index_map=index_map)