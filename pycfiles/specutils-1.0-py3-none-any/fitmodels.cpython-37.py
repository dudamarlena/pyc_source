# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/fitting/fitmodels.py
# Compiled at: 2020-03-18 11:09:56
# Size of source mod 2**32: 31079 bytes
import itertools, logging, operator
import astropy.units as u
import numpy as np
from astropy.modeling import fitting, Model, models
from astropy.table import QTable
from scipy.signal import convolve
import astropy.units as u
from astropy.stats import sigma_clipped_stats
from spectra.spectral_region import SpectralRegion
from spectra.spectrum1d import Spectrum1D
from ..utils import QuantityModel
from ..analysis import fwhm, gaussian_sigma_width, centroid, warn_continuum_below_threshold
from ..manipulation import extract_region, noise_region_uncertainty
from manipulation.utils import excise_regions
__all__ = [
 'find_lines_threshold', 'find_lines_derivative', 'fit_lines',
 'estimate_line_parameters']
_parameter_estimators = {'Gaussian1D':{'amplitude':lambda s: max(s.flux), 
  'mean':lambda s: centroid(s, region=None), 
  'stddev':lambda s: gaussian_sigma_width(s)}, 
 'Lorentz1D':{'amplitude':lambda s: max(s.flux), 
  'x_0':lambda s: centroid(s, region=None), 
  'fwhm':lambda s: fwhm(s)}, 
 'Voigt1D':{'x_0':lambda s: centroid(s, region=None), 
  'amplitude_L':lambda s: max(s.flux), 
  'fwhm_L':lambda s: fwhm(s) / np.sqrt(2), 
  'fwhm_G':lambda s: fwhm(s) / np.sqrt(2)}}

def _set_parameter_estimators(model):
    """
    Helper method used in method below.
    """
    if model.__class__.__name__ in _parameter_estimators:
        model_pars = _parameter_estimators[model.__class__.__name__]
        for name in model.param_names:
            par = getattr(model, name)
            setattr(par, 'estimator', model_pars[name])

    return model


def estimate_line_parameters(spectrum, model):
    """
    The input ``model`` parameters will be estimated from the input
    ``spectrum``. The ``model`` can be specified with default parameters, for
    example ``Gaussian1D()``.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The spectrum object from which we will estimate the model parameters.

    model : `~astropy.modeling.Model`
        Model for which we want to estimate parameters from the spectrum.

    Returns
    -------
    model : `~astropy.modeling.Model`
        Model with parameters estimated.
    """
    model = _set_parameter_estimators(model)
    for name in model.param_names:
        par = getattr(model, name)
        try:
            estimator = getattr(par, 'estimator')
            setattr(model, name, estimator(spectrum))
        except AttributeError:
            raise Exception('No method to estimate parameter {}'.format(name))

    return model


def _consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)


@warn_continuum_below_threshold(threshold=0.01)
def find_lines_threshold(spectrum, noise_factor=1):
    """
    Find the emission and absorption lines in a spectrum. The method
    here is based on deviations larger than the spectrum's uncertainty by the
    ``noise_factor``.

    This method only works with continuum-subtracted spectra and the
    uncertainty must be defined on the spectrum. To add the uncertainty,
    one could use `~specutils.manipulation.noise_region_uncertainty` to add
    the uncertainty.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The spectrum object in which the lines will be found.

    noise_factor : float
       ``noise_factor`` multiplied by the spectrum's``uncertainty``, used for
        thresholding.

    Returns
    -------
    qtable: `~astropy.table.QTable`
        Table of emission and absorption lines. Line center (``line_center``),
        line type (``line_type``) and index of line center
        (``line_center_index``) are stored for each line.
    """
    uncertainty = spectrum.uncertainty
    inds = np.where(np.abs(spectrum.flux) > noise_factor * uncertainty.array * spectrum.flux.unit)[0]
    pos_inds = inds[(spectrum.flux.value[inds] > 0)]
    line_inds_grouped = _consecutive(pos_inds, stepsize=1)
    if len(line_inds_grouped[0]) > 0:
        emission_inds = [inds[np.argmax(spectrum.flux.value[inds])] for inds in line_inds_grouped]
    else:
        emission_inds = []
    neg_inds = inds[(spectrum.flux.value[inds] < 0)]
    line_inds_grouped = _consecutive(neg_inds, stepsize=1)
    if len(line_inds_grouped[0]) > 0:
        absorption_inds = [inds[np.argmin(spectrum.flux.value[inds])] for inds in line_inds_grouped]
    else:
        absorption_inds = []
    qtable = QTable()
    qtable['line_center'] = list((itertools.chain)(*[
     spectrum.spectral_axis.value[emission_inds],
     spectrum.spectral_axis.value[absorption_inds]])) * spectrum.spectral_axis.unit
    qtable['line_type'] = ['emission'] * len(emission_inds) + [
     'absorption'] * len(absorption_inds)
    qtable['line_center_index'] = list((itertools.chain)(*[
     emission_inds, absorption_inds]))
    return qtable


