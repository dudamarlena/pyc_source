# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/read_z_Mstar_SFR_Mgas_datasets.py
# Compiled at: 2019-10-24 23:34:39
# Size of source mod 2**32: 66133 bytes
from __future__ import print_function
import os, sys, re, copy, json, time, datetime, shutil, astropy, numpy as np
from astropy.table import Table, Column, MaskedColumn, hstack
import pandas as pd
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:
    sys.path.append(os.path.dirname(__file__))
    from calc_alpha_CO import calc_alphaCO_from_metalZ_following_Wilson1995, calc_alphaCO_from_metalZ_following_Genzel2015a, calc_alphaCO_from_metalZ_following_Genzel2015b, calc_alphaCO_from_metalZ_following_Bolatto2013, calc_alphaCO_from_metalZ_following_Accurso2017, calc_alphaCO_from_metalZ_following_Bertemes2018, calc_alphaCO_from_metalZ_following_Tacconi2018
    from calc_delta_GD import calc_deltaGD_from_metalZ_following_Leroy2011, calc_deltaGD_from_metalZ_following_Magdis2012, calc_deltaGD_from_metalZ_following_RemyRuyer2014a, calc_deltaGD_from_metalZ_following_RemyRuyer2014b
    from calc_fmol import calc_fmol_from_metalZ_following_Krumholz2009, calc_fmol_from_metalZ_following_Dave2016, calc_fmol_from_metalZ_following_Popping2014
    from calc_metal_Z import calc_metalZ_from_FMR_following_Genzel2015_Eq12a, calc_metalZ_from_FMR_following_Mannucci2010_Eq4, convert_metalZ_M08_to_metalZ_PP04_N2_polynomial, convert_metalZ_KK04_to_metalZ_PP04, calc_metalZ_from_FMR_with_dzliu_selection, calc_metalZ_from_FMR_following_Kewley2008_PP04_O3N2

    def calc_Sargent2014_sSFR(z, lgMstar=10.5, DeltaMS=0.0):
        return 0.095 * 10 ** (-0.21 * (lgMstar - numpy.log10(50000000000.0))) * numpy.exp(2.05 * z / (1.0 + 0.16 * z ** 1.54)) * 10 ** DeltaMS


    def calc_Speagle2014_sSFR(cosmoAge, lgMstar=10.5, DeltaMS=0.0):
        return 10 ** ((0.84 - 0.026 * cosmoAge) * lgMstar - (6.51 - 0.11 * cosmoAge)) / 10 ** lgMstar * 1000000000.0 * 10 ** DeltaMS


    def calc_Scoville2017_sSFR(z, lgMstar=10.5, DeltaMS=0.0):
        lgMstar_ref = 10.5
        SFR_MS_ref = 10 ** (0.59 * lgMstar_ref - 5.77) * np.power(1.0 + z, 0.22 * lgMstar_ref + 0.59)
        SFR_MS = SFR_MS_ref * 10 ** (1.72 - np.log10(1 + np.power(10 ** (lgMstar - 10.31), -1.07))) / 10 ** (1.72 - np.log10(1 + np.power(10 ** (lgMstar_ref - 10.31), -1.07)))
        sSFR_MS = SFR_MS / 10 ** lgMstar * 1000000000.0
        return sSFR_MS


    def calc_sSFR_MS(lgMstar, z, cosmoAge=None):
        if cosmoAge is None:
            cosmoAge = cosmo.age(z).value
        sSFR_MS = calc_Speagle2014_sSFR(cosmoAge, lgMstar)
        return sSFR_MS


    def mask_dataset(input_data, mask_CPA=True, mask_SED=True, mask_IMG=True, mask_known_zspec=False):
        mask_valid_sources = input_data['z'] > 0
        if mask_SED:
            if os.path.isfile('datatable_discarded_sources_by_SED.txt'):
                list_SED = Table.read('datatable_discarded_sources_by_SED.txt', format='ascii.commented_header')
                mask_SED = np.isin(input_data['ID'], list_SED.columns[0].data)
                mask_valid_sources = np.logical_and(mask_valid_sources, ~mask_SED)
        if mask_CPA:
            if os.path.isfile('datatable_discarded_sources_by_CPA.txt'):
                list_CPA = Table.read('datatable_discarded_sources_by_CPA.txt', format='ascii.commented_header')
                mask_CPA = np.isin(input_data['ID'], list_CPA.columns[0].data)
                mask_valid_sources = np.logical_and(mask_valid_sources, ~mask_CPA)
        if mask_IMG:
            if os.path.isfile('datatable_discarded_sources_by_IMG.txt'):
                list_IMG = Table.read('datatable_discarded_sources_by_IMG.txt', format='ascii.commented_header')
                mask_IMG = np.isin(input_data['ID'], list_IMG.columns[0].data)
                mask_valid_sources = np.logical_and(mask_valid_sources, ~mask_IMG)
        if mask_known_zspec:
            if os.path.isfile('datatable_known_zspec.txt'):
                list_known_zspec = Table.read('datatable_known_zspec.txt', format='ascii.commented_header')
                mask_known_zspec = np.isin(input_data['ID'], list_known_zspec.columns[0])
                mask_valid_sources = np.logical_and(mask_valid_sources, mask_known_zspec)
        print('selecting %d data after masking' % np.sum(mask_valid_sources))
        output_data = copy.copy(input_data)
        for keyname in output_data:
            if not np.isscalar(input_data[keyname]):
                output_data[keyname] = np.array(input_data[keyname])[mask_valid_sources]

        return output_data


    def calc_metal_Z_high_z_method(M_star, SFR, z):
        return calc_metalZ_from_FMR_following_Genzel2015_Eq12a(M_star, z)


    def calc_metal_Z_local_galaxy_method(M_star, SFR, z):
        return convert_metalZ_M08_to_metalZ_PP04_N2_polynomial(calc_metalZ_from_FMR_following_Mannucci2010_Eq4(M_star, SFR))


    def read_datasets():
        datasets = []
        ds = {}
        ds['label'] = 'This work (A3COSMOS)'
        ds['color'] = 'gold'
        ds['facecolor'] = 'gold'
        ds['edgecolor'] = 'k'
        ds['edgelinewidth'] = 0.5
        ds['alpha'] = 1.0
        ds['marker'] = 'o'
        ds['markersize'] = 15
        tbfile = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_a3cosmos' + os.sep + 'dataset_v20180801' + os.sep + 'datatable_ID_RA_Dec_z_Mstar_SFR_sSFR_with_deltaGas.fits'
        tbinfo = open(os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_a3cosmos' + os.sep + 'dataset_v20180801' + os.sep + 'datatable_ID_RA_Dec_z_Mstar_SFR_sSFR_with_deltaGas.info.txt').readline().rstrip()
        print("Reading '%s' %s" % (tbfile, tbinfo))
        ds['datatable'] = tbfile
        tb = Table.read(ds['datatable'])
        mask = tb['ID'] != 850535
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['Mmol'] = tb['M_mol_gas_Method2_850_Hughes2017']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((1.0 / tb['SNRObs']) ** 2 + 0.04000000000000001) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((1.0 / tb['SNRObs']) ** 2 + 0.010000000000000002) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Tacconi+2018'
        ds['color'] = 'seagreen'
        ds['facecolor'] = 'seagreen'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = 'D'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Tacconi2018_PHIBSS2/datatable_ID_RA_Dec_z_Mstar_SFR_sSFR_with_deltaGas_with_Survey_Number_GE_1.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mstar'] > 0
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = calc_metal_Z_high_z_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['Mmol'] = tb['deltaGas'] * tb['Mstar'] / calc_alphaCO_from_metalZ_following_Tacconi2018(calc_metalZ_from_FMR_following_Genzel2015_Eq12a(ds['Mstar'], ds['z'])) * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt(0.13) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt(0.1) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Saintonge+2017'
        ds['color'] = 'blue'
        ds['facecolor'] = 'blue'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = '+'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Saintonge2017_xCOLDGASS/xCOLDGASS_PubCat.fits'
        tb = Table.read((ds['datatable']), format='fits')
        mask = np.logical_and(np.logical_and(np.logical_and(tb['SN_CO'] >= 3, tb['LOGMSTAR'] > 0), tb['LCO_COR'] > 0), tb['LOGSFR_BEST'] > -99)
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['Z_SDSS']
        ds['SFR'] = np.power(10.0, tb['LOGSFR_BEST'])
        ds['Mstar'] = np.power(10.0, tb['LOGMSTAR'])
        ds['Mmol_Saintonge2017'] = tb['LCO_COR'] * tb['XCO_A17']
        ds['alphaCO_Saintonge2017'] = tb['XCO_A17']
        ds['LPrmCO10'] = 23.5 * tb['ICO_COR'] * np.pi / (4 * np.log(2)) * 484.0 * tb['LUMDIST'] ** 2 * np.power(1.0 + tb['Z_SDSS'], -3)
        ds['LPrmCO10_err'] = 23.5 * tb['ICO_COR_ERR'] * np.pi / (4 * np.log(2)) * 484.0 * tb['LUMDIST'] ** 2 * np.power(1.0 + tb['Z_SDSS'], -3)
        mask2 = tb['Z_PP04_O3N2'] > 0
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['MetalZ'][mask2] = tb['Z_PP04_O3N2'][mask2]
        ds['MetalZ_Mannucci2010_Eq4_Method'] = calc_metalZ_from_FMR_following_Mannucci2010_Eq4(ds['Mstar'], ds['SFR'])
        ds['MetalZ_Kewley2008_Method'] = calc_metalZ_from_FMR_following_Kewley2008_PP04_O3N2(ds['Mstar'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = ds['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['ICO_COR_ERR'] / tb['ICO_COR']) ** 2 + 0.04000000000000001) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['ICO_COR_ERR'] / tb['ICO_COR']) ** 2 + tb['LOGSFR_ERR'] ** 2) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Saintonge+2017 uplims'
        ds['color'] = 'blue'
        ds['facecolor'] = 'blue'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = 'uplims'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Saintonge2017_xCOLDGASS/xCOLDGASS_PubCat.fits'
        tb = Table.read((ds['datatable']), format='fits')
        mask = np.logical_and(np.logical_and(np.logical_and(tb['SN_CO'] < 3, tb['LOGMSTAR'] > 0), tb['LCO_COR'] > 0), tb['LOGSFR_BEST'] > -99)
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['Z_SDSS']
        ds['SFR'] = np.power(10.0, tb['LOGSFR_BEST'])
        ds['Mstar'] = np.power(10.0, tb['LOGMSTAR'])
        ds['LPrmCO10'] = 117.5 * tb['RMS_CO'] * 300 / (2 * np.sqrt(2 * np.log(2))) * np.sqrt(np.pi) * np.pi / (4 * np.log(2)) * 484.0 * tb['LUMDIST'] ** 2 * np.power(1.0 + tb['Z_SDSS'], -3)
        mask2 = tb['Z_PP04_O3N2'] > 0
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['MetalZ'][mask2] = tb['Z_PP04_O3N2'][mask2]
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = ds['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Villanueva+2017'
        ds['color'] = 'orangered'
        ds['facecolor'] = 'orangered'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = 'x'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Villanueva2017_VALES/datatable_Villanueva2017_VALES_Survey.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(tb['lgMH2'] > 0, tb['e_lgMH2'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['ID_GAMA']
        ds['z'] = tb['z_spec']
        ds['SFR'] = np.power(10, tb['lgLIR']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'])
        ds['LPrmCO10'] = 32500000.0 * tb['SCO10'] / 13287.403441 * cosmo.luminosity_distance(tb['z_spec']).value ** 2 / (1.0 + tb['z_spec'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = tb['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['e_SCO10'] / tb['SCO10']) ** 2 + tb['e_lgMstar'] ** 2) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['e_SCO10'] / tb['SCO10']) ** 2 + (tb['e_SFR'] / tb['SFR']) ** 2) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Villanueva+2017 uplims'
        ds['color'] = 'orangered'
        ds['facecolor'] = 'orangered'
        ds['edgecolor'] = 'orangered'
        ds['alpha'] = 0.7
        ds['marker'] = 'uplims'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Villanueva2017_VALES/datatable_Villanueva2017_VALES_Survey.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(np.logical_or(tb['lgMH2'] <= 0, tb['e_lgMH2'] <= 0), tb['e_SCO10'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['ID_GAMA']
        ds['z'] = tb['z_spec']
        ds['SFR'] = np.power(10, tb['lgLIR']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'])
        ds['LPrmCO10'] = 162500000.0 * tb['e_SCO10'] / 13287.403441 * cosmo.luminosity_distance(tb['z_spec']).value ** 2 / (1.0 + tb['z_spec'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = tb['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Bertemes+2018'
        ds['color'] = 'lime'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'lime'
        ds['alpha'] = 0.7
        ds['marker'] = '^'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatable_z0_Bertemes2018_Stripe82/datatable_Bertemes2018_Stripe82_big_reformatted_by_dzliu_xmatched_to_SDSS_DR7_MPA_JHU_catalog.fits'
        tb = Table.read((ds['datatable']), format='fits')
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = np.power(10.0, tb['logSFR'])
        ds['Mstar'] = np.power(10.0, tb['AVG_LOGMSTAR'])
        ds['MetalZ'] = tb['MetalZ']
        ds['Mmol'] = np.power(10.0, tb['logMgas_via_CO']) / calc_alphaCO_from_metalZ_following_Bertemes2018(tb['MetalZ']) * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['E_logMgas_via_CO'] / tb['logMgas_via_CO']) ** 2 + 0.04000000000000001) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['E_logMgas_via_CO'] / tb['logMgas_via_CO']) ** 2 + 0.010000000000000002) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Lee+2017'
        ds['color'] = 'green'
        ds['facecolor'] = 'green'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = '2'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Lee2017/Lee2017_CO32_z0p5_sample.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = np.power(10, tb['lgMstar'])
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['deltaGas'] * ds['Mstar']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['e_deltaGas'] / tb['deltaGas']) ** 2 + tb['e_lgMstar'] ** 2) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['e_deltaGas'] / tb['deltaGas']) ** 2 + tb['e_lgLIR'] ** 2) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Bauermeister+2013'
        ds['color'] = 'royalblue'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'royalblue'
        ds['alpha'] = 0.7
        ds['marker'] = '<'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0.5_Bauermeister2013/datatable_Bauermeister2013_EGNOG_Survey.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mgas'] > 3.0 * tb['e_Mgas']
        tb = tb[mask]
        ds['ID'] = tb['Source_Name']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = np.power(10.0, tb['lgMstar'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['alphaCO_old'] = tb['Mgas'] * 0.0 + 4.352
        ds['Mmol'] = tb['Mgas'] / ds['alphaCO_old'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['e_Mgas'] / tb['Mgas']) ** 2 + np.max([tb['e_lgMstar_hi'], -tb['e_lgMstar_lo']], axis=0) ** 2) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['e_Mgas'] / tb['Mgas']) ** 2 + (np.max([tb['e_SFR_hi'], -tb['e_SFR_lo']], axis=0) / tb['SFR']) ** 2) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Cicone+2017'
        ds['color'] = 'cyan'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'cyan'
        ds['alpha'] = 0.7
        ds['marker'] = 's'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0_Cicone2017/Cicone2017_combined_table_by_dzliu.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask2 = np.logical_or(tb['Sample'] == 'A', tb['Sample'] == 'I2')
        tb['LCO_CORR'][mask2] = tb['LCO_CORR'][mask2]
        tb['e_LCO_CORR'][mask2] = tb['e_LCO_CORR'][mask2]
        mask = tb['flag_LCO_CORR'] != '<'
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z_SDSS']
        ds['SFR'] = 10 ** tb['lgSFR']
        ds['Mstar'] = 10 ** tb['lgMstar']
        ds['MetalZ'] = tb['Z_PP04_O3N2']
        ds['Mmol'] = tb['LCO_CORR'] * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        ds['deltaGasErr'] = np.sqrt((tb['e_LCO_CORR'] / tb['LCO_CORR']) ** 2 + tb['e_lgMstar'] ** 2) * ds['deltaGas']
        ds['tauDeplErr'] = np.sqrt((tb['e_LCO_CORR'] / tb['LCO_CORR']) ** 2 + tb['e_lgSFR'] ** 2) * ds['tauDepl']
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Cicone+2017 uplims'
        ds['color'] = 'cyan'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'cyan'
        ds['alpha'] = 0.7
        ds['marker'] = 'uplims'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0_Cicone2017/Cicone2017_combined_table_by_dzliu.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask2 = np.logical_or(tb['Sample'] == 'A', tb['Sample'] == 'I2')
        tb['LCO_CORR'][mask2] = tb['LCO_CORR'][mask2]
        tb['e_LCO_CORR'][mask2] = tb['e_LCO_CORR'][mask2]
        mask = tb['flag_LCO_CORR'] == '<'
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z_SDSS']
        ds['SFR'] = 10 ** tb['lgSFR']
        ds['Mstar'] = 10 ** tb['lgMstar']
        ds['MetalZ'] = tb['Z_PP04_O3N2']
        ds['Mmol'] = tb['e_LCO_CORR'] / 3.0 * 5.0 * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Combes+2013'
        ds['color'] = 'none'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = 'd'
        ds['markersize'] = 12
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0.8_Combes2013/Combes2013_combined_table_by_dzliu.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(np.logical_and(tb['flag_SCO'] != '<', tb['lgMstar'] > 0), tb['LineName'] == 'CO(2-1)')
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = np.power(10, tb['lgLIR']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'] - 0.238)
        ds['LPrmCO10'] = 32500000.0 * tb['SCO'] / 53147.769444000005 * cosmo.luminosity_distance(ds['z']).value ** 2 / (1.0 + ds['z']) / 0.8
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = ds['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Combes+2013 uplims'
        ds['color'] = 'magenta'
        ds['facecolor'] = 'magenta'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = 'uplims'
        ds['markersize'] = 12
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0.8_Combes2013/Combes2013_combined_table_by_dzliu.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(np.logical_and(tb['flag_SCO'] == '<', tb['lgMstar'] > 0), tb['LineName'] == 'CO(2-1)')
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = np.power(10, tb['lgLIR']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'] - 0.238)
        ds['LPrmCO10'] = 32500000.0 * (tb['e_SCO'] / 3.0 * 5.0) / 53147.769444000005 * cosmo.luminosity_distance(ds['z']).value ** 2 / (1.0 + ds['z']) / 0.8
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['alphaCO'] = calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['Mmol'] = ds['LPrmCO10'] * ds['alphaCO']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Kirkpatrick+2014'
        ds['color'] = 'lightgreen'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'lightgreen'
        ds['alpha'] = 0.7
        ds['marker'] = '>'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0.1_Kirkpatrick2014/datatable_Kirkpatrick2014.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['LPrmCO10'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Source_Name']
        ds['z'] = tb['z']
        ds['SFR'] = np.power(10.0, tb['lgLIR_SF']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['Mmol'] = tb['LPrmCO10'] * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Cortzen+2019'
        ds['color'] = 'cyan'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'cyan'
        ds['alpha'] = 0.7
        ds['marker'] = '$c$'
        ds['markersize'] = 12
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0.1_Cortzen2019/datatable_Cortzen2019_with_deltaMS.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(tb['LPrmCO10'] > 0, tb['eLPrmCO10'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['Source_Name']
        ds['z'] = tb['z']
        ds['SFR'] = np.power(10.0, tb['lgLIR']) / 10000000000.0
        ds['Mstar'] = np.power(10, tb['lgMstar'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['Mmol'] = tb['LPrmCO10'] * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Spilker+2018'
        ds['color'] = 'red'
        ds['facecolor'] = 'red'
        ds['edgecolor'] = 'none'
        ds['alpha'] = 0.7
        ds['marker'] = '1'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_Spilker2018/Spilker2018_CO21_z0p7_sample.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mmol'] > 3.0 * tb['eMmol']
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['Mmol']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Lisenfeld+2017'
        ds['color'] = 'pink'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'pink'
        ds['alpha'] = 0.7
        ds['marker'] = 'D'
        ds['markersize'] = 12
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z0_Lisenfeld2018/tab2_lourdes_reformatted_by_dzliu.dat'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['det_co_code'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Name']
        ds['z'] = tb['z']
        ds['SFR'] = tb['sfr']
        ds['Mstar'] = np.power(10, tb['log_Mstar'])
        ds['MetalZ'] = calc_metal_Z_local_galaxy_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['Mmol'] = np.power(10, tb['log_Mh2']) / 4.3 * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Magdis+2012a'
        ds['color'] = 'lightgreen'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'lightgreen'
        ds['alpha'] = 0.7
        ds['marker'] = '^'
        ds['markersize'] = 35
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z1.5_Magdis2012/datatable_Magdis2012.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mstar'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Source']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['Mgas']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Magdis+2012b'
        ds['color'] = 'green'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'green'
        ds['alpha'] = 0.7
        ds['marker'] = 'v'
        ds['markersize'] = 35
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z3.0_Magdis2012b/datatable_Magdis2012b.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mstar'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Source']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['Mgas']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Magdis+2017'
        ds['color'] = 'darkgreen'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'darkgreen'
        ds['alpha'] = 0.7
        ds['marker'] = '>'
        ds['markersize'] = 35
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z3.0_Magdis2017/datatable_Magdis2017.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mstar'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Source']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['Mgas']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Kaasinen+2019'
        ds['color'] = 'magenta'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = 'H'
        ds['markersize'] = 18
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z2_Kaasinen2019/Kaasinen2019_CO10_z2_sample.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(np.logical_and(np.logical_and(tb['Mstar'] > 0, tb['SFR'] > 0), tb['LPrmCO10'] > 0), tb['z_CO10'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = tb['z_CO10']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = calc_metal_Z_high_z_method(ds['Mstar'], ds['SFR'], ds['z'])
        ds['Mmol'] = tb['LPrmCO10'] * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'Tan+2014'
        ds['color'] = 'cyan'
        ds['facecolor'] = 'cyan'
        ds['edgecolor'] = 'cyan'
        ds['alpha'] = 0.7
        ds['marker'] = 'd'
        ds['markersize'] = 25
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatables_z_deltaGas' + os.sep + 'datatable_z4.0_Tan2014/datatable_Tan2014.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = tb['Mstar'] > 0
        tb = tb[mask]
        ds['ID'] = tb['Source']
        ds['z'] = tb['z']
        ds['SFR'] = 10 ** tb['lgLIR'] / 10000000000.0
        ds['Mstar'] = tb['Mstar']
        ds['MetalZ'] = ds['z'] * 0.0 - 99
        ds['Mmol'] = tb['MH2']
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'DGS'
        ds['color'] = 'magenta'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = '*'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatable_z0_DGS/RemyRuyer,2015A&A...582A.121R,Mdust,20190206.csv'
        tb = pd.read_csv(ds['datatable'])
        mask = np.logical_and(np.logical_and(np.logical_and(tb['Mstar'] > 0, tb['L_IR'] > 0), tb['MH2'] > 0), tb['Metallicity'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['Source'].values
        ds['z'] = tb['L_IR'].values * 0.0 + 1e-05
        ds['SFR'] = tb['L_IR'].values / 10000000000.0
        ds['Mstar'] = tb['Mstar'].values
        ds['MetalZ'] = tb['Metallicity'].values
        ds['Mmol'] = tb['MH2_L68'].values / 3.16 * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'HRS'
        ds['color'] = 'magenta'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = 'v'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatable_z0_HRS/datatable_Andreani2018_Table1_with_Hughes2013_metallicity.fits'
        tb = Table.read((ds['datatable']), format='fits')
        mask = np.logical_and(np.logical_and(np.logical_and(tb['lgM_star'] > 0, tb['lgL_IR'] > 0), tb['lgM_H2'] > 0), tb['Metallicity'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['ID']
        ds['z'] = 10 ** tb['lgL_IR'] * 0.0 + 0.0036
        ds['SFR'] = 10 ** tb['lgL_IR'] / 10000000000.0
        ds['Mstar'] = 10 ** tb['lgM_star']
        ds['MetalZ'] = tb['Metallicity']
        ds['Mmol'] = 10 ** tb['lgM_H2'] / 3.6 * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        ds = {}
        ds['label'] = 'KINGFISH'
        ds['color'] = 'magenta'
        ds['facecolor'] = 'none'
        ds['edgecolor'] = 'magenta'
        ds['alpha'] = 0.7
        ds['marker'] = 'p'
        ds['markersize'] = 15
        ds['datatable'] = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables' + os.sep + 'datatable_z0_KINGFISH/datatable_Groves2015_FLUX_500.txt'
        tb = Table.read((ds['datatable']), format='ascii.commented_header')
        mask = np.logical_and(np.logical_and(np.logical_and(tb['logMstar'] > 0, tb['SFR'] > 0), tb['MH2'] > 0), tb['Metallicity_KK04'] > 0)
        tb = tb[mask]
        ds['ID'] = tb['Name_KINGFISH']
        ds['z'] = tb['z']
        ds['SFR'] = tb['SFR']
        ds['Mstar'] = 10 ** tb['logMstar']
        ds['MetalZ'] = convert_metalZ_KK04_to_metalZ_PP04(tb['Metallicity_KK04'])
        ds['Mmol'] = tb['MH2'] / 4.4 * calc_alphaCO_from_metalZ_following_Tacconi2018(ds['MetalZ'])
        ds['sSFR'] = ds['SFR'] / ds['Mstar'] * 1000000000.0
        ds['sSFR_MS'] = calc_Speagle2014_sSFR(cosmo.age(ds['z']).value, np.log10(ds['Mstar']))
        ds['DeltaMS'] = np.log10(ds['sSFR'] / ds['sSFR_MS'])
        ds['deltaGas'] = ds['Mmol'] / ds['Mstar']
        ds['tauDepl'] = ds['Mmol'] / ds['SFR'] / 1000000000.0
        datasets.append(ds)
        print('Read "%s" (%d data)' % (ds['datatable'], len(ds['deltaGas'])))
        print('Dataset & z_range & lgMstar_range & N_data')
        for ds in datasets:
            for key in ds:
                if type(ds[key]) in [np.ma.core.MaskedArray, MaskedColumn]:
                    ds[key] = np.array(ds[key].tolist())
                if type(ds[key]) in [Column]:
                    ds[key] = ds[key].data

            ds['lgMstar'] = np.log10(ds['Mstar'])
            print('%s & %0.2f -- %0.2f & %0.2f -- %0.2f & %d \\\\' % (ds['label'], np.min(ds['z']), np.max(ds['z']), np.min(ds['lgMstar']), np.max(ds['lgMstar']), len(ds['deltaGas'])))

        return datasets


    def common_meta_info_columns():
        return [
         'label', 'color', 'facecolor', 'edgecolor', 'alpha', 'marker', 'markersize', 'datatable']


    def common_data_array_columns():
        return [
         'ID', 'z', 'SFR', 'Mstar', 'MetalZ', 'Mmol', 'sSFR', 'sSFR_MS', 'DeltaMS', 'deltaGas', 'tauDepl']


    def merge_datasets(datasets, nouplims=False, savetofile=''):
        if type(datasets) is dict:
            dataset = datasets
            return dataset
        new_dataset = {}
        new_dataset['labels'] = []
        meta_info_columns = []
        data_array_columns = []
        isfirst = True
        for i, dataset in enumerate(datasets):
            if type(dataset) is not dict:
                raise Exception('Error! Each input dataset should be a dict!')
            if nouplims == True:
                if dataset['label'].find('uplims') >= 0:
                    continue
            array_length = 0
            for t in dataset:
                if dataset[t] is None:
                    continue
                if np.isscalar(dataset[t]):
                    if isfirst:
                        meta_info_columns.append(t)
                    continue
                if isfirst:
                    data_array_columns.append(t)
                    new_dataset[t] = copy.copy(dataset[t])
                    array_length = len(dataset[t])
                elif t in data_array_columns:
                    new_dataset[t] = np.concatenate((new_dataset[t], dataset[t]))
                    array_length = len(dataset[t])
                else:
                    print('merge_datasets(): Warning! Skipping column "%s" in dataset "%s"' % (t, dataset['label']))

            if array_length > 0:
                new_dataset['labels'].extend(np.repeat(dataset['label'], array_length))
            isfirst = False

        if savetofile != '':
            if os.path.isfile(savetofile):
                shutil.move(savetofile, savetofile + '.backup')
            dump_data_table = Table(new_dataset)
            for t in dump_data_table.colnames:
                if dump_data_table[t].dtype.kind == 'O':
                    dump_data_table[t] = [str(tval) for tval in dump_data_table[t].data.tolist()]

            dump_data_table.write(savetofile, format='fits')
            print('merge_datasets(): Dumped to "%s"!' % savetofile)
        return new_dataset


    def write_datasets_to_file(datasets, output_filename):
        if os.path.isfile(output_filename):
            print('Found existing "%s"! Backing it up as "%s"!' % (output_filename, output_filename + '.backup'))
            shutil.move(output_filename, output_filename + '.backup')
            if os.path.isfile(output_filename + '.meta.txt'):
                shutil.move(output_filename + '.meta.txt', output_filename + '.meta.txt' + '.backup')
        else:
            if type(datasets) is dict:
                datasets = [
                 datasets]
            for dataset in datasets:
                if type(dataset) is not dict:
                    raise Exception('Error! Each input dataset should be a dict!')
                meta_info = {}
                data_arrays = {}
                for t in dataset:
                    if not np.isscalar(dataset[t]):
                        if len(dataset[t]) > 1:
                            data_arrays[t] = dataset[t]
                        else:
                            meta_info[t] = dataset[t]
                    else:
                        meta_info[t] = dataset[t]

            output_data_table = Table(data_arrays)
            if output_filename.endswith('fits') or output_filename.endswith('FITS'):
                output_data_table.meta = meta_info
                output_data_table.write(output_filename, format='fits')
            else:
                output_data_table.write(output_filename, format='ascii.fixed_width', delimiter='  ', bookend=True)
            with open(output_data_table, 'r') as (fp):
                fp.seek(0)
                fp.write('#')
        print('Output to "%s"!' % output_filename)
        meta_info['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss') + ' ' + time.localtime().tm_zone
        with open(output_data_table + '.meta.txt', 'w') as (fp):
            json.dump(meta_info, fp, sort_keys=True, indent=4)
        print('Output to "%s"!' % (output_filename + '.meta.txt'))


    def count_z_number():
        datasets = read_datasets()
        total_complementary_sample = 0
        low_z_complementary_sample = 0
        for dataset in datasets:
            if dataset['label'].find('A3COSMOS') >= 0:
                continue
            low_z_complementary_sample += np.count_nonzero(dataset['z'] < 0.1)
            total_complementary_sample += len(dataset['z'])

        print('total complementary sample = %d' % total_complementary_sample)
        print('z < 0.1 = %d (%0.2f%%)' % (low_z_complementary_sample, 100.0 * low_z_complementary_sample / total_complementary_sample))