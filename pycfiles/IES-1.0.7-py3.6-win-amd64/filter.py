# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\filters\filter.py
# Compiled at: 2018-01-16 22:36:00
# Size of source mod 2**32: 20996 bytes
"""
filter.py
"""
from itertools import chain
from operator import attrgetter
from numpy import any as np_any, float64, nan, nanpercentile, uint8
from strategycontainer.exception import BadPercentileBounds, NonExistentAssetInTimeFrame, UnsupportedDataType
from strategycontainer.lib.labelarray import LabelArray
from strategycontainer.lib.rank import is_missing, grouped_masked_is_maximal
from strategycontainer.tsp.dtypes import CLASSIFIER_DTYPES, FACTOR_DTYPES, FILTER_DTYPES
from strategycontainer.tsp.expression import BadBinaryOperator, FILTER_BINOPS, method_name_for_op, NumericalExpression
from strategycontainer.tsp.mixins import AliasedMixin, CustomTermMixin, DownsampledMixin, LatestMixin, PositiveWindowLengthMixin, RestrictedDTypeMixin, SingleInputMixin, StandardOutputs
from strategycontainer.tsp.term import ComputableTerm, Term
from strategycontainer.utils.input_validation import expect_types
from strategycontainer.utils.memoize import classlazyval
from strategycontainer.utils.numpy_utils import bool_dtype, int64_dtype, repeat_first_axis

def concat_tuples(*tuples):
    """
    Concatenate a sequence of tuples into one tuple.
    """
    return tuple(chain(*tuples))


def binary_operator(op):
    """
    Factory function for making binary operator methods on a Filter subclass.

    Returns a function "binary_operator" suitable for implementing functions
    like __and__ or __or__.
    """
    commuted_method_getter = attrgetter(method_name_for_op(op, commute=True))

    def binary_operator(self, other):
        if isinstance(self, NumericalExpression):
            self_expr, other_expr, new_inputs = self.build_binary_op(op, other)
            return NumExprFilter.create('({left}) {op} ({right})'.format(left=self_expr,
              op=op,
              right=other_expr), new_inputs)
        else:
            if isinstance(other, NumericalExpression):
                return commuted_method_getter(other)(self)
            if isinstance(other, Term):
                if other.dtype != bool_dtype:
                    raise BadBinaryOperator(op, self, other)
                if self is other:
                    return NumExprFilter.create('x_0 {op} x_0'.format(op=op), (
                     self,))
                else:
                    return NumExprFilter.create('x_0 {op} x_1'.format(op=op), (
                     self, other))
            if isinstance(other, int):
                return NumExprFilter.create('x_0 {op} {constant}'.format(op=op, constant=(int(other))),
                  binds=(
                 self,))
        raise BadBinaryOperator(op, self, other)

    binary_operator.__doc__ = "Binary Operator: '%s'" % op
    return binary_operator


def unary_operator(op):
    """
    Factory function for making unary operator methods for Filters.
    """
    valid_ops = {
     '~'}
    if op not in valid_ops:
        raise ValueError('Invalid unary operator %s.' % op)

    def unary_operator(self):
        if isinstance(self, NumericalExpression):
            return NumExprFilter.create('{op}({expr})'.format(op=op, expr=(self._expr)), self.inputs)
        else:
            return NumExprFilter.create('{op}x_0'.format(op=op), (self,))

    unary_operator.__doc__ = "Unary Operator: '%s'" % op
    return unary_operator