@warn_continuum_below_threshold(threshold=0.01)
def find_lines_derivative(spectrum, flux_threshold=None):
    """
    Find the emission and absorption lines in a spectrum. The method
    here is based on finding the zero crossings in the derivative
    of the spectrum.

    Parameters
    ----------
    spectrum : Spectrum1D
        The spectrum object over which the equivalent width will be calculated.
    flux_threshold : float, `~astropy.units.Quantity` or None
        The threshold a pixel must be above to be considered part of a line. If
        a float, will assume the same units as ``spectrum.flux``. This
        threshold is above and beyond the derivative searching step. Default
        is None so no thresholding. The threshold is positive for emission
        lines and negative for absorption lines.

    Returns
    -------
    qtable: `~astropy.table.QTable`
        Table of emission and absorption lines. Line center (``line_center``),
        line type (``line_type``) and index of line center
        (``line_center_index``) are stored for each line.
    """
    kernel = [
     1, 0, -1]
    dY = convolve(spectrum.flux, kernel, 'valid')
    S = np.sign(dY)
    ddS = convolve(S, kernel, 'valid')
    if flux_threshold is not None:
        if isinstance(flux_threshold, (int, float)):
            flux_threshold = float(flux_threshold) * spectrum.flux.unit
    candidates = np.where(dY > 0)[0] + (len(kernel) - 1)
    line_inds = sorted(set(candidates).intersection(np.where(ddS == -2)[0] + 1))
    if flux_threshold is not None:
        line_inds = np.array(line_inds)[(spectrum.flux[line_inds] > flux_threshold)]
    else:
        line_inds_grouped = _consecutive(line_inds, stepsize=1)
        if len(line_inds_grouped[0]) > 0:
            emission_inds = [inds[np.argmax(spectrum.flux[inds])] for inds in line_inds_grouped]
        else:
            emission_inds = []
        candidates = np.where(dY < 0)[0] + (len(kernel) - 1)
        line_inds = sorted(set(candidates).intersection(np.where(ddS == 2)[0] + 1))
        if flux_threshold is not None:
            line_inds = np.array(line_inds)[(spectrum.flux[line_inds] < -flux_threshold)]
        line_inds_grouped = _consecutive(line_inds, stepsize=1)
        if len(line_inds_grouped[0]) > 0:
            absorption_inds = [inds[np.argmin(spectrum.flux[inds])] for inds in line_inds_grouped]
        else:
            absorption_inds = []
    qtable = QTable()
    qtable['line_center'] = list((itertools.chain)(*[
     spectrum.spectral_axis.value[emission_inds],
     spectrum.spectral_axis.value[absorption_inds]])) * spectrum.spectral_axis.unit
    qtable['line_type'] = ['emission'] * len(emission_inds) + [
     'absorption'] * len(absorption_inds)
    qtable['line_center_index'] = list((itertools.chain)(*[
     emission_inds, absorption_inds]))
    return qtable


