# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\ryan\documents\dev\python\dmf-control-board-firmware\dmf_control_board_firmware\calibrate\hv_attenuator.py
# Compiled at: 2016-11-30 18:21:49
import logging
from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt, numpy as np, pandas as pd, scipy.optimize as optimize
from .feedback import compute_from_transfer_function
logger = logging.getLogger(__name__)

def measure_board_rms(control_board, n_samples=10, sampling_ms=10, delay_between_samples_ms=0):
    """
    Read RMS voltage samples from control board high-voltage feedback circuit.
    """
    try:
        results = control_board.measure_impedance(n_samples, sampling_ms, delay_between_samples_ms, True, True, [])
    except RuntimeError:
        logger.warning('Error encountered during high-voltage RMS measurement.', exc_info=True)
        data = pd.DataFrame(None, columns=['board measured V',
         'divider resistor index'])
    else:
        data = pd.DataFrame({'board measured V': results.V_hv})
        data['divider resistor index'] = results.hv_resistor

    return data


def find_good(control_board, actuation_steps, resistor_index, start_index, end_index):
    """
    Use a binary search over the range of provided actuation_steps to find the
    maximum actuation voltage that is measured by the board feedback circuit
    using the specified feedback resistor.
    """
    lower = start_index
    upper = end_index
    while lower < upper - 1:
        index = lower + (upper - lower) / 2
        v = actuation_steps[index]
        control_board.set_waveform_voltage(v)
        data = measure_board_rms(control_board)
        valid_data = data[(data['divider resistor index'] >= 0)]
        if (valid_data['divider resistor index'] < resistor_index).sum():
            upper = index
        else:
            lower = index

    control_board.set_waveform_voltage(actuation_steps[lower])
    data = measure_board_rms(control_board)
    return (lower, data)


def resistor_max_actuation_readings(control_board, frequencies, oscope_reading_func):
    """
    For each resistor in the high-voltage feedback resistor bank, read the
    board measured voltage and the oscilloscope measured voltage for an
    actuation voltage that nearly saturates the feedback resistor.

    By searching for an actuation voltage near saturation, the signal-to-noise
    ratio is minimized.
    """
    control_board.set_waveform_voltage(0)
    control_board.auto_adjust_amplifier_gain = False
    control_board.amplifier_gain = 1.0
    target_voltage = 0.1
    control_board.set_waveform_voltage(target_voltage)
    oscope_rms = oscope_reading_func()
    estimated_amplifier_gain = oscope_rms / target_voltage
    max_post_gain_V = 0.8 * control_board.max_waveform_voltage
    max_actuation_V = max_post_gain_V / estimated_amplifier_gain
    actuation_steps = np.linspace(0.005, max_actuation_V, num=50)
    resistor_count = len(control_board.a0_series_resistance)
    conditions = pd.DataFrame([ [r, f] for r in range(resistor_count - 1, -1, -1) for f in frequencies
                              ], columns=[
     'resistor index', 'frequency'])

    def max_actuation_reading(x):
        """
        Measure maximum board RMS voltage using specified feedback resistor, at
        the specified frequency.

        Request corresponding oscilloscope RMS voltage reading.
        """
        r = x['resistor index'].values[0]
        f = x['frequency'].values[0]
        control_board.set_waveform_frequency(f)
        actuation_index, data = find_good(control_board, actuation_steps, r, 0, len(actuation_steps) - 1)
        board_measured_rms = data.loc[(data['divider resistor index'] >= 0,
         'board measured V')].mean()
        oscope_rms = oscope_reading_func()
        print 'R=%s, f=%s' % (r, f)
        return pd.DataFrame([
         [r, f, actuation_index, board_measured_rms,
          oscope_rms]], columns=[
         'resistor index', 'frequency',
         'actuation index', 'board measured V',
         'oscope measured V'])

    return conditions.groupby(['resistor index', 'frequency']).apply(max_actuation_reading).reset_index(drop=True)


