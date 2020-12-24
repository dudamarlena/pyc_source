# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/HMFcalc/utils.py
# Compiled at: 2013-06-13 04:29:10
"""
Created on Jun 15, 2012

@author: Steven
"""
from hmf.Perturbations import Perturbations
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np, logging, cosmolopy.distance as cd, pandas, os

def hmf_driver(transfer_file, extrapolate, k_bounds, z_list, WDM_list, approaches, overdensities, cosmology_list, min_M, max_M, M_step, user_model, cosmo_labels, extra_plots):
    os.chdir(os.path.dirname(__file__))
    masses = np.arange(min_M, max_M, M_step)
    mass_data = pandas.DataFrame({'M': 10 ** masses})
    k_data = pandas.DataFrame(index=range(4097))
    labels = {}
    warnings = {}
    growths = []
    pert = Perturbations(M=masses, transfer_file=transfer_file, z=z_list[0], WDM=None, k_bounds=k_bounds[0], extrapolate=extrapolate, reion__use_optical_depth=True, **cosmology_list[0])
    for cosmo_i, cosmo_dict in enumerate(cosmology_list):
        growths.append([])
        labels['cosmo'] = cosmo_labels[cosmo_i]
        for k_bound in k_bounds:
            if len(k_bounds) > 1:
                labels['k'] = 'k{' + str(k_bound[0]) + ',' + str(k_bound[1]) + '}'
            for wdm in [None] + WDM_list:
                if len(WDM_list) > 0:
                    if wdm is None:
                        labels['wdm'] = 'CDM'
                    else:
                        labels['wdm'] = 'WDM=' + str(wdm)
                for z in z_list:
                    if len(z_list) > 1 or z > 0:
                        labels['z'] = 'z=' + str(z)
                    print cosmo_dict
                    pert.update(k_bounds=k_bound, WDM=wdm, z=z, **cosmo_dict)
                    growths[cosmo_i].append(pert.growth)
                    k_data['k_' + getname(labels, excl=['deltavir', 'fsig'])] = pert.k
                    k_data['P(k)_' + getname(labels, excl=['deltavir', 'fsig'])] = pert.power_spectrum
                    mass_data['sigma_' + getname(labels, excl=['deltavir', 'fsig'])] = pert.sigma
                    mass_data['lnsigma_' + getname(labels, excl=['deltavir', 'fsig'])] = pert.lnsigma
                    mass_data['neff_' + getname(labels, excl=['deltavir', 'fsig'])] = pert.n_eff
                    for approach in approaches:
                        labels['fsig'] = approach
                        for overdensity in overdensities:
                            if len(overdensities) > 1:
                                labels['deltavir'] = 'Dvir=' + str(overdensity)
                            mass_func = pert.MassFunction(fsigma=approach, overdensity=overdensity, delta_c=cosmo_dict['delta_c'])
                            mass_data['hmf_' + getname(labels)] = mass_func
                            mass_data['f(sig)_' + getname(labels)] = pert.vfv
                            mass_data['M*hmf_' + getname(labels)] = mass_func * pert.M
                            if 'get_ngtm' in extra_plots:
                                mass_data['NgtM_' + getname(labels)] = pert.NgtM(mass_func)
                            if 'get_mgtm' in extra_plots:
                                mass_data['MgtM_' + getname(labels)] = pert.MgtM(mass_func)
                            if 'get_nltm' in extra_plots:
                                mass_data['NltM_' + getname(labels)] = pert.NltM(mass_func)
                            if 'get_mltm' in extra_plots:
                                mass_data['MltM_' + getname(labels)] = pert.MltM(mass_func)
                            if 'get_L' in extra_plots:
                                mass_data['L(N=1)_' + getname(labels)] = pert.how_big(mass_func)

            if pert.max_error:
                warnings[getname(labels, excl=['deltavir', 'fsig', 'z', 'wdm'])] = [
                 pert.max_error]
            if pert.min_error:
                warnings[getname(labels, excl=['deltavir', 'fsig', 'z', 'wdm'])].append(pert.min_error)

    return (
     mass_data, k_data, growths, warnings)


def cosmography(cosmology_list, cosmo_labels, redshifts, growth):
    distances = []
    for i, cosmology in enumerate(cosmology_list):
        cosmo = {'omega_M_0': cosmology['omegab'] + cosmology['omegac'], 'omega_lambda_0': cosmology['omegav'], 
           'h': cosmology['H0'] / 100.0, 
           'omega_b_0': cosmology['omegab'], 
           'omega_n_0': 0, 
           'N_nu': 0, 
           'n': cosmology['n'], 
           'sigma_8': cosmology['sigma_8']}
        cd.set_omega_k_0(cosmo)
        for j, z in enumerate(redshifts):
            distances = distances + [
             [cosmo_labels[i],
              z,
              cd.age(z, use_flat=False, **cosmo) / (31557600.0 * 1000000000),
              cd.comoving_distance(z, **cosmo) / 1000,
              cd.comoving_volume(z, **cosmo) / 1000000000,
              cd.angular_diameter_distance(z, **cosmo) / 1000,
              cd.luminosity_distance(z, **cosmo) / 1000,
              growth[i][j]]]

    return distances


def create_canvas(masses, mass_data, title, xlab, ylab, yscale):
    fig = Figure(figsize=(11, 6), edgecolor='white', facecolor='white', dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    linecolours = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    lines = ['-', '--', '-.', ':']
    counter = 0
    print mass_data
    for column in mass_data.columns:
        ax.plot(masses, mass_data[column], color=linecolours[(counter / 4 % 7)], linestyle=lines[(counter % 4)], label=column.split('_', 1)[1].replace('_', ', '))
        print column.split('_', 1)[1].replace('_', ', ')
        counter = counter + 1
        print 'Legend info... ', counter
        print ax.get_legend_handles_labels()

    ax.set_xscale('log')
    ax.set_yscale(yscale)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    print 'After...'
    print ax.get_legend_handles_labels()[1]
    canvas = FigureCanvas(fig)
    return canvas


def create_k_canvas(k_data, k_keys, p_keys, title, xlab, ylab):
    fig = Figure(figsize=(12, 6.7), edgecolor='white', facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    linecolours = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    lines = ['-', '--', '-.', ':']
    counter = 0
    for j, k_key in enumerate(k_keys):
        ax.plot(np.exp(k_data[k_key]), np.exp(k_data[p_keys[j]]), color=linecolours[(counter / 4)], linestyle=lines[(counter % 4)], label=k_key.split('_', 1)[1].replace('_', ', '))
        counter = counter + 1

    ax.set_yscale('log')
    ax.set_xscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    canvas = FigureCanvas(fig)
    return canvas


def getname(names, excl=[]):
    """
    Compiles the individual labels from a dictionary to a string label
    """
    label = ''
    for key, val in names.iteritems():
        if key not in excl:
            label = label + val + '_'

    label = label[:-1]
    return label