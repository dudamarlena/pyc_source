# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\exception.py
# Compiled at: 2018-10-31 04:01:38
# Size of source mod 2**32: 6977 bytes
"""
Created on 2017年8月26日

@author: sharon
"""
from strategycontainer.utils.memoize import lazyval
from textwrap import dedent

class IESException(Exception):
    msg = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @lazyval
    def message(self):
        return str(self)

    def __str__(self):
        msg = (self.msg.format)(**self.kwargs)
        return msg

    __unicode__ = __str__
    __repr__ = __str__


class PortfolioNotFoundException(Exception):
    pass


class PortfolioNotStartException(Exception):
    pass


class RestartException(Exception):
    pass


class ContinueException(Exception):
    pass


class BusinessError(Exception):
    pass


class IncompatibleTerms(IESException):
    __doc__ = '\n    Raised when trying to compute correlations/regressions between two 2D\n    factors with different masks.\n    '
    msg = '{term_1} and {term_2} must have the same mask in order to compute correlations and regressions asset-wise.'


class UnknownRankMethod(IESException):
    __doc__ = '\n    Raised during construction of a Rank factor when supplied a bad Rank\n    method.\n    '
    msg = "Unknown ranking method: '{method}'. `method` must be one of {choices}"


class BadPercentileBounds(IESException):
    __doc__ = '\n    Raised by API functions accepting percentile bounds when the passed bounds\n    are invalid.\n    '
    msg = 'Percentile bounds must fall between 0.0 and {upper_bound}, and min must be less than max.\nInputs were min={min_percentile}, max={max_percentile}.'


class WindowLengthTooLong(IESException):
    __doc__ = '\n    Raised when a trailing window is instantiated with a lookback greater than\n    the length of the underlying array.\n    '
    msg = "Can't construct a rolling window of length {window_length} on an array of length {nrows}.".strip()


class WindowLengthNotPositive(IESException):
    __doc__ = '\n    Raised when a trailing window would be instantiated with a length less than\n    1.\n    '
    msg = 'Expected a window_length greater than 0, got {window_length}.'.strip()


class WindowLengthNotSpecified(IESException):
    __doc__ = '\n    Raised if a user attempts to construct a term without specifying window\n    length and that term does not have a class-level default window length.\n    '
    msg = '{termname} requires a window_length, but no window_length was passed.'


class UnsupportedDType(IESException):
    __doc__ = "\n    Raised when a pipeline Term is constructed with a dtype that's not\n    supported.\n    "
    msg = 'Failed to construct {termname}.\nTSP terms of dtype {dtype} are not yet supported.'


class TermOutputsEmpty(IESException):
    __doc__ = '\n    Raised if a user attempts to construct a term with an empty outputs list.\n    '
    msg = '{termname} requires at least one output when passed an outputs argument.'


class TermInputsNotSpecified(IESException):
    __doc__ = '\n    Raised if a user attempts to construct a term without specifying inputs and\n    that term does not have class-level default inputs.\n    '
    msg = '{termname} requires inputs, but no inputs list was passed.'


class NotDType(IESException):
    __doc__ = "\n    Raised when a pipeline Term is constructed with a dtype that isn't a numpy\n    dtype object.\n    "
    msg = '{termname} expected a numpy dtype object for a dtype, but got {dtype} instead.'


class NonWindowSafeInput(IESException):
    __doc__ = "\n    Raised when a Pipeline API term that is not deemed window safe is specified\n    as an input to another windowed term.\n\n    This is an error because it's generally not safe to compose windowed\n    functions on split/dividend adjusted data.\n    "
    msg = "Can't compute windowed expression {parent} with windowed input {child}."


class NonSliceableTerm(IESException):
    __doc__ = '\n    Raised when attempting to index into a non-sliceable term, e.g. instances\n    of `zipline.pipeline.term.LoadableTerm`.\n    '
    msg = 'Taking slices of {term} is not currently supported.'


class NonExistentAssetInTimeFrame(IESException):
    msg = "The target asset '{asset}' does not exist for the entire timeframe between {start_date} and {end_date}."


class InvalidOutputName(IESException):
    __doc__ = "\n    Raised if a term's output names conflict with any of its attributes.\n    "
    msg = '{output_name!r} cannot be used as an output name for {termname}. Output names cannot start with an underscore or be contained in the following list: {disallowed_names}.'


class DTypeNotSpecified(IESException):
    __doc__ = '\n    Raised if a user attempts to construct a term without specifying dtype and\n    that term does not have class-level default dtype.\n    '
    msg = '{termname} requires a dtype, but no dtype was passed.'


class UnsupportedPipelineOutput(IESException):
    __doc__ = '\n    Raised when a 1D term is added as a column to a pipeline.\n    '
    msg = 'Cannot add column {column_name!r} with term {term}. Adding slices or single-column-output terms as TSP columns is not currently supported.'


class UnsupportedDataType(IESException):
    __doc__ = '\n    Raised by CustomFactors with unsupported dtypes.\n    '

    def __init__(self, hint='', **kwargs):
        if hint:
            hint = ' ' + hint
        kwargs['hint'] = hint
        (super(UnsupportedDataType, self).__init__)(**kwargs)

    msg = '{typename} instances with dtype {dtype} are not supported.{hint}'


class NoFurtherDataError(IESException):
    __doc__ = '\n    Raised by calendar operations that would ask for dates beyond the extent of\n    our known data.\n    '
    msg = '{msg}'

    @classmethod
    def from_lookback_window(cls, initial_message, first_date, lookback_start, lookback_length):
        return cls(msg=dedent('\n                {initial_message}\n\n                lookback window started at {lookback_start}\n                earliest known date was {first_date}\n                {lookback_length} extra rows of data were required\n                ').format(initial_message=initial_message,
          first_date=first_date,
          lookback_start=lookback_start,
          lookback_length=lookback_length))