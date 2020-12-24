# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/conf/configuration.py
# Compiled at: 2020-04-23 12:33:50
# Size of source mod 2**32: 2314 bytes
import numpy as np, pkg_resources, os
_path = pkg_resources.resource_filename('pesummary', 'conf')
style_file = os.path.join(_path, 'matplotlib_rcparams.sty')
overwrite = 'Overwriting {} from {} to {}'
palette = 'colorblind'
include_prior = False
user = 'albert.einstein'
burnin = 0
burnin_method = 'burnin_by_step_number'
delimiter = '\t'
kde_plot = False
color = 'b'
colorcycle = 'brgkmc'
injection_color = 'orange'
prior_color = 'k'
public = False
multi_process = 1
corner_kwargs = dict(bins=50,
  smooth=0.9,
  label_kwargs=dict(fontsize=16),
  title_kwargs=dict(fontsize=16),
  color='#0072C1',
  truth_color='tab:orange',
  quantiles=[0.16, 0.84],
  levels=(
 1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-4.5)),
  plot_density=False,
  plot_datapoints=True,
  fill_contours=True,
  max_n_ticks=3)
gw_corner_parameters = [
 'luminosity_distance', 'dec', 'a_2', 'a_1', 'geocent_time', 'phi_jl',
 'psi', 'ra', 'phase', 'mass_2', 'mass_1', 'phi_12', 'tilt_2', 'iota',
 'tilt_1', 'chi_p', 'chirp_mass', 'mass_ratio', 'symmetric_mass_ratio',
 'total_mass', 'chi_eff', 'redshift', 'mass_1_source', 'mass_2_source',
 'total_mass_source', 'chirp_mass_source', 'lambda_1', 'lambda_2',
 'delta_lambda', 'lambda_tilde']
gw_source_frame_corner_parameters = [
 'luminosity_distance', 'mass_1_source', 'mass_2_source',
 'total_mass_source', 'chirp_mass_source', 'redshift']
gw_extrinsic_corner_parameters = [
 'luminosity_distance', 'psi', 'ra', 'dec']
cosmology = 'Planck15'