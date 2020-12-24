# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/get_cosmic_mol_gas_density.py
# Compiled at: 2019-11-08 07:15:40
# Size of source mod 2**32: 13467 bytes
from __future__ import print_function
import os, sys, re, copy, json, time, astropy, numpy as np
from astropy.table import Table
data_table_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data_Tables')

def get_cosmic_mol_gas_density_A3COSMOS(method='using SIDES mock galaxy models'):
    if re.match('^.*\\b(SIDES)\\b.*$', method):
        data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig15_plotted_data.txt')
    else:
        if re.match('^.*\\b(SMF)\\b.*$', method):
            data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig14_plotted_data.txt')
        else:
            raise Exception('Error! The \'method\' should be either "*SIDES*" or "*SMF*", but the input is "%s".' % method)
    if not os.path.isfile(data_table_file):
        raise Exception('Error! Data file "%s" was not found!' % data_table_file)
    tb = Table.read(data_table_file, format='ascii')
    z = copy.deepcopy(tb['z'].data)
    rho_mol_gas = copy.deepcopy(tb['rho_mol_gas_A3COSMOS'].data)
    return (
     z, rho_mol_gas)


def get_cosmic_mol_gas_density_Tacconi2018(method='using SIDES mock galaxy models'):
    if re.match('^.*\\b(SIDES)\\b.*$', method):
        data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig15_plotted_data.txt')
    else:
        if re.match('^.*\\b(SMF)\\b.*$', method):
            data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig14_plotted_data.txt')
        else:
            raise Exception('Error! The \'method\' should be either "*SIDES*" or "*SMF*", but the input is "%s".' % method)
    if not os.path.isfile(data_table_file):
        raise Exception('Error! Data file "%s" was not found!' % data_table_file)
    tb = Table.read(data_table_file, format='ascii')
    z = copy.deepcopy(tb['z'].data)
    rho_mol_gas = copy.deepcopy(tb['rho_mol_gas_Tacconi2018'].data)
    return (
     z, rho_mol_gas)


def get_cosmic_mol_gas_density_Scoville2017(method='using SIDES mock galaxy models'):
    if re.match('^.*\\b(SIDES)\\b.*$', method):
        data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig15_plotted_data.txt')
    else:
        if re.match('^.*\\b(SMF)\\b.*$', method):
            data_table_file = os.path.join(data_table_directory, 'Liu2019b_Fig14_plotted_data.txt')
        else:
            raise Exception('Error! The \'method\' should be either "*SIDES*" or "*SMF*", but the input is "%s".' % method)
    if not os.path.isfile(data_table_file):
        raise Exception('Error! Data file "%s" was not found!' % data_table_file)
    tb = Table.read(data_table_file, format='ascii')
    z = copy.deepcopy(tb['z'].data)
    rho_mol_gas = copy.deepcopy(tb['rho_mol_gas_Scoville2017'].data)
    return (
     z, rho_mol_gas)


def get_cosmic_mol_gas_density_Decarli2016():
    data_point_Decarli2016_x = [
     0.4858, 0.9543, 1.4277, 2.6129, 3.803]
    data_point_Decarli2016_xmin = np.array([0.2713, 0.695, 1.0059, 2.0088, 3.0115])
    data_point_Decarli2016_xmax = np.array([0.6309, 1.1744, 1.7387, 3.108, 4.4771])
    data_point_Decarli2016_ymin = 10 ** np.array([6.56, 6.83, 7.53, 7.69, 5.53])
    data_point_Decarli2016_ymax = 10 ** np.array([7.76, 7.73, 8.09, 8.28, 7.58])
    z = {}
    z['center'] = data_point_Decarli2016_x
    z['lower'] = data_point_Decarli2016_xmin
    z['upper'] = data_point_Decarli2016_xmax
    rho_mol_gas = {}
    rho_mol_gas['center'] = (data_point_Decarli2016_ymin + data_point_Decarli2016_ymax) / 2.0
    rho_mol_gas['lower'] = data_point_Decarli2016_ymin
    rho_mol_gas['upper'] = data_point_Decarli2016_ymax
    return (z, rho_mol_gas)


def get_cosmic_mol_gas_density_Riechers2018():
    data_point_Riechers2018_xmin = np.array([1.95, 1.95, 2.03, 4.9, 4.9])
    data_point_Riechers2018_xmax = np.array([2.85, 2.72, 2.85, 6.7, 6.7])
    data_point_Riechers2018_ymin = np.array([1.1, 0.95, 0.3, 0.14, np.nan]) * 10000000.0
    data_point_Riechers2018_ymax = np.array([5.6, 10.9, 7.3, 1.1, 4.0]) * 10000000.0
    z = {}
    z['center'] = (data_point_Riechers2018_xmin + data_point_Riechers2018_xmax) / 2.0
    z['lower'] = data_point_Riechers2018_xmin
    z['upper'] = data_point_Riechers2018_xmax
    rho_mol_gas = {}
    rho_mol_gas['center'] = (data_point_Riechers2018_ymin + data_point_Riechers2018_ymax) / 2.0
    rho_mol_gas['lower'] = data_point_Riechers2018_ymin
    rho_mol_gas['upper'] = data_point_Riechers2018_ymax
    return (z, rho_mol_gas)


