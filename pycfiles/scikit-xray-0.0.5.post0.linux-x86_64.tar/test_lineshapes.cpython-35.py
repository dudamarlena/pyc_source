# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/tests/test_lineshapes.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 12311 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from numpy.testing import assert_array_almost_equal
from skxray.core.fitting import gaussian, gausssian_step, gaussian_tail, elastic, compton, lorentzian, lorentzian2, voigt, pvoigt
from skxray.core.fitting import ComptonModel, ElasticModel

def test_gauss_peak():
    """
    test of gauss function from xrf fit
    """
    area = 1
    cen = 0
    std = 1
    x = np.arange(-3, 3, 0.5)
    out = gaussian(x, area, cen, std)
    y_true = [
     0.00443185, 0.0175283, 0.05399097, 0.1295176, 0.24197072,
     0.35206533, 0.39894228, 0.35206533, 0.24197072, 0.1295176,
     0.05399097, 0.0175283]
    assert_array_almost_equal(y_true, out)


def test_gauss_step():
    """
    test of gaussian step function from xrf fit
    """
    y_true = [
     1.0, 1.0, 1.0,
     1.0, 0.999999999, 0.999999713,
     0.999968329, 0.998650102, 0.977249868,
     0.841344746, 0.5, 0.158655254,
     0.0227501319, 0.00134989803, 3.16712418e-05]
    area = 1
    cen = 0
    std = 1
    x = np.arange(-10, 5, 1)
    peak_e = 1.0
    out = gausssian_step(x, area, cen, std, peak_e)
    assert_array_almost_equal(y_true, out)


def test_gauss_tail():
    """
    test of gaussian tail function from xrf fit
    """
    y_true = [
     7.48518299e-05, 0.000203468369, 0.00055308437, 0.00150343919,
     0.00408677027, 0.0111086447, 0.03015662, 0.0802175541,
     0.187729388, 0.30326533, 0.261578292, 0.0375086265,
     0.0022256056, 5.22170501e-05, 4.72608544e-07]
    area = 1
    cen = 0
    std = 1
    x = np.arange(-10, 5, 1)
    gamma = 1.0
    out = gaussian_tail(x, area, cen, std, gamma)
    assert_array_almost_equal(y_true, out)


def test_elastic_peak():
    """
    test of elastic peak from xrf fit
    """
    y_true = [
     0.00085311, 0.00164853, 0.00307974, 0.00556237, 0.00971259,
     0.01639604, 0.02675911, 0.04222145, 0.06440556, 0.09498223,
     0.13542228, 0.18666663, 0.24875512, 0.32048386, 0.39918028,
     0.48068522, 0.55960456, 0.62984039, 0.68534389, 0.72096698,
     0.73324816, 0.72096698, 0.68534389, 0.62984039, 0.55960456,
     0.48068522, 0.39918028, 0.32048386, 0.24875512, 0.18666663,
     0.13542228, 0.09498223, 0.06440556, 0.04222145, 0.02675911,
     0.01639604, 0.00971259, 0.00556237, 0.00307974, 0.00164853]
    area = 1
    energy = 10
    offset = 0.01
    fanoprime = 0.01
    e_offset = 0
    e_linear = 1
    e_quadratic = 0
    ev = np.arange(8, 12, 0.1)
    out = elastic(ev, area, energy, offset, fanoprime, e_offset, e_linear, e_quadratic)
    assert_array_almost_equal(y_true, out)


def test_compton_peak():
    """
    test of compton peak from xrf fit
    """
    y_true = [
     0.01332237, 0.01536984, 0.01870113, 0.02401014, 0.03223281,
     0.04455143, 0.0623487, 0.08709168, 0.12013435, 0.16244524,
     0.2142911, 0.27493377, 0.34241693, 0.41352197, 0.48395163,
     0.5487556, 0.6029529, 0.64224726, 0.66369326, 0.65792554,
     0.63050209, 0.58478146, 0.52510892, 0.45674079, 0.38508357,
     0.31500557, 0.25033778, 0.19362201, 0.14610264, 0.10790876,
     0.07834781, 0.05623019, 0.04016135, 0.02876383, 0.02081757,
     0.01532608, 0.01152704, 0.00886833, 0.00696818, 0.00557234]
    energy = 10
    offset = 0.01
    fano = 0.01
    angle = 90
    fwhm_corr = 1
    amp = 1
    f_step = 0
    f_tail = 0.1
    gamma = 10
    hi_f_tail = 0.1
    hi_gamma = 1
    e_offset = 0
    e_linear = 1
    e_quadratic = 0
    ev = np.arange(8, 12, 0.1)
    out = compton(ev, amp, energy, offset, fano, e_offset, e_linear, e_quadratic, angle, fwhm_corr, f_step, f_tail, gamma, hi_f_tail, hi_gamma)
    assert_array_almost_equal(y_true, out)


def test_lorentzian_peak():
    y_true = [
     0.03151583, 0.03881828, 0.04897075, 0.06366198, 0.0860297,
     0.12242688, 0.18724111, 0.31830989, 0.63661977, 1.59154943,
     3.18309886, 1.59154943, 0.63661977, 0.31830989, 0.18724111,
     0.12242688, 0.0860297, 0.06366198, 0.04897075, 0.03881828]
    x = np.arange(-1, 1, 0.1)
    a = 1
    cen = 0
    std = 0.1
    out = lorentzian(x, a, cen, std)
    assert_array_almost_equal(y_true, out)


