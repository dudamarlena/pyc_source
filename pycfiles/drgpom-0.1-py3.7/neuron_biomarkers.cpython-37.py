# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\drgpom\methods\biomarkers\neuron_biomarkers.py
# Compiled at: 2020-04-08 07:56:06
# Size of source mod 2**32: 58284 bytes
import sys, numpy as np, pandas as pd
from scipy import optimize
from matplotlib import pyplot as plt
from . import davidson_biomarkers as db
from .. import simulation_helpers as sh
from .. import analysis as an
RHEO_FAIL = np.nan

def calculate_biomarkers(traces, model):
    """ Calculate every biomarker and output to dict """
    biomarkers = calculate_simple_biomarkers(traces, model)
    biomarkers['RMP'] = np.mean(calculate_rmp(traces))
    biomarkers['Rheobase'] = calculate_rheobase(model, amp_step=0.1, amp_max=5, make_plot=False)
    return biomarkers


def average_biomarker_values(biomarkers, how_to_handle_nans='return'):
    """ Average biomarker values for multiple APs while handling biomarkers that """
    if how_to_handle_nans == 'return':
        pass
    elif how_to_handle_nans == 'remove':
        biomarkers = np.array(biomarkers)
        if biomarkers[(~np.isnan(biomarkers))].size == 0:
            return np.nan
        biomarkers = biomarkers[(~np.isnan(biomarkers))]
    else:
        raise ValueError('{} is not an accepted nan handling method.'.format(how_to_handle_nans))
    mean_result = np.mean(biomarkers)
    return mean_result


def calculate_simple_biomarkers(traces, model='Not needed', how_to_handle_nans='return'):
    """ Calculate every biomarker that can be calculated from a normal simulation trace and output to dict - rheobase and RMP need to be calculated separately."""
    biomarkers = {}

    def error_handle(filename, traces):
        import pickle
        print(sys.exc_info())
        print(traces['numAPs'])
        plt.figure()
        for t, v in zip(traces['t'], traces['v']):
            plt.plot(t, v)

        with open(filename, 'wb') as (handle):
            pickle.dump(traces, handle)
        print('Error, traces dumped to {}.'.format(filename))

    try:
        biomarkers['APFullWidth'] = average_biomarker_values(calculate_ap_full_width(traces, threshold=5.0, method='gradient'), how_to_handle_nans)
    except:
        error_handle('fullwidth.pickle', traces)

    try:
        biomarkers['APHalfWidth'] = average_biomarker_values(calculate_ap_half_width(traces, threshold=5.0, method='gradient'), how_to_handle_nans)
    except:
        error_handle('halfwidth.pickle', traces)

    biomarkers['APPeak'] = average_biomarker_values(calculate_ap_peak(traces), how_to_handle_nans)
    try:
        biomarkers['APRiseTime'] = average_biomarker_values(calculate_ap_rise_time(traces, dvdtthreshold=5), how_to_handle_nans)
    except:
        error_handle('risetime.pickle', traces)

    ap_slope_mins, ap_slope_maxs = calculate_ap_slope_min_max(traces)
    biomarkers['APSlopeMin'] = average_biomarker_values(ap_slope_mins, how_to_handle_nans)
    biomarkers['APSlopeMax'] = average_biomarker_values(ap_slope_maxs, how_to_handle_nans)
    biomarkers['Threshold'] = average_biomarker_values(calculate_threshold(traces), how_to_handle_nans)
    amp, tau, trough = fit_afterhyperpolarization(traces=traces, dvdt_threshold=5, ahp_model='single_exp', full_output=False)
    biomarkers['AHPAmp'] = amp
    biomarkers['AHPTau'] = tau
    biomarkers['AHPTrough'] = trough
    biomarkers['ISI'] = inter_spike_interval(traces)
    biomarkers['numAPs'] = traces['numAPs']
    return biomarkers


def compute_model_biomarkers(model=None, mechanisms=None, make_plot=False, sim_kwargs=None, xlims=None):
    """ Find all standard biomarkers of a model or mechanism set. """
    biomarkers = {}
    if model == None:
        model = sh.build_model(mechanisms)
    else:
        if sim_kwargs:
            sim_kwargs['model'] = model
        else:
            sim_kwargs = sh.get_default_simulation_kwargs(model=model)
        rheobase = calculate_rheobase(model, amp_step=0.1, amp_max=5, make_plot=False, sim_kwargs=sim_kwargs)
        if (isinstance(rheobase, float) == False) & (isinstance(rheobase, int) == False):
            find_other_biomarkers = False
        else:
            find_other_biomarkers = True
        if sim_kwargs:
            sim_kwargs['amp'] = rheobase
            sim_kwargs['model'] = model
        else:
            sim_kwargs = sh.get_default_simulation_kwargs(amp=rheobase, model=model)
    sim_kwargs['make_plot'] = make_plot
    if find_other_biomarkers:
        output = (sh.simulation)(**sim_kwargs)
        t = output['t']
        v = output['v']
        t = t[::2]
        v = v[::2]
        traces = split_trace_into_aps(t, v)
        biomarkers = calculate_simple_biomarkers(traces, model, how_to_handle_nans='remove')
    rmp_kwargs = {'amp':0.0, 
     'dur':3000.0,  'delay':0.0,  'interval':0.0,  'num_stims':1,  't_stop':3000.0}
    for kwarg in sim_kwargs:
        if kwarg not in rmp_kwargs:
            rmp_kwargs[kwarg] = sim_kwargs[kwarg]

    output = (sh.simulation)(**rmp_kwargs)
    rmp_t = output['t']
    rmp_v = output['v']
    rmp_t = rmp_t[::2]
    rmp_v = rmp_v[::2]
    rmp_traces = split_trace_into_aps(rmp_t, rmp_v)
    rmp = np.mean(calculate_rmp(rmp_traces))
    if make_plot & (xlims != None):
        plt.xlim(xlims[0], xlims[1])
    biomarkers['Rheobase'] = rheobase
    biomarkers['RMP'] = rmp
    return biomarkers