def get_cosmic_mol_gas_density_Decarli2019():
    z1_1sig_lo, z1_1sig_hi, z1_2sig_lo, z1_2sig_hi = (5.89, 6.8, 5.4, 7.01)
    z2_1sig_lo, z2_1sig_hi, z2_2sig_lo, z2_2sig_hi = (7.74, 7.96, 7.63, 8.05)
    z3_1sig_lo, z3_1sig_hi, z3_2sig_lo, z3_2sig_hi = (7.5, 7.96, 7.26, 8.1)
    z4_1sig_lo, z4_1sig_hi, z4_2sig_lo, z4_2sig_hi = (7.2, 7.62, 6.97, 7.77)
    data_point_Decarli2019_xmin = np.array([0.002877, 1.006, 2.008, 3.011])
    data_point_Decarli2019_xmax = np.array([0.369, 1.738, 3.107, 4.475])
    data_point_Decarli2019_1sig_lo = np.array([10 ** z1_1sig_lo, 10 ** z2_1sig_lo, 10 ** z3_1sig_lo, 10 ** z4_1sig_lo])
    data_point_Decarli2019_1sig_hi = np.array([10 ** z1_1sig_hi, 10 ** z2_1sig_hi, 10 ** z3_1sig_hi, 10 ** z4_1sig_hi])
    data_point_Decarli2019_2sig_lo = np.array([10 ** z1_2sig_lo, 10 ** z2_2sig_lo, 10 ** z3_2sig_lo, 10 ** z4_2sig_lo])
    data_point_Decarli2019_2sig_hi = np.array([10 ** z1_2sig_hi, 10 ** z2_2sig_hi, 10 ** z3_2sig_hi, 10 ** z4_2sig_hi])
    z = {}
    z['center'] = (data_point_Decarli2019_xmin + data_point_Decarli2019_xmax) / 2.0
    z['lower'] = data_point_Decarli2019_xmin
    z['upper'] = data_point_Decarli2019_xmax
    rho_mol_gas = {}
    rho_mol_gas['center'] = (data_point_Decarli2019_1sig_lo + data_point_Decarli2019_1sig_hi) / 2.0
    rho_mol_gas['lower'] = data_point_Decarli2019_1sig_lo
    rho_mol_gas['upper'] = data_point_Decarli2019_1sig_hi
    rho_mol_gas['lower_2sigma'] = data_point_Decarli2019_2sig_lo
    rho_mol_gas['upper_2sigma'] = data_point_Decarli2019_2sig_hi
    return (z, rho_mol_gas)