def fit_lines(spectrum, model, fitter=fitting.LevMarLSQFitter(), exclude_regions=None, weights=None, window=None, **kwargs):
    """
    Fit the input models to the spectrum. The parameter values of the
    input models will be used as the initial conditions for the fit.

    Parameters
    ----------
    spectrum : Spectrum1D
        The spectrum object over which the equivalent width will be calculated.
    model: `~astropy.modeling.Model` or list of `~astropy.modeling.Model`
        The model or list of models that contain the initial guess.
    fitter : `~astropy.modeling.fitting.Fitter`, optional
        Fitter instance to be used when fitting model to spectrum.
    exclude_regions : list of `~specutils.SpectralRegion`
        List of regions to exclude in the fitting.
    weights : array-like or 'unc', optional
        If 'unc', the unceratinties from the spectrum object are used to
        to calculate the weights. If array-like, represents the weights to
        use in the fitting.  Note that if a mask is present on the spectrum, it
        will be applied to the ``weights`` as it would be to the spectrum
        itself.
    window : `~specutils.SpectralRegion` or list of `~specutils.SpectralRegion`
        Regions of the spectrum to use in the fitting. If None, then the
        whole spectrum will be used in the fitting.
    Additional keyword arguments are passed directly into the call to the
    ``fitter``.

    Returns
    -------
    models : Compound model of `~astropy.modeling.Model`
        A compound model of models with fitted parameters.

    Notes
    -----
       * Could add functionality to set the bounds in
         ``model`` if they are not set.
       * The models in the list of ``model`` are added
          together and passed as a compound model to the
          `~astropy.modeling.fitting.Fitter` class instance.
    """
    if exclude_regions is not None:
        spectrum = excise_regions(spectrum, exclude_regions)
    single_model_in = not isinstance(model, list)
    if single_model_in:
        model = [
         model]
    fitted_models = []
    for modeli, model_guess in enumerate(model):
        if window is not None and isinstance(window, list):
            model_window = window[modeli]
        else:
            if window is not None:
                model_window = window
            else:
                model_window = None
        ignore_units = getattr(model_guess, model_guess.param_names[0]).unit is None
        fit_model = _fit_lines(spectrum, model_guess, fitter, 
         exclude_regions, weights, model_window, 
         ignore_units, **kwargs)
        if model_guess.name is not None:
            fit_model.name = model_guess.name
        fitted_models.append(fit_model)

    if single_model_in:
        fitted_models = fitted_models[0]
    return fitted_models


def _fit_lines(spectrum, model, fitter=fitting.LevMarLSQFitter(), exclude_regions=None, weights=None, window=None, ignore_units=False, **kwargs):
    """
    Fit the input model (initial conditions) to the spectrum.  Output will be
    the same model with the parameters set based on the fitting.

    spectrum, model -> model
    """
    if exclude_regions is not None:
        spectrum = excise_regions(spectrum, exclude_regions)
    elif isinstance(weights, str):
        if weights == 'unc':
            uncerts = spectrum.uncertainty
            if uncerts is not None:
                weights = uncerts.array ** (-1)
            else:
                logging.warning('Uncertainty values are not defined, but are trying to be used in model fitting.')
        else:
            raise ValueError('Unrecognized value `%s` in keyword argument.', weights)
    elif weights is not None:
        weights = np.array(weights)
    mask = spectrum.mask
    dispersion = spectrum.spectral_axis
    dispersion_unit = spectrum.spectral_axis.unit
    flux = spectrum.flux
    flux_unit = spectrum.flux.unit
    window_indices = None
    if window is not None and isinstance(window, (float, int)):
        center = model.mean
        window_indices = np.nonzero((spectrum.spectral_axis >= center - window) & (spectrum.spectral_axis < center + window))
    else:
        if window is not None and isinstance(window, tuple):
            window_indices = np.nonzero((dispersion >= window[0]) & (dispersion < window[1]))
        else:
            if window is not None:
                if isinstance(window, SpectralRegion):
                    idx1, idx2 = window.bounds
                    if idx1 == idx2:
                        raise IndexError('Tried to fit a region containing no pixels.')
                    idxarr = np.arange(spectrum.flux.size).reshape(spectrum.flux.shape)
                    index_spectrum = Spectrum1D(spectral_axis=(spectrum.spectral_axis), flux=u.Quantity(idxarr, (u.Jy), dtype=int))
                    extracted_regions = extract_region(index_spectrum, window)
                    if isinstance(extracted_regions, list):
                        if len(extracted_regions) == 0:
                            raise ValueError('The whole spectrum is windowed out!')
                        window_indices = np.concatenate([s.flux.value.astype(int) for s in extracted_regions])
                    else:
                        if len(extracted_regions.flux) == 0:
                            raise ValueError('The whole spectrum is windowed out!')
                        window_indices = extracted_regions.flux.value.astype(int)
            else:
                if window_indices is not None:
                    dispersion = dispersion[window_indices]
                    flux = flux[window_indices]
                    if mask is not None:
                        mask = mask[window_indices]
                    if weights is not None:
                        weights = weights[window_indices]
                if flux is None or len(flux) == 0:
                    raise Exception('Spectrum flux is empty or None.')
                input_spectrum = spectrum
                spectrum = Spectrum1D(flux=(flux.value * flux_unit),
                  spectral_axis=(dispersion.value * dispersion_unit),
                  wcs=(input_spectrum.wcs),
                  velocity_convention=(input_spectrum.velocity_convention),
                  rest_value=(input_spectrum.rest_value))
                model_unitless, dispersion_unitless, flux_unitless = _strip_units_from_model(model, spectrum, convert=(not ignore_units))
                if mask is not None:
                    nmask = ~mask
                    dispersion_unitless = dispersion_unitless[nmask]
                    flux_unitless = flux_unitless[nmask]
                    if weights is not None:
                        weights = weights[nmask]
            fit_model_unitless = fitter(model_unitless, dispersion_unitless,
 flux_unitless, weights=weights, **kwargs)
            if not ignore_units:
                fit_model = _add_units_to_model(fit_model_unitless, model, spectrum)
            else:
                fit_model = QuantityModel(fit_model_unitless, spectrum.spectral_axis.unit, spectrum.flux.unit)
            return fit_model


