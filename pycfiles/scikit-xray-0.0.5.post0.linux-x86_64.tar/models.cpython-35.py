# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/models.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5987 bytes
from __future__ import absolute_import, division, print_function
import inspect, logging
from lmfit import Model
from .lineshapes import elastic, compton, lorentzian2
from .base.parameter_data import get_para
logger = logging.getLogger(__name__)

def set_default(model_name, func_name):
    """
    Set values and bounds to Model parameters in lmfit.

    Parameters
    ----------
    model_name : class object
        Model class object from lmfit
    func_name : function
        function name of physics peak
    """
    paras = inspect.getargspec(func_name)
    default_len = len(paras.defaults)
    my_args = paras.args[1:]
    para_dict = get_para()
    for name in my_args:
        if name not in para_dict.keys():
            pass
        else:
            my_dict = para_dict[name]
        if my_dict['bound_type'] == 'none':
            model_name.set_param_hint(name, vary=True)
        elif my_dict['bound_type'] == 'fixed':
            model_name.set_param_hint(name, vary=False, value=my_dict['value'])
        elif my_dict['bound_type'] == 'lo':
            model_name.set_param_hint(name, value=my_dict['value'], vary=True, min=my_dict['min'])
        else:
            if my_dict['bound_type'] == 'hi':
                model_name.set_param_hint(name, value=my_dict['value'], vary=True, max=my_dict['max'])
            else:
                if my_dict['bound_type'] == 'lohi':
                    model_name.set_param_hint(name, value=my_dict['value'], vary=True, min=my_dict['min'], max=my_dict['max'])
                else:
                    raise TypeError("Boundary type {0} can't be used".format(my_dict['bound_type']))


def _gen_class_docs(func):
    """
    Parameters
    ----------
    func : function
        function of peak profile

    Returns
    -------
    str :
        documentation of the function
    """
    return 'Wrap the {} function for fitting within lmfit framework\n'.format(func.__name__) + func.__doc__


class ElasticModel(Model):
    __doc__ = _gen_class_docs(elastic)

    def __init__(self, *args, **kwargs):
        super(ElasticModel, self).__init__(elastic, *args, **kwargs)
        self.set_param_hint('epsilon', value=2.96, vary=False)


class ComptonModel(Model):
    __doc__ = _gen_class_docs(compton)

    def __init__(self, *args, **kwargs):
        super(ComptonModel, self).__init__(compton, *args, **kwargs)
        self.set_param_hint('epsilon', value=2.96, vary=False)


class Lorentzian2Model(Model):
    __doc__ = _gen_class_docs(lorentzian2)

    def __init__(self, *args, **kwargs):
        super(Lorentzian2Model, self).__init__(lorentzian2, *args, **kwargs)