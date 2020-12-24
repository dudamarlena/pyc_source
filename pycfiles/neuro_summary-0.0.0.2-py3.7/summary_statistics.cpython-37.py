# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/src/summary_statistics.py
# Compiled at: 2020-04-09 18:55:59
# Size of source mod 2**32: 7760 bytes
import numpy as np, matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys, os, scipy.io, pickle, h5py, argparse
from pathlib import Path
from src.p_util.old_util import getSignals
import src.config as config
import src.p_util.preprocessing as pre
import src.p_util.spike_detection as sd
from statsmodels.tsa.stattools import acf
import neurodsp.spectral.power as welch
import neurodsp.plts.spectral as plot_psd
import neurodsp.plts.time_series as plot_ts
import importlib.util

def import_constants():
    path = '%s/neuro-summary-config' % (Path.home(),)
    if not os.path.isdir(path):
        print('Building neuro-summary-config in your home directory...\nSee ~/neuro-summary-config/constants.py to change constants.')
        os.makedirs(path)
        with open(os.path.join(path, 'constants.py'), 'wb') as (temp_file):
            temp_file.write(config.constants.encode())
        with open(os.path.join(path, '__init__.py'), 'wb') as (temp_file):
            temp_file.write(''.encode())
    spec = importlib.util.spec_from_file_location('neuro-summary-config', '%s/constants.py' % (path,))
    constants = importlib.util.module_from_spec(spec)
    print(constants)
    spec.loader.exec_module(constants)
    return constants


def run_summary():
    """
    Takes in a data set as a commandline argument, it expects a two-dimensional array of [channels x signals]
    """
    parser = argparse.ArgumentParser(description='Create a plot of summary statistics.')
    parser.add_argument('file', metavar='F', help='Navigate to, and name data set to run')
    args = parser.parse_args()
    myFile = args.file
    myDir = os.path.dirname(os.path.abspath(__file__))
    data = None
    fs = 12500
    if os.path.isdir(myFile):
        try:
            fs, data = getSignals(myFile)
        except e:
            print('Please input a valid filetype. Inputs must be either .mat or a OE binary folder structure.')
            sys.exit()

    else:
        fileExtension = myFile.split()[1]
        mat = h5py.File(myFile, 'r')
        data = mat['MEA']
    mea = data
    constants = import_constants()
    ds_fs = 1000
    re_ts = pre.reference_channels(mea)
    lp_ds_ts, hp_ts = pre.filter_channels(re_ts, fs, mea_filter=ds_fs)
    lp_ds_t = np.arange(len(lp_ds_ts[0])) / ds_fs
    hp_t = np.arange(len(hp_ts[0])) / fs
    plt.tight_layout()
    fig = plt.figure(figsize=[12, 12])
    gs = gridspec.GridSpec(4, 2, figure=fig)
    labelSize = 18
    titleSize = 20
    spike_threshold = constants.spike_threshold
    bin_length = int(fs / 1000)
    nperseg = int(ds_fs)
    noverlap = int(nperseg / 2)
    spike_nperseg = int(fs)
    spike_noverlap = int(spike_nperseg / 2)
    wave_size = constants.wave_size
    acf_lags = constants.acf_lags
    mpl.rcParams['lines.linewidth'] = 0.1
    ax = fig.add_subplot(gs[(0, 1)])
    plot_factor = int(len(lp_ds_ts) / 9)
    for i, channel in enumerate(lp_ds_ts):
        if i % plot_factor:
            ax.plot(lp_ds_t, channel)

    ax.set_title('Lowpass Filtered Time Series', fontsize=titleSize)
    ax.set_ylabel('Voltage (uV)', fontsize=labelSize)
    ax.set_xlabel('Time (s)', fontsize=labelSize)
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['lines.linewidth'] = 0.2
    ax = fig.add_subplot(gs[(1, 0)])
    power_list = []
    freq_list = []
    for channel in lp_ds_ts:
        ch_freq, ch_power = welch((np.array(channel)), ds_fs, nperseg=nperseg, noverlap=noverlap)
        power_list.append(ch_power)
        freq_list.append(freq_list)
        plot_psd(ch_freq, ch_power, ax=ax)

    mpl.rcParams['lines.linewidth'] = 0.8
    ax.set_title('PSD', fontsize=titleSize)
    mpl.rcParams['lines.linewidth'] = 1
    spikes = sd.detect_spikes(hp_ts, fs, standard_threshold=spike_threshold)
    if len(np.concatenate(spikes).ravel()) > 0:
        ax = fig.add_subplot(gs[(1, 1)])
        new_spikes = []
        for spike in spikes:
            new_spikes.append(np.array(spike) / fs)

        ax.eventplot(new_spikes)
        ax.set_title('Spike Raster', fontsize=titleSize)
        ax.set_ylabel('Channel number', fontsize=labelSize)
        ax.set_xlabel('Time (s)', fontsize=labelSize)
        t_ms = fs * 1000
        waveforms = sd.collect_spikes(hp_ts, spikes, wave_size)
        ax = fig.add_subplot(gs[(2, 0)])
        for channel in waveforms:
            for waveform in channel:
                wave_t_ms = np.arange(len(waveform)) / t_ms
                ax.plot(wave_t_ms, waveform, linewidth=0.1)

        wave_average = sd.wave_average(waveforms)
        wave_t_ms = np.arange(len(wave_average)) / t_ms
        ax.plot(wave_t_ms, wave_average, linewidth=2, color='red')
        ax.set_title('Spike Waveforms', fontsize=titleSize)
        ax.set_ylabel('Amplitude', fontsize=labelSize)
        ax.set_xlabel('Time (ms)', fontsize=labelSize)
        bins = sd.bin_channels(np.array(spikes), bin_length)
        psv = sd.bin_sum(bins)
        ax = fig.add_subplot(gs[(2, 1)])
        ax.bar(np.arange(len(psv)) * (bin_length / fs), psv)
        ax.set_title('Population Spiking Vector (PSV)', fontsize=titleSize)
        ax.set_ylabel('Bins', fontsize=labelSize)
        ax.set_xlabel('Time (s)', fontsize=labelSize)
        psv_length = len(psv)
        y_auto = acf_sm = acf(psv, nlags=acf_lags, fft=True)
        x_auto = np.arange(len(y_auto))
        ax = fig.add_subplot(gs[(3, 0)])
        ax.plot(np.array(x_auto) * (bin_length / fs), np.array(y_auto) / max(y_auto))
        ax.set_title('Autocorrelation of PSV', fontsize=titleSize)
        ax.set_ylabel('Autocorrelation', fontsize=labelSize)
        ax.set_xlabel('Shifts (s)', fontsize=labelSize)
        psv_freq, psv_power = welch((np.array(psv)), (fs / bin_length), nperseg=spike_nperseg, noverlap=spike_noverlap)
        ax = fig.add_subplot(gs[(3, 1)])
        ax.set_title('PSD of PSV', fontsize=titleSize)
        plot_psd(psv_freq, psv_power, ax=ax)
        print('The summary statistics have finished computing.')
        plt.show()
    else:
        print('There are no spikes, ending analysis early. Please check your spike threshold.')
        plt.show()


def main():
    run_summary()