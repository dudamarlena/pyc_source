# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\mixins.py
# Compiled at: 2018-08-23 04:29:10
# Size of source mod 2**32: 19892 bytes
"""
Mixins classes for use with Filters and Factors.
"""
from textwrap import dedent
from .factor_out_cache import factorOutCache
from numpy import array, full, recarray, vstack
from pandas import NaT as pd_NaT
from strategycontainer.exception import WindowLengthNotPositive, UnsupportedDataType, NoFurtherDataError
from strategycontainer.utils.context_tricks import nop_context
from strategycontainer.utils.input_validation import expect_types
from strategycontainer.utils.sharedoc import format_docstring, PIPELINE_ALIAS_NAME_DOC, PIPELINE_DOWNSAMPLING_FREQUENCY_DOC
from strategycontainer.utils.pandas_utils import nearest_unequal_elements
from .downsample_helpers import select_sampling_indices, expect_downsample_frequency
from .sentinels import NotSpecified
from .term import Term

class PositiveWindowLengthMixin(object):
    __doc__ = '\n    Validation mixin enforcing that a Term gets a positive WindowLength\n    '

    def _validate(self):
        super(PositiveWindowLengthMixin, self)._validate()
        if not self.windowed:
            raise WindowLengthNotPositive(window_length=(self.window_length))


class SingleInputMixin(object):
    __doc__ = '\n    Validation mixin enforcing that a Term gets a length-1 inputs list.\n    '

    def _validate(self):
        super(SingleInputMixin, self)._validate()
        num_inputs = len(self.inputs)
        if num_inputs != 1:
            raise ValueError('{typename} expects only one input, but received {num_inputs} instead.'.format(typename=(type(self).__name__),
              num_inputs=num_inputs))


class StandardOutputs(object):
    __doc__ = '\n    Validation mixin enforcing that a Term cannot produce non-standard outputs.\n    '

    def _validate(self):
        super(StandardOutputs, self)._validate()
        if self.outputs is not NotSpecified:
            raise ValueError('{typename} does not support custom outputs, but received custom outputs={outputs}.'.format(typename=(type(self).__name__),
              outputs=(self.outputs)))


class RestrictedDTypeMixin(object):
    __doc__ = '\n    Validation mixin enforcing that a term has a specific dtype.\n    '
    ALLOWED_DTYPES = NotSpecified

    def _validate(self):
        super(RestrictedDTypeMixin, self)._validate()
        assert self.ALLOWED_DTYPES is not NotSpecified, 'ALLOWED_DTYPES not supplied on subclass of RestrictedDTypeMixin: %s.' % type(self).__name__
        if self.dtype not in self.ALLOWED_DTYPES:
            raise UnsupportedDataType(typename=(type(self).__name__),
              dtype=(self.dtype))


class CustomTermMixin(object):
    __doc__ = '\n    Mixin for user-defined rolling-window Terms.\n\n    Implements `_compute` in terms of a user-defined `compute` function, which\n    is mapped over the input windows.\n\n    Used by CustomFactor, CustomFilter, CustomClassifier, etc.\n    '
    ctx = nop_context

    def __new__(cls, inputs=NotSpecified, outputs=NotSpecified, window_length=NotSpecified, mask=NotSpecified, dtype=NotSpecified, missing_value=NotSpecified, ndim=NotSpecified, **kwargs):
        unexpected_keys = set(kwargs) - set(cls.params)
        if unexpected_keys:
            raise TypeError('{termname} received unexpected keyword arguments {unexpected}'.format(termname=(cls.__name__),
              unexpected={k:kwargs[k] for k in unexpected_keys}))
        return (super(CustomTermMixin, cls).__new__)(
 cls, inputs=inputs, 
         outputs=outputs, 
         window_length=window_length, 
         mask=mask, 
         dtype=dtype, 
         missing_value=missing_value, 
         ndim=ndim, **kwargs)

    def compute(self, today, assets, out, *arrays):
        """
        Override this method with a function that writes a value into `out`.
        """
        raise NotImplementedError()

    def _allocate_output(self, windows, shape):
        """
        Allocate an output array whose rows should be passed to `self.compute`.

        The resulting array must have a shape of ``shape``.

        If we have standard outputs (i.e. self.outputs is NotSpecified), the
        default is an empty ndarray whose dtype is ``self.dtype``.

        If we have an outputs tuple, the default is an empty recarray with
        ``self.outputs`` as field names. Each field will have dtype
        ``self.dtype``.

        This can be overridden to control the kind of array constructed
        (e.g. to produce a LabelArray instead of an ndarray).
        """
        missing_value = self.missing_value
        outputs = self.outputs
        if outputs is not NotSpecified:
            out = recarray(shape,
              formats=([
             self.dtype.str] * len(outputs)),
              names=outputs)
            out[:] = missing_value
        else:
            out = full(shape, missing_value, dtype=(self.dtype))
        return out

    def _format_inputs(self, windows, column_mask):
        inputs = []
        for input_ in windows:
            window = next(input_)
            if window.shape[1] == 1:
                inputs.append(window)
            else:
                inputs.append(window[:, column_mask])

        return inputs

    def _compute(self, windows, dates, assets, mask):
        """
        Call the user's `compute` function on each window with a pre-built
        output array.
        """
        format_inputs = self._format_inputs
        compute = self.compute
        params = self.params
        ndim = self.ndim
        shape = (len(mask), 1) if ndim == 1 else mask.shape
        out = self._allocate_output(windows, shape)
        with self.ctx:
            for idx, date in enumerate(dates):
                out_mask = array([True]) if ndim == 1 else mask[idx]
                inputs_mask = mask[idx]
                masked_assets = assets[inputs_mask]
                out_row = out[idx][out_mask]
                inputs = format_inputs(windows, inputs_mask)
                cached_out = factorOutCache[self].getCache(date.strftime('%Y%m%d'))
                if cached_out is not None:
                    out[idx][out_mask] = cached_out
                else:
                    compute(date, masked_assets, out_row, *inputs, **params)
                    out[idx][out_mask] = out_row

            factorOutCache[self].clearCache()
        return out

    def short_repr(self):
        """Short repr to use when rendering Pipeline graphs."""
        return type(self).__name__ + '(%d)' % self.window_length


