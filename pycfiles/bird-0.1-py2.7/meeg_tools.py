# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/bird/meeg_tools.py
# Compiled at: 2014-10-01 09:27:36
import numpy as np, mne
from mne import pick_types_evoked, pick_types_forward
from mne.datasets import sample
from mne.time_frequency import iir_filter_raw, morlet
from mne.simulation import generate_sparse_stc, generate_evoked
data_path = sample.data_path()
raw = mne.io.Raw(data_path + '/MEG/sample/sample_audvis_raw.fif')
proj = mne.read_proj(data_path + '/MEG/sample/sample_audvis_ecg_proj.fif')
raw.info['projs'] += proj
raw.info['bads'] = ['MEG 2443', 'EEG 053']
fwd_fname = data_path + '/MEG/sample/sample_audvis-meg-eeg-oct-6-fwd.fif'
ave_fname = data_path + '/MEG/sample/sample_audvis-no-filter-ave.fif'
cov_fname = data_path + '/MEG/sample/sample_audvis-cov.fif'
fwd = mne.read_forward_solution(fwd_fname, force_fixed=True, surf_ori=True)
fwd = pick_types_forward(fwd, meg=True, eeg=True, exclude=raw.info['bads'])
cov = mne.read_cov(cov_fname)
evoked_template = mne.read_evokeds(ave_fname, condition=0, baseline=None)
evoked_template = pick_types_evoked(evoked_template, meg=True, eeg=True, exclude=raw.info['bads'])
label_names = [
 'Aud-lh', 'Aud-lh']
labels = [ mne.read_label(data_path + '/MEG/sample/labels/%s.label' % ln) for ln in label_names
         ]

def simu_meg(snr=6, white=True, seed=None):
    tmin = -0.1
    sfreq = 1000.0
    tstep = 1.0 / sfreq
    n_samples = 600
    times = np.linspace(tmin, tmin + n_samples * tstep, n_samples)
    stc_data = np.zeros((len(labels), len(times)))
    Ws = morlet(sfreq, [3, 10], n_cycles=[1, 1.5])
    stc_data[0][:(len(Ws[0]))] = np.real(Ws[0])
    stc_data[1][:(len(Ws[1]))] = np.real(Ws[1])
    stc_data *= 1.0000000000000001e-07
    stc_data[1] = np.roll(stc_data[1], 80)
    stc = generate_sparse_stc(fwd['src'], labels, stc_data, tmin, tstep, random_state=0)
    picks = mne.pick_types(raw.info, meg=True, exclude='bads')
    if white:
        iir_filter = None
    else:
        iir_filter = iir_filter_raw(raw, order=5, picks=picks, tmin=60, tmax=180)
    evoked = generate_evoked(fwd, stc, evoked_template, cov, snr, tmin=0.0, tmax=0.2, iir_filter=iir_filter, random_state=seed)
    return evoked


def simu_bimodal_meg(snr=6, white=True, seed=None, freqs=[3, 50], n_cycles=[1, 1.5], phases=[
 0, 0], offsets=[0, 80]):
    tmin = -0.1
    sfreq = 1000.0
    tstep = 1.0 / sfreq
    n_samples = 600
    times = np.linspace(tmin, tmin + n_samples * tstep, n_samples)
    stc_data = np.zeros((len(labels), len(times)))
    Ws = morlet(sfreq, freqs, n_cycles=n_cycles)
    stc_data[0][:(len(Ws[0]))] = np.real(Ws[0] * np.exp(complex(0.0, 1.0) * phases[0]))
    stc_data[1][:(len(Ws[1]))] = np.real(Ws[1] * np.exp(complex(0.0, 1.0) * phases[1]))
    stc_data *= 1.0000000000000001e-07
    stc_data[0] = np.roll(stc_data[0], offsets[0])
    stc_data[1] = np.roll(stc_data[1], offsets[1])
    stc = generate_sparse_stc(fwd['src'], labels, stc_data, tmin, tstep, random_state=0)
    picks = mne.pick_types(raw.info, meg=True, exclude='bads')
    if white:
        iir_filter = None
    else:
        iir_filter = iir_filter_raw(raw, order=5, picks=picks, tmin=60, tmax=180)
    evoked = generate_evoked(fwd, stc, evoked_template, cov, snr, tmin=0.0, tmax=0.2, iir_filter=iir_filter, random_state=seed)
    return evoked