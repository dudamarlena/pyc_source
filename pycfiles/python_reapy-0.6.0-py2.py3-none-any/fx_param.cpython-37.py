# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\core\fx\fx_param.py
# Compiled at: 2020-03-18 12:09:09
# Size of source mod 2**32: 9380 bytes
import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import DistError

class FXParam(float):
    __doc__ = 'FX parameter.'

    def __init__(self, value, parent_list, index, functions):
        float.__init__(value)
        self.parent_list = parent_list
        self.index = index
        self.functions = functions

    def __new__(self, value, *args, **kwargs):
        return float.__new__(self, value)

    def add_envelope(self):
        """
        Create envelope for the parameter and return it.

        Returns
        -------
        envelope : Envelope
            New envelope for the parameter.

        Notes
        -----
        If the envelope already exists, the function returns it.
        """
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        if isinstance(parent, reapy.Track):
            callback = RPR.GetFXEnvelope
        else:
            callback = self.functions['GetEnvelope']
        envelope = reapy.Envelope(parent, callback(parent.id, parent_fx.index, self.index, True))
        return envelope

    @property
    def envelope(self):
        """
        Parameter envelope (or None if it doesn't exist).

        :type: Envelope or NoneType
        """
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        if isinstance(parent, reapy.Track):
            callback = RPR.GetFXEnvelope
        else:
            callback = self.functions['GetEnvelope']
        envelope = reapy.Envelope(parent, callback(parent.id, parent_fx.index, self.index, False))
        if not envelope._is_defined:
            envelope = None
        return envelope

    def format_value(self, value):
        """
        Return human readable string for value.

        It is the way ``value`` would be printed in REAPER GUI if it
        was the actual parameter value. Only works with FX that
        support Cockos VST extensions.

        Parameters
        ----------
        value : float
            Value to format.

        Returns
        -------
        formatted : str
            Formatted value.
        """
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        return self.functions['FormatParamValue'](parent.id, parent_fx.index, self.index, value, '', 2048)[5]

    @property
    def formatted(self):
        """
        Human readable string for parameter value.

        Only works with FX that support Cockos VST extensions.

        :type: str
        """
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        return self.functions['GetFormattedParamValue'](parent.id, parent_fx.index, self.index, '', 2048)[4]

    @property
    def name(self):
        """
        Parameter name.

        :type: str
        """
        parent_list = self.parent_list
        name = self.functions['GetParamName'](parent_list.parent_id, parent_list.fx_index, self.index, '', 2048)[4]
        return name

    @property
    def normalized(self):
        """
        Normalized FX parameter.

        Attribute can be set with a float, but be careful that since
        floats are immutable, this parameter won't have to right value
        anymore. See Examples below.

        :type: NormalizedFXParam

        Examples
        --------
        Say the parameter range is (0.0, 20.0).

        >>> param = fx.params[0]
        >>> param
        10.0
        >>> param.normalized
        0.5

        If you set the parameter like below, the parameter moves in
        REPAER, but the FXParam object you are using is not valid
        anymore.

        >>> param.normalized = 1
        >>> param, param.normalized
        10.0, 0.5

        You thus have to grab the updated FXParam from the FX like
        below.

        >>> param = fx.params[0]
        >>> param, param.normalized
        20.0, 1.0
        """
        min, max = self.range
        value = (self - min) / (max - min)
        return NormalizedFXParam(value, self.parent_list, self.index, self.functions)

    @normalized.setter
    def normalized(self, value):
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        self.functions['SetParamNormalized'](parent.id, parent_fx.id, self.index, value)

    @property
    def range(self):
        """
        Parameter range.

        :type: float, float
        """
        parent_list = self.parent_list
        min, max = self.functions['GetParam'](parent_list.parent_id, parent_list.fx_index, self.index, 0, 0)[-2:]
        return (min, max)


class FXParamsList(ReapyObjectList):
    __doc__ = '\n    Container class for a list of FX parameters.\n\n    Parameters can be accessed by name or index.\n\n    Examples\n    --------\n    >>> params_list = fx.params\n    >>> params_list[0]  # Say this is "Dry Gain" parameter\n    0.5\n    >>> params_list["Dry Gain"]\n    0.5\n    >>> params_list["Dry Gain"] = 0.1\n    >>> params_list[0]\n    0.1\n    '

    def __init__(self, parent_fx=None, parent_id=None, parent_fx_index=None):
        if parent_fx is None:
            parent_fx = reapy.FX(parent_id=parent_id, index=parent_fx_index)
        self.parent_id = parent_fx.parent_id
        self.fx_index = parent_fx.index
        self.functions = parent_fx.functions

    def __getitem__(self, i):
        with reapy.inside_reaper():
            if isinstance(i, str):
                i = self._get_param_index(i)
            n_params = len(self)
            if i >= n_params:
                raise IndexError('{} has only {} params'.format(self.parent_fx, n_params))
            i = i % n_params
        value = self.functions['GetParam'](self.parent_id, self.fx_index, i, 0, 0)[0]
        param = FXParam(value, self, i, self.functions)
        return param

    def __iter__(self):
        for i, value in enumerate(self._get_values()):
            yield FXParam(value, self, i, self.functions)

    def __len__(self):
        length = self.parent_fx.n_params
        return length

    def __setitem__(self, i, value):
        with reapy.inside_reaper():
            if isinstance(i, str):
                i = self._get_param_index(i)
            n_params = len(self)
            if i >= n_params:
                raise IndexError('{} has only {} params'.format(self.parent_fx, n_params))
            i = i % n_params
        self.functions['SetParam'](self.parent_id, self.fx_index, i, value)

    @reapy.inside_reaper()
    def _get_param_index(self, name):
        try:
            return [fx.name for fx in self].index(name)
        except ValueError:
            raise IndexError('{} has no param named {}'.format(self.parent_fx, name))

    @reapy.inside_reaper()
    def _get_values(self):
        """Return values of all parameters in self."""
        return [self.functions['GetParam'](self.parent_id, self.fx_index, i, 0, 0)[0] for i in range(len(self))]

    @property
    def _kwargs(self):
        return {'parent_fx_index':self.fx_index, 
         'parent_id':self.parent_id}

    @property
    def parent_fx(self):
        """
        Parent FX.

        :type: FX
        """
        fx = reapy.FX(parent_id=(self.parent_id), index=(self.fx_index))
        return fx


class NormalizedFXParam(FXParam):
    __doc__ = '\n    Normalized FX parameter.\n\n    Access it via FXParam.normalized.\n\n    Examples\n    --------\n    >>> fx.params[0]\n    0.0\n    >>> fx.params[0].range\n    (-2.0, 0.0)\n    >>> fx.params[0].normalized\n    1.0\n    >>> fx.params[0].normalized.range\n    (0.0, 1.0)\n    '

    def format_value(self, value):
        """
        Return human readable string for value.

        It is the way ``value`` would be printed in REAPER GUI if it
        was the actual parameter value. Only works with FX that
        support Cockos VST extensions.

        Parameters
        ----------
        value : float
            Value to format.

        Returns
        -------
        formatted : str
            Formatted value.
        """
        parent_fx = self.parent_list.parent_fx
        parent = parent_fx.parent
        return self.functions['FormatParamValueNormalized'](parent.id, parent_fx.index, self.index, value, '', 2048)[5]

    @property
    def range(self):
        """
        Parameter range (always equal to (0.0, 1.0)).
        """
        return (0.0, 1.0)

    @property
    def raw(self):
        """
        Raw (i.e. unnormalized) parameter.

        :type: FXParam
        """
        return self.parent_list[self.index]