def _convert(quantity, dispersion_unit, dispersion, flux_unit):
    """
    Convert the quantity to the spectrum's units, and then we will use
    the *value* of it in the new unitless-model.
    """
    with u.set_enabled_equivalencies(u.spectral()):
        if quantity.unit.is_equivalent(dispersion_unit):
            quantity = quantity.to(dispersion_unit)
    with u.set_enabled_equivalencies(u.spectral_density(dispersion)):
        if quantity.unit.is_equivalent(flux_unit):
            quantity = quantity.to(flux_unit)
    return quantity


def _convert_and_dequantify(poss_quantity, dispersion_unit, dispersion, flux_unit, convert=True):
    """
    This method will convert the ``poss_quantity`` value to the proper
    dispersion or flux units and then strip the units.

    If the ``poss_quantity`` is None, or a number, we just return that.

    Notes
    -----
        This method can be removed along with most of the others here
        when astropy.fitting will fit models that contain units.

    """
    if poss_quantity is None or isinstance(poss_quantity, (float, int)):
        return poss_quantity
    if convert and hasattr(poss_quantity, 'quantity') and poss_quantity.quantity is not None:
        q = poss_quantity.quantity
        quantity = _convert(q, dispersion_unit, dispersion, flux_unit)
        v = quantity.value
    else:
        if convert and isinstance(poss_quantity, u.Quantity):
            quantity = _convert(poss_quantity, dispersion_unit, dispersion, flux_unit)
            v = quantity.value
        else:
            v = poss_quantity.value
    return v


def _strip_units_from_model(model_in, spectrum, convert=True):
    """
    This method strips the units from the model, so the result can
    be passed to the fitting routine. This is necessary as CoumpoundModel
    with units does not work in the fitters.

    Notes
    -----
        When CompoundModel with units works in the fitters this method
        can be removed.

        This assumes there are two types of models, those that are
        based on `~astropy.modeling.models.PolynomialModel` and therefore
        require the ``degree`` parameter when instantiating the class, and
        "everything else" that does not require an "extra" parameter for
        class instantiation.

        If convert is False, then we will *not* do the conversion of units
        to the units of the Spectrum1D object.  Otherwise we will convert.
    """
    dispersion = spectrum.spectral_axis
    dispersion_unit = spectrum.spectral_axis.unit
    flux = spectrum.flux
    flux_unit = spectrum.flux.unit
    compound_model = model_in.n_submodels > 1
    if not compound_model:
        model_in = [
         model_in]
    else:
        model_in = model_in.traverse_postorder(include_operator=True)
    model_out_stack = []
    for sub_model in model_in:
        if not isinstance(sub_model, Model):
            model_out_stack.append(sub_model)
            continue
        elif isinstance(sub_model, models.PolynomialModel):
            new_sub_model = sub_model.__class__((sub_model.degree), name=(sub_model.name))
        else:
            new_sub_model = sub_model.__class__(name=(sub_model.name))
        for pn in new_sub_model.param_names:
            v = _convert_and_dequantify((getattr(sub_model, pn)), dispersion_unit, dispersion, flux_unit, convert=convert)
            setattr(new_sub_model, pn, v)
            for constraint in ('tied', 'fixed'):
                for k, v in getattr(sub_model, constraint).items():
                    getattr(new_sub_model, constraint)[k] = v

            new_bounds = []
            for a in sub_model.bounds[pn]:
                v = _convert_and_dequantify(a, dispersion_unit, dispersion, flux_unit, convert=convert)
                new_bounds.append(v)

            new_sub_model.bounds[pn] = tuple(new_bounds)

        model_out_stack.append(new_sub_model)

    if compound_model:
        model_out = _combine_postfix(model_out_stack)
    else:
        model_out = model_out_stack[0]
    return (model_out, dispersion.value, flux.value)