def split_trace_into_aps(t, v, threshold=0, time_threshold=5, check_voltage_gradient=True):
    """
    Threshold is at 0 mV which can let RF to cause spurious AP detection unless
    we perform a voltage gradient check, which defaults to True.
    
    -- Old ideas to solve the spurious AP detection problem with threshold at 0 mV --
    One idea is to do split trace and then calculate AP width using a voltage threshold of something like -25 mV.
    Then, if AP width is really long (> 100 ms?), redo the calculation with a lower threshold (0 mV?). 
    If mean AP width is then < 100 ms, we use the new split. We could write a log file to say that this happened,
    with the trace in it. 

    However, that is complex and may break if something comes up I haven't thought of.
    Instead we could reset the default threshold to 0 mV but add in a gradient check on the voltage crossing from below.
    Currently a gradient threshold of 1 mV/ms seems like it should be effective although I don't have any examples of slow
    calcium initated APs to test against. 
    """
    assert len(t) == len(v), 'v and t length mismatch'
    crossings = []
    time_crossings = np.array([])
    for i, voltage in enumerate(v[:-1]):
        if (voltage < threshold) & (v[(i + 1)] >= threshold):
            if check_voltage_gradient & is_voltage_gradient_too_small(i, t, v, dvdt_threshold=1.0, time_window=1.0):
                continue
            crossings.append(i)
            time_crossings = np.append(time_crossings, t[i])

    grouped_crossings = np.zeros(np.size(crossings), float)
    for i in range(len(crossings) - 1):
        if grouped_crossings[i] == 0:
            nearby_crossings = np.array(time_crossings[i + 1:] - time_crossings[i] < time_threshold)
            grouped_crossings[i + 1:] += nearby_crossings
            assert all(grouped_crossings < 2), 'Grouped crossing grouped more than once'

    firstCrossIndices = np.where(grouped_crossings == 0)
    firstCrossings = np.array(crossings)[firstCrossIndices]
    numAPs = len(firstCrossings)
    assert numAPs >= 0, 'Negative number of APs!'
    times = []
    voltages = []
    if numAPs > 0:
        startIdx = np.zeros(numAPs, int)
        endIdx = np.zeros(numAPs, int)
        for AP in range(numAPs):
            if AP == 0:
                startIdx[0] = 0
            else:
                startIdx[AP] = endIdx[(AP - 1)] + 1
            if AP == numAPs - 1:
                endIdx[AP] = len(v) - 1
            else:
                voltageDuringCurrentAP = v[firstCrossings[AP]:firstCrossings[(AP + 1)]]
                max_idx = np.argmax(voltageDuringCurrentAP)
                minVmIdx = np.argmin(voltageDuringCurrentAP[max_idx:])
                endIdx[AP] = firstCrossings[AP] + max_idx + minVmIdx
            times.append(t[startIdx[AP]:endIdx[AP] + 1])
            voltages.append(v[startIdx[AP]:endIdx[AP] + 1])

        for i in range(len(startIdx) - 1):
            assert endIdx[i] + 1 == startIdx[(i + 1)], "startIdx and endIdx don't match up."

    else:
        if numAPs == 0:
            times.append(t)
            voltages.append(v)
            startIdx = np.array([0], int)
            endIdx = np.array([len(v) - 1], int)
    assert startIdx[0] == 0, "First AP doesn't start at beginning of trace."
    assert endIdx[(-1)] == len(v) - 1, "Last AP doesn't end at end of trace."
    return {'t':times, 
     'v':voltages,  'startIndices':startIdx,  'endIndices':endIdx,  'numAPs':numAPs}


SplitTraceIntoAPs = split_trace_into_aps

def voltage_gradient(t, v, method='gradient'):
    if method == 'gradient':
        dvdt = np.gradient(v, t)
    else:
        if method == 'diff':
            dvdt = np.diff(v) / np.diff(t)
        else:
            raise ValueError('Method not found.')
    return dvdt


VoltageGradient = voltage_gradient

def is_voltage_gradient_too_small(i, t, v, dvdt_threshold, time_window):
    """
    Check if the voltage gradient around the threshold crossing from below at v[i] to v[i+1]
    is too small to have a reasonable likelihood of being a real AP.
    Inputs:
    i - index at which threshold is crossed, between v[i] and v[i+1]
    t,v - time and voltage arrays
    dvdt threshold - mV/ms
    time window (either side of indices i and i+1, so effective window is double the size) - ms
    """
    voltage_gradient_too_small = False
    lower_t_bound = t[i] - time_window
    if lower_t_bound < 0:
        lower_t_bound = 0
    upper_t_bound = t[(i + 1)] + time_window
    t = np.array(t)
    window_indices = (t >= lower_t_bound) & (t <= upper_t_bound)
    _t = t[window_indices]
    _v = v[window_indices]
    _dvdt = np.gradient(_v, _t)
    if np.mean(_dvdt) < dvdt_threshold:
        voltage_gradient_too_small = True
    return voltage_gradient_too_small


def rmp(v):
    vLen = len(v)
    startIdx = 90 * vLen // 100
    RMP = min(v[startIdx:])
    RMPIdx = np.argmin(v[startIdx:])
    return (RMP, RMPIdx)


