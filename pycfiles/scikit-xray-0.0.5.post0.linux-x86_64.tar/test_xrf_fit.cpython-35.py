# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/tests/test_xrf_fit.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 6877 bytes
from __future__ import absolute_import, division, print_function
import copy, logging, six, numpy as np
from numpy.testing import assert_equal, assert_array_almost_equal
from nose.tools import assert_true, raises, assert_raises
from skxray.core.fitting.base.parameter_data import get_para, e_calibration
from skxray.core.fitting.xrf_model import ModelSpectrum, ParamController, linear_spectrum_fitting, construct_linear_model, trim, sum_area, compute_escape_peak, register_strategy, update_parameter_dict, _set_parameter_hint, _STRATEGY_REGISTRY
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filemode='w')

def synthetic_spectrum():
    param = get_para()
    x = np.arange(2000)
    pileup_peak = ['Si_Ka1-Si_Ka1', 'Si_Ka1-Ce_La1']
    elemental_lines = ['Ar_K', 'Fe_K', 'Ce_L', 'Pt_M'] + pileup_peak
    elist, matv, area_v = construct_linear_model(x, param, elemental_lines, default_area=100000.0)
    return np.sum(matv, 1) + 100


def test_param_controller_fail():
    param = get_para()
    PC = ParamController(param, [])
    assert_raises(ValueError, PC._add_area_param, 'Ar')


def test_parameter_controller():
    param = get_para()
    pileup_peak = ['Si_Ka1-Si_Ka1', 'Si_Ka1-Ce_La1']
    elemental_lines = ['Ar_K', 'Fe_K', 'Ce_L', 'Pt_M'] + pileup_peak
    PC = ParamController(param, elemental_lines)
    set_opt = dict(pos='hi', width='lohi', area='hi', ratio='lo')
    PC.update_element_prop(['Fe_K', 'Ce_L', pileup_peak[0]], **set_opt)
    PC.set_strategy('linear')
    for k, v in six.iteritems(PC.params):
        if 'Fe' in k:
            if 'ratio' in k:
                assert_equal(str(v['bound_type']), set_opt['ratio'])
            if 'center' in k:
                assert_equal(str(v['bound_type']), set_opt['pos'])
            else:
                if 'area' in k:
                    assert_equal(str(v['bound_type']), set_opt['area'])
                elif 'sigma' in k:
                    assert_equal(str(v['bound_type']), set_opt['width'])
        elif 'pileup_' + pileup_peak[0].replace('-', '_') in k:
            if 'ratio' in k:
                assert_equal(str(v['bound_type']), set_opt['ratio'])
            if 'center' in k:
                assert_equal(str(v['bound_type']), set_opt['pos'])
            else:
                if 'area' in k:
                    assert_equal(str(v['bound_type']), set_opt['area'])
                elif 'sigma' in k:
                    assert_equal(str(v['bound_type']), set_opt['width'])


def test_fit():
    param = get_para()
    pileup_peak = ['Si_Ka1-Si_Ka1', 'Si_Ka1-Ce_La1']
    elemental_lines = ['Ar_K', 'Fe_K', 'Ce_L', 'Pt_M'] + pileup_peak
    x0 = np.arange(2000)
    y0 = synthetic_spectrum()
    x, y = trim(x0, y0, 100, 1300)
    MS = ModelSpectrum(param, elemental_lines)
    MS.assemble_models()
    result = MS.model_fit(x, y, weights=1 / np.sqrt(y), maxfev=200)
    for k, v in six.iteritems(result.values):
        if 'area' in k:
            assert_true((v - 100000.0) / 100000.0 < 0.01)

    sum_Fe = sum_area('Fe_K', result)
    assert_true(sum_Fe > 100000.0)
    sum_Ce = sum_area('Ce_L', result)
    assert_true(sum_Ce > 100000.0)
    sum_Pt = sum_area('Pt_M', result)
    assert_true(sum_Pt > 100000.0)
    PC = ParamController(param, elemental_lines)
    new_params = PC.params
    update_parameter_dict(new_params, result)
    for k, v in six.iteritems(new_params):
        if 'area' in k:
            assert_equal(v['value'], result.values[k])

    MS = ModelSpectrum(new_params, elemental_lines)
    MS.assemble_models()
    result = MS.model_fit(x, y, weights=1 / np.sqrt(y), maxfev=200)
    for k, v in six.iteritems(result.values):
        if 'area' in k:
            assert_true((v - 100000.0) / 100000.0 < 0.001)


def test_register():
    new_strategy = e_calibration
    register_strategy('e_calibration', new_strategy, overwrite=False)
    assert_equal(len(_STRATEGY_REGISTRY), 5)
    new_strategy = copy.deepcopy(e_calibration)
    new_strategy['coherent_sct_amplitude'] = 'fixed'
    register_strategy('new_strategy', new_strategy)
    assert_equal(len(_STRATEGY_REGISTRY), 6)


@raises(RuntimeError)
def test_register_error():
    new_strategy = copy.deepcopy(e_calibration)
    new_strategy['coherent_sct_amplitude'] = 'fixed'
    register_strategy('e_calibration', new_strategy, overwrite=False)


def test_pre_fit():
    y0 = synthetic_spectrum()
    x0 = np.arange(len(y0))
    item_list = [
     'Ar_K', 'Fe_K', 'compton', 'elastic']
    param = get_para()
    x, y_total, area_v = linear_spectrum_fitting(x0, y0, param, weights=None)
    for v in item_list:
        assert_true(v in y_total)

    sum1 = np.sum(six.itervalues(y_total))
    r1 = 1 - np.sum((sum1 - y0) ** 2) / np.sum((y0 - np.mean(y0)) ** 2)
    assert_true(r1 > 0.85)
    w = 1 / np.sqrt(y0)
    x, y_total, area_v = linear_spectrum_fitting(x0, y0, param, weights=1 / np.sqrt(y0))
    for v in item_list:
        assert_true(v in y_total)

    sum2 = np.sum(six.itervalues(y_total))
    r2 = 1 - np.sum((sum2 - y0) ** 2) / np.sum((y0 - np.mean(y0)) ** 2)
    assert_true(r2 > 0.85)


def test_escape_peak():
    y0 = synthetic_spectrum()
    ratio = 0.01
    param = get_para()
    xnew, ynew = compute_escape_peak(y0, ratio, param)
    assert_array_almost_equal(np.sum(ynew) / np.sum(y0), ratio, decimal=3)


def test_set_param_hint():
    param = get_para()
    elemental_lines = ['Ar_K', 'Fe_K', 'Ce_L', 'Pt_M']
    bound_options = ['none', 'lohi', 'fixed', 'lo', 'hi']
    MS = ModelSpectrum(param, elemental_lines)
    MS.assemble_models()
    compton = MS.mod.components[0]
    for v in bound_options:
        input_param = {'bound_type': v, 'max': 13.0, 'min': 9.0, 'value': 11.0}
        _set_parameter_hint('coherent_sct_energy', input_param, compton)
        p = compton.make_params()
        if v == 'fixed':
            assert_equal(p['coherent_sct_energy'].vary, False)
        else:
            assert_equal(p['coherent_sct_energy'].vary, True)


@raises(ValueError)
def test_set_param():
    param = get_para()
    elemental_lines = ['Ar_K', 'Fe_K', 'Ce_L', 'Pt_M']
    MS = ModelSpectrum(param, elemental_lines)
    MS.assemble_models()
    compton = MS.mod.components[0]
    input_param = {'bound_type': 'other', 'max': 13.0, 'min': 9.0, 'value': 11.0}
    _set_parameter_hint('coherent_sct_energy', input_param, compton)