class Filter(RestrictedDTypeMixin, ComputableTerm):
    __doc__ = "\n    Pipeline expression computing a boolean output.\n\n    Filters are most commonly useful for describing sets of assets to include\n    or exclude for some particular purpose. Many Pipeline API functions accept\n    a ``mask`` argument, which can be supplied a Filter indicating that only\n    values passing the Filter should be considered when performing the\n    requested computation. For example, :meth:`zipline.pipeline.Factor.top`\n    accepts a mask indicating that ranks should be computed only on assets that\n    passed the specified Filter.\n\n    The most common way to construct a Filter is via one of the comparison\n    operators (``<``, ``<=``, ``!=``, ``eq``, ``>``, ``>=``) of\n    :class:`~zipline.pipeline.Factor`. For example, a natural way to construct\n    a Filter for stocks with a 10-day VWAP less than $20.0 is to first\n    construct a Factor computing 10-day VWAP and compare it to the scalar value\n    20.0::\n\n        >>> from zipline.pipeline.factors import VWAP\n        >>> vwap_10 = VWAP(window_length=10)\n        >>> vwaps_under_20 = (vwap_10 <= 20)\n\n    Filters can also be constructed via comparisons between two Factors.  For\n    example, to construct a Filter producing True for asset/date pairs where\n    the asset's 10-day VWAP was greater than it's 30-day VWAP::\n\n        >>> short_vwap = VWAP(window_length=10)\n        >>> long_vwap = VWAP(window_length=30)\n        >>> higher_short_vwap = (short_vwap > long_vwap)\n\n    Filters can be combined via the ``&`` (and) and ``|`` (or) operators.\n\n    ``&``-ing together two filters produces a new Filter that produces True if\n    **both** of the inputs produced True.\n\n    ``|``-ing together two filters produces a new Filter that produces True if\n    **either** of its inputs produced True.\n\n    The ``~`` operator can be used to invert a Filter, swapping all True values\n    with Falses and vice-versa.\n\n    Filters may be set as the ``screen`` attribute of a Pipeline, indicating\n    asset/date pairs for which the filter produces False should be excluded\n    from the Pipeline's output.  This is useful both for reducing noise in the\n    output of a Pipeline and for reducing memory consumption of Pipeline\n    results.\n    "
    window_safe = True
    ALLOWED_DTYPES = FILTER_DTYPES
    dtype = bool_dtype
    clsdict = locals()
    clsdict.update({method_name_for_op(op):binary_operator(op) for op in FILTER_BINOPS})
    clsdict.update({method_name_for_op(op, commute=True):binary_operator(op) for op in FILTER_BINOPS})
    __invert__ = unary_operator('~')

    def _validate(self):
        retval = super(Filter, self)._validate()
        if self.dtype != bool_dtype:
            raise UnsupportedDataType(typename=(type(self).__name__),
              dtype=(self.dtype))
        return retval

    @classlazyval
    def _downsampled_type(self):
        return DownsampledMixin.make_downsampled_type(Filter)

    @classlazyval
    def _aliased_type(self):
        return AliasedMixin.make_aliased_type(Filter)


class NumExprFilter(NumericalExpression, Filter):
    __doc__ = '\n    A Filter computed from a numexpr expression.\n    '

    @classmethod
    def create(cls, expr, binds):
        """
        Helper for creating new NumExprFactors.

        This is just a wrapper around NumericalExpression.__new__ that always
        forwards `bool` as the dtype, since Filters can only be of boolean
        dtype.
        """
        return cls(expr=expr, binds=binds, dtype=bool_dtype)

    def _compute(self, arrays, dates, assets, mask):
        return super(NumExprFilter, self)._compute(arrays, dates, assets, mask) & mask


class NullFilter(SingleInputMixin, Filter):
    __doc__ = '\n    A Filter indicating whether input values are missing from an input.\n\n    Parameters\n    ----------\n    factor : zipline.pipeline.Term\n        The factor to compare against its missing_value.\n    '
    window_length = 0

    def __new__(cls, term):
        return super(NullFilter, cls).__new__(cls,
          inputs=(
         term,))

    def _compute(self, arrays, dates, assets, mask):
        data = arrays[0]
        if isinstance(data, LabelArray):
            return data.is_missing()
        else:
            return is_missing(arrays[0], self.inputs[0].missing_value)


class NotNullFilter(SingleInputMixin, Filter):
    __doc__ = '\n    A Filter indicating whether input values are **not** missing from an input.\n\n    Parameters\n    ----------\n    factor : zipline.pipeline.Term\n        The factor to compare against its missing_value.\n    '
    window_length = 0

    def __new__(cls, term):
        return super(NotNullFilter, cls).__new__(cls,
          inputs=(
         term,))

    def _compute(self, arrays, dates, assets, mask):
        data = arrays[0]
        if isinstance(data, LabelArray):
            return ~data.is_missing()
        else:
            return ~is_missing(arrays[0], self.inputs[0].missing_value)