RMP = rmp

def input_res(t, v, current_injection_time):
    """ To Do - check that simulations is a bunch of simulations, not just an array """
    pass


def rheobase(simulations, amps):
    for i in range(len(amps) - 1):
        assert amps[(i + 1)] > amps[i], 'Amps in rheobase biomarker not increasing monotonically!'

    for simulation, amp in zip(simulations, amps):
        result = SplitTraceIntoAPs(simulation['t'], simulation['v'])
        if result['numAPs'] > 0:
            return {'rheobase':amp, 
             'trace':simulation}

    return {'rheobase':np.nan, 
     'trace':[]}


Rheobase = rheobase

def ap_peak(v):
    peak = max(v)
    location = np.argmax(v)
    return [peak, location]


APPeak = ap_peak

def threshold(t, v, dvdt_threshold=5.0):
    dvdt = np.gradient(v, t)
    thresholds = []
    for i, gradient in enumerate(dvdt[0:-1]):
        if (gradient < dvdt_threshold) & (dvdt[(i + 1)] > dvdt_threshold):
            thresholds.append(v[i])

    if thresholds:
        return thresholds[0]
    return np.nan


def ap_rise_time(t, v, threshold=5):
    """ 
    Threshold here is a dVdt threshold in mV/ms`
    Default threshold is taken from Davidson et al. 2014, PAIN
    """
    if not threshold > 0:
        raise AssertionError('Rise time threshold is a gradient threshold, should be > 0!')
    else:
        dVdt = np.gradient(v, t)
        peak = ap_peak(v)
        peak_idx = peak[1]
        peak_time = t[peak_idx]
        found_thresholds = []
        for i, gradient in enumerate(dVdt[0:-1]):
            if gradient < threshold and dVdt[(i + 1)] > threshold:
                found_thresholds.append(i)

        num_threshold = len(found_thresholds)
        if num_threshold == 1:
            threshold_time = t[found_thresholds[0]]
            rise_time = peak_time - threshold_time
            if rise_time < 0:
                rise_time = np.nan
        elif num_threshold == 0:
            rise_time = np.nan
        else:
            if num_threshold > 1:
                threshold_time = t[found_thresholds[0]]
                rise_time = peak_time - threshold_time
    return rise_time


APRiseTime = ap_rise_time

def ap_slope_min_max(t, v):
    dVdt = np.gradient(v, t)
    slope_min = min(dVdt)
    slope_max = max(dVdt)
    return [
     slope_min, slope_max]


APSlopeMinMax = ap_slope_min_max

def ap_width(t, v, alpha, _threshold=5.0, threshold_type='gradient'):
    """
    Generic ap width calculating function. Alpha determines the fraction of the voltage
    gap between threshold and ap peak that is used to set the voltage threshold.

    Specifically, if Th is the calculate threshold voltage and P is the peak voltage,
    the voltage threshold used depends on alpha so that width threshold WTh = alpha*P + (1-alpha)*Th

    So for full width alpha = 0, as we just use the bare threshold Th, for half width alpha = 0.5,
    and alpha = 1 should give a width of 0 as it goes all the way to the peak.
    
    Defaults are consistent with Davidson et al. 2014 (5 mV/ms gradient to find threshold voltage)

    _threshold named to avoid overlapping with threshold function
    """
    if threshold_type == 'gradient':
        v_threshold = threshold(t, v, _threshold)
    else:
        if threshold_type == 'voltage':
            v_threshold = _threshold
        else:
            raise ValueError('threshold type: {} not recognised'.format(threshold_type))
    if np.isnan(v_threshold):
        return np.nan
    v_peak = ap_peak(v)[0]
    width_v_threshold = alpha * v_peak + (1.0 - alpha) * v_threshold
    ups, downs = find_threshold_crossings(v, width_v_threshold)
    if ups:
        if downs:
            last_down = downs[(-1)]
            first_up = ups[0]
            width = t[last_down] - t[first_up]
            return width
    return np.nan


def ap_full_width(t, v, _threshold=5.0, threshold_type='gradient'):
    """
    Calculate full width of AP by one of two methods, a voltage threshold
    or a voltage/time gradient threshold
    Defaults are consistent with Davidson et al. 2014 (5 mV/ms gradient to find threshold voltage)

    _threshold named to avoid overlapping with threshold function
    """
    if threshold_type == 'voltage':
        if np.isnan(_threshold):
            raise AssertionError('Threshold {} is nan'.format(_threshold))
        ups, downs = find_threshold_crossings(v, _threshold)
    else:
        if threshold_type == 'gradient':
            dvdt = np.gradient(v, t)
            gradient_threshold = None
            for i, _ in enumerate(dvdt[:-1]):
                if dvdt[i] < _threshold and dvdt[(i + 1)] >= _threshold:
                    gradient_threshold = v[i]
                    break

            if gradient_threshold:
                ups, downs = find_threshold_crossings(v, gradient_threshold)
            else:
                return np.nan
        else:
            raise ValueError('threshold type: {} not recognised'.format(threshold_type))
    num_ups = len(ups)
    num_downs = len(downs)
    if (num_ups < 1) | (num_downs < 1):
        full_width = np.nan
    else:
        if (num_ups == 1) & (num_downs == 1):
            full_width = t[downs[0]] - t[ups[0]]
        else:
            if (num_ups > 1) | (num_downs > 1):
                first_up = ups[0]
                last_down = downs[(-1)]
                full_width = t[last_down] - t[first_up]
            return full_width


APFullWidth = ap_full_width