class LatestMixin(SingleInputMixin):
    __doc__ = '\n    Mixin for behavior shared by Custom{Factor,Filter,Classifier}.\n    '
    window_length = 1

    def compute(self, today, assets, out, data):
        out[:] = data[(-1)]

    def _validate(self):
        super(LatestMixin, self)._validate()
        if self.inputs[0].dtype != self.dtype:
            raise TypeError('{name} expected an input of dtype {expected}, but got {actual} instead.'.format(name=(type(self).__name__),
              expected=(self.dtype),
              actual=(self.inputs[0].dtype)))

    def short_repr(self):
        return '{}.latest'.format(self.inputs[0].short_repr())


class AliasedMixin(SingleInputMixin):
    __doc__ = '\n    Mixin for aliased terms.\n    '

    def __new__(cls, term, name):
        return super(AliasedMixin, cls).__new__(cls,
          inputs=(
         term,),
          outputs=(term.outputs),
          window_length=0,
          name=name,
          dtype=(term.dtype),
          missing_value=(term.missing_value),
          ndim=(term.ndim),
          window_safe=(term.window_safe))

    def _init(self, name, *args, **kwargs):
        self.name = name
        return (super(AliasedMixin, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, name, *args, **kwargs):
        return (
         (super(AliasedMixin, cls)._static_identity)(*args, **kwargs),
         name)

    def _compute(self, inputs, dates, assets, mask):
        return inputs[0]

    def __repr__(self):
        return '{type}({inner_type}(...), name={name!r})'.format(type=(type(self).__name__),
          inner_type=(type(self.inputs[0]).__name__),
          name=(self.name))

    def short_repr(self):
        """Short repr to use when rendering Pipeline graphs."""
        return self.name

    @classmethod
    def make_aliased_type(cls, other_base):
        """
        Factory for making Aliased{Filter,Factor,Classifier}.
        """
        docstring = dedent('\n            A {t} that names another {t}.\n\n            Parameters\n            ----------\n            term : {t}\n            {{name}}\n            ').format(t=(other_base.__name__))
        doc = format_docstring(owner_name=(other_base.__name__),
          docstring=docstring,
          formatters={'name': PIPELINE_ALIAS_NAME_DOC})
        return type('Aliased' + other_base.__name__, (
         cls, other_base), {'__doc__':doc, 
         '__module__':other_base.__module__})


class DownsampledMixin(StandardOutputs):
    __doc__ = '\n    Mixin for behavior shared by Downsampled{Factor,Filter,Classifier}\n\n    A downsampled term is a wrapper around the "real" term that performs actual\n    computation. The downsampler is responsible for calling the real term\'s\n    `compute` method at selected intervals and forward-filling the computed\n    values.\n\n    Downsampling is not currently supported for terms with multiple outputs.\n    '
    window_safe = False

    @expect_types(term=Term)
    @expect_downsample_frequency
    def __new__(cls, term, frequency):
        return super(DownsampledMixin, cls).__new__(cls,
          inputs=(term.inputs),
          outputs=(term.outputs),
          window_length=(term.window_length),
          mask=(term.mask),
          frequency=frequency,
          wrapped_term=term,
          dtype=(term.dtype),
          missing_value=(term.missing_value),
          ndim=(term.ndim))

    def _init(self, frequency, wrapped_term, *args, **kwargs):
        self._frequency = frequency
        self._wrapped_term = wrapped_term
        return (super(DownsampledMixin, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, frequency, wrapped_term, *args, **kwargs):
        return (
         (super(DownsampledMixin, cls)._static_identity)(*args, **kwargs),
         frequency,
         wrapped_term)

    def compute_extra_rows(self, all_dates, start_date, end_date, min_extra_rows):
        """
        Ensure that min_extra_rows pushes us back to a computation date.

        Parameters
        ----------
        all_dates : pd.DatetimeIndex
            The trading sessions against which ``self`` will be computed.
        start_date : pd.Timestamp
            The first date for which final output is requested.
        end_date : pd.Timestamp
            The last date for which final output is requested.
        min_extra_rows : int
            The minimum number of extra rows required of ``self``, as
            determined by other terms that depend on ``self``.

        Returns
        -------
        extra_rows : int
            The number of extra rows to compute.  This will be the minimum
            number of rows required to make our computed start_date fall on a
            recomputation date.
        """
        try:
            current_start_pos = all_dates.get_loc(start_date) - min_extra_rows
            if current_start_pos < 0:
                raise NoFurtherDataError.from_lookback_window(initial_message='Insufficient data to compute Pipeline:',
                  first_date=(all_dates[0]),
                  lookback_start=start_date,
                  lookback_length=min_extra_rows)
        except KeyError:
            before, after = nearest_unequal_elements(all_dates, start_date)
            raise ValueError('Pipeline start_date {start_date} is not in calendar.\nLatest date before start_date is {before}.\nEarliest date after start_date is {after}.'.format(start_date=start_date,
              before=before,
              after=after))

        candidates = all_dates[:current_start_pos + 1]
        choices = select_sampling_indices(candidates, self._frequency)
        new_start_date = candidates[choices[(-1)]]
        new_start_pos = all_dates.get_loc(new_start_date)
        assert new_start_pos <= current_start_pos, 'Computed negative extra rows!'
        return min_extra_rows + (current_start_pos - new_start_pos)

    def _compute(self, inputs, dates, assets, mask):
        """
        Compute by delegating to self._wrapped_term._compute on sample dates.

        On non-sample dates, forward-fill from previously-computed samples.
        """
        to_sample = dates[select_sampling_indices(dates, self._frequency)]
        if not to_sample[0] == dates[0]:
            raise AssertionError('Misaligned sampling dates in %s.' % type(self).__name__)
        else:
            real_compute = self._wrapped_term._compute
            if self.windowed:

                def prepare_inputs():
                    return inputs

                def skip_this_input():
                    for w in inputs:
                        next(w)

            else:

                def prepare_inputs():
                    return [a[[i]] for a in inputs]

            def skip_this_input():
                pass

        results = []
        samples = iter(to_sample)
        next_sample = next(samples)
        for i, compute_date in enumerate(dates):
            if next_sample == compute_date:
                results.append(real_compute(prepare_inputs(), dates[i:i + 1], assets, mask[i:i + 1]))
                try:
                    next_sample = next(samples)
                except StopIteration:
                    next_sample = pd_NaT

            else:
                skip_this_input()
                results.append(results[(-1)])

        try:
            next_sample = next(samples)
        except StopIteration:
            pass
        else:
            raise AssertionError('Unconsumed sample date: %s' % next_sample)
        return vstack(results)

    @classmethod
    def make_downsampled_type(cls, other_base):
        """
        Factory for making Downsampled{Filter,Factor,Classifier}.
        """
        docstring = dedent('\n            A {t} that defers to another {t} at lower-than-daily frequency.\n\n            Parameters\n            ----------\n            term : {t}\n            {{frequency}}\n            ').format(t=(other_base.__name__))
        doc = format_docstring(owner_name=(other_base.__name__),
          docstring=docstring,
          formatters={'frequency': PIPELINE_DOWNSAMPLING_FREQUENCY_DOC})
        return type('Downsampled' + other_base.__name__, (
         cls, other_base), {'__doc__':doc, 
         '__module__':other_base.__module__})