class PercentileFilter(SingleInputMixin, Filter):
    __doc__ = '\n    A Filter representing assets falling between percentile bounds of a Factor.\n\n    Parameters\n    ----------\n    factor : zipline.pipeline.factor.Factor\n        The factor over which to compute percentile bounds.\n    min_percentile : float [0.0, 1.0]\n        The minimum percentile rank of an asset that will pass the filter.\n    max_percentile : float [0.0, 1.0]\n        The maxiumum percentile rank of an asset that will pass the filter.\n    '
    window_length = 0

    def __new__(cls, factor, min_percentile, max_percentile, mask):
        return super(PercentileFilter, cls).__new__(cls,
          inputs=(
         factor,),
          mask=mask,
          min_percentile=min_percentile,
          max_percentile=max_percentile)

    def _init(self, min_percentile, max_percentile, *args, **kwargs):
        self._min_percentile = min_percentile
        self._max_percentile = max_percentile
        return (super(PercentileFilter, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, min_percentile, max_percentile, *args, **kwargs):
        return (
         (super(PercentileFilter, cls)._static_identity)(*args, **kwargs),
         min_percentile,
         max_percentile)

    def _validate(self):
        if not 0.0 <= self._min_percentile < self._max_percentile <= 100.0:
            raise BadPercentileBounds(min_percentile=(self._min_percentile),
              max_percentile=(self._max_percentile),
              upper_bound=100.0)
        return super(PercentileFilter, self)._validate()

    def _compute(self, arrays, dates, assets, mask):
        """
        For each row in the input, compute a mask of all values falling between
        the given percentiles.
        """
        data = arrays[0].copy().astype(float64)
        data[~mask] = nan
        lower_bounds = nanpercentile(data,
          (self._min_percentile),
          axis=1,
          keepdims=True)
        upper_bounds = nanpercentile(data,
          (self._max_percentile),
          axis=1,
          keepdims=True)
        return (lower_bounds <= data) & (data <= upper_bounds)


class CustomFilter(PositiveWindowLengthMixin, CustomTermMixin, Filter):
    __doc__ = '\n    Base class for user-defined Filters.\n\n    Parameters\n    ----------\n    inputs : iterable, optional\n        An iterable of `BoundColumn` instances (e.g. USEquityPricing.close),\n        describing the data to load and pass to `self.compute`.  If this\n        argument is passed to the CustomFilter constructor, we look for a\n        class-level attribute named `inputs`.\n    window_length : int, optional\n        Number of rows to pass for each input.  If this argument is not passed\n        to the CustomFilter constructor, we look for a class-level attribute\n        named `window_length`.\n\n    Notes\n    -----\n    Users implementing their own Filters should subclass CustomFilter and\n    implement a method named `compute` with the following signature:\n\n    .. code-block:: python\n\n        def compute(self, today, assets, out, *inputs):\n           ...\n\n    On each simulation date, ``compute`` will be called with the current date,\n    an array of sids, an output array, and an input array for each expression\n    passed as inputs to the CustomFilter constructor.\n\n    The specific types of the values passed to `compute` are as follows::\n\n        today : np.datetime64[ns]\n            Row label for the last row of all arrays passed as `inputs`.\n        assets : np.array[int64, ndim=1]\n            Column labels for `out` and`inputs`.\n        out : np.array[bool, ndim=1]\n            Output array of the same shape as `assets`.  `compute` should write\n            its desired return values into `out`.\n        *inputs : tuple of np.array\n            Raw data arrays corresponding to the values of `self.inputs`.\n\n    See the documentation for\n    :class:`~zipline.pipeline.factors.factor.CustomFactor` for more details on\n    implementing a custom ``compute`` method.\n\n    See Also\n    --------\n    zipline.pipeline.factors.factor.CustomFactor\n    '

    def _validate(self):
        try:
            super(CustomFilter, self)._validate()
        except UnsupportedDataType:
            if self.dtype in CLASSIFIER_DTYPES:
                raise UnsupportedDataType(typename=(type(self).__name__),
                  dtype=(self.dtype),
                  hint='Did you mean to create a CustomClassifier?')
            else:
                if self.dtype in FACTOR_DTYPES:
                    raise UnsupportedDataType(typename=(type(self).__name__),
                      dtype=(self.dtype),
                      hint='Did you mean to create a CustomFactor?')
            raise


class ArrayPredicate(SingleInputMixin, Filter):
    __doc__ = '\n    A filter applying a function from (ndarray, *args) -> ndarray[bool].\n\n    Parameters\n    ----------\n    term : zipline.pipeline.Term\n        Term producing the array over which the predicate will be computed.\n    op : function(ndarray, *args) -> ndarray[bool]\n        Function to apply to the result of `term`.\n    opargs : tuple[hashable]\n        Additional argument to apply to ``op``.\n    '
    params = ('op', 'opargs')
    window_length = 0

    @expect_types(term=Term, opargs=tuple)
    def __new__(cls, term, op, opargs):
        hash(opargs)
        return super(ArrayPredicate, cls).__new__(ArrayPredicate,
          op=op,
          opargs=opargs,
          inputs=(
         term,),
          mask=(term.mask))

    def _compute(self, arrays, dates, assets, mask):
        params = self.params
        data = arrays[0]
        return (params['op'])(data, *params['opargs']) & mask


class Latest(LatestMixin, CustomFilter):
    __doc__ = '\n    Filter producing the most recently-known value of `inputs[0]` on each day.\n    '


class SingleAsset(Filter):
    __doc__ = '\n    A Filter that computes to True only for the given asset.\n    '
    inputs = []
    window_length = 1

    def __new__(cls, asset):
        return super(SingleAsset, cls).__new__(cls, asset=asset)

    def _init(self, asset, *args, **kwargs):
        self._asset = asset
        return (super(SingleAsset, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, asset, *args, **kwargs):
        return (
         (super(SingleAsset, cls)._static_identity)(*args, **kwargs), asset)

    def _compute(self, arrays, dates, assets, mask):
        is_my_asset = assets == self._asset.sid
        out = repeat_first_axis(is_my_asset, len(mask))
        if is_my_asset.sum() != 1 or (out & mask).sum() != len(mask):
            raise NonExistentAssetInTimeFrame(asset=(self._asset),
              start_date=(dates[0]),
              end_date=(dates[(-1)]))
        return out


class StaticSids(Filter):
    __doc__ = '\n    A Filter that computes True for a specific set of predetermined sids.\n\n    ``StaticSids`` is mostly useful for debugging or for interactively\n    computing pipeline terms for a fixed set of sids that are known ahead of\n    time.\n\n    Parameters\n    ----------\n    sids : iterable[int]\n        An iterable of sids for which to filter.\n    '
    inputs = ()
    window_length = 0
    params = ('sids', )

    def __new__(cls, sids):
        sids = frozenset(sids)
        return super(StaticSids, cls).__new__(cls, sids=sids)

    def _compute(self, arrays, dates, sids, mask):
        my_columns = sids.isin(self.params['sids'])
        return repeat_first_axis(my_columns, len(mask)) & mask


class StaticAssets(StaticSids):
    __doc__ = '\n    A Filter that computes True for a specific set of predetermined assets.\n\n    ``StaticAssets`` is mostly useful for debugging or for interactively\n    computing pipeline terms for a fixed set of assets that are known ahead of\n    time.\n\n    Parameters\n    ----------\n    assets : iterable[Asset]\n        An iterable of assets for which to filter.\n    '

    def __new__(cls, assets):
        sids = frozenset(asset.sid for asset in assets)
        return super(StaticAssets, cls).__new__(cls, sids)


class AllPresent(CustomFilter, SingleInputMixin, StandardOutputs):
    __doc__ = 'Pipeline filter indicating input term has data for a given window.\n    '

    def _validate(self):
        if isinstance(self.inputs[0], Filter):
            raise TypeError('Input to filter `AllPresent` cannot be a Filter.')
        return super(AllPresent, self)._validate()

    def compute(self, today, assets, out, value):
        if isinstance(value, LabelArray):
            out[:] = ~np_any((value.is_missing()), axis=0)
        else:
            out[:] = ~np_any((is_missing(value, self.inputs[0].missing_value)),
              axis=0)


class MaximumFilter(Filter, StandardOutputs):
    __doc__ = 'Pipeline filter that selects the top asset, possibly grouped and masked.\n    '
    window_length = 0

    def __new__(cls, factor, groupby, mask):
        return super(MaximumFilter, cls).__new__(cls,
          inputs=(
         factor, groupby),
          mask=mask)

    def _compute(self, arrays, dates, assets, mask):
        data = arrays[0]
        group_labels, null_label = self.inputs[1]._to_integral(arrays[1])
        effective_mask = (mask & (group_labels != null_label) & ~is_missing(data, self.inputs[0].missing_value)).view(uint8)
        return grouped_masked_is_maximal(data.view(int64_dtype), group_labels.astype(int64_dtype), effective_mask)

    def __repr__(self):
        return ('Maximum({}, groupby={}, mask={})'.format)(*self.inputs)