def ap_half_width(t, v, dvdt_threshold=5.0):
    """
    Definition from neuroelectro.org:
    AP duration at membrane voltage halfway between AP threshold and AP peak.
    Currently only uses gradient method for finding threshold for simplicity.
    """
    v_threshold = threshold(t, v, dvdt_threshold=dvdt_threshold)
    v_peak = ap_peak(v)[0]
    half_width_v_threshold = (v_threshold + v_peak) / 2.0
    ups, downs = find_threshold_crossings(v, half_width_v_threshold)
    if ups:
        if downs:
            last_down = downs[(-1)]
            first_up = ups[0]
            half_width = t[last_down] - t[first_up]
            return half_width
    return np.nan


def fit_afterhyperpolarization(traces, dvdt_threshold, max_time_from_peak=50.0, ahp_model='single_exp', full_output=False):
    """ 
    Gather afterhyperpolarisation regions from a set of traces and fit them to a model 
    of a single exponential (other models can be added as needed)
    
    Outputs:
    Returns either amp,tau or if full_output is selected returns five outputs.
    """
    if ahp_model == 'single_exp':

        def model(x, a, b, c):
            return a - b * np.exp(-x / c)

    else:
        raise ValueError('Model "{}" not valid'.format(ahp_model))

    def hyperpolarisation_fit_failure(full_output):
        if full_output:
            return (
             np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
        return (np.nan, np.nan, np.nan)

    num_APs = traces['numAPs']
    if num_APs < 1:
        return hyperpolarisation_fit_failure(full_output)
    if num_APs == 1:
        _t = traces['t'][0]
        _v = traces['v'][0]
        max_idx = np.argmax(_v)
        if max_idx == len(_v) - 1:
            return hyperpolarisation_fit_failure(full_output)
        t_peak = _t[max_idx]
        t_end = t_peak + max_time_from_peak
        end_idx = np.argmin(abs(_t - t_end))
        ts = [
         _t[max_idx + 1:end_idx]]
        vs = [_v[max_idx + 1:end_idx]]
    else:
        if num_APs > 1:
            ts = []
            vs = []
            for i in range(num_APs - 1):
                _ts = [traces['t'][idx] for idx in [i, i + 1]]
                _vs = [traces['v'][idx] for idx in [i, i + 1]]
                max_idxs = [np.argmax(_v) for _v in _vs]
                _t_start = _ts[0][max_idxs[0]:]
                _t_end = _ts[1][:max_idxs[1] - 1]
                _v_start = _vs[0][max_idxs[0]:]
                _v_end = _vs[1][:max_idxs[1] - 1]
                _t = np.concatenate([_t_start, _t_end], axis=0)
                _v = np.concatenate([_v_start, _v_end], axis=0)
                ts.append(_t)
                vs.append(_v)

            _t = traces['t'][(num_APs - 1)]
            _v = traces['v'][(num_APs - 1)]
            max_idx = np.argmax(_v)
            if max_idx == len(_v) - 1:
                return hyperpolarisation_fit_failure(full_output)
            t_peak = _t[max_idx]
            t_end = t_peak + max_time_from_peak
            end_idx = np.argmin(abs(_t - t_end))
            ts.append(_t[max_idx + 1:end_idx])
            vs.append(_v[max_idx + 1:end_idx])
        amps = []
        taus = []
        troughs = []
        if full_output:
            output_ts = []
            output_vs = []
            popts = []
        for i, (t, v) in enumerate(zip(ts, vs)):
            min_idx = np.argmin(v)
            dvdt = np.gradient(v, t)
            threshold_exceeded = dvdt > dvdt_threshold
            if any(threshold_exceeded):
                cutoff_idx = np.where(threshold_exceeded)[0][0] - 1
            else:
                cutoff_idx = len(t) - 1
            t = t[min_idx:cutoff_idx]
            v = v[min_idx:cutoff_idx]
            if any(np.isnan(v)) | any(np.isnan(t)):
                return hyperpolarisation_fit_failure(full_output)
                length_threshold = 10
                if (len(t) <= length_threshold) | (len(v) <= length_threshold):
                    return hyperpolarisation_fit_failure(full_output)
                dt = np.gradient(t)
                if not np.mean(dt) < 0.1:
                    raise AssertionError('dt is large, check length_threshold')
                elif ahp_model == 'single_exp':
                    t = t - t[0]
                    popt, pcov = optimize.curve_fit(model, t, v)
                    trough = min(v)
                    thresh = threshold(traces['t'][i], traces['v'][i], dvdt_threshold)
                    ahp_amp = trough - thresh
                    ahp_tau = popt[2]
                    ahp_trough = trough
                else:
                    raise ValueError('Model "{}" not valid'.format(ahp_model))
                amps.append(ahp_amp)
                taus.append(ahp_tau)
                troughs.append(ahp_trough)
                if full_output:
                    output_ts.append(t)
                    output_vs.append(v)
                    popts.append(popt)

        if full_output == True:
            return (
             amps, taus, troughs, output_ts, output_vs, popts)
        amp = np.mean(amps)
        tau = np.mean(taus)
        trough = np.mean(troughs)
        return (amp, tau, trough)


def inter_spike_interval(traces):
    """ Calculate average interspike interval from a divided set of traces
        Total interspike interval is the time difference between the first and last peak of a trace,
        divided by the number of intervals (number of APs - 1)
    """
    numAPs = traces['numAPs']
    if numAPs < 2:
        return np.nan
    voltages = traces['v']
    first_spike = np.argmax(voltages[0])
    last_spike = np.argmax(voltages[(-1)])
    times = traces['t']
    time_diff = times[(-1)][last_spike] - times[0][first_spike]
    assert time_diff > 0, 'time_diff for ISI < 0: {}'.format(time_diff)
    inter_spike_interval = time_diff / (numAPs - 1)
    return inter_spike_interval


def absmax(i):
    """
    Returns the largest absolute value present in an array in its raw form
    (e.g. in [-2, 0, 1] it returns -2, in [-2,0,3] it returns 3.)
    """
    if max(i) > abs(min(i)):
        return max(i)
    if abs(min(i)) >= max(i):
        return min(i)
    raise ValueError()


def calculate_rmp(traces):
    RMPVals = []
    for i, v in enumerate(traces['v']):
        RMPValue, RMPIdx = RMP(v)
        RMPVals.append(RMPValue)

    return RMPVals


CalculateRMP = calculate_rmp

def calculate_input_res():
    input_res_vals = []
    for i, v in enumerate(traces['v']):
        input_res_vals.append(input_res(v))

    return input_res_vals


CalculateInputRes = calculate_input_res

def calculate_ramp_ap():
    """ 
    Can't remember what this biomarker was supposed to do? 
    We just run ramp simulations and calculate biomarkers on those now.
    """
    return 0


CalculateRampAP = calculate_ramp_ap

def calculate_rheobase(cell_model, amp_step=0.1, amp_max=5.0, make_plot=False, sim_kwargs=None, search='simple'):
    """ Run a series of simulations to calculate rheobase"""
    if sim_kwargs is None:
        sim_kwargs = {}
    else:
        default_kwargs = {'dur':500.0, 
         'delay':1000.0,  'interval':0.0,  'num_stims':1,  't_stop':1500.0,  'mechanisms':None, 
         'make_plot':False,  'plot_type':'default',  'model':cell_model}
        for kwarg in default_kwargs.keys():
            if kwarg in sim_kwargs.keys():
                continue
            sim_kwargs[kwarg] = default_kwargs[kwarg]

        def rheobase_simulation(amp):
            sim_kwargs['amp'] = amp
            output = (sh.simulation)(**sim_kwargs)
            t = output['t']
            v = output['v']
            run_up = 1.0
            delay = sim_kwargs['delay']
            stim_period_indices = tuple(t >= delay - run_up)
            t = t[stim_period_indices]
            v = v[stim_period_indices]
            traces = split_trace_into_aps(t, v, threshold=0.0, time_threshold=5.0)
            if traces['numAPs'] > 0:
                if make_plot:
                    plot_traces(traces)
                rheobase = amp
                return rheobase
            return RHEO_FAIL

        amp_min = 0.0
        amps = np.arange(amp_min, amp_max, amp_step)
        if search == 'simple':
            for amp in amps:
                rheobase = rheobase_simulation(amp)
                if rheobase is not RHEO_FAIL:
                    return rheobase

            return RHEO_FAIL
            if search == 'divide':
                idx0 = 0
                idxn = len(amps) - 1
                rheobases = np.empty(len(amps))
                rheobases[:] = None
                while idx0 <= idxn:
                    midval = (idx0 + idxn) // 2
                    rheobase = rheobase_simulations(amps[midval])
                    rheobases[midval] = rheobase
                    if rheobase is not RHEO_FAIL:
                        if midval == 0:
                            return amps[0]
                        if rheobases[(midval - 1)] is not RHEO_FAIL:
                            return amps[midval]
                        idxn = midval - 1
                    elif rheobase is not RHEO_FAIL:
                        if midval == len(amps) - 1:
                            return RHEO_FAIL
                        if isinstance(rheobases[(midval + 1)], float):
                            return amps[(midval + 1)]
                        idx0 = midval + 1
                    else:
                        raise Exception('Rheobase not accepted value.')

                raise Exception('No rheobase found')
        elif search == 'smart':
            pass


CalculateRheobase = calculate_rheobase

def calculate_threshold(traces, dvdt_threshold=5.0):
    thresholds = []
    for t, v in zip(traces['t'], traces['v']):
        thresholds.append(threshold(t, v, dvdt_threshold=dvdt_threshold))

    return thresholds


def calculate_ap_peak(traces):
    ap_peak_vals = []
    for _, v in zip(range(len(traces['t'])), traces['v']):
        ap_peak_vals.append(ap_peak(v)[0])

    return ap_peak_vals


CalculateAPPeak = calculate_ap_peak

def calculate_ap_rise_time(traces, dvdtthreshold=5.0):
    ap_rise_time_vals = []
    for t, v in zip(traces['t'], traces['v']):
        ap_rise_time_vals.append(ap_rise_time(t, v, dvdtthreshold))

    return ap_rise_time_vals


CalculateAPRiseTime = calculate_ap_rise_time

def calculate_ap_slope_min_max(traces):
    ap_slope_min_vals = []
    ap_slope_max_vals = []
    for t, v in zip(traces['t'], traces['v']):
        dvdt = np.gradient(v, t)
        ap_slope_min_vals.append(min(dvdt))
        ap_slope_max_vals.append(max(dvdt))

    return (
     ap_slope_min_vals, ap_slope_max_vals)


CalculateAPSlopeMinMax = calculate_ap_slope_min_max

def calculate_ap_width(traces, alpha, threshold=0, method='voltage'):
    ap_width_vals = []
    for t, v in zip(traces['t'], traces['v']):
        ap_width_vals.append(ap_width(t, v, alpha, threshold, method))

    return ap_width_vals


def calculate_ap_half_width(traces, threshold=0, method='voltage'):
    alpha = 0.5
    ap_half_width_vals = calculate_ap_width(traces, alpha, threshold, method)
    return ap_half_width_vals


def calculate_ap_full_width(traces, threshold=0, method='voltage'):
    alpha = 0.0
    ap_full_width_vals = calculate_ap_width(traces, alpha, threshold, method)
    return ap_full_width_vals


CalculateAPFullWidth = calculate_ap_full_width

def calculate_ahp_amp--- This code section failed: ---

 L. 944         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ahp_amp_vals'

 L. 945         4  LOAD_FAST                'traces'
                6  LOAD_STR                 'numAPs'
                8  BINARY_SUBSCR    
               10  LOAD_CONST               1
               12  COMPARE_OP               >
               14  POP_JUMP_IF_FALSE   132  'to 132'

 L. 946        16  SETUP_LOOP          196  'to 196'
               18  LOAD_GLOBAL              range
               20  LOAD_FAST                'traces'
               22  LOAD_STR                 'numAPs'
               24  BINARY_SUBSCR    
               26  LOAD_CONST               1
               28  BINARY_SUBTRACT  
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  GET_ITER         
               34  FOR_ITER            128  'to 128'
               36  STORE_FAST               'i'

 L. 947        38  LOAD_FAST                'traces'
               40  LOAD_STR                 't'
               42  BINARY_SUBSCR    
               44  LOAD_FAST                'i'
               46  BINARY_SUBSCR    
               48  STORE_FAST               't'

 L. 948        50  LOAD_FAST                'traces'
               52  LOAD_STR                 'v'
               54  BINARY_SUBSCR    
               56  LOAD_FAST                'i'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'v'

 L. 949        62  LOAD_FAST                'traces'
               64  LOAD_STR                 't'
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'i'
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  BINARY_SUBSCR    
               76  STORE_FAST               't2'

 L. 950        78  LOAD_FAST                'traces'
               80  LOAD_STR                 'v'
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'i'
               86  LOAD_CONST               1
               88  BINARY_ADD       
               90  BINARY_SUBSCR    
               92  STORE_FAST               'v2'

 L. 951        94  LOAD_GLOBAL              fit_afterhyperpolarization
               96  LOAD_FAST                't'
               98  LOAD_FAST                'v'
              100  LOAD_FAST                't2'
              102  LOAD_FAST                'v2'
              104  LOAD_FAST                'dvdt_threshold'
              106  CALL_FUNCTION_5       5  '5 positional arguments'
              108  UNPACK_SEQUENCE_3     3 
              110  STORE_FAST               'amp'
              112  STORE_FAST               'tau'
              114  STORE_FAST               'trough'

 L. 952       116  LOAD_GLOBAL              AHPAmpVals
              118  LOAD_METHOD              append
              120  LOAD_FAST                'amp'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          
              126  JUMP_BACK            34  'to 34'
              128  POP_BLOCK        
              130  JUMP_FORWARD        196  'to 196'
            132_0  COME_FROM            14  '14'

 L. 953       132  LOAD_FAST                'traces'
              134  LOAD_STR                 'numAPs'
              136  BINARY_SUBSCR    
              138  LOAD_CONST               1
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   196  'to 196'

 L. 954       144  LOAD_FAST                'traces'
              146  LOAD_STR                 'v'
              148  BINARY_SUBSCR    
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  STORE_FAST               'v'

 L. 955       156  LOAD_GLOBAL              np
              158  LOAD_METHOD              argmax
              160  LOAD_FAST                'v'
              162  CALL_METHOD_1         1  '1 positional argument'
              164  STORE_FAST               'max_idx'

 L. 956       166  LOAD_FAST                'v'
              168  LOAD_FAST                'max_idx'
              170  LOAD_CONST               None
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  STORE_FAST               'working_voltage'

 L. 957       178  LOAD_GLOBAL              min
              180  LOAD_FAST                'working_voltage'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  STORE_FAST               'amp'

 L. 958       186  LOAD_FAST                'ahp_amp_vals'
              188  LOAD_METHOD              append
              190  LOAD_FAST                'amp'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           142  '142'
            196_1  COME_FROM           130  '130'
            196_2  COME_FROM_LOOP       16  '16'

 L. 959       196  LOAD_FAST                'ahp_amp_vals'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 196_2


CalculateAHPAmp = calculate_ahp_amp

def calculate_ahp_tau():
    return 0


CalculateAHPTau = calculate_ahp_tau

def determine_firing_pattern(traces, stim_start, stim_end):
    """
    Define firing pattern of traces as one or more of n types:
    1. Reluctant
    2. Single
    3. Tonic
    4. Delayed
    5. Gap
    6. Phasic - multi-AP firing that ends before end of stimulus
    7. Burst firing
    8. Wide
    9. Repolarisation failure
    """

    def first_spike_delay(traces, stim_start):
        first_spike_v = traces['v'][0]
        first_spike_t = traces['t'][0]
        single_spike_index = ap_peak(first_spike_v)[1]
        single_spike_time = first_spike_t[single_spike_index]
        delay = single_spike_time - stim_start
        return delay

    def first_two_spikes_isi(traces):
        spike_times = []
        for i in (0, 1):
            spike_idx = ap_peak(traces['v'][i])[1]
            spike_times.append(traces['t'][i][spike_idx])

        delay = spike_times[1] - spike_times[0]
        return delay

    def second_third_spikes_isi(traces):
        spike_times = []
        for i in (1, 2):
            spike_idx = ap_peak(traces['v'][i])[1]
            spike_times.append(traces['t'][i][spike_idx])

        delay = spike_times[1] - spike_times[0]
        return delay

    def check_delayed(traces):
        delayed = False
        num_aps = traces['numAPs']
        if num_aps == 1:
            if first_spike_delay(traces, stim_start) > 100.0:
                delayed = True
        elif num_aps > 1:
            if first_spike_delay(traces, stim_start) > 1.5 * first_two_spikes_isi(traces):
                delayed = True
        return delayed

    def check_gap(traces):
        gap = False
        num_aps = traces['numAPs']
        gap = False
        if num_aps > 2:
            if first_two_spikes_isi(traces) > 1.5 * second_third_spikes_isi(traces):
                gap = True
        return gap

    def check_phasic(traces, stim_end, ratio_threshold=0.25):
        """
        Phasic - firing of multiple APs followed by a period of quiescence. 
        Cases
        1. Idea is use ratio of - Time from last spike to stimulus end:time from first to last spike
        If the ratio is above some threshold.
        2. Simply time from last peak to end of stimulus compared to a threshold.
        """
        phasic = False
        case1 = True
        case2 = False
        num_aps = traces['numAPs']
        if num_aps < 2:
            return False
        spike_times = []
        for i in range(num_aps):
            spike_idx = ap_peak(traces['v'][i])[1]
            spike_times.append(traces['t'][i][spike_idx])

        if case1:
            last_spike_to_stim_end = stim_end - spike_times[(-1)]
            if last_spike_to_stim_end > 0:
                first_to_last_spike = spike_times[(-1)] - spike_times[0]
                assert first_to_last_spike > 0
                ratio = last_spike_to_stim_end / first_to_last_spike
                if ratio > ratio_threshold:
                    phasic = True
        if case2:
            raw_time_threshold = 50.0
            if last_spike_to_stimulus_end > raw_time_threshold:
                phasic = True
        return phasic

    def check_bursting(traces, stim_start):
        """
        Bursting - bursts of APs separated by rest periods
        Not sure how to characterize currently.
        1. Find all AP peaks.
        2. Divide trace up into quiet periods and firing periods
        Quiet period is region where distance between two APs or last AP and 
        stimulus end is greater than some multiple of the average ISI (median?).
        """
        bursting = False
        return bursting

    def check_wide(traces, mean_width_threshold=10.0):
        """
        Abnormally wide APs - feature seen when inserting hNav 1.8 into mice (Han et al. 2015).
        """
        wide = False
        half_widths = []
        for t, v in zip(traces['t'], traces['v']):
            half_widths.append(ap_half_width(t, v, dvdt_threshold=5.0))

        if half_widths:
            if np.mean(half_widths) > mean_width_threshold:
                wide = True
        return wide

    def check_rep_fail(traces, rep_fail_threshold=0.0):
        """
        Repolarisation failure - trace does not recover to a reasonably depolarised voltage
        This can be set by user but we'll start with using 0 mV as default threshold and 
        can tune as needed.
        """
        rep_fail = False
        last_trace = traces['v'][(-1)]
        if last_trace[(-1)] > rep_fail_threshold:
            rep_fail = True
        return rep_fail

    firing_pattern = []
    num_aps = traces['numAPs']
    if num_aps == 0:
        firing_pattern.append('reluctant')
    else:
        if num_aps == 1:
            firing_pattern.append('single')
            if check_delayed(traces):
                firing_pattern.append('delayed')
            if check_wide(traces):
                firing_pattern.append('wide')
            if check_rep_fail(traces):
                firing_pattern.append('rep_fail')
        else:
            if num_aps > 1:
                firing_pattern.append('multi')
                phasic = check_phasic(traces, stim_end, ratio_threshold=0.25)
                delayed = check_delayed(traces)
                gap = check_gap(traces)
                rep_fail = check_rep_fail(traces)
                if not delayed:
                    if not gap:
                        if not phasic:
                            if not rep_fail:
                                firing_pattern.append('tonic')
                if phasic:
                    firing_pattern.append('phasic')
                if delayed:
                    firing_pattern.append('delayed')
                if gap:
                    firing_pattern.append('gap')
                if rep_fail:
                    firing_pattern.append('rep_fail')
                if check_wide(traces, mean_width_threshold=10.0):
                    firing_pattern.append('wide')
            return firing_pattern


def plot_traces(traces):
    for t, v in zip(traces['t'], traces['v']):
        plt.plot(t, v)


def write_header(biomarker_file):
    string = 'Index'
    for biomarker in db.biomarkerNames:
        string += ';' + biomarker

    string += ';stimAmp'
    string += '\n'
    biomarker_file.write(string)


WriteHeader = write_header

def write_biomarkers(biomarkers, biomarker_file):
    string = str(biomarkers['Index'])
    for biomarker in db.biomarkerNames:
        string += ';' + str(biomarkers[biomarker])

    string += ';' + str(biomarkers['stimAmp'])
    string += '\n'
    biomarker_file.write(string)


WriteBiomarkers = write_biomarkers

class FICurves(object):
    __doc__ = '\n    Class to hold FI curve data\n    Frequencies\n    Amplitudes\n    Results\n    Which simulations go together\n    \n    And allow you to extract FI curves, plot them and obtain summary statistics\n    '

    def __init__(self, results, simulations):
        self.results = results.copy()
        self.simulations = simulations.copy()
        self.groups = []
        self.group_simulations()
        self.get_FI_curves()
        if 'Parameters' in self.results.columns.levels[0]:
            self.results = self.results.drop('Parameters', axis=1, level=0)
            self.results.columns = self.results.columns.drop('Parameters', level=0)

    def group_simulations(self):
        """
        Group simulations together that are the same except for their stimulus amplitudes
        """
        self.groups = []
        for name, sim in self.simulations.items():
            amp, shared_params = self.get_simulation_parameters(sim.protocols)
            if amp:
                group = self.check_for_existing_group(shared_params)
                if group is not None:
                    self.groups[group]['simulations'][name] = amp
                else:
                    new_group = {'simulations':{name: amp}, 
                     'shared_params':shared_params}
                    self.groups.append(new_group)

    def get_simulation_parameters(self, sim_protocols):
        """
        Extract needed simulation parameters
        Currently: amplitude, stimulus type and scaling factors
        """
        amp = sim_protocols['amp']
        shared_params = {}
        shared_params['stim_type'] = sim_protocols['stim_func']
        if 'parameter_scaling' in sim_protocols:
            shared_params['parameter_scaling'] = sim_protocols['parameter_scaling']
        return (
         amp, shared_params)

    def check_for_existing_group(self, shared_params):
        """
        Check groups for a group that mathches other_params.
        Returns:
        Group index if group exists
        None if group does not exist
        """
        group_idx = None
        for i, group in enumerate(self.groups):
            if shared_params == group['shared_params']:
                assert group_idx is None, 'group_idx should equal None, instead: {}'.format(group_idx)
                group_idx = i

        return group_idx

    def get_FI_curves(self):
        """
        Use the ISIs to compute firing curves for each group, for models that have non-nan ISIs
        Firing curves are calculated for each simulation group
        """
        num_groups = len(self.groups)
        assert num_groups > 0, 'Num groups: {} is not > 0'.format(num_groups)
        for group in self.groups:
            idx = self.results.index
            amps = [amp for amp in group['simulations'].values()]
            fi_data = pd.DataFrame(index=idx, columns=amps)
            for sim_name, amp in group['simulations'].items():
                ISIs = self.results.loc[:, (sim_name, 'ISI')]
                frequencies = self.calculate_frequencies(ISIs)
                fi_data.loc[:, amp] = frequencies

            group['FI'] = fi_data

    def plot_FI_curves(self):
        """
        Plot FI curves and maybe compute some summary statistics
        Do scatter and line plots so that if we have a single datapoint for a model it still gets plotted
        """
        num_groups = len(self.groups)
        subplot_dim = int(np.ceil(np.sqrt(num_groups)))
        plt.figure(figsize=(10, 10))
        for i, group in enumerate(self.groups):
            plt.subplot(subplot_dim, subplot_dim, i + 1)
            fi_data = group['FI'].copy()
            for idx in fi_data.index:
                data = fi_data.loc[idx, :]
                plt.plot(data.index, data)
                plt.scatter(data.index, data)

            plt.xlim(min(fi_data.columns) - 0.1, max(fi_data.columns) + 0.1)
            plt.ylim(0, None)
            separator = '_'
            for i, sim_name in enumerate(group['simulations']):
                if i == 0:
                    temp_title = sim_name
                else:
                    s1 = temp_title.split(separator)
                    s2 = sim_name.split(separator)
                    title_parts = [part for part in s1 if part in s2]
                    title = separator.join(title_parts)

            plt.title(title)
            plt.xlabel('I (nA)')
            plt.ylabel('f (Hz)')

    def calculate_frequencies(self, ISIs):
        return 1000.0 / ISIs


def get_biomarker_names(biomarker_set='all'):
    """ 
    Biomarkers TODO from neuroelectro:
    * Input resistance
    * AP Half width
    * Membrane time constant
    * Cell capacitance (fixed by simulation)
    * Maximum firing rate
    * Sag ratio
    * Adaptation ratio
    * First spike latency
    * FI slope
    * Spike rise time
    * Spontaneous firing rate
    * There are others but think they are other names for the same concepts
    """
    if biomarker_set == 'all':
        biomarker_names = [
         'Threshold', 'APFullWidth', 'APPeak', 'APRiseTime', 'APSlopeMin', 'APSlopeMax', 'AHPAmp', 'AHPTau', 'AHPTrough', 'ISI', 'RMP', 'Rheobase']
    else:
        raise ValueError('biomarker_set {} not found'.format(biomarker_set))
    return biomarker_names


def find_threshold_crossings(arr, _threshold):
    """
    Find all indices at which a threshold is crossed from above and from below
    in an array. Used for finding indices to compute ap widths and half widths.
    """
    ups = []
    downs = []
    for i, _ in enumerate(arr[:-1]):
        if arr[i] < _threshold:
            if arr[(i + 1)] >= _threshold:
                ups.append(i)
        if arr[i] > _threshold and arr[(i + 1)] <= _threshold:
            downs.append(i)

    return (
     ups, downs)


def add_total_width_biomarker(pop, width_biomarker='APHalfWidth', filter_width=False, verbose=False):
    """
    Add a total width biomarker to each simulation in a population's results 
    """

    def compute_total_width(df, width_biomarker, filter_width=False):
        """
        Compute the total width of a simulation from its results dataframe
        with optional filtering out of AP Width outliers
        """
        freq = 1000.0 / df['ISI']
        numAPs = df['numAPs']
        freq[numAPs == 1] = 1
        width = df[width_biomarker]
        if filter_width:
            outlier_definition = an.get_outlier_definition(width_biomarker)
            width = width[(width < outlier_definition)]
        total_width = width * freq
        total_width = total_width.fillna(0)
        return total_width

    simulations = [col for col in pop.results.columns.levels[0] if col not in ('Parameters', )]
    for col in simulations:
        if verbose:
            print(col)
        total_width = compute_total_width(df=(pop.results[col]), width_biomarker=width_biomarker,
          filter_width=filter_width)
        pop.results.loc[:, (col, 'APTotalWidth')] = total_width