def fit_feedback_params(calibration, max_resistor_readings):
    """
    Fit model of control board high-voltage feedback resistor and
    parasitic capacitance values based on measured voltage readings.
    """
    R1 = 10000000.0

    def fit_resistor_params(x):
        resistor_index = x['resistor index'].values[0]
        p0 = [calibration.R_hv[resistor_index],
         calibration.C_hv[resistor_index]]

        def error(p, df, R1):
            v1 = compute_from_transfer_function(calibration.hw_version.major, 'V1', V2=df['board measured V'], R1=R1, R2=p[0], C2=p[1], f=df['frequency'].values)
            e = df['oscope measured V'] - v1
            return e

        p1, success = optimize.leastsq(error, p0, args=(x, R1))
        p1 = np.abs(p1)
        return pd.DataFrame([p0 + p1.tolist()], columns=[
         'original R', 'original C',
         'fitted R', 'fitted C']).T

    results = max_resistor_readings[(max_resistor_readings['resistor index'] >= 0)].groupby([
     'resistor index']).apply(fit_resistor_params)
    data = results.unstack()
    data.columns = data.columns.droplevel()
    return data


def plot_feedback_params(hw_major_version, max_resistor_readings, feedback_params, axis=None):
    """
    Plot the effective attenuation _(i.e., gain less than 1)_ of the control
    board measurements of high-voltage AC input according to:

     - AC signal frequency.
     - feedback resistor used _(varies based on amplitude of AC signal)_.

    Each high-voltage feedback resistor (unintentionally) forms a low-pass
    filter, resulting in attenuation of the voltage measured on the control
    board.  The plot generated by this function plots each of the following
    trends for each feedback resistor:

     - Oscilloscope measurements.
     - Previous model of attenuation.
     - Newly fitted model of attenuation, based on oscilloscope readings.
    """
    R1 = 10000000.0
    if axis is None:
        fig = plt.figure()
        axis = fig.add_subplot(111)
    markers = MarkerStyle.filled_markers

    def plot_resistor_params(args):
        resistor_index, x = args
        try:
            color = axis._get_lines.color_cycle.next()
        except:
            color = axis._get_lines.prop_cycler.next()['color']

        F = feedback_params.loc[resistor_index]
        values = np.empty_like(x['frequency'])
        values[:] = compute_from_transfer_function(hw_major_version, 'V2', V1=1.0, R1=R1, R2=F['original R'], C2=F['original C'], f=x['frequency'])
        axis.loglog(x['frequency'], values, color=color, linestyle='--', label='R$_{%d}$ (previous fit)' % resistor_index)
        values[:] = compute_from_transfer_function(hw_major_version, 'V2', V1=1.0, R1=R1, R2=F['fitted R'], C2=F['fitted C'], f=x['frequency'])
        axis.loglog(x['frequency'], values, color=color, linestyle='-', alpha=0.6, label='R$_{%d}$ (new fit)' % resistor_index)
        attenuation = x['board measured V'] / x['oscope measured V']
        axis.plot(x['frequency'], attenuation, color='none', marker=markers[(resistor_index % len(markers))], label='R$_{%d}$ (scope measured)' % resistor_index, linestyle='none', markeredgecolor=color, markeredgewidth=2, markersize=8)
        return 0

    map(plot_resistor_params, max_resistor_readings.groupby('resistor index'))
    legend = axis.legend(ncol=3)
    legend.draw_frame(False)
    axis.set_xlabel('Frequency (Hz)')
    axis.set_ylabel('$\\frac{V_{BOARD}}{V_{SCOPE}}$', fontsize=25)
    return


def update_control_board_calibration(control_board, fitted_params):
    """
    Update the control board with the specified fitted parameters.
    """
    control_board.a0_series_resistance = fitted_params['fitted R'].values
    control_board.a0_series_capacitance = fitted_params['fitted C'].values