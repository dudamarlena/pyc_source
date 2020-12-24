# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\data\dataset.py
# Compiled at: 2018-11-27 20:15:31
# Size of source mod 2**32: 8338 bytes
"""
dataset.py
"""
from functools import total_ordering
from six import iteritems, with_metaclass
from toolz import first
from strategycontainer.tsp.classifiers import Classifier, Latest as LatestClassifier
from strategycontainer.tsp.factors import Factor, Latest as LatestFactor
from strategycontainer.tsp.filters import Filter, Latest as LatestFilter
from strategycontainer.tsp.sentinels import NotSpecified
from strategycontainer.tsp.term import AssetExists, LoadableTerm, validate_dtype
from strategycontainer.utils.input_validation import ensure_dtype
from strategycontainer.utils.numpy_utils import NoDefaultMissingValue
from strategycontainer.utils.preprocess import preprocess

class Column(object):
    __doc__ = '\n    An abstract column of data, not yet associated with a dataset.\n    '

    @preprocess(dtype=ensure_dtype)
    def __init__(self, dtype, missing_value=NotSpecified, doc=None, metadata=None):
        self.dtype = dtype
        self.missing_value = missing_value
        self.doc = doc
        self.metadata = metadata.copy() if metadata is not None else {}

    def bind(self, name):
        """
        Bind a `Column` object to its name.
        """
        return _BoundColumnDescr(dtype=(self.dtype),
          missing_value=(self.missing_value),
          name=name,
          doc=(self.doc),
          metadata=(self.metadata))


class _BoundColumnDescr(object):
    __doc__ = "\n    Intermediate class that sits on `DataSet` objects and returns memoized\n    `BoundColumn` objects when requested.\n\n    This exists so that subclasses of DataSets don't share columns with their\n    parent classes.\n    "

    def __init__(self, dtype, missing_value, name, doc, metadata):
        try:
            self.dtype, self.missing_value = validate_dtype(termname='Column(name={name!r})'.format(name=name),
              dtype=dtype,
              missing_value=missing_value)
        except NoDefaultMissingValue:
            raise NoDefaultMissingValue('Failed to create Column with name {name!r} and dtype {dtype} because no missing_value was provided\n\nColumns with dtype {dtype} require a missing_value.\nPlease pass missing_value to Column() or use a different dtype.'.format(dtype=dtype,
              name=name))

        self.name = name
        self.doc = doc
        self.metadata = metadata

    def __get__(self, instance, owner):
        """
        Produce a concrete BoundColumn object when accessed.

        We don't bind to datasets at class creation time so that subclasses of
        DataSets produce different BoundColumns.
        """
        return BoundColumn(dtype=(self.dtype),
          missing_value=(self.missing_value),
          dataset=owner,
          name=(self.name),
          doc=(self.doc),
          metadata=(self.metadata))


class BoundColumn(LoadableTerm):
    __doc__ = "\n    A column of data that's been concretely bound to a particular dataset.\n\n    Instances of this class are dynamically created upon access to attributes\n    of DataSets (for example, USEquityPricing.close is an instance of this\n    class).\n\n    Attributes\n    ----------\n    dtype : numpy.dtype\n        The dtype of data produced when this column is loaded.\n    latest : zipline.pipeline.data.Factor or zipline.pipeline.data.Filter\n        A Filter, Factor, or Classifier computing the most recently known value\n        of this column on each date.\n\n        Produces a Filter if self.dtype == ``np.bool_``.\n        Produces a Classifier if self.dtype == ``np.int64``\n        Otherwise produces a Factor.\n    dataset : zipline.pipeline.data.DataSet\n        The dataset to which this column is bound.\n    name : str\n        The name of this column.\n    metadata : dict\n        Extra metadata associated with this column.\n    "
    mask = AssetExists()
    window_safe = True

    def __new__(cls, dtype, missing_value, dataset, name, doc, metadata):
        return super(BoundColumn, cls).__new__(cls,
          domain=(dataset.domain),
          dtype=dtype,
          missing_value=missing_value,
          dataset=dataset,
          name=name,
          ndim=(dataset.ndim),
          doc=doc,
          metadata=metadata)

    def _init(self, dataset, name, doc, metadata, *args, **kwargs):
        self._dataset = dataset
        self._name = name
        self.__doc__ = doc
        self._metadata = metadata
        return (super(BoundColumn, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, dataset, name, doc, metadata, *args, **kwargs):
        return (
         (super(BoundColumn, cls)._static_identity)(*args, **kwargs),
         dataset,
         name,
         doc,
         frozenset(sorted((metadata.items()), key=first)))

    @property
    def dataset(self):
        """
        The dataset to which this column is bound.
        """
        return self._dataset

    @property
    def name(self):
        """
        The name of this column.
        """
        return self._name

    @property
    def metadata(self):
        """
        A copy of the metadata for this column.
        """
        return self._metadata.copy()

    @property
    def qualname(self):
        """
        The fully-qualified name of this column.

        Generated by doing '.'.join([self.dataset.__name__, self.name]).
        """
        return '.'.join([self.dataset.__name__, self.name])

    @property
    def latest(self):
        dtype = self.dtype
        if dtype in Filter.ALLOWED_DTYPES:
            Latest = LatestFilter
        else:
            if dtype in Classifier.ALLOWED_DTYPES:
                Latest = LatestClassifier
            else:
                assert dtype in Factor.ALLOWED_DTYPES, 'Unknown dtype %s.' % dtype
                Latest = LatestFactor
        return Latest(inputs=(
         self,),
          dtype=dtype,
          missing_value=(self.missing_value),
          ndim=(self.ndim))

    def __repr__(self):
        return '{qualname}::{dtype}'.format(qualname=(self.qualname),
          dtype=(self.dtype.name))

    def short_repr(self):
        """Short repr to use when rendering Pipeline graphs."""
        return self.qualname

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.qualname == other.qualname

    def __hash__(self):
        return self.qualname.__hash__()


@total_ordering
class DataSetMeta(type):
    __doc__ = '\n    Metaclass for DataSets\n\n    Supplies name and dataset information to Column attributes.\n    '

    def __new__(mcls, name, bases, dict_):
        newtype = super(DataSetMeta, mcls).__new__(mcls, name, bases, dict_)
        column_names = (set().union)(*(getattr(base, '_column_names', ()) for base in bases))
        for maybe_colname, maybe_column in iteritems(dict_):
            if isinstance(maybe_column, Column):
                bound_column_descr = maybe_column.bind(maybe_colname)
                setattr(newtype, maybe_colname, bound_column_descr)
                column_names.add(maybe_colname)

        newtype._column_names = frozenset(column_names)
        return newtype

    @property
    def columns(self):
        return frozenset(getattr(self, colname) for colname in self._column_names)

    def __lt__(self, other):
        return id(self) < id(other)

    def __repr__(self):
        return '<DataSet: %r>' % self.__name__


class DataSet(with_metaclass(DataSetMeta, object)):
    domain = None
    ndim = 2