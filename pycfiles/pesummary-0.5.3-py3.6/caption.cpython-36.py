# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/conf/caption.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 4676 bytes
caption_1d_histogram = 'Plot showing the marginalized posterior distribution for {}. The vertical dashed lines show the 90% credible interval. The title gives the median and 90% confidence interval.'
caption_autocorrelation = 'Plot showing the autocorrelation function for {}. This plot is commonly used to check for randomness in the data. An autocorrelation of 1/-1 means that the samples are correlated and 0 means no correlation. The autocorrelation function at a lag of N gives the correlation between the 0th sample and the Nth sample.'
caption_sample_evolution = 'Scatter plot showing the evolution of the collected samples for {}.'
caption_skymap_preliminary = "Plot showing the most likely position of the source. This map has been produced by creating a 2d histogram from the samples of 'ra' and 'dec'. This is a valid approximation near the equator but breaks down near the poles. The 50% and 90% credible intervals are approximate. For true 50% and 90% credible intervals a 'ligo.skymap' skymap should be generated."
caption_skymap = 'Plot showing the most likely position of the source that generated the gravitational wave. We give the 50% and 90% credible intervals. The black region corresponds to the most likely position and light orange least likely.'
caption_strain = 'Plot showing the comparison between the gravitational wave strain measured at the detectors (grey) and the maximum likelihood waveform (orange) for all available detectors. A 30Hz high and 300Hz low pass filter have been applied to the gravitational wave strain.'
caption_frequency_waveform = 'Plot showing the frequency domain waveform generated from the maximum likelihood samples.'
caption_time_waveform = 'Plot showing the time domain waveform generated from the maximum likelihood samples.'
caption_psd = 'Plot showing the instrument noise for each detector near the time of detection; the power spectral density is expressed in terms of equivalent gravitational-wave strain amplitude.'
caption_calibration = 'Plot showing the calibration posteriors (solid lines) and calibration priors (solid band) for amplitude (top) and phase (bottom).'
caption_default_classification_mass_1_mass_2 = 'Scatter plot showing the individual samples with their classifications over the mass_1 and mass_2 parameter space. The samples have not been reweighted. Green regions correspond to BBHs, blue BNS, orange NSBH and red MassGap.'
caption_population_classification_mass_1_mass_2 = 'Scatter plot showing the individual samples with their classifications over the mass_1 and mass_2 parameter space. The samples have been reweighted to a population prior. Green regions correspond to BBHs, blue BNS, orange NSBH and red MassGap.'
caption_default_classification_bar = 'Bar plot showing the most likely classification of the binary based on the samples.'
caption_population_classification_bar = 'Bar plot showing the most likely classification of the binary based on the samples which have been reweighted to a population prior.'
caption_2d_contour = '2d contour plot showing the bounded posterior distributions for {} and {}. Each contour shows the 90% credible interval and the posterior distributions are normalized.'
caption_violin = 'Violin plot showing the posterior distributions for {}. The horizontal black lines show the 90% credible intervals.'
caption_spin_disk = 'Posterior probability distributions for the dimensionless component spins relative to the normal to the orbital plane, L, marginalized over the  azimuthal angles. The bins are constructed linearly in spin magnitude and the cosine of the tilt angles and are assigned equal prior probability.'