def test_lorentzian_squared_peak():
    y_true = [
     0.000312037924, 0.000473393644, 0.00075339618,
     0.00127323954, 0.002325127, 0.00470872613,
     0.0110141829, 0.0318309886, 0.127323954,
     0.795774715, 3.18309886, 0.795774715,
     0.127323954, 0.0318309886, 0.0110141829,
     0.00470872613, 0.002325127, 0.00127323954,
     0.00075339618, 0.000473393644]
    x = np.arange(-1, 1, 0.1)
    a = 1
    cen = 0
    std = 0.1
    out = lorentzian2(x, a, cen, std)
    assert_array_almost_equal(y_true, out)


def test_voigt_peak():
    y_true = [
     0.03248735, 0.04030525, 0.05136683, 0.06778597, 0.09377683,
     0.13884921, 0.22813635, 0.43385822, 0.90715199, 1.65795663,
     2.08709281, 1.65795663, 0.90715199, 0.43385822, 0.22813635,
     0.13884921, 0.09377683, 0.06778597, 0.05136683, 0.04030525]
    x = np.arange(-1, 1, 0.1)
    a = 1
    cen = 0
    std = 0.1
    out1 = voigt(x, a, cen, std, gamma=0.1)
    out2 = voigt(x, a, cen, std)
    assert_array_almost_equal(y_true, out1)
    assert_array_almost_equal(y_true, out2)


def test_pvoigt_peak():
    y_true = [
     0.01575792, 0.01940914, 0.02448538, 0.03183099, 0.04301488,
     0.06122087, 0.09428971, 0.18131419, 0.58826472, 2.00562834,
     3.58626083, 2.00562834, 0.58826472, 0.18131419, 0.09428971,
     0.06122087, 0.04301488, 0.03183099, 0.02448538, 0.01940914]
    x = np.arange(-1, 1, 0.1)
    a = 1
    cen = 0
    std = 0.1
    fraction = 0.5
    out = pvoigt(x, a, cen, std, fraction)
    assert_array_almost_equal(y_true, out)


def test_elastic_model():
    area = 11
    energy = 10
    offset = 0.02
    fanoprime = 0.03
    e_offset = 0
    e_linear = 0.01
    e_quadratic = 0
    true_param = [
     fanoprime, area, energy]
    x = np.arange(800, 1200, 1)
    out = elastic(x, area, energy, offset, fanoprime, e_offset, e_linear, e_quadratic)
    elastic_model = ElasticModel()
    elastic_model.set_param_hint(name='e_offset', value=0, vary=False)
    elastic_model.set_param_hint(name='e_linear', value=0.01, vary=False)
    elastic_model.set_param_hint(name='e_quadratic', value=0, vary=False)
    elastic_model.set_param_hint(name='coherent_sct_energy', value=10, vary=False)
    elastic_model.set_param_hint(name='fwhm_offset', value=0.02, vary=False)
    elastic_model.set_param_hint(name='fwhm_fanoprime', value=0.03, vary=False)
    result = elastic_model.fit(out, x=x, coherent_sct_amplitude=10)
    fitted_val = [
     result.values['fwhm_fanoprime'], result.values['coherent_sct_amplitude'],
     result.values['coherent_sct_energy']]
    assert_array_almost_equal(true_param, fitted_val, decimal=2)


def test_compton_model():
    energy = 10
    offset = 0.001
    fano = 0.01
    angle = 90
    fwhm_corr = 1
    amp = 20
    f_step = 0.05
    f_tail = 0.1
    gamma = 2
    hi_f_tail = 0.01
    hi_gamma = 1
    e_offset = 0
    e_linear = 0.01
    e_quadratic = 0
    x = np.arange(800, 1200, 1.0)
    true_param = [
     energy, amp]
    out = compton(x, amp, energy, offset, fano, e_offset, e_linear, e_quadratic, angle, fwhm_corr, f_step, f_tail, gamma, hi_f_tail, hi_gamma)
    cm = ComptonModel()
    cm.set_param_hint(name='compton_hi_gamma', value=hi_gamma, vary=False)
    cm.set_param_hint(name='fwhm_offset', value=offset, vary=False)
    cm.set_param_hint(name='compton_angle', value=angle, vary=False)
    cm.set_param_hint(name='e_offset', value=e_offset, vary=False)
    cm.set_param_hint(name='e_linear', value=e_linear, vary=False)
    cm.set_param_hint(name='e_quadratic', value=e_quadratic, vary=False)
    cm.set_param_hint(name='fwhm_fanoprime', value=fano, vary=False)
    cm.set_param_hint(name='compton_hi_f_tail', value=hi_f_tail, vary=False)
    cm.set_param_hint(name='compton_f_step', value=f_step, vary=False)
    cm.set_param_hint(name='compton_f_tail', value=f_tail, vary=False)
    cm.set_param_hint(name='compton_gamma', value=gamma, vary=False)
    cm.set_param_hint(name='compton_amplitude', value=20, vary=False)
    cm.set_param_hint(name='compton_fwhm_corr', value=fwhm_corr, vary=False)
    p = cm.make_params()
    result = cm.fit(out, x=x, params=p, compton_amplitude=20, coherent_sct_energy=10)
    fit_val = [
     result.values['coherent_sct_energy'], result.values['compton_amplitude']]
    assert_array_almost_equal(true_param, fit_val, decimal=2)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)