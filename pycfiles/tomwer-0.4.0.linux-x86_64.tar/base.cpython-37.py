# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/base.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 7281 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/03/2019'
import copy, itertools
from collections import OrderedDict

class _ReconsParam(object):
    __doc__ = '\n    Base class of the Reconstruction parameters\n    '
    _UNSPLIT_KEYS = tuple()

    def __init__(self):
        self._ReconsParam__unmanaged_params = {}
        self._managed_params = {}
        self._ReconsParam__managed_params_property = {}

    def changed(self):
        """callback function when a parameter value is changed"""
        pass

    @property
    def unmanaged_params(self):
        return self._ReconsParam__unmanaged_params

    @property
    def managed_params(self):
        return self._managed_params

    @property
    def all_params(self):
        res = list(self.managed_params.keys())
        res.extend(self.unmanaged_params.keys())
        return res

    def _add_unmanaged_param(self, param, value):
        self._ReconsParam__unmanaged_params[param] = value

    def _reset_unmanaged_params(self):
        self._ReconsParam__unmanaged_params = {}

    def _remove_unmanaged_param(self, param):
        if param in self._ReconsParam__unmanaged_params:
            del self._ReconsParam__unmanaged_params[param]

    def to_dict(self):
        """convert object to a dict readable by fastomo3"""
        raise NotImplementedError()

    @staticmethod
    def from_dict(_dict):
        """create _ReconsParam from a dict readable / writable by fastomo3"""
        raise NotImplementedError()

    def load_from_dict(self, _dict):
        """Update current paramters values from a dictionary"""
        raise NotImplementedError()

    def _get_parameter_value(self, parameter):
        """Find the parameter value from a dict name, to keep compatibility
        with fastomo3."""
        if parameter in self._managed_params:
            return self._managed_params[parameter].fget(self)
        if parameter in self._ReconsParam__unmanaged_params:
            return self.unmanaged_params[parameter]
        raise ValueError('requested parameter is not registered (%s)' % parameter)

    def _set_parameter_value(self, parameter, value):
        """Find the parameter value from a dict name, to keep compatibility
        with fastomo3."""
        if parameter in self._managed_params:
            assert self._managed_params[parameter] is not None
            self._managed_params[parameter].fset(self, value)
        else:
            self._ReconsParam__unmanaged_params[parameter] = value
            self.changed()

    def to_unique_recons_set(self, as_to_dict=False):
        """

        :return: a tuple of unique reconstruction parameters in order to have
                 each parameter as a single value (and no list)
        :param bool as_to_dict: True if we want to get the same value as if we
                                where exporting it with to_dict function. There
                                is some cast in the to_dict function.
        :type: Union[tuple, None]
        :rtype: tuple
        """
        params_list = OrderedDict()
        dict_values = self.to_dict()
        for parameter in self.all_params:
            value = self._get_parameter_value(parameter)
            if isinstance(value, _ReconsParam):
                value = value.to_unique_recons_set(as_to_dict=as_to_dict)
            else:
                if as_to_dict is True:
                    value = dict_values[parameter]
            params_list[parameter] = value
            if parameter in self._UNSPLIT_KEYS:
                params_list[parameter] = [
                 params_list[parameter]]
                continue
            if type(params_list[parameter]) not in (list, tuple):
                params_list[parameter] = [
                 params_list[parameter]]
            if not isinstance(params_list[parameter][0], dict):
                params_list[parameter] = set(params_list[parameter])

        res = list()
        for _set_rp in (itertools.product)(*list(params_list.values())):
            _dict_set = {}
            for key, value in zip(params_list.keys(), _set_rp):
                _dict_set[key] = value

            res.append(_dict_set)

        return tuple(res)

    def __getitem__(self, arg):
        return self._get_parameter_value(arg)

    def __setitem__(self, key, value):
        self._set_parameter_value(parameter=key, value=value)

    def _load_unmanaged_params(self, _dict):
        """reset unmanaged parameters and store all parameters not defined in
        `_managed_params` into __unmanaged_params

        :params dict _dict: dict to parse to find unmanaged parameters
        """
        assert isinstance(_dict, dict)
        self._reset_unmanaged_params()
        for _key in _dict:
            if _key not in self.managed_params:
                _tmp_dict = {_key: _dict[_key]}
                self._ReconsParam__unmanaged_params.update(_tmp_dict)

    def copy(self, other_rp):
        """
        copy parameters value from other_rp

        :param _ReconsParam: reconsparam to copy
        """
        if other_rp is None:
            return
        for parameter_name in other_rp._managed_params:
            value = other_rp._get_parameter_value(parameter=parameter_name)
            if isinstance(value, _ReconsParam) and parameter_name in self:
                self._managed_params[parameter_name].copy(value)
            else:
                self._set_parameter_value(parameter=parameter_name, value=value)

        self._set_unmanaged_params(other_rp.unmanaged_params)

    def _set_unmanaged_params(self, params):
        assert type(params) is dict
        self._ReconsParam__unmanaged_params = copy.copy(params)


class TomoRP(_ReconsParam):
    pass