def _add_units_to_model(model_in, model_orig, spectrum):
    """
    This method adds the units to the model based on the units of the
    model passed in.  This is necessary as CoumpoundModel
    with units does not work in the fitters.

    Notes
    -----
        When CompoundModel with units works in the fitters this method
        can be removed.

        This assumes there are two types of models, those that are
        based on `~astropy.modeling.models.PolynomialModel` and therefore
        require the ``degree`` parameter when instantiating the class, and
        "everything else" that does not require an "extra" parameter for
        class instantiation.
    """
    dispersion = spectrum.spectral_axis
    compound_model = model_in.n_submodels > 1
    if not compound_model:
        model_in_list = [
         model_in]
        model_orig_list = [model_orig]
    else:
        compound_model_in = model_in
        model_in_list = model_in.traverse_postorder(include_operator=True)
        model_orig_list = model_orig.traverse_postorder(include_operator=True)
    model_out_stack = []
    model_index = 0
    for ii, m_in in enumerate(model_in_list):
        if not isinstance(m_in, Model):
            model_out_stack.append(m_in)
            continue
        else:
            m_orig = model_orig_list[ii]
            if isinstance(m_in, models.PolynomialModel):
                new_sub_model = m_in.__class__((m_in.degree), name=(m_in.name))
            else:
                new_sub_model = m_in.__class__(name=(m_in.name))
        for pi, pn in enumerate(new_sub_model.param_names):
            m_orig_param = getattr(m_orig, pn)
            m_in_param = getattr(m_in, pn)
            if hasattr(m_orig_param, 'quantity'):
                if m_orig_param.quantity is not None:
                    m_orig_param_quantity = m_orig_param.quantity
                    if m_orig_param_quantity.unit.is_equivalent((spectrum.spectral_axis.unit), equivalencies=(u.equivalencies.spectral())):
                        if compound_model:
                            current_value = getattr(compound_model_in, '{}_{}'.format(pn, model_index)).value * spectrum.spectral_axis.unit
                        else:
                            current_value = m_in_param.value * spectrum.spectral_axis.unit
                        v = current_value.to((m_orig_param_quantity.unit), equivalencies=(u.equivalencies.spectral()))
                elif m_orig_param_quantity.unit.is_equivalent((spectrum.flux.unit), equivalencies=(u.equivalencies.spectral_density(dispersion))):
                    if compound_model:
                        current_value = getattr(compound_model_in, '{}_{}'.format(pn, model_index)).value * spectrum.flux.unit
                    else:
                        current_value = m_in_param.value * spectrum.flux.unit
                    v = current_value.to((m_orig_param_quantity.unit), equivalencies=(u.equivalencies.spectral_density(dispersion)))
                else:
                    raise ValueError("The parameter '{}' with unit '{}' is not convertible to either the current flux unit '{}' or spectral axis unit '{}'.".format(m_orig_param.name, m_orig_param.unit, spectrum.flux.unit, spectrum.spectral_axis.unit))
            else:
                v = getattr(m_in, pn).value
            setattr(new_sub_model, pn, v)
            for constraint in ('tied', 'bounds', 'fixed'):
                for k, v in getattr(m_orig, constraint).items():
                    getattr(new_sub_model, constraint)[k] = v

        model_out_stack.append(new_sub_model)
        model_index += 1

    if compound_model:
        model_out = _combine_postfix(model_out_stack)
    else:
        model_out = model_out_stack[0]
    if getattr(model_orig, model_orig.param_names[0]).unit is None:
        model_out = QuantityModel(model_out, spectrum.spectral_axis.unit, spectrum.flux.unit)
    return model_out


def _combine_postfix(equation):
    """
    Given a Python list in post order (RPN) of an equation, convert/apply the
    operations to evaluate. The list order is the same as what is output from
    ``model._tree.traverse_postorder()``.

    Structure modified from https://codereview.stackexchange.com/questions/79795/reverse-polish-notation-calculator-in-python
    """
    ops = {'+':operator.add, 
     '-':operator.sub, 
     '*':operator.mul, 
     '/':operator.truediv, 
     '^':operator.pow, 
     '**':operator.pow}
    stack = []
    result = 0
    for i in equation:
        if isinstance(i, Model):
            stack.insert(0, i)
        elif len(stack) < 2:
            print('Error: insufficient values in expression')
            break
        else:
            n1 = stack.pop(1)
            n2 = stack.pop(0)
            result = ops[i](n1, n2)
            stack.insert(0, result)

    return result