def plot_cosmic_mol_gas_density():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6.8, 4.8))
    fig.subplots_adjust(left=0.15, right=0.95, bottom=0.105, top=0.885)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Redshift', fontsize=16, labelpad=1)
    ax.set_ylabel('$\\rho_{\\mathrm{mol\\,gas}}$ [$\\mathrm{M_{\\odot}\\,Mpc^{-3}}$]', fontsize=17, labelpad=15)
    ax.tick_params(axis='both', labelsize=14)
    ax.tick_params(direction='in', axis='both', which='both')
    ax.tick_params(top=False, right=True, which='both')
    ax_tick_locations = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    ax.set_xticks(ax_tick_locations)
    ax.set_xlim([-0.3, np.max(ax_tick_locations)])
    ax.set_ylim([10000.0, 2000000000.0])
    ax.set_yscale('log')
    ax.grid(True, ls='--', lw=0.25)
    z, y = get_cosmic_mol_gas_density_Decarli2016()
    for i in range(len(z['center'])):
        if not np.isnan(y['lower'][i]):
            plot_obj_data_1a = ax.fill_between([z['lower'][i], z['upper'][i]], [
             y['lower'][i], y['lower'][i]],
              [
             y['upper'][i], y['upper'][i]],
              color='#a3e2bc',
              alpha=0.4,
              zorder=11)

    z, y = get_cosmic_mol_gas_density_Riechers2018()
    for i in range(len(z['center'])):
        if not np.isnan(y['lower'][i]):
            plot_obj_data_2a = ax.fill_between([z['lower'][i], z['upper'][i]], [
             y['lower'][i], y['lower'][i]],
              [
             y['upper'][i], y['upper'][i]],
              color='#1e90ff',
              alpha=0.2,
              zorder=11)
        else:
            plot_obj_data_2b = ax.plot([z['lower'][i], z['upper'][i]], [
             y['upper'][i], y['upper'][i]],
              color='#1e90ff',
              alpha=0.25,
              lw=5,
              zorder=11)
            plot_obj_data_2c = plt.arrow((np.mean([z['lower'][i], z['upper'][i]])), (np.mean([y['upper'][i], y['upper'][i]])),
              0.0,
              (-np.mean([y['upper'][i], y['upper'][i]]) * 0.6),
              head_length=(np.mean([y['upper'][i], y['upper'][i]]) * 0.1),
              head_width=0.2,
              length_includes_head=True,
              head_starts_at_zero=False,
              transform=(ax.transData),
              color='#1e90ff',
              alpha=0.25,
              lw=3,
              zorder=11)

    z, y = get_cosmic_mol_gas_density_Decarli2019()
    for i in range(len(z['center'])):
        if not np.isnan(y['lower'][i]):
            plot_obj_data_3a = ax.fill_between([z['lower'][i], z['upper'][i]], [
             y['lower'][i], y['lower'][i]],
              [
             y['upper'][i], y['upper'][i]],
              color='#ffa8a8',
              alpha=0.6,
              zorder=13)
        if not np.isnan(y['lower_2sigma'][i]):
            plot_obj_data_3b = ax.fill_between([z['lower'][i], z['upper'][i]], [
             y['lower_2sigma'][i], y['lower_2sigma'][i]],
              [
             y['upper_2sigma'][i], y['upper_2sigma'][i]],
              color='#ffb9b9',
              alpha=0.3,
              zorder=12)

    z_A3COSMOS, rho_mol_gas_A3COSMOS = get_cosmic_mol_gas_density_A3COSMOS()
    z_Tacconi2018, rho_mol_gas_Tacconi2018 = get_cosmic_mol_gas_density_Tacconi2018()
    z_Scoville2017, rho_mol_gas_Scoville2017 = get_cosmic_mol_gas_density_Scoville2017()
    plot_obj_Scoville2017 = ax.plot(z_Scoville2017, rho_mol_gas_Scoville2017, dashes=(2,
                                                                                      1), color='#f383d7', linewidth=3.5, alpha=0.6, label='__none__', zorder=15)
    plot_obj_Tacconi2018 = ax.plot(z_Tacconi2018, rho_mol_gas_Tacconi2018, dashes=(5,
                                                                                   1), color='#3c9254', linewidth=3.5, alpha=0.6, label='__none__', zorder=15)
    plot_obj_A3COSMOS = ax.plot(z_A3COSMOS, rho_mol_gas_A3COSMOS, linestyle='solid', color='#fd7b0f', linewidth=4.8, alpha=0.8, label='__none__', zorder=15)
    plot_label_Scoville2017 = '$\\rho_{M_{\\mathrm{mol\\,gas}}}$ (Scoville+2017 Eq.)'
    plot_label_Tacconi2018 = '$\\rho_{M_{\\mathrm{mol\\,gas}}}$ (Tacconi+2018 Eq.)'
    plot_label_A3COSMOS = '$\\rho_{M_{\\mathrm{mol\\,gas}}}$ (D.Liu+2019b Eq.11)'
    plot_obj_Mgas_list = [plot_obj_A3COSMOS[0],
     plot_obj_Tacconi2018[0],
     plot_obj_Scoville2017[0]]
    plot_label_Mgas_list = [
     plot_label_A3COSMOS,
     plot_label_Tacconi2018,
     plot_label_Scoville2017]
    plot_label_data_1 = 'Decarli+2016'
    plot_label_data_2 = 'Riechers+2019 (COLDz)'
    plot_label_data_3 = 'Decarli+2019 (ASPECS)'
    plot_obj_data_list = [
     plot_obj_data_1a,
     plot_obj_data_2a,
     plot_obj_data_3a]
    plot_label_data_list = [
     plot_label_data_1,
     plot_label_data_2,
     plot_label_data_3]
    plot_legend_1 = plt.legend(plot_obj_data_list, plot_label_data_list, loc='lower left', labelspacing=0.12, borderaxespad=0.25, framealpha=0.5, fontsize=11)
    plot_legend_2 = plt.legend(plot_obj_Mgas_list, plot_label_Mgas_list, loc='lower right', labelspacing=0.12, borderaxespad=0.25, framealpha=0.5, fontsize=11)
    plt.gca().add_artist(plot_legend_1)
    plt.show()


if __name__ == '__main__':
    plot_cosmic_mol_gas_density()