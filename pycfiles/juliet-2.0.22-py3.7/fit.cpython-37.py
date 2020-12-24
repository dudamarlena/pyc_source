# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/juliet/fit.py
# Compiled at: 2020-03-20 18:06:06
# Size of source mod 2**32: 179542 bytes
import batman
try:
    import catwoman
    have_catwoman = True
except:
    have_catwoman = False

import radvel
try:
    import george
except:
    print('Warning: no george installation found. No non-celerite GPs will be able to be used')

try:
    import celerite
    from celerite import terms

    class RotationTerm(terms.Term):
        parameter_names = ('log_amp', 'log_timescale', 'log_period', 'log_factor')

        def get_real_coefficients(self, params):
            log_amp, log_timescale, log_period, log_factor = params
            f = np.exp(log_factor)
            return (
             np.exp(log_amp) * (1.0 + f) / (2.0 + f),
             np.exp(-log_timescale))

        def get_complex_coefficients(self, params):
            log_amp, log_timescale, log_period, log_factor = params
            f = np.exp(log_factor)
            return (
             np.exp(log_amp) / (2.0 + f),
             0.0,
             np.exp(-log_timescale),
             2 * np.pi * np.exp(-log_period))


except:
    print('Warning: no celerite installation found. No celerite GPs will be able to be used')

try:
    import dynesty
    from dynesty.utils import resample_equal
    force_pymultinest = False
except:
    force_pymultinest = True

try:
    import pymultinest
    force_dynesty = False
except:
    force_dynesty = True

import os, sys, numpy as np
G = 6.67408e-11
log2pi = np.log(2.0 * np.pi)
from .utils import *
__all__ = [
 'load', 'fit', 'gaussian_process', 'model']

class load(object):
    __doc__ = "\n    Given a dictionary with priors (or a filename pointing to a prior file) and data either given through arrays \n    or through files containing the data, this class loads data into a juliet object which holds all the information \n    about the dataset. Example usage:\n\n               >>> data = juliet.load(priors=priors,t_lc=times,y_lc=fluxes,yerr_lc=fluxes_errors)\n\n    Or, also,\n             \n               >>> data = juliet.load(input_folder = folder)\n\n    :param priors: (optional, dict or string)                         \n        This can be either a python ``string`` or a python ``dict``. If a ``dict``, this has to contain each of \n        the parameters to be fit, along with their respective prior distributions and hyperparameters. Each key \n        of this dictionary has to have a parameter name (e.g., ``r1_p1``, ``sigma_w_TESS``), and each of \n        those elements are, in turn, dictionaries as well containing two keys: a ``distribution``\n        key which defines the prior distribution of the parameter and a ``hyperparameters`` key, \n        which contains the hyperparameters of that distribution. \n\n        Example setup of the ``priors`` dictionary:\n            >> priors = {}\n            >> priors['r1_p1'] = {}\n            >> priors['r1_p1']['distribution'] = 'Uniform'\n            >> priors['r1_p1']['hyperparameters'] = [0.,1.]\n\n        If a ``string``, this has to contain the filename to a proper juliet prior file; the prior ``dict`` will \n        then be generated from there. A proper prior file has in the first column the name of the parameter, \n        in the second the name of the distribution, and in the third the hyperparameters of that distribution for \n        the parameter.\n \n        Note that this along with either lightcurve or RV data or a ``input_folder`` has to be given in order to properly \n        load a juliet data object.\n\n    :param input_folder: (optional, string)\n        Python ``string`` containing the path to a folder containing all the input data --- this will thus be load into a \n        juliet data object. This input folder has to contain at least a ``priors.dat`` file with the priors and either a ``lc.dat`` \n        file containing lightcurve data or a ``rvs.dat`` file containing radial-velocity data. If in this folder a ``GP_lc_regressors.dat`` \n        file or a ``GP_rv_regressors.dat`` file is found, data will be loaded into the juliet object as well.\n\n        Note that at least this or a ``priors`` string or dictionary, along with either lightcurve or RV data has to be given \n        in order to properly load a juliet data object.\n\n    :param t_lc: (optional, dictionary)\n        Dictionary whose keys are instrument names; each of those keys is expected to have arrays with the times corresponding to those instruments.\n        For example,\n                                    >>> t_lc = {}\n                                    >>> t_lc['TESS'] = np.linspace(0,100,100)\n\n        Is a valid input dictionary for ``t_lc``.\n\n    :param y_lc: (optional, dictionary)\n        Similarly to ``t_lc``, dictionary whose keys are instrument names; each of those keys is expected to have arrays with the fluxes corresponding to those instruments. \n        These are expected to be consistent with the ``t_lc`` dictionaries.\n\n    :param yerr_lc: (optional, dictionary)\n        Similarly to ``t_lc``, dictionary whose keys are instrument names; each of those keys is expected to have arrays with the errors on the fluxes corresponding to those instruments. \n        These are expected to be consistent with the ``t_lc`` dictionaries. \n\n    :param GP_regressors_lc: (optional, dictionary) \n        Dictionary whose keys are names of instruments where a GP is to be fit. On each name/element, an array of \n        regressors of shape ``(m,n)`` containing in each column the ``n`` GP regressors to be used for \n        ``m`` photometric measurements has to be given. Note that ``m`` for a given instrument has to be of the same length \n        as the corresponding ``t_lc`` for that instrument. Also, note the order of each regressor of each instrument has to match \n        the corresponding order in the ``t_lc`` array. \n        For example,\n\n                                    >>> GP_regressors_lc = {}\n                                    >>> GP_regressors_lc['TESS'] = np.linspace(-1,1,100)\n\n        If a global model wants to be used, then the instrument should be ``rv``, and each of the ``m`` rows should correspond to the ``m`` times.\n\n    :param linear_regressors_lc: (optional, dictionary)\n        Similarly as for ``GP_regressors_lc``, this is a dictionary whose keys are names of instruments where a linear regression is to be fit. \n        On each name/element, an array of shape ``(q,p)`` containing in each column the ``p`` linear regressors to be used for the ``q`` \n        photometric measurements. Again, note the order of each regressor of each instrument has to match the corresponding order in the ``t_lc`` array. \n         \n    :param GP_regressors_rv: (optional, dictionary)  \n        Same as ``GP_regressors_lc`` but for the radial-velocity data. If a global model wants to be used, then the instrument should be ``lc``, and each of the ``m`` rows should correspond to the ``m`` times.\n\n    :param linear_regressors_rv: (optional, dictionary)\n        Same as ``linear_regressors_lc``, but for the radial-velocities.\n\n    :param t_rv: (optional, dictionary)                    \n        Same as ``t_lc``, but for the radial-velocities.\n   \n    :param y_rv: (optional, dictionary)\n        Same as ``y_lc``, but for the radial-velocities.\n\n    :param yerr_rv: (optional, dictionary)\n        Same as ``yerr_lc``, but for the radial-velocities.\n\n    :param out_folder: (optional, string) \n        If a path is given, results will be saved to that path as a ``pickle`` file, along with all inputs in the standard juliet format.\n\n    :param lcfilename:  (optional, string)             \n        If a path to a lightcurve file is given, ``t_lc``, ``y_lc``, ``yerr_lc`` and ``instruments_lc`` will be read from there. The basic file format is a pure \n        ascii file where times are in the first column, relative fluxes in the second, errors in the third and instrument names in the fourth. If more columns are given for \n        a given instrument, those will be identified as linear regressors for those instruments.\n\n    :param rvfilename: (optional, string)               \n        Same as ``lcfilename``, but for the radial-velocities.\n\n    :param GPlceparamfile: (optional, string)          \n        If a path to a file is given, the columns of that file will be used as GP regressors for the lightcurve fit. The file format is a pure ascii file \n        where regressors are given in different columns, and the last column holds the instrument name. The order of this file has to be consistent with \n        ``t_lc`` and/or the ``lcfilename`` file. If a global model wants to be used, set the instrument names of all regressors to ``lc``.\n\n    :param GPrveparamfile: (optional, string)          \n        Same as ``GPlceparamfile`` but for the radial-velocities. If a global model wants to be used, set the instrument names of all regressors to ``rv``.\n\n    :param LMlceparamfile: (optional, string)          \n        If a path to a file is given, the columns of that file will be used as linear regressors for the lightcurve fit. The file format is a pure ascii file \n        where regressors are given in different columns, and the last column holds the instrument name. The order of this file has to be consistent with \n        ``t_lc`` and/or the ``lcfilename`` file. If a global model wants to be used, set the instrument names of all regressors to ``lc``.\n\n    :param LMrveparamfile: (optional, string)          \n        Same as ``LMlceparamfile`` but for the radial-velocities. If a global model wants to be used, set the instrument names of all regressors to ``rv``.\n\n    :param lctimedef: (optional, string)               \n        Time definitions for each of the lightcurve instruments. Default is to assume all instruments (in lcs and rvs) have the same time definitions. If more than one instrument is given, this string \n        should have instruments and time-definitions separated by commas, e.g., ``TESS-TDB, LCOGT-UTC``, etc.\n\n    :param rvtimedef: (optional, string)               \n        Time definitions for each of the radial-velocity instruments. Default is to assume all instruments (in lcs and rvs) have the same time definitions. If more than one instrument is given, \n        this string should have instruments and time-definitions separated by commas, e.g., ``FEROS-TDB, HARPS-UTC``, etc.\n\n    :param ld_laws: (optional, string)                 \n        Limb-darkening law to be used for each instrument. Default is ``quadratic`` for all instruments. If more than one instrument is given, \n        this string should have instruments and limb-darkening laws separated by commas, e.g., ``TESS-quadratic, LCOGT-linear``.\n\n    :param priorfile: (optional, string)                \n        If a path to a file is given, it will be assumed this is a prior file. The ``priors`` dictionary will be overwritten by the data in this \n        file. The file structure is a plain ascii file, with the name of the parameters in the first column, name of the prior distribution in the \n        second column and hyperparameters in the third column.\n\n    :param lc_instrument_supersamp: (optional, array of strings)     \n        Define for which lightcurve instruments super-sampling will be applied (e.g., in the case of long-cadence integrations). e.g., ``lc_instrument_supersamp = ['TESS','K2']``\n\n    :param lc_n_supersamp: (optional, array of ints)              \n        Define the number of datapoints to supersample. Order should be consistent with order in ``lc_instrument_supersamp``. e.g., ``lc_n_supersamp = [20,30]``.\n\n    :param lc_exptime_supersamp: (optional, array of floats)        \n        Define the exposure-time of the observations for the supersampling. Order should be consistent with order in ``lc_instrument_supersamp``. e.g., ``lc_exptime_supersamp = [0.020434,0.020434]``\n\n    :param verbose: (optional, boolean)\n        If True, all outputs of the code are printed to terminal. Default is False.\n    \n    :param matern_eps: (optional, float)\n        Epsilon parameter for the Matern approximation (see celerite documentation).\n\n    :param pickle_encoding: (optional, string)\n        Define pickle encoding in case fit was done with Python 2.7 and results are read with Python 3.\n\n    "

    def data_preparation(self, times, instruments, linear_regressors):
        """
        This function generates f useful internal arrays for this class: inames which saves the instrument names, ``global_times`` 
        which is a "flattened" array of the ``times`` dictionary where all the times for all instruments are stacked, instrument_indexes, 
        which is a dictionary that has, for each instrument the indexes of the ``global_times`` corresponding to each instrument, lm_boolean which saves booleans for each 
        instrument to indicate if there are linear regressors and lm_arguments which are the linear-regressors for each instrument.
        """
        inames = []
        for i in range(len(times)):
            if instruments[i] not in inames:
                inames.append(instruments[i])

        ninstruments = len(inames)
        instrument_indexes = {}
        for instrument in inames:
            instrument_indexes[instrument] = np.where(instruments == instrument)[0]

        lm_boolean = {}
        lm_arguments = {}
        if linear_regressors is not None:
            linear_instruments = linear_regressors.keys()
            for instrument in inames:
                if instrument in linear_instruments:
                    lm_boolean[instrument] = True
                else:
                    lm_boolean[instrument] = False

        else:
            for instrument in inames:
                lm_boolean[instrument] = False

        return (
         inames, instrument_indexes, lm_boolean)

    def convert_input_data(self, t, y, yerr):
        """
        This converts the input dictionaries to arrays (this is easier to handle internally within juliet; input dictionaries are just asked because 
        it is easier for the user to pass them). 
        """
        instruments = list(t.keys())
        all_times = np.array([])
        all_y = np.array([])
        all_yerr = np.array([])
        all_instruments = np.array([])
        for instrument in instruments:
            for i in range(len(t[instrument])):
                all_times = np.append(all_times, t[instrument][i])
                all_y = np.append(all_y, y[instrument][i])
                all_yerr = np.append(all_yerr, yerr[instrument][i])
                all_instruments = np.append(all_instruments, instrument)

        return (
         all_times, all_y, all_yerr, all_instruments)

    def convert_to_dictionary(self, t, y, yerr, instrument_indexes):
        """
        Convert data given in arrays to dictionaries for easier user usage
        """
        times = {}
        data = {}
        errors = {}
        for instrument in instrument_indexes.keys():
            times[instrument] = t[instrument_indexes[instrument]]
            data[instrument] = y[instrument_indexes[instrument]]
            errors[instrument] = yerr[instrument_indexes[instrument]]

        return (
         times, data, errors)

    def save_regressors(self, fname, GP_arguments):
        """
        This function saves the GP regressors to fname.
        """
        fout = open(fname, 'w')
        for GP_instrument in GP_arguments.keys():
            GP_regressors = GP_arguments[GP_instrument]
            multi_dimensional = False
            if len(GP_regressors.shape) == 2:
                multi_dimensional = True
            if multi_dimensional:
                for i in range(GP_regressors.shape[0]):
                    for j in range(GP_regressors.shape[1]):
                        fout.write('{0:.10f} '.format(GP_regressors[(i, j)]))

                    fout.write('{0:}\n'.format(GP_instrument))

            else:
                for i in range(GP_regressors.shape[0]):
                    fout.write('{0:.10f} {1:}\n'.format(GP_regressors[i], GP_instrument))

        fout.close()

    def save_data(self, fname, t, y, yerr, instruments, lm_boolean, lm_arguments):
        """
        This function saves t,y,yerr,instruments,lm_boolean and lm_arguments data to fname.
        """
        fout = open(fname, 'w')
        lm_counters = {}
        for i in range(len(t)):
            fout.write('{0:.10f} {1:.10f} {2:.10f} {3:}'.format(t[i], y[i], yerr[i], instruments[i]))
            if lm_boolean[instruments[i]]:
                if instruments[i] not in lm_counters.keys():
                    lm_counters[instruments[i]] = 0
                for j in range(lm_arguments[instruments[i]].shape[1]):
                    fout.write(' {0:.10f}'.format(lm_arguments[instruments[i]][lm_counters[instruments[i]]][j]))

                lm_counters[instruments[i]] += 1
            fout.write('\n')

        fout.close()

    def save_priorfile(self, fname):
        """
        This function saves a priorfile file out to fname
        """
        fout = open(fname, 'w')
        for pname in self.priors.keys():
            if self.priors[pname]['distribution'].lower() != 'fixed':
                value = ','.join(np.array(self.priors[pname]['hyperparameters']).astype(str))
            else:
                value = str(self.priors[pname]['hyperparameters'])
            fout.write('{0: <20} {1: <20} {2: <20}\n'.format(pname, self.priors[pname]['distribution'], value))

        fout.close()

    def check_global(self, name):
        for pname in self.priors.keys():
            if name in pname.split('_')[1:]:
                return True

        return False

    def append_GP(self, ndata, instrument_indexes, GP_arguments, inames):
        """
            This function appends all the GP regressors into one --- useful for the global models.
        """
        if len(GP_arguments[inames[0]].shape) == 2:
            nregressors = GP_arguments[inames[0]].shape[1]
            multidimensional = True
            out = np.zeros([ndata, nregressors])
        else:
            multidimensional = False
            out = np.zeros(ndata)
        for instrument in inames:
            if multidimensional:
                out[instrument_indexes[instrument], :] = GP_arguments[instrument]
            else:
                out[instrument_indexes[instrument]] = GP_arguments[instrument]

        return out

    def sort_GP(self, dictype):
        if dictype == 'lc':
            idx_sort = np.argsort(self.GP_lc_arguments['lc'][:, 0])
            self.t_lc = self.t_lc[idx_sort]
            self.y_lc = self.y_lc[idx_sort]
            self.yerr_lc = self.yerr_lc[idx_sort]
            self.GP_lc_arguments['lc'][:, 0] = self.GP_lc_arguments['lc'][(idx_sort, 0)]
            for instrument in self.inames_lc:
                new_instrument_indexes = np.zeros(len(self.instrument_indexes_lc[instrument]))
                instrument_indexes = self.instrument_indexes_lc[instrument]
                counter = 0
                for i in instrument_indexes:
                    new_instrument_indexes[counter] = np.where(i == idx_sort)[0][0]
                    counter += 1

                self.instrument_indexes_lc[instrument] = new_instrument_indexes.astype('int')

        else:
            if dictype == 'rv':
                idx_sort = np.argsort(self.GP_rv_arguments['rv'][:, 0])
                self.t_rv = self.t_rv[idx_sort]
                self.y_rv = self.y_rv[idx_sort]
                self.yerr_rv = self.yerr_rv[idx_sort]
                self.GP_rv_arguments['rv'][:, 0] = self.GP_rv_arguments['rv'][(idx_sort, 0)]
                for instrument in self.inames_rv:
                    new_instrument_indexes = np.zeros(len(self.instrument_indexes_rv[instrument]))
                    instrument_indexes = self.instrument_indexes_rv[instrument]
                    counter = 0
                    for i in instrument_indexes:
                        new_instrument_indexes[counter] = np.where(i == idx_sort)[0][0]
                        counter += 1

                    self.instrument_indexes_rv[instrument] = new_instrument_indexes.astype('int')

    def generate_datadict(self, dictype):
        """
        This generates the options dictionary for lightcurves, RVs, and everything else you want to fit. Useful for the 
        fit, as it separaters options per instrument.

        :param dictype: (string)
            Defines the type of dictionary type. It can either be 'lc' (for the lightcurve dictionary) or 'rv' (for the 
            radial-velocity one). 
        """
        dictionary = {}
        if dictype == 'lc':
            inames = self.inames_lc
            ninstruments = self.ninstruments_lc
            instrument_supersamp = self.lc_instrument_supersamp
            n_supersamp = self.lc_n_supersamp
            exptime_supersamp = self.lc_exptime_supersamp
            numbering_planets = self.numbering_transiting_planets
            self.global_lc_model = self.check_global('lc')
            global_model = self.global_lc_model
            GP_regressors = self.GP_lc_arguments
        else:
            if dictype == 'rv':
                inames = self.inames_rv
                ninstruments = self.ninstruments_rv
                instrument_supersamp = None
                n_supersamp = None
                exptime_supersamp = None
                numbering_planets = self.numbering_rv_planets
                self.global_rv_model = self.check_global('rv')
                global_model = self.global_rv_model
                GP_regressors = self.GP_rv_arguments
            else:
                raise Exception('INPUT ERROR: dictype not understood. Has to be either lc or rv.')
        for i in range(ninstruments):
            instrument = inames[i]
            dictionary[instrument] = {}
            dictionary[instrument]['resampling'] = False
            dictionary[instrument]['GPDetrend'] = False
            if dictype == 'lc':
                dictionary[instrument]['TransitFit'] = False
                dictionary[instrument]['TransitFitCatwoman'] = False

        if dictype == 'lc':
            all_ld_laws = self.ld_laws.split(',')
            if len(all_ld_laws) == 1:
                for i in range(ninstruments):
                    instrument = inames[i]
                    q1_given = False
                    q2_given = False
                    for parameter in self.priors.keys():
                        if parameter[0:2] == 'q1':
                            if instrument in parameter.split('_')[1:]:
                                q1_given = True
                            if parameter[0:2] == 'q2' and instrument in parameter.split('_')[1:]:
                                q2_given = True

                    if q1_given:
                        if not q2_given:
                            dictionary[instrument]['ldlaw'] = 'linear'
                    if q1_given:
                        if q2_given:
                            dictionary[instrument]['ldlaw'] = all_ld_laws[0].split('-')[(-1)].split()[0].lower()
                    if q1_given or q2_given:
                        raise Exception('INPUT ERROR: it appears q1 for instrument ' + instrument + ' was not defined (but q2 was) in the prior file.')

            else:
                for ld_law in all_ld_laws:
                    instrument, ld = ld_law.split('-')
                    dictionary[instrument.split()[0]]['ldlaw'] = ld.split()[0].lower()

        elif instrument_supersamp is not None:
            if dictype == 'lc':
                for i in range(len(instrument_supersamp)):
                    if self.verbose:
                        print('\t Resampling detected for instrument ', instrument_supersamp[i])
                    dictionary[instrument_supersamp[i]]['resampling'] = True
                    dictionary[instrument_supersamp[i]]['nresampling'] = n_supersamp[i]
                    dictionary[instrument_supersamp[i]]['exptimeresampling'] = exptime_supersamp[i]

            else:
                cp_pnumber = np.array([])
                cp_period = np.array([])
                for pri in self.priors.keys():
                    if pri[0:2] == 'P_':
                        if self.priors[pri]['distribution'].lower() in ('normal', 'truncated normal'):
                            cp_pnumber = np.append(cp_pnumber, int(pri.split('_')[(-1)][1:]))
                            cp_period = np.append(cp_period, self.priors[pri]['hyperparameters'][0])
                        elif self.priors[pri]['distribution'].lower() == 'fixed':
                            cp_pnumber = np.append(cp_pnumber, int(pri.split('_')[(-1)][1:]))
                            cp_period = np.append(cp_period, self.priors[pri]['hyperparameters'])

                if len(cp_period) > 1:
                    idx = np.argsort(cp_pnumber)
                    cP = cp_period[idx[0]]
                    cP_idx = cp_pnumber[idx[0]]
                    for cidx in idx[1:]:
                        P = cp_period[cidx]
                        if P > cP:
                            cP = P
                            cP_idx = cp_pnumber[cidx]
                        else:
                            print('\n')
                            raise Exception('INPUT ERROR: planetary periods in the priors are not ordered in chronological order. ' + 'Planet p{0:} has a period of {1:} days, while planet p{2:} has a period of {3:} days (P_p{0:}<P_p{2:}).'.format(int(cp_pnumber[cidx]), P, int(cP_idx), cP))

                if dictype == 'lc':
                    for i in range(ninstruments):
                        dictionary[inames[i]]['TTVs'] = {}
                        for pi in numbering_planets:
                            dictionary[inames[i]]['TTVs'][pi] = {}
                            dictionary[inames[i]]['TTVs'][pi]['status'] = False
                            dictionary[inames[i]]['TTVs'][pi]['parametrization'] = 'dt'
                            dictionary[inames[i]]['TTVs'][pi]['transit_number'] = []

                        for pri in self.priors.keys():
                            if pri[0:2] == 'q1':
                                if inames[i] in pri.split('_'):
                                    dictionary[inames[i]]['TransitFit'] = True
                                    if self.verbose:
                                        print('\t Transit fit detected for instrument ', inames[i])
                                    if pri[0:3] == 'phi':
                                        dictionary[inames[i]]['TransitFit'] = True
                                        dictionary[inames[i]]['TransitFitCatwoman'] = True
                                        if self.verbose:
                                            print('\t Transit (catwoman) fit detected for instrument ', inames[i])
                                    if pri[0:2] == 'dt' or pri[0:2] == 'T_':
                                        pass
                                    if pri[0:2] == 'T_':
                                        dictionary[inames[i]]['TTVs'][pi]['parametrization'] = 'T'
                                planet_number, instrument, ntransit = pri.split('_')[1:]
                                if inames[i] == instrument:
                                    dictionary[inames[i]]['TTVs'][int(planet_number[1:])]['status'] = True
                                    dictionary[inames[i]]['TTVs'][int(planet_number[1:])]['transit_number'].append(int(ntransit))

                    for pi in numbering_planets:
                        for i in range(ninstruments):
                            if dictionary[inames[i]]['TTVs'][pi]['status']:
                                dictionary[inames[i]]['TTVs'][pi]['totalTTVtransits'] = len(dictionary[inames[i]]['TTVs'][pi]['transit_number'])

                if global_model:
                    dictionary['global_model'] = {}
                    if GP_regressors is not None:
                        dictionary['global_model']['GPDetrend'] = True
                        dictionary['global_model']['noise_model'] = gaussian_process(self, model_type=dictype, instrument=dictype, matern_eps=(self.matern_eps))
                        if (dictionary['global_model']['noise_model'].isInit or dictype) == 'lc':
                            self.sort_GP('lc')
                        else:
                            if dictype == 'rv':
                                self.sort_GP('rv')
                        dictionary['global_model']['noise_model'] = gaussian_process(self, model_type=dictype, instrument=dictype, matern_eps=(self.matern_eps))
                        if not dictionary['global_model']['noise_model'].isInit:
                            raise Exception('INPUT ERROR: GP initialization for object for ' + dictype + ' global kernel failed.')
                else:
                    dictionary['global_model']['GPDetrend'] = False
        else:
            for i in range(ninstruments):
                instrument = inames[i]
                if GP_regressors is not None and instrument in GP_regressors.keys():
                    dictionary[instrument]['GPDetrend'] = True
                    dictionary[instrument]['noise_model'] = gaussian_process(self, model_type=dictype, instrument=instrument, matern_eps=(self.matern_eps))
                    assert dictionary[instrument]['noise_model'].isInit, 'INPUT ERROR: GP regressors for instrument ' + instrument + ' use celerite, and are not in ascending or descending order. Please, give the input in those orders --- it will not work othersie.'

        dictionary['ecc_parametrization'] = {}
        if dictype == 'lc':
            dictionary['efficient_bp'] = {}
        else:
            for i in numbering_planets:
                if 'ecosomega_p' + str(i) in self.priors.keys():
                    dictionary['ecc_parametrization'][i] = 1
                    if self.verbose:
                        print('\t >> ecosomega,esinomega parametrization detected for ' + dictype + ' planet p' + str(i))
                    else:
                        if 'secosomega_p' + str(i) in self.priors.keys():
                            dictionary['ecc_parametrization'][i] = 2
                            if self.verbose:
                                print('\t >> sqrt(e)cosomega, sqrt(e)sinomega parametrization detected for ' + dictype + ' planet p' + str(i))
                        else:
                            dictionary['ecc_parametrization'][i] = 0
                            if self.verbose:
                                print('\t >> ecc,omega parametrization detected for ' + dictype + ' planet p' + str(i))
                        if dictype == 'lc':
                            if 'r1_p' + str(i) in self.priors.keys():
                                dictionary['efficient_bp'][i] = True
                                if self.verbose:
                                    print('\t >> (b,p) parametrization detected for ' + dictype + ' planet p' + str(i))
                            else:
                                dictionary['efficient_bp'][i] = False

            if dictype == 'lc':
                dictionary['fitrho'] = False
                if 'rho' in self.priors.keys():
                    dictionary['fitrho'] = True
                if dictype == 'rv':
                    dictionary['fitrvline'] = False
                    dictionary['fitrvquad'] = False
                    if 'rv_slope' in self.priors.keys():
                        if 'rv_quad' in self.priors.keys():
                            dictionary['fitrvquad'] = True
                            if self.verbose:
                                print('\t Fitting quadratic trend to RVs.')
            else:
                dictionary['fitrvline'] = True
            if self.verbose:
                print('\t Fitting linear trend to RVs.')
            elif dictype == 'lc':
                self.lc_options = dictionary
            else:
                if dictype == 'rv':
                    self.rv_options = dictionary
                else:
                    raise Exception('INPUT ERROR: dictype not understood. Has to be either lc or rv.')

    def set_lc_data(self, t_lc, y_lc, yerr_lc, instruments_lc, instrument_indexes_lc, ninstruments_lc, inames_lc, lm_lc_boolean, lm_lc_arguments):
        self.t_lc = t_lc.astype('float64')
        self.y_lc = y_lc
        self.yerr_lc = yerr_lc
        self.inames_lc = inames_lc
        self.instruments_lc = instruments_lc
        self.ninstruments_lc = ninstruments_lc
        self.instrument_indexes_lc = instrument_indexes_lc
        self.lm_lc_boolean = lm_lc_boolean
        self.lm_lc_arguments = lm_lc_arguments
        self.lc_data = True

    def set_rv_data(self, t_rv, y_rv, yerr_rv, instruments_rv, instrument_indexes_rv, ninstruments_rv, inames_rv, lm_rv_boolean, lm_rv_arguments):
        self.t_rv = t_rv.astype('float64')
        self.y_rv = y_rv
        self.yerr_rv = yerr_rv
        self.inames_rv = inames_rv
        self.instruments_rv = instruments_rv
        self.ninstruments_rv = ninstruments_rv
        self.instrument_indexes_rv = instrument_indexes_rv
        self.lm_rv_boolean = lm_rv_boolean
        self.lm_rv_arguments = lm_rv_arguments
        self.rv_data = True

    def save(self):
        if self.out_folder[(-1)] != '/':
            self.out_folder = self.out_folder + '/'
        else:
            if not os.path.exists(self.out_folder):
                os.makedirs(self.out_folder)
            elif (os.path.exists(self.out_folder + 'lc.dat') or self.lcfilename) is not None:
                os.system('cp ' + self.lcfilename + ' ' + self.out_folder + 'lc.dat')
            else:
                if self.t_lc is not None:
                    self.save_data(self.out_folder + 'lc.dat', self.t_lc, self.y_lc, self.yerr_lc, self.instruments_lc, self.lm_lc_boolean, self.lm_lc_arguments)
                else:
                    if (os.path.exists(self.out_folder + 'rvs.dat') or self.rvfilename) is not None:
                        os.system('cp ' + self.rvfilename + ' ' + self.out_folder + 'rvs.dat')
                    else:
                        if self.t_rv is not None:
                            self.save_data(self.out_folder + 'rvs.dat', self.t_rv, self.y_rv, self.yerr_rv, self.instruments_rv, self.lm_rv_boolean, self.lm_rv_arguments)
                    if (os.path.exists(self.out_folder + 'GP_lc_regressors.dat') or self.GPlceparamfile) is not None:
                        os.system('cp ' + self.GPlceparamfile + ' ' + self.out_folder + 'GP_lc_regressors.dat')
                    else:
                        if self.GP_lc_arguments is not None:
                            self.save_regressors(self.out_folder + 'GP_lc_regressors.dat', self.GP_lc_arguments)
                    if (os.path.exists(self.out_folder + 'GP_rv_regressors.dat') or self.GPrveparamfile) is not None:
                        os.system('cp ' + self.GPrveparamfile + ' ' + self.out_folder + 'GP_rv_regressors.dat')
                    else:
                        if self.GP_rv_arguments is not None:
                            self.save_regressors(self.out_folder + 'GP_rv_regressors.dat', self.GP_rv_arguments)
                    if (os.path.exists(self.out_folder + 'LM_lc_regressors.dat') or self.LMlceparamfile) is not None:
                        os.system('cp ' + self.LMlceparamfile + ' ' + self.out_folder + 'LM_lc_regressors.dat')
                    else:
                        if self.LM_lc_arguments is not None:
                            self.save_regressors(self.out_folder + 'LM_lc_regressors.dat', self.LM_lc_arguments)
            if (os.path.exists(self.out_folder + 'LM_rv_regressors.dat') or self.LMrveparamfile) is not None:
                os.system('cp ' + self.LMrveparamfile + ' ' + self.out_folder + 'LM_rv_regressors.dat')
            else:
                if self.LM_rv_arguments is not None:
                    self.save_regressors(self.out_folder + 'LM_rv_regressors.dat', self.LM_rv_arguments)
                self.prior_fname = os.path.exists(self.out_folder + 'priors.dat') or self.out_folder + 'priors.dat'
                self.save_priorfile(self.out_folder + 'priors.dat')

    def fit(self, use_dynesty=False, dynamic=False, dynesty_bound='multi', dynesty_sample='rwalk', dynesty_nthreads=None, n_live_points=1000, ecclim=1.0, delta_z_lim=0.5, pl=0.0, pu=1.0):
        """
        Perhaps the most important function of the juliet data object. This function fits your data using the nested 
        sampler of choice. This returns a results object which contains all the posteriors information.
        """
        return fit(self, use_dynesty=use_dynesty, dynamic=dynamic, dynesty_bound=dynesty_bound, dynesty_sample=dynesty_sample, dynesty_nthreads=dynesty_nthreads,
          n_live_points=n_live_points,
          ecclim=ecclim,
          delta_z_lim=delta_z_lim,
          pl=pl,
          pu=pu)

    def __init__(self, priors=None, input_folder=None, t_lc=None, y_lc=None, yerr_lc=None, t_rv=None, y_rv=None, yerr_rv=None, GP_regressors_lc=None, linear_regressors_lc=None, GP_regressors_rv=None, linear_regressors_rv=None, out_folder=None, lcfilename=None, rvfilename=None, GPlceparamfile=None, GPrveparamfile=None, LMlceparamfile=None, LMrveparamfile=None, lctimedef='TDB', rvtimedef='UTC', ld_laws='quadratic', priorfile=None, lc_n_supersamp=None, lc_exptime_supersamp=None, lc_instrument_supersamp=None, mag_to_flux=True, verbose=False, matern_eps=0.01, pickle_encoding=None):
        self.lcfilename = lcfilename
        self.rvfilename = rvfilename
        self.GPlceparamfile = GPlceparamfile
        self.GPrveparamfile = GPrveparamfile
        self.LMlceparamfile = LMlceparamfile
        self.LMrveparamfile = LMrveparamfile
        self.verbose = verbose
        self.pickle_encoding = pickle_encoding
        self.matern_eps = matern_eps
        self.t_lc = None
        self.y_lc = None
        self.yerr_lc = None
        self.instruments_lc = None
        self.ninstruments_lc = None
        self.inames_lc = None
        self.instrument_indexes_lc = None
        self.lm_lc_boolean = None
        self.lm_lc_arguments = None
        self.GP_lc_arguments = None
        self.LM_lc_arguments = None
        self.lctimedef = lctimedef
        self.ld_laws = ld_laws
        self.lc_n_supersamp = lc_n_supersamp
        self.lc_exptime_supersamp = lc_exptime_supersamp
        self.lc_instrument_supersamp = lc_instrument_supersamp
        self.lc_data = False
        self.global_lc_model = False
        self.lc_options = {}
        self.t_rv = None
        self.y_rv = None
        self.yerr_rv = None
        self.instruments_rv = None
        self.ninstruments_rv = None
        self.inames_rv = None
        self.instrument_indexes_rv = None
        self.lm_rv_boolean = None
        self.lm_rv_arguments = None
        self.GP_rv_arguments = None
        self.LM_rv_arguments = None
        self.rvtimedef = rvtimedef
        self.rv_data = False
        self.global_rv_model = False
        self.rv_options = {}
        self.out_folder = None
        if input_folder is not None:
            if input_folder[(-1)] != '/':
                self.input_folder = input_folder + '/'
            else:
                self.input_folder = input_folder
            if os.path.exists(self.input_folder + 'lc.dat'):
                lcfilename = self.input_folder + 'lc.dat'
            if os.path.exists(self.input_folder + 'rvs.dat'):
                rvfilename = self.input_folder + 'rvs.dat'
        elif not os.path.exists(self.input_folder + 'lc.dat'):
            if not os.path.exists(self.input_folder + 'rvs.dat'):
                raise Exception('INPUT ERROR: No lightcurve data file (lc.dat) or radial-velocity data file (rvs.dat) found in folder ' + self.input_folder + '. \n Create them and try again. For details, check juliet.load?')
            elif os.path.exists(self.input_folder + 'GP_lc_regressors.dat'):
                GPlceparamfile = self.input_folder + 'GP_lc_regressors.dat'
            else:
                if os.path.exists(self.input_folder + 'GP_rv_regressors.dat'):
                    GPrveparamfile = self.input_folder + 'GP_rv_regressors.dat'
                else:
                    if os.path.exists(self.input_folder + 'LM_lc_regressors.dat'):
                        LMlceparamfile = self.input_folder + 'LM_lc_regressors.dat'
                    if os.path.exists(self.input_folder + 'LM_rv_regressors.dat'):
                        LMrveparamfile = self.input_folder + 'LM_rv_regressors.dat'
                    if os.path.exists(self.input_folder + 'priors.dat'):
                        priors = self.input_folder + 'priors.dat'
                    else:
                        raise Exception('INPUT ERROR: Prior file (priors.dat) not found in folder ' + self.input_folder + '.' + 'Create it and try again. For details, check juliet.load?')
                if out_folder is None:
                    self.out_folder = self.input_folder
                else:
                    self.input_folder = None
            if type(priors) == str:
                self.prior_fname = priors
                priors, n_transit, n_rv, numbering_transit, numbering_rv, n_params = readpriors(priors)
                self.priors = priors
                self.n_transiting_planets = n_transit
                self.n_rv_planets = n_rv
                self.numbering_transiting_planets = numbering_transit
                self.numbering_rv_planets = numbering_rv
                self.nparams = n_params
        elif type(priors) == dict:
            self.priors = priors
            n_transit, n_rv, numbering_transit, numbering_rv, n_params = readpriors(priors)
            self.n_transiting_planets = n_transit
            self.n_rv_planets = n_rv
            self.numbering_transiting_planets = numbering_transit
            self.numbering_rv_planets = numbering_rv
            self.nparams = n_params
            self.prior_fname = None
        else:
            raise Exception('INPUT ERROR: Prior file is not a string or a dictionary (and it has to). Do juliet.load? for details.')
        if t_lc is None:
            if lcfilename is not None:
                t_lc, y_lc, yerr_lc, instruments_lc, instrument_indexes_lc, ninstruments_lc, inames_lc, lm_lc_boolean, lm_lc_arguments = read_data(lcfilename)
                self.set_lc_data(t_lc, y_lc, yerr_lc, instruments_lc, instrument_indexes_lc, ninstruments_lc, inames_lc, lm_lc_boolean, lm_lc_arguments)
        if t_rv is None:
            if rvfilename is not None:
                t_rv, y_rv, yerr_rv, instruments_rv, instrument_indexes_rv, ninstruments_rv, inames_rv, lm_rv_boolean, lm_rv_arguments = read_data(rvfilename)
                self.set_rv_data(t_rv, y_rv, yerr_rv, instruments_rv, instrument_indexes_rv, ninstruments_rv, inames_rv, lm_rv_boolean, lm_rv_arguments)
        if t_lc is None and t_rv is None and lcfilename is None:
            if rvfilename is None:
                raise Exception('INPUT ERROR: No complete dataset (photometric or radial-velocity) given.\n Make sure to feed times (t_lc and/or t_rv), values (y_lc and/or y_rv), \n errors (yerr_lc and/or yerr_rv).')
            if GPlceparamfile is not None:
                self.GP_lc_arguments, self.global_lc_model = readGPeparams(GPlceparamfile)
        elif GP_regressors_lc is not None:
            self.GP_lc_arguments = GP_regressors_lc
            instruments = set(list(self.GP_lc_arguments.keys()))
        if GPrveparamfile is not None:
            self.GP_rv_arguments, self.global_rv_model = readGPeparams(GPrveparamfile)
        else:
            if GP_regressors_rv is not None:
                self.GP_rv_arguments = GP_regressors_rv
                instruments = set(list(self.GP_rv_arguments.keys()))
            else:
                if LMlceparamfile is not None:
                    LM_lc_arguments, dummy_var = readGPeparams(LMlceparamfile)
                    for lmi in list(LM_lc_arguments.keys()):
                        lm_lc_boolean[lmi] = True
                        lm_lc_arguments[lmi] = LM_lc_arguments[lmi]

                if LMrveparamfile is not None:
                    LM_rv_arguments, dummy_var = readGPeparams(LMrveparamfile)
                    for lmi in list(LM_rv_arguments.keys()):
                        lm_rv_boolean[lmi] = True
                        lm_rv_arguments[lmi] = LM_rv_arguments[lmi]

                if lcfilename is None and t_lc is not None:
                    input_error_catcher(t_lc, y_lc, yerr_lc, 'lightcurve')
                    for instrument in t_lc.keys():
                        t_lc[instrument] = t_lc[instrument].astype('float64')

                    tglobal_lc, yglobal_lc, yglobalerr_lc, instruments_lc = self.convert_input_data(t_lc, y_lc, yerr_lc)
                    inames_lc, instrument_indexes_lc, lm_lc_boolean = self.data_preparation(tglobal_lc, instruments_lc, linear_regressors_lc)
                    lm_lc_arguments = linear_regressors_lc
                    ninstruments_lc = len(inames_lc)
                    self.set_lc_data(tglobal_lc, yglobal_lc, yglobalerr_lc, instruments_lc, instrument_indexes_lc, ninstruments_lc, inames_lc, lm_lc_boolean, lm_lc_arguments)
                    self.times_lc = t_lc
                    self.data_lc = y_lc
                    self.errors_lc = yerr_lc
                else:
                    if t_lc is not None:
                        times_lc, data_lc, errors_lc = self.convert_to_dictionary(t_lc, y_lc, yerr_lc, instrument_indexes_lc)
                        self.times_lc = times_lc
                        self.data_lc = data_lc
                        self.errors_lc = errors_lc
        if rvfilename is None and t_rv is not None:
            input_error_catcher(t_rv, y_rv, yerr_rv, 'radial-velocity')
            tglobal_rv, yglobal_rv, yglobalerr_rv, instruments_rv = self.convert_input_data(t_rv, y_rv, yerr_rv)
            inames_rv, instrument_indexes_rv, lm_rv_boolean = self.data_preparation(tglobal_rv, instruments_rv, linear_regressors_rv)
            lm_rv_arguments = linear_regressors_rv
            ninstruments_rv = len(inames_rv)
            self.set_rv_data(tglobal_rv, yglobal_rv, yglobalerr_rv, instruments_rv, instrument_indexes_rv, ninstruments_rv, inames_rv, lm_rv_boolean, lm_rv_arguments)
            self.times_rv = t_rv
            self.data_rv = y_rv
            self.errors_rv = yerr_rv
        else:
            if t_rv is not None:
                times_rv, data_rv, errors_rv = self.convert_to_dictionary(t_rv, y_rv, yerr_rv, instrument_indexes_rv)
                self.times_rv = times_rv
                self.data_rv = data_rv
                self.errors_rv = errors_rv
            if out_folder is not None:
                self.out_folder = out_folder
                self.save()
            if t_lc is not None:
                self.generate_datadict('lc')
            if t_rv is not None:
                self.generate_datadict('rv')


class fit(object):
    __doc__ = '\n    Given a juliet data object, this class performs a fit to the data and returns a results object to explore the \n    results. Example usage:\n\n               >>> results = juliet.fit(data)\n\n    :params data: (juliet object)\n        An object containing all the information regarding the data to be fitted, including options of the fit. \n        Generated via juliet.load().\n\n    :param use_dynesty: (optional, boolean)              \n        If ``True``, use dynesty instead of `MultiNest` for posterior sampling and evidence evaluation. Default is \n        ``False``, unless `MultiNest` via ``pymultinest`` is not working on the system.\n \n    :param dynamic: (optional, boolean)                 \n        If ``True``, use dynamic Nested Sampling with dynesty. Default is ``False``.\n \n    :param dynesty_bound: (optional, string)           \n        Define the dynesty bound method to use (currently either ``single`` or ``multi``, to use either single ellipsoids or multiple \n        ellipsoids). Default is ``multi`` (for details, see the `dynesty API <https://dynesty.readthedocs.io/en/latest/api.html>`_).\n\n    :param dynesty_sample: (optional, string)         \n        Define the sampling method for dynesty to use. Default is ``rwalk``. Accorfing to the `dynesty API <https://dynesty.readthedocs.io/en/latest/api.html>`_, \n        this should be changed depending on the number of parameters being fitted. If smaller than about 20, ``rwalk`` is optimal. For larger dimensions, \n        ``slice`` or ``rslice`` should be used.\n\n    :param dynesty_nthreads: (optional, int)        \n        Define the number of threads to use within dynesty. Default is to use just 1.\n\n    :param n_live_points: (optional, int)            \n        Number of live-points to be sampled. Default is ``500``.\n\n    :param ecclim: (optional, float)                   \n        Upper limit on the maximum eccentricity to sample. Default is ``1``.\n\n    :param delta_z_lim: (optional, double)\n        Define the convergence delta_z limit for the nested samplers. Default is 0.5.\n\n    :param pl: (optional, float)                      \n        If the ``(r1,r2)`` parametrization for ``(b,p)`` is used, this defines the lower limit of the planet-to-star radius ratio to be sampled. \n        Default is ``0``.\n\n    :param pu: (optional, float)                    \n        Same as ``pl``, but for the upper limit. Default is ``1``.\n\n    :param ta: (optional, float)\n        Time to be substracted to the input times in order to generate the linear and/or quadratic trend to be added to the model. \n        Default is 2458460.\n    '

    def set_prior_transform(self):
        for pname in self.model_parameters:
            if self.data.priors[pname]['distribution'] != 'fixed':
                if self.data.priors[pname]['distribution'] == 'uniform':
                    self.transform_prior[pname] = transform_uniform
                if self.data.priors[pname]['distribution'] == 'normal':
                    self.transform_prior[pname] = transform_normal
                if self.data.priors[pname]['distribution'] == 'truncatednormal':
                    self.transform_prior[pname] = transform_truncated_normal
                if self.data.priors[pname]['distribution'] == 'jeffreys' or self.data.priors[pname]['distribution'] == 'loguniform':
                    self.transform_prior[pname] = transform_loguniform
                if self.data.priors[pname]['distribution'] == 'beta':
                    self.transform_prior[pname] = transform_beta
                if self.data.priors[pname]['distribution'] == 'exponential':
                    self.transform_prior[pname] = exponential

    def prior(self, cube, ndim=None, nparams=None):
        pcounter = 0
        for pname in self.model_parameters:
            if self.data.priors[pname]['distribution'] != 'fixed':
                if self.use_dynesty:
                    self.transformed_priors[pcounter] = self.transform_prior[pname](cube[pcounter], self.data.priors[pname]['hyperparameters'])
                else:
                    cube[pcounter] = self.transform_prior[pname](cube[pcounter], self.data.priors[pname]['hyperparameters'])
                pcounter += 1

        if self.use_dynesty:
            return self.transformed_priors

    def loglike(self, cube, ndim=None, nparams=None):
        pcounter = 0
        for pname in self.model_parameters:
            if self.data.priors[pname]['distribution'] != 'fixed':
                self.posteriors[pname] = cube[pcounter]
                pcounter += 1

        log_likelihood = 0.0
        if self.data.t_lc is not None:
            self.lc.generate(self.posteriors)
            if self.lc.modelOK:
                log_likelihood += self.lc.get_log_likelihood(self.posteriors)
            else:
                return -1e+101
        if self.data.t_rv is not None:
            self.rv.generate(self.posteriors)
            if self.rv.modelOK:
                log_likelihood += self.rv.get_log_likelihood(self.posteriors)
            else:
                return -1e+101
        return log_likelihood

    def __init__--- This code section failed: ---

 L.1069         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               results

 L.1071         6  LOAD_FAST                'use_dynesty'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               use_dynesty

 L.1072        12  LOAD_FAST                'dynamic'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               dynamic

 L.1073        18  LOAD_FAST                'dynesty_bound'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               dynesty_bound

 L.1074        24  LOAD_FAST                'dynesty_sample'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               dynesty_sample

 L.1075        30  LOAD_FAST                'dynesty_nthreads'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               dynesty_nthreads

 L.1076        36  LOAD_FAST                'n_live_points'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               n_live_points

 L.1077        42  LOAD_FAST                'ecclim'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               ecclim

 L.1078        48  LOAD_FAST                'delta_z_lim'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               delta_z_lim

 L.1079        54  LOAD_FAST                'pl'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               pl

 L.1080        60  LOAD_FAST                'pu'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               pu

 L.1081        66  LOAD_FAST                'ta'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               ta

 L.1083        72  LOAD_FAST                'data'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               data

 L.1091        78  LOAD_FAST                'data'
               80  LOAD_ATTR                out_folder
               82  LOAD_FAST                'self'
               84  STORE_ATTR               out_folder

 L.1092        86  LOAD_GLOBAL              np
               88  LOAD_METHOD              zeros
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                data
               94  LOAD_ATTR                nparams
               96  CALL_METHOD_1         1  '1 positional argument'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               transformed_priors

 L.1095       102  LOAD_FAST                'self'
              104  LOAD_ATTR                use_dynesty
              106  POP_JUMP_IF_FALSE   130  'to 130'

 L.1096       108  LOAD_FAST                'self'
              110  LOAD_ATTR                dynamic
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L.1097       114  LOAD_STR                 'dynamic_dynesty_'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               sampler_prefix
              120  JUMP_ABSOLUTE       136  'to 136'
            122_0  COME_FROM           112  '112'

 L.1099       122  LOAD_STR                 'dynesty_'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               sampler_prefix
              128  JUMP_FORWARD        136  'to 136'
            130_0  COME_FROM           106  '106'

 L.1101       130  LOAD_STR                 'multinest_'
              132  LOAD_FAST                'self'
              134  STORE_ATTR               sampler_prefix
            136_0  COME_FROM           128  '128'

 L.1104       136  BUILD_MAP_0           0 
              138  LOAD_FAST                'self'
              140  STORE_ATTR               posteriors

 L.1105       142  LOAD_GLOBAL              list
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                data
              148  LOAD_ATTR                priors
              150  LOAD_METHOD              keys
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  LOAD_FAST                'self'
              158  STORE_ATTR               model_parameters

 L.1106       160  SETUP_LOOP          230  'to 230'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                model_parameters
              166  GET_ITER         
              168  FOR_ITER            228  'to 228'
              170  STORE_FAST               'pname'

 L.1107       172  LOAD_FAST                'self'
              174  LOAD_ATTR                data
              176  LOAD_ATTR                priors
              178  LOAD_FAST                'pname'
              180  BINARY_SUBSCR    
              182  LOAD_STR                 'distribution'
              184  BINARY_SUBSCR    
              186  LOAD_STR                 'fixed'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   216  'to 216'

 L.1108       192  LOAD_FAST                'self'
              194  LOAD_ATTR                data
              196  LOAD_ATTR                priors
              198  LOAD_FAST                'pname'
              200  BINARY_SUBSCR    
              202  LOAD_STR                 'hyperparameters'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                posteriors
              210  LOAD_FAST                'pname'
              212  STORE_SUBSCR     
              214  JUMP_BACK           168  'to 168'
            216_0  COME_FROM           190  '190'

 L.1110       216  LOAD_CONST               0.0
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                posteriors
              222  LOAD_FAST                'pname'
              224  STORE_SUBSCR     
              226  JUMP_BACK           168  'to 168'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP      160  '160'

 L.1116       230  BUILD_MAP_0           0 
              232  LOAD_FAST                'self'
              234  STORE_ATTR               transform_prior

 L.1117       236  LOAD_FAST                'self'
              238  LOAD_METHOD              set_prior_transform
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  POP_TOP          

 L.1120       244  LOAD_FAST                'self'
              246  LOAD_ATTR                data
              248  LOAD_ATTR                t_lc
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   288  'to 288'

 L.1121       258  LOAD_GLOBAL              model
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                data
              264  LOAD_STR                 'lc'
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                pl
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                pu
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                ecclim
              278  LOAD_CONST               True
              280  LOAD_CONST               ('modeltype', 'pl', 'pu', 'ecclim', 'log_like_calc')
              282  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              284  LOAD_FAST                'self'
              286  STORE_ATTR               lc
            288_0  COME_FROM           254  '254'

 L.1122       288  LOAD_FAST                'self'
              290  LOAD_ATTR                data
              292  LOAD_ATTR                t_rv
              294  LOAD_CONST               None
              296  COMPARE_OP               is-not
          298_300  POP_JUMP_IF_FALSE   328  'to 328'

 L.1123       302  LOAD_GLOBAL              model
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                data
              308  LOAD_STR                 'rv'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                ecclim
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                ta
              318  LOAD_CONST               True
              320  LOAD_CONST               ('modeltype', 'ecclim', 'ta', 'log_like_calc')
              322  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              324  LOAD_FAST                'self'
              326  STORE_ATTR               rv
            328_0  COME_FROM           298  '298'

 L.1126       328  LOAD_GLOBAL              force_dynesty
          330_332  POP_JUMP_IF_FALSE   356  'to 356'
              334  LOAD_FAST                'self'
              336  LOAD_ATTR                use_dynesty
          338_340  POP_JUMP_IF_TRUE    356  'to 356'

 L.1127       342  LOAD_GLOBAL              print
              344  LOAD_STR                 'PyMultinest installation not detected. Forcing dynesty as the sampler.'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  POP_TOP          

 L.1128       350  LOAD_CONST               True
              352  LOAD_FAST                'self'
              354  STORE_ATTR               use_dynesty
            356_0  COME_FROM           338  '338'
            356_1  COME_FROM           330  '330'

 L.1129       356  LOAD_GLOBAL              force_pymultinest
          358_360  POP_JUMP_IF_FALSE   384  'to 384'
              362  LOAD_FAST                'self'
              364  LOAD_ATTR                use_dynesty
          366_368  POP_JUMP_IF_FALSE   384  'to 384'

 L.1130       370  LOAD_GLOBAL              print
              372  LOAD_STR                 'dynesty installation not detected. Forcing PyMultinest as the sampler.'
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  POP_TOP          

 L.1131       378  LOAD_CONST               False
              380  LOAD_FAST                'self'
              382  STORE_ATTR               use_dynesty
            384_0  COME_FROM           366  '366'
            384_1  COME_FROM           358  '358'

 L.1134       384  BUILD_MAP_0           0 
              386  STORE_FAST               'out'

 L.1135       388  LOAD_CONST               False
              390  STORE_FAST               'runMultiNest'

 L.1136       392  LOAD_CONST               False
              394  STORE_FAST               'runDynesty'

 L.1137       396  LOAD_FAST                'self'
              398  LOAD_ATTR                use_dynesty
          400_402  POP_JUMP_IF_TRUE    626  'to 626'

 L.1138       404  LOAD_FAST                'self'
              406  LOAD_ATTR                out_folder
              408  LOAD_CONST               None
              410  COMPARE_OP               is
          412_414  POP_JUMP_IF_FALSE   436  'to 436'

 L.1139       416  LOAD_GLOBAL              os
              418  LOAD_METHOD              getcwd
              420  CALL_METHOD_0         0  '0 positional arguments'
              422  LOAD_STR                 '/'
              424  BINARY_ADD       
              426  LOAD_FAST                'self'
              428  STORE_ATTR               out_folder

 L.1140       430  LOAD_CONST               True
              432  STORE_FAST               'runMultiNest'
              434  JUMP_FORWARD        460  'to 460'
            436_0  COME_FROM           412  '412'

 L.1142       436  LOAD_GLOBAL              os
              438  LOAD_ATTR                path
              440  LOAD_METHOD              exists
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                out_folder
              446  LOAD_STR                 'posteriors.pkl'
              448  BINARY_ADD       
              450  CALL_METHOD_1         1  '1 positional argument'
          452_454  POP_JUMP_IF_TRUE    460  'to 460'

 L.1143       456  LOAD_CONST               True
              458  STORE_FAST               'runMultiNest'
            460_0  COME_FROM           452  '452'
            460_1  COME_FROM           434  '434'

 L.1144       460  LOAD_FAST                'runMultiNest'
          462_464  POP_JUMP_IF_FALSE   990  'to 990'

 L.1145       466  LOAD_GLOBAL              pymultinest
              468  LOAD_ATTR                run
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                loglike
              474  LOAD_FAST                'self'
              476  LOAD_ATTR                prior
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                data
              482  LOAD_ATTR                nparams

 L.1146       484  LOAD_FAST                'self'
              486  LOAD_ATTR                n_live_points

 L.1147       488  LOAD_CONST               100

 L.1148       490  LOAD_FAST                'self'
              492  LOAD_ATTR                out_folder
              494  LOAD_STR                 'jomnest_'
              496  BINARY_ADD       
              498  LOAD_CONST               False

 L.1149       500  LOAD_FAST                'self'
              502  LOAD_ATTR                data
              504  LOAD_ATTR                verbose
              506  LOAD_CONST               ('n_live_points', 'max_modes', 'outputfiles_basename', 'resume', 'verbose')
              508  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              510  POP_TOP          

 L.1151       512  LOAD_GLOBAL              pymultinest
              514  LOAD_ATTR                Analyzer
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                out_folder
              520  LOAD_STR                 'jomnest_'
              522  BINARY_ADD       
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                data
              528  LOAD_ATTR                nparams
              530  LOAD_CONST               ('outputfiles_basename', 'n_params')
              532  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              534  STORE_FAST               'output'

 L.1153       536  LOAD_FAST                'output'
              538  LOAD_METHOD              get_equal_weighted_posterior
              540  CALL_METHOD_0         0  '0 positional arguments'
              542  LOAD_CONST               None
              544  LOAD_CONST               None
              546  BUILD_SLICE_2         2 
              548  LOAD_CONST               None
              550  LOAD_CONST               -1
              552  BUILD_SLICE_2         2 
              554  BUILD_TUPLE_2         2 
              556  BINARY_SUBSCR    
              558  STORE_FAST               'posterior_samples'

 L.1155       560  LOAD_FAST                'output'
              562  LOAD_METHOD              get_stats
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  LOAD_STR                 'global evidence'
              568  BINARY_SUBSCR    
              570  LOAD_FAST                'out'
              572  LOAD_STR                 'lnZ'
              574  STORE_SUBSCR     

 L.1156       576  LOAD_FAST                'output'
              578  LOAD_METHOD              get_stats
              580  CALL_METHOD_0         0  '0 positional arguments'
              582  LOAD_STR                 'global evidence error'
              584  BINARY_SUBSCR    
              586  LOAD_FAST                'out'
              588  LOAD_STR                 'lnZerr'
              590  STORE_SUBSCR     

 L.1157       592  LOAD_FAST                'self'
              594  LOAD_ATTR                out_folder
              596  LOAD_CONST               None
              598  COMPARE_OP               is
          600_602  POP_JUMP_IF_FALSE   990  'to 990'

 L.1158       604  LOAD_GLOBAL              os
              606  LOAD_METHOD              system
              608  LOAD_STR                 'rm '
              610  LOAD_GLOBAL              out_folder
              612  BINARY_ADD       
              614  LOAD_STR                 'jomnest_*'
              616  BINARY_ADD       
              618  CALL_METHOD_1         1  '1 positional argument'
              620  POP_TOP          
          622_624  JUMP_FORWARD        990  'to 990'
            626_0  COME_FROM           400  '400'

 L.1159       626  LOAD_FAST                'self'
              628  LOAD_ATTR                use_dynesty
          630_632  POP_JUMP_IF_FALSE   990  'to 990'

 L.1160       634  LOAD_FAST                'self'
              636  LOAD_ATTR                out_folder
              638  LOAD_CONST               None
              640  COMPARE_OP               is
          642_644  POP_JUMP_IF_FALSE   652  'to 652'

 L.1161       646  LOAD_CONST               True
              648  STORE_FAST               'runDynesty'
              650  JUMP_FORWARD        730  'to 730'
            652_0  COME_FROM           642  '642'

 L.1163       652  LOAD_FAST                'self'
              654  LOAD_ATTR                dynamic
          656_658  POP_JUMP_IF_FALSE   692  'to 692'
              660  LOAD_GLOBAL              os
              662  LOAD_ATTR                path
              664  LOAD_METHOD              exists
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                out_folder
              670  LOAD_STR                 '_dynesty_DNS_posteriors.pkl'
              672  BINARY_ADD       
              674  CALL_METHOD_1         1  '1 positional argument'
          676_678  POP_JUMP_IF_TRUE    692  'to 692'

 L.1164       680  LOAD_GLOBAL              dynesty
              682  LOAD_ATTR                DynamicNestedSampler
              684  STORE_FAST               'DynestySampler'

 L.1165       686  LOAD_CONST               True
              688  STORE_FAST               'runDynesty'
              690  JUMP_FORWARD        730  'to 730'
            692_0  COME_FROM           676  '676'
            692_1  COME_FROM           656  '656'

 L.1166       692  LOAD_FAST                'self'
              694  LOAD_ATTR                dynamic
          696_698  POP_JUMP_IF_TRUE    730  'to 730'
              700  LOAD_GLOBAL              os
              702  LOAD_ATTR                path
              704  LOAD_METHOD              exists
              706  LOAD_FAST                'self'
              708  LOAD_ATTR                out_folder
              710  LOAD_STR                 '_dynesty_NS_posteriors.pkl'
              712  BINARY_ADD       
              714  CALL_METHOD_1         1  '1 positional argument'
          716_718  POP_JUMP_IF_TRUE    730  'to 730'

 L.1167       720  LOAD_GLOBAL              dynesty
              722  LOAD_ATTR                NestedSampler
              724  STORE_FAST               'DynestySampler'

 L.1168       726  LOAD_CONST               True
              728  STORE_FAST               'runDynesty'
            730_0  COME_FROM           716  '716'
            730_1  COME_FROM           696  '696'
            730_2  COME_FROM           690  '690'
            730_3  COME_FROM           650  '650'

 L.1169       730  LOAD_FAST                'runDynesty'
          732_734  POP_JUMP_IF_FALSE   990  'to 990'

 L.1170       736  LOAD_FAST                'self'
              738  LOAD_ATTR                dynesty_nthreads
              740  LOAD_CONST               None
              742  COMPARE_OP               is
          744_746  POP_JUMP_IF_FALSE   800  'to 800'

 L.1171       748  LOAD_GLOBAL              dynesty
              750  LOAD_ATTR                DynamicNestedSampler
              752  LOAD_FAST                'self'
              754  LOAD_ATTR                loglike
              756  LOAD_FAST                'self'
              758  LOAD_ATTR                prior
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                data
              764  LOAD_ATTR                nparams
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                n_live_points

 L.1172       770  LOAD_FAST                'self'
              772  LOAD_ATTR                dynesty_bound
              774  LOAD_FAST                'self'
              776  LOAD_ATTR                dynesty_sample
              778  LOAD_CONST               ('nlive', 'bound', 'sample')
              780  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              782  STORE_FAST               'sampler'

 L.1174       784  LOAD_FAST                'sampler'
              786  LOAD_METHOD              run_nested
              788  CALL_METHOD_0         0  '0 positional arguments'
              790  POP_TOP          

 L.1175       792  LOAD_FAST                'sampler'
              794  LOAD_ATTR                results
              796  STORE_FAST               'results'
              798  JUMP_FORWARD        916  'to 916'
            800_0  COME_FROM           744  '744'

 L.1177       800  LOAD_CONST               0
              802  LOAD_CONST               ('Pool',)
              804  IMPORT_NAME              multiprocessing
              806  IMPORT_FROM              Pool
              808  STORE_FAST               'Pool'
              810  POP_TOP          

 L.1178       812  LOAD_CONST               0
              814  LOAD_CONST               None
              816  IMPORT_NAME              contextlib
              818  STORE_FAST               'contextlib'

 L.1179       820  LOAD_GLOBAL              int
              822  LOAD_FAST                'self'
              824  LOAD_ATTR                dynesty_nthreads
              826  CALL_FUNCTION_1       1  '1 positional argument'
              828  STORE_FAST               'nthreads'

 L.1180       830  LOAD_FAST                'contextlib'
              832  LOAD_METHOD              closing
              834  LOAD_FAST                'Pool'
              836  LOAD_FAST                'nthreads'
              838  LOAD_CONST               1
              840  BINARY_SUBTRACT  
              842  LOAD_CONST               ('processes',)
              844  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              846  CALL_METHOD_1         1  '1 positional argument'
              848  SETUP_WITH          910  'to 910'
              850  STORE_FAST               'executor'

 L.1181       852  LOAD_GLOBAL              dynesty
              854  LOAD_ATTR                DynamicNestedSampler
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                loglike
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                prior
              864  LOAD_FAST                'self'
              866  LOAD_ATTR                data
              868  LOAD_ATTR                nparams
              870  LOAD_FAST                'self'
              872  LOAD_ATTR                n_live_points

 L.1182       874  LOAD_FAST                'self'
              876  LOAD_ATTR                dynesty_bound
              878  LOAD_FAST                'self'
              880  LOAD_ATTR                dynesty_sample
              882  LOAD_FAST                'executor'
              884  LOAD_FAST                'nthreads'
              886  LOAD_CONST               ('nlive', 'bound', 'sample', 'pool', 'queue_size')
              888  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              890  STORE_FAST               'sampler'

 L.1183       892  LOAD_FAST                'sampler'
              894  LOAD_METHOD              run_nested
              896  CALL_METHOD_0         0  '0 positional arguments'
              898  POP_TOP          

 L.1184       900  LOAD_FAST                'sampler'
              902  LOAD_ATTR                results
              904  STORE_FAST               'results'
              906  POP_BLOCK        
              908  LOAD_CONST               None
            910_0  COME_FROM_WITH      848  '848'
              910  WITH_CLEANUP_START
              912  WITH_CLEANUP_FINISH
              914  END_FINALLY      
            916_0  COME_FROM           798  '798'

 L.1185       916  LOAD_FAST                'results'
              918  LOAD_FAST                'out'
              920  LOAD_STR                 'dynesty_output'
              922  STORE_SUBSCR     

 L.1187       924  LOAD_GLOBAL              np
              926  LOAD_METHOD              exp
              928  LOAD_FAST                'results'
              930  LOAD_STR                 'logwt'
              932  BINARY_SUBSCR    
              934  LOAD_FAST                'results'
              936  LOAD_STR                 'logz'
              938  BINARY_SUBSCR    
              940  LOAD_CONST               -1
              942  BINARY_SUBSCR    
              944  BINARY_SUBTRACT  
              946  CALL_METHOD_1         1  '1 positional argument'
              948  STORE_FAST               'weights'

 L.1188       950  LOAD_GLOBAL              resample_equal
              952  LOAD_FAST                'results'
              954  LOAD_ATTR                samples
              956  LOAD_FAST                'weights'
              958  CALL_FUNCTION_2       2  '2 positional arguments'
              960  STORE_FAST               'posterior_samples'

 L.1190       962  LOAD_FAST                'results'
              964  LOAD_ATTR                logz
              966  LOAD_CONST               -1
              968  BINARY_SUBSCR    
              970  LOAD_FAST                'out'
              972  LOAD_STR                 'lnZ'
              974  STORE_SUBSCR     

 L.1191       976  LOAD_FAST                'results'
              978  LOAD_ATTR                logzerr
              980  LOAD_CONST               -1
              982  BINARY_SUBSCR    
              984  LOAD_FAST                'out'
              986  LOAD_STR                 'lnZerr'
              988  STORE_SUBSCR     
            990_0  COME_FROM           732  '732'
            990_1  COME_FROM           630  '630'
            990_2  COME_FROM           622  '622'
            990_3  COME_FROM           600  '600'
            990_4  COME_FROM           462  '462'

 L.1192       990  LOAD_FAST                'runMultiNest'
          992_994  POP_JUMP_IF_TRUE   1002  'to 1002'
              996  LOAD_FAST                'runDynesty'
         998_1000  POP_JUMP_IF_FALSE  2154  'to 2154'
           1002_0  COME_FROM           992  '992'

 L.1194      1002  BUILD_MAP_0           0 
             1004  LOAD_FAST                'out'
             1006  LOAD_STR                 'posterior_samples'
             1008  STORE_SUBSCR     

 L.1195      1010  LOAD_FAST                'posterior_samples'
             1012  LOAD_FAST                'out'
             1014  LOAD_STR                 'posterior_samples'
             1016  BINARY_SUBSCR    
             1018  LOAD_STR                 'unnamed'
             1020  STORE_SUBSCR     

 L.1198      1022  LOAD_GLOBAL              np
             1024  LOAD_METHOD              zeros
             1026  LOAD_FAST                'posterior_samples'
             1028  LOAD_ATTR                shape
             1030  LOAD_CONST               0
             1032  BINARY_SUBSCR    
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  LOAD_FAST                'out'
             1038  LOAD_STR                 'posterior_samples'
             1040  BINARY_SUBSCR    
             1042  LOAD_STR                 'loglike'
             1044  STORE_SUBSCR     

 L.1199      1046  SETUP_LOOP         1106  'to 1106'
             1048  LOAD_GLOBAL              range
             1050  LOAD_FAST                'posterior_samples'
             1052  LOAD_ATTR                shape
             1054  LOAD_CONST               0
             1056  BINARY_SUBSCR    
             1058  CALL_FUNCTION_1       1  '1 positional argument'
             1060  GET_ITER         
             1062  FOR_ITER           1104  'to 1104'
             1064  STORE_FAST               'i'

 L.1200      1066  LOAD_FAST                'self'
             1068  LOAD_METHOD              loglike
             1070  LOAD_FAST                'posterior_samples'
             1072  LOAD_FAST                'i'
             1074  LOAD_CONST               None
             1076  LOAD_CONST               None
             1078  BUILD_SLICE_2         2 
             1080  BUILD_TUPLE_2         2 
             1082  BINARY_SUBSCR    
             1084  CALL_METHOD_1         1  '1 positional argument'
             1086  LOAD_FAST                'out'
             1088  LOAD_STR                 'posterior_samples'
             1090  BINARY_SUBSCR    
             1092  LOAD_STR                 'loglike'
             1094  BINARY_SUBSCR    
             1096  LOAD_FAST                'i'
             1098  STORE_SUBSCR     
         1100_1102  JUMP_BACK          1062  'to 1062'
             1104  POP_BLOCK        
           1106_0  COME_FROM_LOOP     1046  '1046'

 L.1202      1106  LOAD_CONST               0
             1108  STORE_FAST               'pcounter'

 L.1203      1110  SETUP_LOOP         1208  'to 1208'
             1112  LOAD_FAST                'self'
             1114  LOAD_ATTR                model_parameters
             1116  GET_ITER         
           1118_0  COME_FROM          1138  '1138'
             1118  FOR_ITER           1206  'to 1206'
             1120  STORE_FAST               'pname'

 L.1204      1122  LOAD_FAST                'data'
             1124  LOAD_ATTR                priors
             1126  LOAD_FAST                'pname'
             1128  BINARY_SUBSCR    
             1130  LOAD_STR                 'distribution'
             1132  BINARY_SUBSCR    
             1134  LOAD_STR                 'fixed'
             1136  COMPARE_OP               !=
         1138_1140  POP_JUMP_IF_FALSE  1118  'to 1118'

 L.1205      1142  LOAD_GLOBAL              np
             1144  LOAD_METHOD              median
             1146  LOAD_FAST                'posterior_samples'
             1148  LOAD_CONST               None
             1150  LOAD_CONST               None
             1152  BUILD_SLICE_2         2 
             1154  LOAD_FAST                'pcounter'
             1156  BUILD_TUPLE_2         2 
             1158  BINARY_SUBSCR    
             1160  CALL_METHOD_1         1  '1 positional argument'
             1162  LOAD_FAST                'self'
             1164  LOAD_ATTR                posteriors
             1166  LOAD_FAST                'pname'
             1168  STORE_SUBSCR     

 L.1206      1170  LOAD_FAST                'posterior_samples'
             1172  LOAD_CONST               None
             1174  LOAD_CONST               None
             1176  BUILD_SLICE_2         2 
             1178  LOAD_FAST                'pcounter'
             1180  BUILD_TUPLE_2         2 
             1182  BINARY_SUBSCR    
             1184  LOAD_FAST                'out'
             1186  LOAD_STR                 'posterior_samples'
             1188  BINARY_SUBSCR    
             1190  LOAD_FAST                'pname'
             1192  STORE_SUBSCR     

 L.1207      1194  LOAD_FAST                'pcounter'
             1196  LOAD_CONST               1
             1198  INPLACE_ADD      
             1200  STORE_FAST               'pcounter'
         1202_1204  JUMP_BACK          1118  'to 1118'
             1206  POP_BLOCK        
           1208_0  COME_FROM_LOOP     1110  '1110'

 L.1213      1208  LOAD_GLOBAL              list
             1210  LOAD_FAST                'out'
             1212  LOAD_STR                 'posterior_samples'
             1214  BINARY_SUBSCR    
             1216  LOAD_METHOD              keys
             1218  CALL_METHOD_0         0  '0 positional arguments'
             1220  CALL_FUNCTION_1       1  '1 positional argument'
             1222  STORE_FAST               'fitted_parameters'

 L.1214      1224  LOAD_CONST               (True, False)
             1226  UNPACK_SEQUENCE_2     2 
             1228  STORE_FAST               'firstTime'
             1230  STORE_FAST               'Tparametrization'

 L.1215  1232_1234  SETUP_LOOP         1552  'to 1552'
             1236  LOAD_FAST                'fitted_parameters'
             1238  GET_ITER         
           1240_0  COME_FROM          1456  '1456'
         1240_1242  FOR_ITER           1550  'to 1550'
             1244  STORE_FAST               'posterior_parameter'

 L.1216      1246  LOAD_FAST                'posterior_parameter'
             1248  LOAD_METHOD              split
             1250  LOAD_STR                 '_'
             1252  CALL_METHOD_1         1  '1 positional argument'
             1254  STORE_FAST               'pvector'

 L.1217      1256  LOAD_FAST                'pvector'
             1258  LOAD_CONST               0
             1260  BINARY_SUBSCR    
             1262  LOAD_STR                 'dt'
             1264  COMPARE_OP               ==
         1266_1268  POP_JUMP_IF_FALSE  1446  'to 1446'

 L.1219      1270  LOAD_FAST                'pvector'
             1272  LOAD_CONST               1
             1274  LOAD_CONST               None
             1276  BUILD_SLICE_2         2 
             1278  BINARY_SUBSCR    
             1280  UNPACK_SEQUENCE_3     3 
             1282  STORE_FAST               'pnum'
             1284  STORE_FAST               'ins'
             1286  STORE_FAST               'tnum'

 L.1221      1288  LOAD_STR                 'P_'
             1290  LOAD_FAST                'pnum'
             1292  BINARY_ADD       
             1294  LOAD_FAST                'fitted_parameters'
             1296  COMPARE_OP               in
         1298_1300  POP_JUMP_IF_FALSE  1320  'to 1320'

 L.1222      1302  LOAD_FAST                'out'
             1304  LOAD_STR                 'posterior_samples'
             1306  BINARY_SUBSCR    
             1308  LOAD_STR                 'P_'
             1310  LOAD_FAST                'pnum'
             1312  BINARY_ADD       
             1314  BINARY_SUBSCR    
             1316  STORE_FAST               'P'
             1318  JUMP_FORWARD       1338  'to 1338'
           1320_0  COME_FROM          1298  '1298'

 L.1224      1320  LOAD_FAST                'data'
             1322  LOAD_ATTR                priors
             1324  LOAD_STR                 'P_'
             1326  LOAD_FAST                'pnum'
             1328  BINARY_ADD       
             1330  BINARY_SUBSCR    
             1332  LOAD_STR                 'hyperparameters'
             1334  BINARY_SUBSCR    
             1336  STORE_FAST               'P'
           1338_0  COME_FROM          1318  '1318'

 L.1226      1338  LOAD_STR                 't0_'
             1340  LOAD_FAST                'pnum'
             1342  BINARY_ADD       
             1344  LOAD_FAST                'fitted_parameters'
             1346  COMPARE_OP               in
         1348_1350  POP_JUMP_IF_FALSE  1370  'to 1370'

 L.1227      1352  LOAD_FAST                'out'
             1354  LOAD_STR                 'posterior_samples'
             1356  BINARY_SUBSCR    
             1358  LOAD_STR                 't0_'
             1360  LOAD_FAST                'pnum'
             1362  BINARY_ADD       
             1364  BINARY_SUBSCR    
             1366  STORE_FAST               't0'
             1368  JUMP_FORWARD       1388  'to 1388'
           1370_0  COME_FROM          1348  '1348'

 L.1229      1370  LOAD_FAST                'data'
             1372  LOAD_ATTR                priors
             1374  LOAD_STR                 't0_'
             1376  LOAD_FAST                'pnum'
             1378  BINARY_ADD       
             1380  BINARY_SUBSCR    
             1382  LOAD_STR                 'hyperparameters'
             1384  BINARY_SUBSCR    
             1386  STORE_FAST               't0'
           1388_0  COME_FROM          1368  '1368'

 L.1231      1388  LOAD_FAST                't0'
             1390  LOAD_GLOBAL              np
             1392  LOAD_METHOD              double
             1394  LOAD_FAST                'tnum'
             1396  CALL_METHOD_1         1  '1 positional argument'
             1398  LOAD_FAST                'P'
             1400  BINARY_MULTIPLY  
             1402  BINARY_ADD       
             1404  LOAD_FAST                'out'
             1406  LOAD_STR                 'posterior_samples'
             1408  BINARY_SUBSCR    
             1410  LOAD_FAST                'posterior_parameter'
             1412  BINARY_SUBSCR    
             1414  BINARY_ADD       
             1416  LOAD_FAST                'out'
             1418  LOAD_STR                 'posterior_samples'
             1420  BINARY_SUBSCR    
             1422  LOAD_STR                 'T_'
             1424  LOAD_FAST                'pnum'
             1426  BINARY_ADD       
             1428  LOAD_STR                 '_'
             1430  BINARY_ADD       
             1432  LOAD_FAST                'ins'
             1434  BINARY_ADD       
             1436  LOAD_STR                 '_'
             1438  BINARY_ADD       
             1440  LOAD_FAST                'tnum'
             1442  BINARY_ADD       
             1444  STORE_SUBSCR     
           1446_0  COME_FROM          1266  '1266'

 L.1232      1446  LOAD_FAST                'pvector'
             1448  LOAD_CONST               0
             1450  BINARY_SUBSCR    
             1452  LOAD_STR                 'T'
             1454  COMPARE_OP               ==
         1456_1458  POP_JUMP_IF_FALSE  1240  'to 1240'

 L.1233      1460  LOAD_FAST                'firstTime'
         1462_1464  POP_JUMP_IF_FALSE  1478  'to 1478'

 L.1234      1466  LOAD_CONST               True
             1468  STORE_FAST               'Tparametrization'

 L.1235      1470  BUILD_MAP_0           0 
             1472  STORE_FAST               'Tdict'

 L.1236      1474  LOAD_CONST               False
             1476  STORE_FAST               'firstTime'
           1478_0  COME_FROM          1462  '1462'

 L.1238      1478  LOAD_FAST                'pvector'
             1480  LOAD_CONST               1
             1482  LOAD_CONST               None
             1484  BUILD_SLICE_2         2 
             1486  BINARY_SUBSCR    
             1488  UNPACK_SEQUENCE_3     3 
             1490  STORE_FAST               'pnum'
             1492  STORE_FAST               'ins'
             1494  STORE_FAST               'tnum'

 L.1239      1496  LOAD_FAST                'pnum'
             1498  LOAD_GLOBAL              list
             1500  LOAD_FAST                'Tdict'
             1502  LOAD_METHOD              keys
             1504  CALL_METHOD_0         0  '0 positional arguments'
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  COMPARE_OP               not-in
         1510_1512  POP_JUMP_IF_FALSE  1522  'to 1522'

 L.1240      1514  BUILD_MAP_0           0 
             1516  LOAD_FAST                'Tdict'
             1518  LOAD_FAST                'pnum'
             1520  STORE_SUBSCR     
           1522_0  COME_FROM          1510  '1510'

 L.1241      1522  LOAD_FAST                'out'
             1524  LOAD_STR                 'posterior_samples'
             1526  BINARY_SUBSCR    
             1528  LOAD_FAST                'posterior_parameter'
             1530  BINARY_SUBSCR    
             1532  LOAD_FAST                'Tdict'
             1534  LOAD_FAST                'pnum'
             1536  BINARY_SUBSCR    
             1538  LOAD_GLOBAL              int
             1540  LOAD_FAST                'tnum'
             1542  CALL_FUNCTION_1       1  '1 positional argument'
             1544  STORE_SUBSCR     
         1546_1548  JUMP_BACK          1240  'to 1240'
             1550  POP_BLOCK        
           1552_0  COME_FROM_LOOP     1232  '1232'

 L.1242      1552  LOAD_FAST                'Tparametrization'
         1554_1556  POP_JUMP_IF_FALSE  1912  'to 1912'

 L.1243  1558_1560  SETUP_LOOP         1912  'to 1912'
             1562  LOAD_GLOBAL              list
             1564  LOAD_FAST                'Tdict'
             1566  LOAD_METHOD              keys
             1568  CALL_METHOD_0         0  '0 positional arguments'
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  GET_ITER         
         1574_1576  FOR_ITER           1910  'to 1910'
             1578  STORE_FAST               'pnum'

 L.1244      1580  LOAD_GLOBAL              np
             1582  LOAD_METHOD              array
             1584  LOAD_GLOBAL              list
             1586  LOAD_FAST                'Tdict'
             1588  LOAD_FAST                'pnum'
             1590  BINARY_SUBSCR    
             1592  LOAD_METHOD              keys
             1594  CALL_METHOD_0         0  '0 positional arguments'
             1596  CALL_FUNCTION_1       1  '1 positional argument'
             1598  CALL_METHOD_1         1  '1 positional argument'
             1600  STORE_FAST               'all_ns'

 L.1245      1602  LOAD_GLOBAL              len
             1604  LOAD_FAST                'Tdict'
             1606  LOAD_FAST                'pnum'
             1608  BINARY_SUBSCR    
             1610  LOAD_FAST                'all_ns'
             1612  LOAD_CONST               0
             1614  BINARY_SUBSCR    
             1616  BINARY_SUBSCR    
             1618  CALL_FUNCTION_1       1  '1 positional argument'
             1620  STORE_FAST               'Nsamples'

 L.1246      1622  LOAD_GLOBAL              np
             1624  LOAD_METHOD              zeros
             1626  LOAD_FAST                'Nsamples'
             1628  CALL_METHOD_1         1  '1 positional argument'
             1630  LOAD_GLOBAL              np
             1632  LOAD_METHOD              zeros
             1634  LOAD_FAST                'Nsamples'
             1636  CALL_METHOD_1         1  '1 positional argument'
             1638  ROT_TWO          
             1640  LOAD_FAST                'out'
             1642  LOAD_STR                 'posterior_samples'
             1644  BINARY_SUBSCR    
             1646  LOAD_STR                 'P_'
             1648  LOAD_FAST                'pnum'
             1650  BINARY_ADD       
             1652  STORE_SUBSCR     
             1654  LOAD_FAST                'out'
             1656  LOAD_STR                 'posterior_samples'
             1658  BINARY_SUBSCR    
             1660  LOAD_STR                 't0_'
             1662  LOAD_FAST                'pnum'
             1664  BINARY_ADD       
             1666  STORE_SUBSCR     

 L.1247      1668  LOAD_GLOBAL              len
             1670  LOAD_FAST                'all_ns'
             1672  CALL_FUNCTION_1       1  '1 positional argument'
             1674  STORE_FAST               'N'

 L.1248      1676  SETUP_LOOP         1906  'to 1906'
             1678  LOAD_GLOBAL              range
             1680  LOAD_FAST                'Nsamples'
             1682  CALL_FUNCTION_1       1  '1 positional argument'
             1684  GET_ITER         
             1686  FOR_ITER           1904  'to 1904'
             1688  STORE_FAST               'i'

 L.1249      1690  LOAD_GLOBAL              np
             1692  LOAD_METHOD              zeros
             1694  LOAD_FAST                'N'
             1696  CALL_METHOD_1         1  '1 positional argument'
             1698  STORE_FAST               'all_Ts'

 L.1250      1700  SETUP_LOOP         1748  'to 1748'
             1702  LOAD_GLOBAL              range
             1704  LOAD_GLOBAL              len
             1706  LOAD_FAST                'all_ns'
             1708  CALL_FUNCTION_1       1  '1 positional argument'
             1710  CALL_FUNCTION_1       1  '1 positional argument'
             1712  GET_ITER         
             1714  FOR_ITER           1746  'to 1746'
             1716  STORE_FAST               'j'

 L.1251      1718  LOAD_FAST                'Tdict'
             1720  LOAD_FAST                'pnum'
             1722  BINARY_SUBSCR    
             1724  LOAD_FAST                'all_ns'
             1726  LOAD_FAST                'j'
             1728  BINARY_SUBSCR    
             1730  BINARY_SUBSCR    
             1732  LOAD_FAST                'i'
             1734  BINARY_SUBSCR    
             1736  LOAD_FAST                'all_Ts'
             1738  LOAD_FAST                'j'
             1740  STORE_SUBSCR     
         1742_1744  JUMP_BACK          1714  'to 1714'
             1746  POP_BLOCK        
           1748_0  COME_FROM_LOOP     1700  '1700'

 L.1252      1748  LOAD_GLOBAL              np
             1750  LOAD_METHOD              sum
             1752  LOAD_FAST                'all_Ts'
             1754  LOAD_FAST                'all_ns'
             1756  BINARY_MULTIPLY  
             1758  CALL_METHOD_1         1  '1 positional argument'
             1760  LOAD_FAST                'N'
             1762  BINARY_TRUE_DIVIDE
             1764  LOAD_GLOBAL              np
             1766  LOAD_METHOD              sum
             1768  LOAD_FAST                'all_Ts'
             1770  CALL_METHOD_1         1  '1 positional argument'
             1772  LOAD_FAST                'N'
             1774  BINARY_TRUE_DIVIDE
             1776  LOAD_GLOBAL              np
             1778  LOAD_METHOD              sum
             1780  LOAD_FAST                'all_ns'
             1782  CALL_METHOD_1         1  '1 positional argument'
             1784  LOAD_FAST                'N'
             1786  BINARY_TRUE_DIVIDE
             1788  LOAD_GLOBAL              np
             1790  LOAD_METHOD              sum
             1792  LOAD_FAST                'all_ns'
             1794  LOAD_CONST               2
             1796  BINARY_POWER     
             1798  CALL_METHOD_1         1  '1 positional argument'
             1800  LOAD_FAST                'N'
             1802  BINARY_TRUE_DIVIDE
             1804  BUILD_TUPLE_4         4 
             1806  UNPACK_SEQUENCE_4     4 
             1808  STORE_FAST               'XY'
             1810  STORE_FAST               'Y'
             1812  STORE_FAST               'X'
             1814  STORE_FAST               'X2'

 L.1254      1816  LOAD_FAST                'XY'
             1818  LOAD_FAST                'X'
             1820  LOAD_FAST                'Y'
             1822  BINARY_MULTIPLY  
             1824  BINARY_SUBTRACT  
             1826  LOAD_FAST                'X2'
             1828  LOAD_FAST                'X'
             1830  LOAD_CONST               2
             1832  BINARY_POWER     
             1834  BINARY_SUBTRACT  
             1836  BINARY_TRUE_DIVIDE
             1838  LOAD_FAST                'out'
             1840  LOAD_STR                 'posterior_samples'
             1842  BINARY_SUBSCR    
             1844  LOAD_STR                 'P_'
             1846  LOAD_FAST                'pnum'
             1848  BINARY_ADD       
             1850  BINARY_SUBSCR    
             1852  LOAD_FAST                'i'
             1854  STORE_SUBSCR     

 L.1256      1856  LOAD_FAST                'Y'
             1858  LOAD_FAST                'out'
             1860  LOAD_STR                 'posterior_samples'
             1862  BINARY_SUBSCR    
             1864  LOAD_STR                 'P_'
             1866  LOAD_FAST                'pnum'
             1868  BINARY_ADD       
             1870  BINARY_SUBSCR    
             1872  LOAD_FAST                'i'
             1874  BINARY_SUBSCR    
             1876  LOAD_FAST                'X'
             1878  BINARY_MULTIPLY  
             1880  BINARY_SUBTRACT  
             1882  LOAD_FAST                'out'
             1884  LOAD_STR                 'posterior_samples'
             1886  BINARY_SUBSCR    
             1888  LOAD_STR                 't0_'
             1890  LOAD_FAST                'pnum'
             1892  BINARY_ADD       
             1894  BINARY_SUBSCR    
             1896  LOAD_FAST                'i'
             1898  STORE_SUBSCR     
         1900_1902  JUMP_BACK          1686  'to 1686'
             1904  POP_BLOCK        
           1906_0  COME_FROM_LOOP     1676  '1676'
         1906_1908  JUMP_BACK          1574  'to 1574'
             1910  POP_BLOCK        
           1912_0  COME_FROM_LOOP     1558  '1558'
           1912_1  COME_FROM          1554  '1554'

 L.1257      1912  LOAD_FAST                'self'
             1914  LOAD_ATTR                data
             1916  LOAD_ATTR                t_lc
             1918  LOAD_CONST               None
             1920  COMPARE_OP               is-not
         1922_1924  POP_JUMP_IF_FALSE  1964  'to 1964'

 L.1258      1926  LOAD_CONST               True
             1928  LOAD_FAST                'self'
             1930  LOAD_ATTR                data
             1932  LOAD_ATTR                lc_options
             1934  LOAD_STR                 'efficient_bp'
             1936  BINARY_SUBSCR    
             1938  COMPARE_OP               in
         1940_1942  POP_JUMP_IF_FALSE  1964  'to 1964'

 L.1259      1944  LOAD_FAST                'self'
             1946  LOAD_ATTR                pu
             1948  LOAD_FAST                'out'
             1950  LOAD_STR                 'pu'
             1952  STORE_SUBSCR     

 L.1260      1954  LOAD_FAST                'self'
             1956  LOAD_ATTR                pl
             1958  LOAD_FAST                'out'
             1960  LOAD_STR                 'pl'
             1962  STORE_SUBSCR     
           1964_0  COME_FROM          1940  '1940'
           1964_1  COME_FROM          1922  '1922'

 L.1261      1964  LOAD_FAST                'self'
             1966  LOAD_ATTR                data
             1968  LOAD_ATTR                t_rv
             1970  LOAD_CONST               None
             1972  COMPARE_OP               is-not
         1974_1976  POP_JUMP_IF_FALSE  2016  'to 2016'

 L.1262      1978  LOAD_FAST                'self'
             1980  LOAD_ATTR                data
             1982  LOAD_ATTR                rv_options
             1984  LOAD_STR                 'fitrvline'
             1986  BINARY_SUBSCR    
         1988_1990  POP_JUMP_IF_TRUE   2006  'to 2006'
             1992  LOAD_FAST                'self'
             1994  LOAD_ATTR                data
             1996  LOAD_ATTR                rv_options
             1998  LOAD_STR                 'fitrvquad'
             2000  BINARY_SUBSCR    
         2002_2004  POP_JUMP_IF_FALSE  2016  'to 2016'
           2006_0  COME_FROM          1988  '1988'

 L.1263      2006  LOAD_FAST                'self'
             2008  LOAD_ATTR                ta
             2010  LOAD_FAST                'out'
             2012  LOAD_STR                 'ta'
             2014  STORE_SUBSCR     
           2016_0  COME_FROM          2002  '2002'
           2016_1  COME_FROM          1974  '1974'

 L.1264      2016  LOAD_FAST                'runDynesty'
         2018_2020  POP_JUMP_IF_FALSE  2114  'to 2114'

 L.1265      2022  LOAD_FAST                'self'
             2024  LOAD_ATTR                dynamic
         2026_2028  POP_JUMP_IF_FALSE  2068  'to 2068'
             2030  LOAD_FAST                'self'
             2032  LOAD_ATTR                out_folder
             2034  LOAD_CONST               None
             2036  COMPARE_OP               is-not
         2038_2040  POP_JUMP_IF_FALSE  2068  'to 2068'

 L.1266      2042  LOAD_GLOBAL              pickle
             2044  LOAD_METHOD              dump
             2046  LOAD_FAST                'out'
             2048  LOAD_GLOBAL              open
             2050  LOAD_FAST                'self'
             2052  LOAD_ATTR                out_folder
             2054  LOAD_STR                 '_dynesty_DNS_posteriors.pkl'
             2056  BINARY_ADD       
             2058  LOAD_STR                 'wb'
             2060  CALL_FUNCTION_2       2  '2 positional arguments'
             2062  CALL_METHOD_2         2  '2 positional arguments'
             2064  POP_TOP          
             2066  JUMP_FORWARD       2112  'to 2112'
           2068_0  COME_FROM          2038  '2038'
           2068_1  COME_FROM          2026  '2026'

 L.1267      2068  LOAD_FAST                'self'
             2070  LOAD_ATTR                dynamic
         2072_2074  POP_JUMP_IF_TRUE   2150  'to 2150'
             2076  LOAD_FAST                'self'
             2078  LOAD_ATTR                out_folder
             2080  LOAD_CONST               None
             2082  COMPARE_OP               is-not
         2084_2086  POP_JUMP_IF_FALSE  2150  'to 2150'

 L.1268      2088  LOAD_GLOBAL              pickle
             2090  LOAD_METHOD              dump
             2092  LOAD_FAST                'out'
             2094  LOAD_GLOBAL              open
             2096  LOAD_FAST                'self'
             2098  LOAD_ATTR                out_folder
             2100  LOAD_STR                 '_dynesty_NS_posteriors.pkl'
             2102  BINARY_ADD       
             2104  LOAD_STR                 'wb'
             2106  CALL_FUNCTION_2       2  '2 positional arguments'
             2108  CALL_METHOD_2         2  '2 positional arguments'
             2110  POP_TOP          
           2112_0  COME_FROM          2066  '2066'
             2112  JUMP_FORWARD       2770  'to 2770'
           2114_0  COME_FROM          2018  '2018'

 L.1270      2114  LOAD_FAST                'self'
             2116  LOAD_ATTR                out_folder
             2118  LOAD_CONST               None
             2120  COMPARE_OP               is-not
         2122_2124  POP_JUMP_IF_FALSE  2770  'to 2770'

 L.1271      2126  LOAD_GLOBAL              pickle
             2128  LOAD_METHOD              dump
             2130  LOAD_FAST                'out'
             2132  LOAD_GLOBAL              open
             2134  LOAD_FAST                'self'
             2136  LOAD_ATTR                out_folder
             2138  LOAD_STR                 'posteriors.pkl'
             2140  BINARY_ADD       
             2142  LOAD_STR                 'wb'
             2144  CALL_FUNCTION_2       2  '2 positional arguments'
             2146  CALL_METHOD_2         2  '2 positional arguments'
             2148  POP_TOP          
           2150_0  COME_FROM          2084  '2084'
           2150_1  COME_FROM          2072  '2072'
         2150_2152  JUMP_FORWARD       2770  'to 2770'
           2154_0  COME_FROM           998  '998'

 L.1274      2154  LOAD_FAST                'self'
             2156  LOAD_ATTR                use_dynesty
         2158_2160  POP_JUMP_IF_FALSE  2398  'to 2398'
             2162  LOAD_FAST                'self'
             2164  LOAD_ATTR                out_folder
             2166  LOAD_CONST               None
             2168  COMPARE_OP               is-not
         2170_2172  POP_JUMP_IF_FALSE  2398  'to 2398'

 L.1275      2174  LOAD_FAST                'self'
             2176  LOAD_ATTR                dynamic
         2178_2180  POP_JUMP_IF_FALSE  2290  'to 2290'

 L.1276      2182  LOAD_GLOBAL              os
             2184  LOAD_ATTR                path
             2186  LOAD_METHOD              exists
             2188  LOAD_FAST                'self'
             2190  LOAD_ATTR                out_folder
             2192  LOAD_STR                 '_dynesty_DNS_posteriors.pkl'
             2194  BINARY_ADD       
             2196  CALL_METHOD_1         1  '1 positional argument'
         2198_2200  POP_JUMP_IF_FALSE  2396  'to 2396'

 L.1277      2202  LOAD_FAST                'self'
             2204  LOAD_ATTR                data
             2206  LOAD_ATTR                verbose
         2208_2210  POP_JUMP_IF_FALSE  2220  'to 2220'

 L.1278      2212  LOAD_GLOBAL              print
             2214  LOAD_STR                 'Detected (dynesty) Dynamic NS output files --- extracting...'
             2216  CALL_FUNCTION_1       1  '1 positional argument'
             2218  POP_TOP          
           2220_0  COME_FROM          2208  '2208'

 L.1279      2220  LOAD_FAST                'self'
             2222  LOAD_ATTR                data
             2224  LOAD_ATTR                pickle_encoding
             2226  LOAD_CONST               None
             2228  COMPARE_OP               is
         2230_2232  POP_JUMP_IF_FALSE  2258  'to 2258'

 L.1280      2234  LOAD_GLOBAL              pickle
             2236  LOAD_METHOD              load
             2238  LOAD_GLOBAL              open
             2240  LOAD_FAST                'self'
             2242  LOAD_ATTR                out_folder
             2244  LOAD_STR                 '_dynesty_DNS_posteriors.pkl'
             2246  BINARY_ADD       
             2248  LOAD_STR                 'rb'
             2250  CALL_FUNCTION_2       2  '2 positional arguments'
             2252  CALL_METHOD_1         1  '1 positional argument'
             2254  STORE_FAST               'out'
             2256  JUMP_FORWARD       2288  'to 2288'
           2258_0  COME_FROM          2230  '2230'

 L.1282      2258  LOAD_GLOBAL              pickle
             2260  LOAD_ATTR                load
             2262  LOAD_GLOBAL              open
             2264  LOAD_FAST                'self'
             2266  LOAD_ATTR                out_folder
             2268  LOAD_STR                 '_dynesty_DNS_posteriors.pkl'
             2270  BINARY_ADD       
             2272  LOAD_STR                 'rb'
             2274  CALL_FUNCTION_2       2  '2 positional arguments'
             2276  LOAD_FAST                'self'
             2278  LOAD_ATTR                data
             2280  LOAD_ATTR                pickle_encoding
             2282  LOAD_CONST               ('encoding',)
             2284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2286  STORE_FAST               'out'
           2288_0  COME_FROM          2256  '2256'
             2288  JUMP_FORWARD       2396  'to 2396'
           2290_0  COME_FROM          2178  '2178'

 L.1284      2290  LOAD_GLOBAL              os
             2292  LOAD_ATTR                path
             2294  LOAD_METHOD              exists
             2296  LOAD_FAST                'self'
             2298  LOAD_ATTR                out_folder
             2300  LOAD_STR                 '_dynesty_NS_posteriors.pkl'
             2302  BINARY_ADD       
             2304  CALL_METHOD_1         1  '1 positional argument'
         2306_2308  POP_JUMP_IF_FALSE  2496  'to 2496'

 L.1285      2310  LOAD_FAST                'self'
             2312  LOAD_ATTR                data
             2314  LOAD_ATTR                verbose
         2316_2318  POP_JUMP_IF_FALSE  2328  'to 2328'

 L.1286      2320  LOAD_GLOBAL              print
             2322  LOAD_STR                 'Detected (dynesty) NS output files --- extracting...'
             2324  CALL_FUNCTION_1       1  '1 positional argument'
             2326  POP_TOP          
           2328_0  COME_FROM          2316  '2316'

 L.1287      2328  LOAD_FAST                'self'
             2330  LOAD_ATTR                data
             2332  LOAD_ATTR                pickle_encoding
             2334  LOAD_CONST               None
             2336  COMPARE_OP               is
         2338_2340  POP_JUMP_IF_FALSE  2366  'to 2366'

 L.1288      2342  LOAD_GLOBAL              pickle
             2344  LOAD_METHOD              load
             2346  LOAD_GLOBAL              open
             2348  LOAD_FAST                'self'
             2350  LOAD_ATTR                out_folder
             2352  LOAD_STR                 '_dynesty_NS_posteriors.pkl'
             2354  BINARY_ADD       
             2356  LOAD_STR                 'rb'
             2358  CALL_FUNCTION_2       2  '2 positional arguments'
             2360  CALL_METHOD_1         1  '1 positional argument'
             2362  STORE_FAST               'out'
             2364  JUMP_FORWARD       2396  'to 2396'
           2366_0  COME_FROM          2338  '2338'

 L.1290      2366  LOAD_GLOBAL              pickle
             2368  LOAD_ATTR                load
             2370  LOAD_GLOBAL              open
             2372  LOAD_FAST                'self'
             2374  LOAD_ATTR                out_folder
             2376  LOAD_STR                 '_dynesty_NS_posteriors.pkl'
             2378  BINARY_ADD       
             2380  LOAD_STR                 'rb'
             2382  CALL_FUNCTION_2       2  '2 positional arguments'
             2384  LOAD_FAST                'self'
             2386  LOAD_ATTR                data
             2388  LOAD_ATTR                pickle_encoding
             2390  LOAD_CONST               ('encoding',)
             2392  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2394  STORE_FAST               'out'
           2396_0  COME_FROM          2364  '2364'
           2396_1  COME_FROM          2288  '2288'
           2396_2  COME_FROM          2198  '2198'
             2396  JUMP_FORWARD       2496  'to 2496'
           2398_0  COME_FROM          2170  '2170'
           2398_1  COME_FROM          2158  '2158'

 L.1291      2398  LOAD_FAST                'self'
             2400  LOAD_ATTR                out_folder
             2402  LOAD_CONST               None
             2404  COMPARE_OP               is-not
         2406_2408  POP_JUMP_IF_FALSE  2496  'to 2496'

 L.1292      2410  LOAD_FAST                'self'
             2412  LOAD_ATTR                data
             2414  LOAD_ATTR                verbose
         2416_2418  POP_JUMP_IF_FALSE  2428  'to 2428'

 L.1293      2420  LOAD_GLOBAL              print
             2422  LOAD_STR                 'Detected (MultiNest) NS output files --- extracting...'
             2424  CALL_FUNCTION_1       1  '1 positional argument'
             2426  POP_TOP          
           2428_0  COME_FROM          2416  '2416'

 L.1294      2428  LOAD_FAST                'self'
             2430  LOAD_ATTR                data
             2432  LOAD_ATTR                pickle_encoding
             2434  LOAD_CONST               None
             2436  COMPARE_OP               is
         2438_2440  POP_JUMP_IF_FALSE  2466  'to 2466'

 L.1295      2442  LOAD_GLOBAL              pickle
             2444  LOAD_METHOD              load
             2446  LOAD_GLOBAL              open
             2448  LOAD_FAST                'self'
             2450  LOAD_ATTR                out_folder
             2452  LOAD_STR                 'posteriors.pkl'
             2454  BINARY_ADD       
             2456  LOAD_STR                 'rb'
             2458  CALL_FUNCTION_2       2  '2 positional arguments'
             2460  CALL_METHOD_1         1  '1 positional argument'
             2462  STORE_FAST               'out'
             2464  JUMP_FORWARD       2496  'to 2496'
           2466_0  COME_FROM          2438  '2438'

 L.1297      2466  LOAD_GLOBAL              pickle
             2468  LOAD_ATTR                load
             2470  LOAD_GLOBAL              open
             2472  LOAD_FAST                'self'
             2474  LOAD_ATTR                out_folder
             2476  LOAD_STR                 'posteriors.pkl'
             2478  BINARY_ADD       
             2480  LOAD_STR                 'rb'
             2482  CALL_FUNCTION_2       2  '2 positional arguments'
             2484  LOAD_FAST                'self'
             2486  LOAD_ATTR                data
             2488  LOAD_ATTR                pickle_encoding
             2490  LOAD_CONST               ('encoding',)
             2492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2494  STORE_FAST               'out'
           2496_0  COME_FROM          2464  '2464'
           2496_1  COME_FROM          2406  '2406'
           2496_2  COME_FROM          2396  '2396'
           2496_3  COME_FROM          2306  '2306'

 L.1298      2496  LOAD_GLOBAL              len
             2498  LOAD_FAST                'out'
             2500  LOAD_METHOD              keys
             2502  CALL_METHOD_0         0  '0 positional arguments'
             2504  CALL_FUNCTION_1       1  '1 positional argument'
             2506  LOAD_CONST               0
             2508  COMPARE_OP               ==
         2510_2512  POP_JUMP_IF_FALSE  2524  'to 2524'

 L.1299      2514  LOAD_GLOBAL              print
             2516  LOAD_STR                 'Warning: no output generated or extracted. Check the fit options given to juliet.fit().'
             2518  CALL_FUNCTION_1       1  '1 positional argument'
             2520  POP_TOP          
             2522  JUMP_FORWARD       2770  'to 2770'
           2524_0  COME_FROM          2510  '2510'

 L.1303      2524  SETUP_LOOP         2604  'to 2604'
             2526  LOAD_FAST                'out'
             2528  LOAD_STR                 'posterior_samples'
             2530  BINARY_SUBSCR    
             2532  LOAD_METHOD              keys
             2534  CALL_METHOD_0         0  '0 positional arguments'
             2536  GET_ITER         
           2538_0  COME_FROM          2556  '2556'
             2538  FOR_ITER           2602  'to 2602'
             2540  STORE_FAST               'pname'

 L.1304      2542  LOAD_STR                 'sigma_w_rv'
             2544  LOAD_FAST                'pname'
             2546  LOAD_CONST               None
             2548  LOAD_CONST               10
             2550  BUILD_SLICE_2         2 
             2552  BINARY_SUBSCR    
             2554  COMPARE_OP               ==
         2556_2558  POP_JUMP_IF_FALSE  2538  'to 2538'

 L.1305      2560  LOAD_FAST                'pname'
             2562  LOAD_METHOD              split
             2564  LOAD_STR                 '_'
             2566  CALL_METHOD_1         1  '1 positional argument'
             2568  LOAD_CONST               -1
             2570  BINARY_SUBSCR    
             2572  STORE_FAST               'instrument'

 L.1306      2574  LOAD_FAST                'out'
             2576  LOAD_STR                 'posterior_samples'
             2578  BINARY_SUBSCR    
             2580  LOAD_FAST                'pname'
             2582  BINARY_SUBSCR    
             2584  LOAD_FAST                'out'
             2586  LOAD_STR                 'posterior_samples'
             2588  BINARY_SUBSCR    
             2590  LOAD_STR                 'sigma_w_'
             2592  LOAD_FAST                'instrument'
             2594  BINARY_ADD       
             2596  STORE_SUBSCR     
         2598_2600  JUMP_BACK          2538  'to 2538'
             2602  POP_BLOCK        
           2604_0  COME_FROM_LOOP     2524  '2524'

 L.1308      2604  SETUP_LOOP         2670  'to 2670'
             2606  LOAD_FAST                'self'
             2608  LOAD_ATTR                posteriors
             2610  LOAD_METHOD              keys
             2612  CALL_METHOD_0         0  '0 positional arguments'
             2614  GET_ITER         
           2616_0  COME_FROM          2636  '2636'
             2616  FOR_ITER           2668  'to 2668'
             2618  STORE_FAST               'pname'

 L.1309      2620  LOAD_FAST                'data'
             2622  LOAD_ATTR                priors
             2624  LOAD_FAST                'pname'
             2626  BINARY_SUBSCR    
             2628  LOAD_STR                 'distribution'
             2630  BINARY_SUBSCR    
             2632  LOAD_STR                 'fixed'
             2634  COMPARE_OP               !=
         2636_2638  POP_JUMP_IF_FALSE  2616  'to 2616'

 L.1310      2640  LOAD_GLOBAL              np
             2642  LOAD_METHOD              median
             2644  LOAD_FAST                'out'
             2646  LOAD_STR                 'posterior_samples'
             2648  BINARY_SUBSCR    
             2650  LOAD_FAST                'pname'
             2652  BINARY_SUBSCR    
             2654  CALL_METHOD_1         1  '1 positional argument'
             2656  LOAD_FAST                'self'
             2658  LOAD_ATTR                posteriors
             2660  LOAD_FAST                'pname'
             2662  STORE_SUBSCR     
         2664_2666  JUMP_BACK          2616  'to 2616'
             2668  POP_BLOCK        
           2670_0  COME_FROM_LOOP     2604  '2604'

 L.1311      2670  LOAD_FAST                'out'
             2672  LOAD_STR                 'posterior_samples'
             2674  BINARY_SUBSCR    
             2676  LOAD_STR                 'unnamed'
             2678  BINARY_SUBSCR    
             2680  STORE_FAST               'posterior_samples'

 L.1312      2682  LOAD_STR                 'pu'
             2684  LOAD_FAST                'out'
             2686  LOAD_METHOD              keys
             2688  CALL_METHOD_0         0  '0 positional arguments'
             2690  COMPARE_OP               in
         2692_2694  POP_JUMP_IF_FALSE  2746  'to 2746'

 L.1313      2696  LOAD_FAST                'out'
             2698  LOAD_STR                 'pu'
             2700  BINARY_SUBSCR    
             2702  LOAD_FAST                'self'
             2704  STORE_ATTR               pu

 L.1314      2706  LOAD_FAST                'out'
             2708  LOAD_STR                 'pl'
             2710  BINARY_SUBSCR    
             2712  LOAD_FAST                'self'
             2714  STORE_ATTR               pl

 L.1315      2716  LOAD_FAST                'self'
             2718  LOAD_ATTR                pu
             2720  LOAD_FAST                'self'
             2722  LOAD_ATTR                pl
             2724  BINARY_SUBTRACT  
             2726  LOAD_CONST               2.0
             2728  LOAD_FAST                'self'
           2730_0  COME_FROM          2112  '2112'
             2730  LOAD_ATTR                pl
             2732  BINARY_ADD       
             2734  LOAD_FAST                'self'
             2736  LOAD_ATTR                pu
             2738  BINARY_ADD       
             2740  BINARY_TRUE_DIVIDE
             2742  LOAD_FAST                'self'
             2744  STORE_ATTR               Ar
           2746_0  COME_FROM          2692  '2692'

 L.1316      2746  LOAD_STR                 'ta'
             2748  LOAD_FAST                'out'
             2750  LOAD_METHOD              keys
             2752  CALL_METHOD_0         0  '0 positional arguments'
             2754  COMPARE_OP               in
         2756_2758  POP_JUMP_IF_FALSE  2770  'to 2770'

 L.1317      2760  LOAD_FAST                'out'
             2762  LOAD_STR                 'ta'
             2764  BINARY_SUBSCR    
             2766  LOAD_FAST                'self'
             2768  STORE_ATTR               ta
           2770_0  COME_FROM          2756  '2756'
           2770_1  COME_FROM          2522  '2522'
           2770_2  COME_FROM          2150  '2150'
           2770_3  COME_FROM          2122  '2122'

 L.1320      2770  LOAD_FAST                'self'
             2772  LOAD_ATTR                out_folder
             2774  LOAD_CONST               None
             2776  COMPARE_OP               is-not
         2778_2780  POP_JUMP_IF_FALSE  2832  'to 2832'

 L.1321      2782  LOAD_GLOBAL              os
             2784  LOAD_ATTR                path
             2786  LOAD_METHOD              exists
             2788  LOAD_FAST                'self'
             2790  LOAD_ATTR                out_folder
             2792  LOAD_STR                 'posteriors.dat'
             2794  BINARY_ADD       
             2796  CALL_METHOD_1         1  '1 positional argument'
         2798_2800  POP_JUMP_IF_TRUE   2832  'to 2832'

 L.1322      2802  LOAD_GLOBAL              open
             2804  LOAD_FAST                'self'
             2806  LOAD_ATTR                out_folder
             2808  LOAD_STR                 'posteriors.dat'
             2810  BINARY_ADD       
             2812  LOAD_STR                 'w'
             2814  CALL_FUNCTION_2       2  '2 positional arguments'
             2816  STORE_FAST               'outpp'

 L.1323      2818  LOAD_GLOBAL              writepp
             2820  LOAD_FAST                'outpp'
             2822  LOAD_FAST                'out'
             2824  LOAD_FAST                'data'
             2826  LOAD_ATTR                priors
             2828  CALL_FUNCTION_3       3  '3 positional arguments'
             2830  POP_TOP          
           2832_0  COME_FROM          2798  '2798'
           2832_1  COME_FROM          2778  '2778'

 L.1326      2832  LOAD_FAST                'out'
             2834  LOAD_FAST                'self'
             2836  STORE_ATTR               posteriors

 L.1329      2838  LOAD_FAST                'self'
             2840  LOAD_ATTR                data
             2842  LOAD_ATTR                t_lc
             2844  LOAD_CONST               None
             2846  COMPARE_OP               is-not
         2848_2850  POP_JUMP_IF_FALSE  2868  'to 2868'

 L.1330      2852  LOAD_FAST                'self'
             2854  LOAD_ATTR                lc
             2856  LOAD_METHOD              set_posterior_samples
             2858  LOAD_FAST                'out'
             2860  LOAD_STR                 'posterior_samples'
             2862  BINARY_SUBSCR    
             2864  CALL_METHOD_1         1  '1 positional argument'
             2866  POP_TOP          
           2868_0  COME_FROM          2848  '2848'

 L.1331      2868  LOAD_FAST                'self'
             2870  LOAD_ATTR                data
             2872  LOAD_ATTR                t_rv
             2874  LOAD_CONST               None
             2876  COMPARE_OP               is-not
         2878_2880  POP_JUMP_IF_FALSE  2898  'to 2898'

 L.1332      2882  LOAD_FAST                'self'
             2884  LOAD_ATTR                rv
             2886  LOAD_METHOD              set_posterior_samples
             2888  LOAD_FAST                'out'
             2890  LOAD_STR                 'posterior_samples'
             2892  BINARY_SUBSCR    
             2894  CALL_METHOD_1         1  '1 positional argument'
             2896  POP_TOP          
           2898_0  COME_FROM          2878  '2878'

Parse error at or near `COME_FROM' instruction at offset 2730_0


class model(object):
    __doc__ = "\n    Given a juliet data object, this kernel generates either a lightcurve or a radial-velocity object. Example usage:\n\n               >>> model = juliet.model(data, modeltype = 'lc')\n\n    :param data: (juliet.load object)\n        An object containing all the information about the current dataset.\n\n    :param modeltype: (optional, string)\n        String indicating whether the model to generate should be a lightcurve ('lc') or a radial-velocity ('rv') model. \n\n    :param pl: (optional, float)                      \n        If the ``(r1,r2)`` parametrization for ``(b,p)`` is used, this defines the lower limit of the planet-to-star radius ratio to be sampled. \n        Default is ``0``.\n\n    :param pu: (optional, float)                    \n        Same as ``pl``, but for the upper limit. Default is ``1``.\n\n    :param ecclim: (optional, float)\n        This parameter sets the maximum eccentricity allowed such that a model is actually evaluated. Default is ``1``.\n\n    :param log_like_calc: (optional, boolean)\n        If True, it is assumed the model is generated to generate likelihoods values, and thus this skips the saving/calculation of the individual \n        models per planet (i.e., ``self.model['p1']``, ``self.model['p2']``, etc. will not exist). Default is False.\n\n    "

    def generate_rv_model(self, parameter_values, evaluate_global_errors=True):
        self.modelOK = True
        first_time = True
        for i in self.numbering:
            if first_time:
                cP = parameter_values[('P_p' + str(i))]
                first_time = False
            elif cP < parameter_values[('P_p' + str(i))]:
                cP = parameter_values[('P_p' + str(i))]
            else:
                self.modelOK = False
                return False

        for n in range(self.nplanets):
            i = self.numbering[n]
            K, t0, P = parameter_values[('K_p' + str(i))], parameter_values[('t0_p' + str(i))], parameter_values[('P_p' + str(i))]
            if self.dictionary['ecc_parametrization'][i] == 0:
                ecc, omega = parameter_values[('ecc_p' + str(i))], parameter_values[('omega_p' + str(i))] * np.pi / 180.0
            else:
                if self.dictionary['ecc_parametrization'][i] == 1:
                    ecc = np.sqrt(parameter_values[('ecosomega_p' + str(i))] ** 2 + parameter_values[('esinomega_p' + str(i))] ** 2)
                    omega = np.arctan2(parameter_values[('esinomega_p' + str(i))], parameter_values[('ecosomega_p' + str(i))])
                else:
                    ecc = parameter_values[('secosomega_p' + str(i))] ** 2 + parameter_values[('sesinomega_p' + str(i))] ** 2
                    omega = np.arctan2(parameter_values[('sesinomega_p' + str(i))], parameter_values[('secosomega_p' + str(i))])
            if ecc > self.ecclim:
                self.modelOK = False
                return False
            self.model['radvel']['per' + str(n + 1)] = radvel.Parameter(value=P)
            self.model['radvel']['tc' + str(n + 1)] = radvel.Parameter(value=t0)
            self.model['radvel']['w' + str(n + 1)] = radvel.Parameter(value=omega)
            self.model['radvel']['e' + str(n + 1)] = radvel.Parameter(value=ecc)
            self.model['radvel']['k' + str(n + 1)] = radvel.Parameter(value=K)

        if self.log_like_calc:
            self.model['Keplerian'] = radvel.model.RVModel(self.model['radvel']).__call__(self.t)
        else:
            self.model['Keplerian'] = radvel.model.RVModel(self.model['radvel']).__call__(self.t)
            for n in range(self.nplanets):
                i = self.numbering[n]
                self.model['p' + str(i)] = radvel.model.RVModel(self.model['radvel']).__call__((self.t), planet_num=(n + 1))

        if self.dictionary['fitrvline']:
            self.model['Keplerian+Trend'] = self.model['Keplerian'] + parameter_values['rv_intercept'] + (self.t - self.ta) * parameter_values['rv_slope']
        else:
            if self.dictionary['fitrvquad']:
                self.model['Keplerian+Trend'] = self.model['Keplerian'] + parameter_values['rv_intercept'] + (self.t - self.ta) * parameter_values['rv_slope'] + (self.t - self.ta) ** 2 * parameter_values['rv_quad']
            else:
                self.model['Keplerian+Trend'] = self.model['Keplerian']
        for instrument in self.inames:
            self.model[instrument]['deterministic'] = self.model['Keplerian+Trend'][self.instrument_indexes[instrument]] + parameter_values[('mu_' + instrument)]
            self.model[instrument]['deterministic_variances'] = self.errors[instrument] ** 2 + parameter_values[('sigma_w_' + instrument)] ** 2
            if self.lm_boolean[instrument]:
                self.model[instrument]['LM'] = np.zeros(self.ndatapoints_per_instrument[instrument])
                for i in range(self.lm_n[instrument]):
                    self.model[instrument]['LM'] += parameter_values[('theta' + str(i) + '_' + instrument)] * self.lm_arguments[instrument][:, i]

                self.model[instrument]['deterministic'] += self.model[instrument]['LM']
            if self.global_model:
                self.model['global'][self.instrument_indexes[instrument]] = self.model[instrument]['deterministic']
                if evaluate_global_errors:
                    self.model['global_variances'][self.instrument_indexes[instrument]] = self.yerr[self.instrument_indexes[instrument]] ** 2 + parameter_values[('sigma_w_' + instrument)] ** 2

    def get_GP_plus_deterministic_model(self, parameter_values, instrument=None):
        if self.global_model:
            if self.dictionary['global_model']['GPDetrend']:
                self.dictionary['global_model']['noise_model'].set_parameter_vector(parameter_values)
                self.dictionary['global_model']['noise_model'].yerr = np.sqrt(self.variances)
                self.dictionary['global_model']['noise_model'].compute_GP(X=(self.original_GPregressors))
                self.model['GP'] = self.dictionary['global_model']['noise_model'].GP.predict((self.residuals), (self.dictionary['global_model']['noise_model'].X), return_var=False,
                  return_cov=False)
                return (self.model['global'], self.model['GP'], self.model['global'] + self.model['GP'])
            return self.model['global']
        else:
            if self.dictionary[instrument]['GPDetrend']:
                self.dictionary[instrument]['noise_model'].set_parameter_vector(parameter_values)
                self.model[instrument]['GP'] = self.dictionary[instrument]['noise_model'].GP.predict((self.residuals), (self.dictionary[instrument]['noise_model'].X), return_var=False,
                  return_cov=False)
                return (self.model[instrument]['deterministic'], self.model[instrument]['GP'], self.model[instrument]['deterministic'] + self.model[instrument]['GP'])
            return self.model[instrument]['deterministic']

    def evaluate_model--- This code section failed: ---

 L.1512         0  LOAD_FAST                'instrument'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.1513         8  LOAD_FAST                'self'
               10  LOAD_ATTR                global_model
               12  POP_JUMP_IF_TRUE     22  'to 22'

 L.1514        14  LOAD_GLOBAL              Exception
               16  LOAD_STR                 'Input error: an instrument has to be defined for non-global models in order to evaluate the model.'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'
             22_1  COME_FROM             6  '6'

 L.1516        22  LOAD_FAST                'resampling'
               24  LOAD_CONST               None
               26  COMPARE_OP               is-not
               28  POP_JUMP_IF_FALSE   160  'to 160'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                modeltype
               34  LOAD_STR                 'lc'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE   160  'to 160'
               40  LOAD_FAST                'instrument'
               42  LOAD_CONST               None
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE   160  'to 160'

 L.1517        48  LOAD_FAST                'resampling'
               50  POP_JUMP_IF_FALSE   110  'to 110'

 L.1518        52  LOAD_GLOBAL              init_batman
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                times
               58  LOAD_FAST                'instrument'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                dictionary
               66  LOAD_FAST                'instrument'
               68  BINARY_SUBSCR    
               70  LOAD_STR                 'ldlaw'
               72  BINARY_SUBSCR    

 L.1519        74  LOAD_FAST                'nresampling'

 L.1520        76  LOAD_FAST                'etresampling'
               78  LOAD_CONST               ('nresampling', 'etresampling')
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  UNPACK_SEQUENCE_2     2 
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                model
               88  LOAD_FAST                'instrument'
               90  BINARY_SUBSCR    
               92  LOAD_STR                 'params'
               94  STORE_SUBSCR     
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                model
              100  LOAD_FAST                'instrument'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'm'
              106  STORE_SUBSCR     
              108  JUMP_FORWARD        160  'to 160'
            110_0  COME_FROM            50  '50'

 L.1522       110  LOAD_GLOBAL              init_batman
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                times
              116  LOAD_FAST                'instrument'
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                dictionary
              124  LOAD_FAST                'instrument'
              126  BINARY_SUBSCR    
              128  LOAD_STR                 'ldlaw'
              130  BINARY_SUBSCR    
              132  CALL_FUNCTION_2       2  '2 positional arguments'
              134  UNPACK_SEQUENCE_2     2 
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                model
              140  LOAD_FAST                'instrument'
              142  BINARY_SUBSCR    
              144  LOAD_STR                 'params'
              146  STORE_SUBSCR     
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                model
              152  LOAD_FAST                'instrument'
              154  BINARY_SUBSCR    
              156  LOAD_STR                 'm'
              158  STORE_SUBSCR     
            160_0  COME_FROM           108  '108'
            160_1  COME_FROM            46  '46'
            160_2  COME_FROM            38  '38'
            160_3  COME_FROM            28  '28'

 L.1528       160  LOAD_FAST                'self'
              162  LOAD_ATTR                global_model
              164  POP_JUMP_IF_TRUE    198  'to 198'

 L.1529       166  LOAD_GLOBAL              np
              168  LOAD_METHOD              copy
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                inames
              174  CALL_METHOD_1         1  '1 positional argument'
              176  STORE_FAST               'original_inames'

 L.1530       178  LOAD_FAST                'instrument'
              180  BUILD_LIST_1          1 
              182  LOAD_FAST                'self'
              184  STORE_ATTR               inames

 L.1531       186  LOAD_FAST                'self'
              188  LOAD_ATTR                dictionary
              190  LOAD_METHOD              keys
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  STORE_FAST               'instruments'
              196  JUMP_FORWARD        204  'to 204'
            198_0  COME_FROM           164  '164'

 L.1533       198  LOAD_FAST                'self'
              200  LOAD_ATTR                inames
              202  STORE_FAST               'instruments'
            204_0  COME_FROM           196  '196'

 L.1536       204  LOAD_FAST                'parameter_values'
              206  LOAD_CONST               None
              208  COMPARE_OP               is-not
          210_212  POP_JUMP_IF_FALSE  5664  'to 5664'

 L.1538       214  LOAD_FAST                'return_components'
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L.1539       218  LOAD_CONST               False
              220  LOAD_FAST                'self'
              222  STORE_ATTR               log_like_calc

 L.1540       224  BUILD_MAP_0           0 
              226  STORE_FAST               'components'
            228_0  COME_FROM           216  '216'

 L.1544       228  LOAD_GLOBAL              list
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                priors
              234  LOAD_METHOD              keys
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'parameters'

 L.1545       242  LOAD_GLOBAL              list
              244  LOAD_FAST                'parameter_values'
              246  LOAD_METHOD              keys
              248  CALL_METHOD_0         0  '0 positional arguments'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  STORE_FAST               'input_parameters'

 L.1546       254  LOAD_GLOBAL              type
              256  LOAD_FAST                'parameter_values'
              258  LOAD_FAST                'input_parameters'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  BINARY_SUBSCR    
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  LOAD_GLOBAL              np
              270  LOAD_ATTR                ndarray
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_FALSE  4880  'to 4880'

 L.1550       278  LOAD_GLOBAL              len
              280  LOAD_FAST                'parameter_values'
              282  LOAD_FAST                'input_parameters'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  BINARY_SUBSCR    
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  STORE_FAST               'nsampled'

 L.1551       294  LOAD_FAST                'all_samples'
          296_298  POP_JUMP_IF_FALSE   316  'to 316'

 L.1552       300  LOAD_FAST                'nsampled'
              302  STORE_FAST               'nsamples'

 L.1553       304  LOAD_GLOBAL              np
              306  LOAD_METHOD              arange
              308  LOAD_FAST                'nsamples'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  STORE_FAST               'idx_samples'
              314  JUMP_FORWARD        364  'to 364'
            316_0  COME_FROM           296  '296'

 L.1555       316  LOAD_GLOBAL              np
              318  LOAD_ATTR                random
              320  LOAD_ATTR                choice
              322  LOAD_GLOBAL              np
              324  LOAD_METHOD              arange
              326  LOAD_FAST                'nsampled'
              328  CALL_METHOD_1         1  '1 positional argument'
              330  LOAD_GLOBAL              np
              332  LOAD_METHOD              min
              334  LOAD_FAST                'nsamples'
              336  LOAD_FAST                'nsampled'
              338  BUILD_LIST_2          2 
              340  CALL_METHOD_1         1  '1 positional argument'
              342  LOAD_CONST               False
              344  LOAD_CONST               ('replace',)
              346  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              348  STORE_FAST               'idx_samples'

 L.1556       350  LOAD_FAST                'idx_samples'
              352  LOAD_GLOBAL              np
              354  LOAD_METHOD              argsort
              356  LOAD_FAST                'idx_samples'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  BINARY_SUBSCR    
              362  STORE_FAST               'idx_samples'
            364_0  COME_FROM           314  '314'

 L.1561       364  LOAD_FAST                't'
              366  LOAD_CONST               None
              368  COMPARE_OP               is
          370_372  POP_JUMP_IF_FALSE   424  'to 424'

 L.1563       374  LOAD_FAST                'self'
              376  LOAD_ATTR                global_model
          378_380  POP_JUMP_IF_FALSE   400  'to 400'

 L.1564       382  LOAD_GLOBAL              np
              384  LOAD_METHOD              zeros
              386  LOAD_FAST                'nsamples'
              388  LOAD_FAST                'self'
              390  LOAD_ATTR                ndatapoints_all_instruments
              392  BUILD_LIST_2          2 
              394  CALL_METHOD_1         1  '1 positional argument'
              396  STORE_FAST               'output_model_samples'
              398  JUMP_FORWARD        994  'to 994'
            400_0  COME_FROM           378  '378'

 L.1566       400  LOAD_GLOBAL              np
              402  LOAD_METHOD              zeros
              404  LOAD_FAST                'nsamples'
              406  LOAD_FAST                'self'
              408  LOAD_ATTR                ndatapoints_per_instrument
              410  LOAD_FAST                'instrument'
              412  BINARY_SUBSCR    
              414  BUILD_LIST_2          2 
              416  CALL_METHOD_1         1  '1 positional argument'
              418  STORE_FAST               'output_model_samples'
          420_422  JUMP_FORWARD        994  'to 994'
            424_0  COME_FROM           370  '370'

 L.1570       424  LOAD_GLOBAL              len
              426  LOAD_FAST                't'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  STORE_FAST               'nt'

 L.1572       432  LOAD_GLOBAL              np
              434  LOAD_METHOD              zeros
              436  LOAD_FAST                'nsamples'
              438  LOAD_FAST                'nt'
              440  BUILD_LIST_2          2 
              442  CALL_METHOD_1         1  '1 positional argument'
              444  STORE_FAST               'output_model_samples'

 L.1573       446  LOAD_FAST                'self'
              448  LOAD_ATTR                global_model
          450_452  POP_JUMP_IF_FALSE   520  'to 520'

 L.1579       454  BUILD_MAP_0           0 
              456  BUILD_MAP_0           0 
              458  ROT_TWO          
              460  STORE_FAST               'nt_original'
              462  STORE_FAST               'original_instrument_times'

 L.1580       464  SETUP_LOOP          550  'to 550'
              466  LOAD_FAST                'instruments'
              468  GET_ITER         
              470  FOR_ITER            516  'to 516'
              472  STORE_FAST               'ginstrument'

 L.1581       474  LOAD_GLOBAL              len
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                times
              480  LOAD_FAST                'ginstrument'
              482  BINARY_SUBSCR    
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  LOAD_FAST                'nt_original'
              488  LOAD_FAST                'ginstrument'
              490  STORE_SUBSCR     

 L.1582       492  LOAD_GLOBAL              np
              494  LOAD_METHOD              copy
              496  LOAD_FAST                'self'
              498  LOAD_ATTR                times
              500  LOAD_FAST                'ginstrument'
              502  BINARY_SUBSCR    
              504  CALL_METHOD_1         1  '1 positional argument'
              506  LOAD_FAST                'original_instrument_times'
              508  LOAD_FAST                'ginstrument'
              510  STORE_SUBSCR     
          512_514  JUMP_BACK           470  'to 470'
              516  POP_BLOCK        
              518  JUMP_FORWARD        550  'to 550'
            520_0  COME_FROM           450  '450'

 L.1587       520  LOAD_GLOBAL              len
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                times
              526  LOAD_FAST                'instrument'
              528  BINARY_SUBSCR    
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  STORE_FAST               'nt_original'

 L.1588       534  LOAD_GLOBAL              np
              536  LOAD_METHOD              copy
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                times
              542  LOAD_FAST                'instrument'
              544  BINARY_SUBSCR    
              546  CALL_METHOD_1         1  '1 positional argument'
              548  STORE_FAST               'original_instrument_times'
            550_0  COME_FROM           518  '518'
            550_1  COME_FROM_LOOP      464  '464'

 L.1589       550  LOAD_FAST                'self'
              552  LOAD_ATTR                modeltype
              554  LOAD_STR                 'lc'
              556  COMPARE_OP               ==
          558_560  POP_JUMP_IF_FALSE   938  'to 938'

 L.1592       562  LOAD_FAST                'self'
              564  LOAD_ATTR                global_model
          566_568  POP_JUMP_IF_FALSE   778  'to 778'

 L.1596       570  SETUP_LOOP          776  'to 776'
              572  LOAD_FAST                'instruments'
              574  GET_ITER         
            576_0  COME_FROM           608  '608'
              576  FOR_ITER            774  'to 774'
              578  STORE_FAST               'ginstrument'

 L.1597       580  LOAD_FAST                'self'
              582  LOAD_ATTR                dictionary
              584  LOAD_FAST                'ginstrument'
              586  BINARY_SUBSCR    
              588  LOAD_STR                 'TransitFit'
              590  BINARY_SUBSCR    
          592_594  POP_JUMP_IF_TRUE    612  'to 612'
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                dictionary
              600  LOAD_FAST                'ginstrument'
              602  BINARY_SUBSCR    
              604  LOAD_STR                 'TransitFitCatwoman'
              606  BINARY_SUBSCR    
          608_610  POP_JUMP_IF_FALSE   576  'to 576'
            612_0  COME_FROM           592  '592'

 L.1598       612  LOAD_FAST                'self'
              614  LOAD_ATTR                dictionary
              616  LOAD_FAST                'ginstrument'
              618  BINARY_SUBSCR    
              620  LOAD_STR                 'TransitFitCatwoman'
              622  BINARY_SUBSCR    
          624_626  POP_JUMP_IF_TRUE    700  'to 700'

 L.1599       628  LOAD_GLOBAL              init_batman
              630  LOAD_FAST                't'
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                dictionary
              636  LOAD_FAST                'ginstrument'
              638  BINARY_SUBSCR    
              640  LOAD_STR                 'ldlaw'
              642  BINARY_SUBSCR    
              644  CALL_FUNCTION_2       2  '2 positional arguments'
              646  UNPACK_SEQUENCE_2     2 
              648  LOAD_FAST                'supersample_params'
              650  LOAD_FAST                'ginstrument'
              652  STORE_SUBSCR     
              654  LOAD_FAST                'supersample_m'
              656  LOAD_FAST                'ginstrument'
              658  STORE_SUBSCR     

 L.1600       660  LOAD_GLOBAL              init_batman
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                times
              666  LOAD_FAST                'ginstrument'
              668  BINARY_SUBSCR    
              670  LOAD_FAST                'self'
              672  LOAD_ATTR                dictionary
              674  LOAD_FAST                'ginstrument'
              676  BINARY_SUBSCR    
              678  LOAD_STR                 'ldlaw'
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_2       2  '2 positional arguments'
              684  UNPACK_SEQUENCE_2     2 
              686  LOAD_FAST                'sample_params'
              688  LOAD_FAST                'ginstrument'
              690  STORE_SUBSCR     
              692  LOAD_FAST                'sample_m'
              694  LOAD_FAST                'ginstrument'
              696  STORE_SUBSCR     
              698  JUMP_BACK           576  'to 576'
            700_0  COME_FROM           624  '624'

 L.1602       700  LOAD_GLOBAL              init_catwoman
              702  LOAD_FAST                't'
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                dictionary
              708  LOAD_FAST                'ginstrument'
              710  BINARY_SUBSCR    
              712  LOAD_STR                 'ldlaw'
              714  BINARY_SUBSCR    
              716  CALL_FUNCTION_2       2  '2 positional arguments'
              718  UNPACK_SEQUENCE_2     2 
              720  LOAD_FAST                'supersample_params'
              722  LOAD_FAST                'ginstrument'
              724  STORE_SUBSCR     
              726  LOAD_FAST                'supersample_m'
              728  LOAD_FAST                'ginstrument'
              730  STORE_SUBSCR     

 L.1603       732  LOAD_GLOBAL              init_catwoman
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                times
              738  LOAD_FAST                'ginstrument'
              740  BINARY_SUBSCR    
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                dictionary
              746  LOAD_FAST                'ginstrument'
              748  BINARY_SUBSCR    
              750  LOAD_STR                 'ldlaw'
              752  BINARY_SUBSCR    
              754  CALL_FUNCTION_2       2  '2 positional arguments'
              756  UNPACK_SEQUENCE_2     2 
              758  LOAD_FAST                'sample_params'
              760  LOAD_FAST                'ginstrument'
              762  STORE_SUBSCR     
              764  LOAD_FAST                'sample_m'
              766  LOAD_FAST                'ginstrument'
              768  STORE_SUBSCR     
          770_772  JUMP_BACK           576  'to 576'
              774  POP_BLOCK        
            776_0  COME_FROM_LOOP      570  '570'
              776  JUMP_FORWARD        936  'to 936'
            778_0  COME_FROM           566  '566'

 L.1607       778  LOAD_FAST                'self'
              780  LOAD_ATTR                dictionary
              782  LOAD_FAST                'instrument'
              784  BINARY_SUBSCR    
              786  LOAD_STR                 'TransitFit'
              788  BINARY_SUBSCR    
          790_792  POP_JUMP_IF_TRUE    810  'to 810'
              794  LOAD_FAST                'self'
              796  LOAD_ATTR                dictionary
              798  LOAD_FAST                'instrument'
              800  BINARY_SUBSCR    
              802  LOAD_STR                 'TransitFitCatwoman'
              804  BINARY_SUBSCR    
          806_808  POP_JUMP_IF_FALSE   994  'to 994'
            810_0  COME_FROM           790  '790'

 L.1608       810  LOAD_FAST                'self'
              812  LOAD_ATTR                dictionary
              814  LOAD_FAST                'instrument'
              816  BINARY_SUBSCR    
              818  LOAD_STR                 'TransitFitCatwoman'
              820  BINARY_SUBSCR    
          822_824  POP_JUMP_IF_TRUE    882  'to 882'

 L.1609       826  LOAD_GLOBAL              init_batman
              828  LOAD_FAST                't'
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                dictionary
              834  LOAD_FAST                'instrument'
              836  BINARY_SUBSCR    
              838  LOAD_STR                 'ldlaw'
              840  BINARY_SUBSCR    
              842  CALL_FUNCTION_2       2  '2 positional arguments'
              844  UNPACK_SEQUENCE_2     2 
              846  STORE_FAST               'supersample_params'
              848  STORE_FAST               'supersample_m'

 L.1610       850  LOAD_GLOBAL              init_batman
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                times
              856  LOAD_FAST                'instrument'
              858  BINARY_SUBSCR    
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                dictionary
              864  LOAD_FAST                'instrument'
              866  BINARY_SUBSCR    
              868  LOAD_STR                 'ldlaw'
              870  BINARY_SUBSCR    
              872  CALL_FUNCTION_2       2  '2 positional arguments'
              874  UNPACK_SEQUENCE_2     2 
              876  STORE_FAST               'sample_params'
              878  STORE_FAST               'sample_m'
              880  JUMP_FORWARD        936  'to 936'
            882_0  COME_FROM           822  '822'

 L.1612       882  LOAD_GLOBAL              init_catwoman
              884  LOAD_FAST                't'
              886  LOAD_FAST                'self'
              888  LOAD_ATTR                dictionary
              890  LOAD_FAST                'instrument'
              892  BINARY_SUBSCR    
              894  LOAD_STR                 'ldlaw'
              896  BINARY_SUBSCR    
              898  CALL_FUNCTION_2       2  '2 positional arguments'
              900  UNPACK_SEQUENCE_2     2 
              902  STORE_FAST               'supersample_params'
              904  STORE_FAST               'supersample_m'

 L.1613       906  LOAD_GLOBAL              init_catwoman
              908  LOAD_FAST                'self'
              910  LOAD_ATTR                times
              912  LOAD_FAST                'instrument'
              914  BINARY_SUBSCR    
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                dictionary
              920  LOAD_FAST                'instrument'
              922  BINARY_SUBSCR    
              924  LOAD_STR                 'ldlaw'
              926  BINARY_SUBSCR    
              928  CALL_FUNCTION_2       2  '2 positional arguments'
              930  UNPACK_SEQUENCE_2     2 
              932  STORE_FAST               'sample_params'
              934  STORE_FAST               'sample_m'
            936_0  COME_FROM           880  '880'
            936_1  COME_FROM           776  '776'
              936  JUMP_FORWARD        994  'to 994'
            938_0  COME_FROM           558  '558'

 L.1618       938  LOAD_GLOBAL              np
              940  LOAD_METHOD              copy
              942  LOAD_FAST                'self'
              944  LOAD_ATTR                t
              946  CALL_METHOD_1         1  '1 positional argument'
              948  STORE_FAST               'original_t'

 L.1619       950  LOAD_FAST                'self'
              952  LOAD_ATTR                global_model
          954_956  POP_JUMP_IF_FALSE   970  'to 970'

 L.1621       958  LOAD_FAST                'self'
              960  LOAD_ATTR                instrument_indexes
              962  LOAD_METHOD              copy
              964  CALL_METHOD_0         0  '0 positional arguments'
              966  STORE_FAST               'original_instrument_indexes'
              968  JUMP_FORWARD        980  'to 980'
            970_0  COME_FROM           954  '954'
            970_1  COME_FROM           398  '398'

 L.1625       970  LOAD_FAST                'self'
              972  LOAD_ATTR                instrument_indexes
              974  LOAD_FAST                'instrument'
              976  BINARY_SUBSCR    
              978  STORE_FAST               'original_instrument_index'
            980_0  COME_FROM           968  '968'

 L.1626       980  LOAD_GLOBAL              np
              982  LOAD_METHOD              arange
              984  LOAD_GLOBAL              len
              986  LOAD_FAST                't'
              988  CALL_FUNCTION_1       1  '1 positional argument'
              990  CALL_METHOD_1         1  '1 positional argument'
              992  STORE_FAST               'dummy_indexes'
            994_0  COME_FROM           936  '936'
            994_1  COME_FROM           806  '806'
            994_2  COME_FROM           420  '420'

 L.1631       994  LOAD_FAST                'return_components'
          996_998  POP_JUMP_IF_FALSE  1388  'to 1388'

 L.1632      1000  SETUP_LOOP         1124  'to 1124'
             1002  LOAD_FAST                'self'
             1004  LOAD_ATTR                numbering
             1006  GET_ITER         
             1008  FOR_ITER           1122  'to 1122'
             1010  STORE_FAST               'i'

 L.1633      1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                global_model
         1016_1018  POP_JUMP_IF_FALSE  1094  'to 1094'
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                modeltype
             1024  LOAD_STR                 'lc'
             1026  COMPARE_OP               ==
         1028_1030  POP_JUMP_IF_FALSE  1094  'to 1094'

 L.1634      1032  BUILD_MAP_0           0 
             1034  LOAD_FAST                'components'
             1036  LOAD_STR                 'p'
             1038  LOAD_GLOBAL              str
             1040  LOAD_FAST                'i'
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  BINARY_ADD       
             1046  STORE_SUBSCR     

 L.1635      1048  SETUP_LOOP         1118  'to 1118'
             1050  LOAD_FAST                'instruments'
             1052  GET_ITER         
             1054  FOR_ITER           1090  'to 1090'
             1056  STORE_FAST               'ginstrument'

 L.1636      1058  LOAD_GLOBAL              np
             1060  LOAD_METHOD              zeros
             1062  LOAD_FAST                'output_model_samples'
             1064  LOAD_ATTR                shape
             1066  CALL_METHOD_1         1  '1 positional argument'
             1068  LOAD_FAST                'components'
             1070  LOAD_STR                 'p'
             1072  LOAD_GLOBAL              str
             1074  LOAD_FAST                'i'
             1076  CALL_FUNCTION_1       1  '1 positional argument'
             1078  BINARY_ADD       
             1080  BINARY_SUBSCR    
             1082  LOAD_FAST                'ginstrument'
             1084  STORE_SUBSCR     
         1086_1088  JUMP_BACK          1054  'to 1054'
             1090  POP_BLOCK        
             1092  JUMP_BACK          1008  'to 1008'
           1094_0  COME_FROM          1028  '1028'
           1094_1  COME_FROM          1016  '1016'

 L.1638      1094  LOAD_GLOBAL              np
             1096  LOAD_METHOD              zeros
             1098  LOAD_FAST                'output_model_samples'
             1100  LOAD_ATTR                shape
             1102  CALL_METHOD_1         1  '1 positional argument'
             1104  LOAD_FAST                'components'
             1106  LOAD_STR                 'p'
             1108  LOAD_GLOBAL              str
             1110  LOAD_FAST                'i'
             1112  CALL_FUNCTION_1       1  '1 positional argument'
             1114  BINARY_ADD       
             1116  STORE_SUBSCR     
           1118_0  COME_FROM_LOOP     1048  '1048'
         1118_1120  JUMP_BACK          1008  'to 1008'
             1122  POP_BLOCK        
           1124_0  COME_FROM_LOOP     1000  '1000'

 L.1639      1124  LOAD_FAST                'self'
             1126  LOAD_ATTR                global_model
         1128_1130  POP_JUMP_IF_FALSE  1178  'to 1178'

 L.1640      1132  BUILD_MAP_0           0 
             1134  LOAD_FAST                'components'
             1136  LOAD_STR                 'lm'
             1138  STORE_SUBSCR     

 L.1641      1140  SETUP_LOOP         1194  'to 1194'
             1142  LOAD_FAST                'instruments'
             1144  GET_ITER         
             1146  FOR_ITER           1174  'to 1174'
             1148  STORE_FAST               'ginstrument'

 L.1642      1150  LOAD_GLOBAL              np
             1152  LOAD_METHOD              zeros
             1154  LOAD_FAST                'output_model_samples'
             1156  LOAD_ATTR                shape
             1158  CALL_METHOD_1         1  '1 positional argument'
             1160  LOAD_FAST                'components'
             1162  LOAD_STR                 'lm'
             1164  BINARY_SUBSCR    
             1166  LOAD_FAST                'ginstrument'
             1168  STORE_SUBSCR     
         1170_1172  JUMP_BACK          1146  'to 1146'
             1174  POP_BLOCK        
             1176  JUMP_FORWARD       1194  'to 1194'
           1178_0  COME_FROM          1128  '1128'

 L.1644      1178  LOAD_GLOBAL              np
             1180  LOAD_METHOD              zeros
             1182  LOAD_FAST                'output_model_samples'
             1184  LOAD_ATTR                shape
             1186  CALL_METHOD_1         1  '1 positional argument'
             1188  LOAD_FAST                'components'
             1190  LOAD_STR                 'lm'
             1192  STORE_SUBSCR     
           1194_0  COME_FROM          1176  '1176'
           1194_1  COME_FROM_LOOP     1140  '1140'

 L.1645      1194  LOAD_FAST                'self'
             1196  LOAD_ATTR                modeltype
             1198  LOAD_STR                 'lc'
             1200  COMPARE_OP               ==
         1202_1204  POP_JUMP_IF_FALSE  1278  'to 1278'

 L.1646      1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                global_model
         1210_1212  POP_JUMP_IF_FALSE  1260  'to 1260'

 L.1647      1214  BUILD_MAP_0           0 
             1216  LOAD_FAST                'components'
             1218  LOAD_STR                 'transit'
             1220  STORE_SUBSCR     

 L.1648      1222  SETUP_LOOP         1276  'to 1276'
             1224  LOAD_FAST                'instruments'
             1226  GET_ITER         
             1228  FOR_ITER           1256  'to 1256'
             1230  STORE_FAST               'ginstrument'

 L.1649      1232  LOAD_GLOBAL              np
             1234  LOAD_METHOD              zeros
             1236  LOAD_FAST                'output_model_samples'
             1238  LOAD_ATTR                shape
             1240  CALL_METHOD_1         1  '1 positional argument'
             1242  LOAD_FAST                'components'
             1244  LOAD_STR                 'transit'
             1246  BINARY_SUBSCR    
             1248  LOAD_FAST                'ginstrument'
             1250  STORE_SUBSCR     
         1252_1254  JUMP_BACK          1228  'to 1228'
             1256  POP_BLOCK        
             1258  JUMP_FORWARD       1276  'to 1276'
           1260_0  COME_FROM          1210  '1210'

 L.1651      1260  LOAD_GLOBAL              np
             1262  LOAD_METHOD              zeros
             1264  LOAD_FAST                'output_model_samples'
             1266  LOAD_ATTR                shape
             1268  CALL_METHOD_1         1  '1 positional argument'
             1270  LOAD_FAST                'components'
             1272  LOAD_STR                 'transit'
             1274  STORE_SUBSCR     
           1276_0  COME_FROM          1258  '1258'
           1276_1  COME_FROM_LOOP     1222  '1222'
             1276  JUMP_FORWARD       1388  'to 1388'
           1278_0  COME_FROM          1202  '1202'

 L.1653      1278  LOAD_GLOBAL              np
             1280  LOAD_METHOD              zeros
             1282  LOAD_FAST                'output_model_samples'
             1284  LOAD_ATTR                shape
             1286  CALL_METHOD_1         1  '1 positional argument'
             1288  LOAD_FAST                'components'
             1290  LOAD_STR                 'keplerian'
             1292  STORE_SUBSCR     

 L.1654      1294  LOAD_GLOBAL              np
             1296  LOAD_METHOD              zeros
             1298  LOAD_FAST                'output_model_samples'
             1300  LOAD_ATTR                shape
             1302  CALL_METHOD_1         1  '1 positional argument'
             1304  LOAD_FAST                'components'
             1306  LOAD_STR                 'trend'
             1308  STORE_SUBSCR     

 L.1655      1310  LOAD_FAST                'self'
             1312  LOAD_ATTR                global_model
         1314_1316  POP_JUMP_IF_FALSE  1368  'to 1368'

 L.1656      1318  BUILD_MAP_0           0 
             1320  LOAD_FAST                'components'
             1322  LOAD_STR                 'mu'
             1324  STORE_SUBSCR     

 L.1657      1326  SETUP_LOOP         1388  'to 1388'
             1328  LOAD_FAST                'instruments'
             1330  GET_ITER         
             1332  FOR_ITER           1364  'to 1364'
             1334  STORE_FAST               'ginstrument'

 L.1658      1336  LOAD_GLOBAL              np
             1338  LOAD_METHOD              zeros
             1340  LOAD_FAST                'output_model_samples'
             1342  LOAD_ATTR                shape
             1344  LOAD_CONST               0
             1346  BINARY_SUBSCR    
             1348  CALL_METHOD_1         1  '1 positional argument'
             1350  LOAD_FAST                'components'
             1352  LOAD_STR                 'mu'
             1354  BINARY_SUBSCR    
             1356  LOAD_FAST                'ginstrument'
             1358  STORE_SUBSCR     
         1360_1362  JUMP_BACK          1332  'to 1332'
             1364  POP_BLOCK        
             1366  JUMP_FORWARD       1388  'to 1388'
           1368_0  COME_FROM          1314  '1314'

 L.1660      1368  LOAD_GLOBAL              np
             1370  LOAD_METHOD              zeros
             1372  LOAD_FAST                'output_model_samples'
             1374  LOAD_ATTR                shape
             1376  LOAD_CONST               0
             1378  BINARY_SUBSCR    
             1380  CALL_METHOD_1         1  '1 positional argument'
             1382  LOAD_FAST                'components'
             1384  LOAD_STR                 'mu'
             1386  STORE_SUBSCR     
           1388_0  COME_FROM          1366  '1366'
           1388_1  COME_FROM_LOOP     1326  '1326'
           1388_2  COME_FROM          1276  '1276'
           1388_3  COME_FROM           996  '996'

 L.1663      1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                global_model
         1392_1394  POP_JUMP_IF_FALSE  1434  'to 1434'

 L.1664      1396  LOAD_FAST                'self'
             1398  LOAD_ATTR                dictionary
             1400  LOAD_STR                 'global_model'
             1402  BINARY_SUBSCR    
             1404  LOAD_STR                 'GPDetrend'
             1406  BINARY_SUBSCR    
         1408_1410  POP_JUMP_IF_FALSE  1470  'to 1470'

 L.1665      1412  LOAD_GLOBAL              np
             1414  LOAD_METHOD              copy
             1416  LOAD_FAST                'output_model_samples'
             1418  CALL_METHOD_1         1  '1 positional argument'
             1420  STORE_FAST               'output_modelGP_samples'

 L.1666      1422  LOAD_GLOBAL              np
             1424  LOAD_METHOD              copy
             1426  LOAD_FAST                'output_model_samples'
             1428  CALL_METHOD_1         1  '1 positional argument'
             1430  STORE_FAST               'output_modelDET_samples'
             1432  JUMP_FORWARD       1470  'to 1470'
           1434_0  COME_FROM          1392  '1392'

 L.1668      1434  LOAD_FAST                'self'
             1436  LOAD_ATTR                dictionary
             1438  LOAD_FAST                'instrument'
             1440  BINARY_SUBSCR    
             1442  LOAD_STR                 'GPDetrend'
             1444  BINARY_SUBSCR    
         1446_1448  POP_JUMP_IF_FALSE  1470  'to 1470'

 L.1669      1450  LOAD_GLOBAL              np
             1452  LOAD_METHOD              copy
             1454  LOAD_FAST                'output_model_samples'
             1456  CALL_METHOD_1         1  '1 positional argument'
             1458  STORE_FAST               'output_modelGP_samples'

 L.1670      1460  LOAD_GLOBAL              np
             1462  LOAD_METHOD              copy
             1464  LOAD_FAST                'output_model_samples'
             1466  CALL_METHOD_1         1  '1 positional argument'
             1468  STORE_FAST               'output_modelDET_samples'
           1470_0  COME_FROM          1446  '1446'
           1470_1  COME_FROM          1432  '1432'
           1470_2  COME_FROM          1408  '1408'

 L.1673      1470  LOAD_GLOBAL              dict
             1472  LOAD_METHOD              fromkeys
             1474  LOAD_FAST                'parameters'
             1476  CALL_METHOD_1         1  '1 positional argument'
             1478  STORE_FAST               'current_parameter_values'

 L.1677      1480  SETUP_LOOP         1534  'to 1534'
             1482  LOAD_FAST                'parameters'
             1484  GET_ITER         
           1486_0  COME_FROM          1506  '1506'
             1486  FOR_ITER           1532  'to 1532'
             1488  STORE_FAST               'parameter'

 L.1678      1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                priors
             1494  LOAD_FAST                'parameter'
             1496  BINARY_SUBSCR    
             1498  LOAD_STR                 'distribution'
             1500  BINARY_SUBSCR    
             1502  LOAD_STR                 'fixed'
             1504  COMPARE_OP               ==
         1506_1508  POP_JUMP_IF_FALSE  1486  'to 1486'

 L.1679      1510  LOAD_FAST                'self'
             1512  LOAD_ATTR                priors
             1514  LOAD_FAST                'parameter'
             1516  BINARY_SUBSCR    
             1518  LOAD_STR                 'hyperparameters'
             1520  BINARY_SUBSCR    
             1522  LOAD_FAST                'current_parameter_values'
             1524  LOAD_FAST                'parameter'
             1526  STORE_SUBSCR     
         1528_1530  JUMP_BACK          1486  'to 1486'
             1532  POP_BLOCK        
           1534_0  COME_FROM_LOOP     1480  '1480'

 L.1688      1534  LOAD_FAST                't'
             1536  LOAD_CONST               None
             1538  COMPARE_OP               is-not
         1540_1542  POP_JUMP_IF_FALSE  1726  'to 1726'

 L.1689      1544  LOAD_FAST                'self'
             1546  LOAD_ATTR                global_model
         1548_1550  POP_JUMP_IF_FALSE  1640  'to 1640'

 L.1690      1552  LOAD_GLOBAL              np
             1554  LOAD_METHOD              copy
             1556  LOAD_FAST                'self'
             1558  LOAD_ATTR                lm_arguments
             1560  CALL_METHOD_1         1  '1 positional argument'
             1562  STORE_FAST               'original_lm_arguments'

 L.1691      1564  LOAD_FAST                'self'
             1566  LOAD_ATTR                dictionary
             1568  LOAD_STR                 'global_model'
             1570  BINARY_SUBSCR    
             1572  LOAD_STR                 'GPDetrend'
             1574  BINARY_SUBSCR    
         1576_1578  POP_JUMP_IF_FALSE  1726  'to 1726'

 L.1692      1580  LOAD_GLOBAL              np
             1582  LOAD_METHOD              copy
             1584  LOAD_FAST                'self'
             1586  LOAD_ATTR                dictionary
             1588  LOAD_STR                 'global_model'
             1590  BINARY_SUBSCR    
             1592  LOAD_STR                 'noise_model'
             1594  BINARY_SUBSCR    
             1596  LOAD_ATTR                X
             1598  CALL_METHOD_1         1  '1 positional argument'
             1600  LOAD_FAST                'self'
             1602  STORE_ATTR               original_GPregressors

 L.1693      1604  LOAD_FAST                'GPregressors'
             1606  LOAD_FAST                'self'
             1608  LOAD_ATTR                dictionary
             1610  LOAD_STR                 'global_model'
             1612  BINARY_SUBSCR    
             1614  LOAD_STR                 'noise_model'
             1616  BINARY_SUBSCR    
             1618  STORE_ATTR               X

 L.1694      1620  LOAD_FAST                'GPregressors'
             1622  LOAD_CONST               None
             1624  COMPARE_OP               is
         1626_1628  POP_JUMP_IF_FALSE  1726  'to 1726'

 L.1695      1630  LOAD_GLOBAL              Exception
             1632  LOAD_STR                 '\t Gobal model has a GP, and requires a GPregressors to be inputted to be evaluated.'
             1634  CALL_FUNCTION_1       1  '1 positional argument'
             1636  RAISE_VARARGS_1       1  'exception instance'
             1638  JUMP_FORWARD       1726  'to 1726'
           1640_0  COME_FROM          1548  '1548'

 L.1697      1640  LOAD_FAST                'self'
             1642  LOAD_ATTR                dictionary
             1644  LOAD_FAST                'instrument'
             1646  BINARY_SUBSCR    
             1648  LOAD_STR                 'GPDetrend'
             1650  BINARY_SUBSCR    
         1652_1654  POP_JUMP_IF_FALSE  1698  'to 1698'

 L.1698      1656  LOAD_FAST                'GPregressors'
             1658  LOAD_FAST                'self'
             1660  LOAD_ATTR                dictionary
             1662  LOAD_FAST                'instrument'
             1664  BINARY_SUBSCR    
             1666  LOAD_STR                 'noise_model'
             1668  BINARY_SUBSCR    
             1670  STORE_ATTR               X

 L.1699      1672  LOAD_FAST                'GPregressors'
             1674  LOAD_CONST               None
             1676  COMPARE_OP               is
         1678_1680  POP_JUMP_IF_FALSE  1698  'to 1698'

 L.1700      1682  LOAD_GLOBAL              Exception
             1684  LOAD_STR                 '\t Model for instrument '
             1686  LOAD_FAST                'instrument'
             1688  BINARY_ADD       
             1690  LOAD_STR                 ' has a GP, and requires a GPregressors to be inputted to be evaluated.'
             1692  BINARY_ADD       
             1694  CALL_FUNCTION_1       1  '1 positional argument'
             1696  RAISE_VARARGS_1       1  'exception instance'
           1698_0  COME_FROM          1678  '1678'
           1698_1  COME_FROM          1652  '1652'

 L.1701      1698  LOAD_FAST                'self'
             1700  LOAD_ATTR                lm_boolean
             1702  LOAD_FAST                'instrument'
             1704  BINARY_SUBSCR    
         1706_1708  POP_JUMP_IF_FALSE  1726  'to 1726'

 L.1702      1710  LOAD_GLOBAL              np
             1712  LOAD_METHOD              copy
             1714  LOAD_FAST                'self'
             1716  LOAD_ATTR                lm_arguments
             1718  LOAD_FAST                'instrument'
             1720  BINARY_SUBSCR    
             1722  CALL_METHOD_1         1  '1 positional argument'
             1724  STORE_FAST               'original_lm_arguments'
           1726_0  COME_FROM          1706  '1706'
           1726_1  COME_FROM          1638  '1638'
           1726_2  COME_FROM          1626  '1626'
           1726_3  COME_FROM          1576  '1576'
           1726_4  COME_FROM          1540  '1540'

 L.1705      1726  LOAD_CONST               0
             1728  STORE_FAST               'counter'

 L.1706  1730_1732  SETUP_LOOP         3652  'to 3652'
             1734  LOAD_FAST                'idx_samples'
             1736  GET_ITER         
         1738_1740  FOR_ITER           3650  'to 3650'
             1742  STORE_FAST               'i'

 L.1708      1744  SETUP_LOOP         1776  'to 1776'
             1746  LOAD_FAST                'input_parameters'
             1748  GET_ITER         
             1750  FOR_ITER           1774  'to 1774'
             1752  STORE_FAST               'parameter'

 L.1710      1754  LOAD_FAST                'parameter_values'
             1756  LOAD_FAST                'parameter'
             1758  BINARY_SUBSCR    
             1760  LOAD_FAST                'i'
             1762  BINARY_SUBSCR    
             1764  LOAD_FAST                'current_parameter_values'
             1766  LOAD_FAST                'parameter'
             1768  STORE_SUBSCR     
         1770_1772  JUMP_BACK          1750  'to 1750'
             1774  POP_BLOCK        
           1776_0  COME_FROM_LOOP     1744  '1744'

 L.1713      1776  LOAD_FAST                'self'
             1778  LOAD_ATTR                modeltype
             1780  LOAD_STR                 'lc'
             1782  COMPARE_OP               ==
         1784_1786  POP_JUMP_IF_FALSE  1804  'to 1804'

 L.1714      1788  LOAD_FAST                'self'
             1790  LOAD_ATTR                generate_lc_model
             1792  LOAD_FAST                'current_parameter_values'
             1794  LOAD_CONST               True
             1796  LOAD_CONST               ('evaluate_lc',)
             1798  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1800  POP_TOP          
             1802  JUMP_FORWARD       1818  'to 1818'
           1804_0  COME_FROM          1784  '1784'

 L.1716      1804  LOAD_FAST                'self'
             1806  LOAD_ATTR                generate_rv_model
             1808  LOAD_FAST                'current_parameter_values'
             1810  LOAD_CONST               True
             1812  LOAD_CONST               ('evaluate_global_errors',)
             1814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1816  POP_TOP          
           1818_0  COME_FROM          1802  '1802'

 L.1719      1818  LOAD_FAST                'self'
             1820  LOAD_ATTR                global_model
         1822_1824  POP_JUMP_IF_FALSE  1858  'to 1858'

 L.1720      1826  LOAD_FAST                'self'
             1828  LOAD_ATTR                y
             1830  LOAD_FAST                'self'
             1832  LOAD_ATTR                model
             1834  LOAD_STR                 'global'
             1836  BINARY_SUBSCR    
             1838  BINARY_SUBTRACT  
             1840  LOAD_FAST                'self'
             1842  STORE_ATTR               residuals

 L.1721      1844  LOAD_FAST                'self'
             1846  LOAD_ATTR                model
             1848  LOAD_STR                 'global_variances'
             1850  BINARY_SUBSCR    
             1852  LOAD_FAST                'self'
             1854  STORE_ATTR               variances
             1856  JUMP_FORWARD       1884  'to 1884'
           1858_0  COME_FROM          1822  '1822'

 L.1723      1858  LOAD_FAST                'self'
             1860  LOAD_ATTR                data
             1862  LOAD_FAST                'instrument'
             1864  BINARY_SUBSCR    
             1866  LOAD_FAST                'self'
             1868  LOAD_ATTR                model
             1870  LOAD_FAST                'instrument'
             1872  BINARY_SUBSCR    
             1874  LOAD_STR                 'deterministic'
             1876  BINARY_SUBSCR    
             1878  BINARY_SUBTRACT  
             1880  LOAD_FAST                'self'
             1882  STORE_ATTR               residuals
           1884_0  COME_FROM          1856  '1856'

 L.1727      1884  LOAD_FAST                't'
             1886  LOAD_CONST               None
             1888  COMPARE_OP               is-not
         1890_1892  POP_JUMP_IF_FALSE  2436  'to 2436'

 L.1728      1894  LOAD_FAST                'self'
             1896  LOAD_ATTR                modeltype
             1898  LOAD_STR                 'lc'
             1900  COMPARE_OP               ==
         1902_1904  POP_JUMP_IF_FALSE  2242  'to 2242'

 L.1729      1906  LOAD_FAST                'self'
             1908  LOAD_ATTR                global_model
         1910_1912  POP_JUMP_IF_FALSE  2110  'to 2110'

 L.1731      1914  SETUP_LOOP         2066  'to 2066'
             1916  LOAD_FAST                'instruments'
             1918  GET_ITER         
             1920  FOR_ITER           2064  'to 2064'
             1922  STORE_FAST               'ginstrument'

 L.1732      1924  LOAD_FAST                'self'
             1926  LOAD_ATTR                dictionary
             1928  LOAD_FAST                'ginstrument'
             1930  BINARY_SUBSCR    
             1932  LOAD_STR                 'TransitFit'
             1934  BINARY_SUBSCR    
         1936_1938  POP_JUMP_IF_TRUE   1956  'to 1956'
             1940  LOAD_FAST                'self'
             1942  LOAD_ATTR                dictionary
             1944  LOAD_FAST                'ginstrument'
             1946  BINARY_SUBSCR    
             1948  LOAD_STR                 'TransitFitCatwoman'
             1950  BINARY_SUBSCR    
         1952_1954  POP_JUMP_IF_FALSE  1994  'to 1994'
           1956_0  COME_FROM          1936  '1936'

 L.1733      1956  LOAD_FAST                'supersample_params'
             1958  LOAD_FAST                'ginstrument'
             1960  BINARY_SUBSCR    
             1962  LOAD_FAST                'supersample_m'
             1964  LOAD_FAST                'ginstrument'
             1966  BINARY_SUBSCR    
             1968  ROT_TWO          
             1970  LOAD_FAST                'self'
             1972  LOAD_ATTR                model
             1974  LOAD_FAST                'ginstrument'
             1976  BINARY_SUBSCR    
             1978  LOAD_STR                 'params'
             1980  STORE_SUBSCR     
             1982  LOAD_FAST                'self'
             1984  LOAD_ATTR                model
             1986  LOAD_FAST                'ginstrument'
             1988  BINARY_SUBSCR    
             1990  LOAD_STR                 'm'
             1992  STORE_SUBSCR     
           1994_0  COME_FROM          1952  '1952'

 L.1734      1994  LOAD_FAST                'self'
             1996  LOAD_ATTR                lm_boolean
             1998  LOAD_FAST                'ginstrument'
             2000  BINARY_SUBSCR    
         2002_2004  POP_JUMP_IF_FALSE  2020  'to 2020'

 L.1735      2006  LOAD_FAST                'LMregressors'
             2008  LOAD_FAST                'ginstrument'
             2010  BINARY_SUBSCR    
             2012  LOAD_FAST                'self'
             2014  LOAD_ATTR                lm_arguments
             2016  LOAD_FAST                'ginstrument'
             2018  STORE_SUBSCR     
           2020_0  COME_FROM          2002  '2002'

 L.1736      2020  LOAD_GLOBAL              np
             2022  LOAD_METHOD              ones
             2024  LOAD_FAST                'nt'
             2026  CALL_METHOD_1         1  '1 positional argument'
             2028  LOAD_FAST                'self'
             2030  LOAD_ATTR                model
             2032  LOAD_FAST                'ginstrument'
             2034  BINARY_SUBSCR    
             2036  LOAD_STR                 'ones'
             2038  STORE_SUBSCR     

 L.1737      2040  LOAD_FAST                'nt'
             2042  LOAD_FAST                'self'
             2044  LOAD_ATTR                ndatapoints_per_instrument
             2046  LOAD_FAST                'ginstrument'
             2048  STORE_SUBSCR     

 L.1738      2050  LOAD_FAST                'dummy_indexes'
             2052  LOAD_FAST                'self'
             2054  LOAD_ATTR                instrument_indexes
             2056  LOAD_FAST                'ginstrument'
             2058  STORE_SUBSCR     
         2060_2062  JUMP_BACK          1920  'to 1920'
             2064  POP_BLOCK        
           2066_0  COME_FROM_LOOP     1914  '1914'

 L.1739      2066  LOAD_GLOBAL              np
             2068  LOAD_METHOD              copy
             2070  LOAD_FAST                'self'
             2072  LOAD_ATTR                inames
             2074  CALL_METHOD_1         1  '1 positional argument'
             2076  STORE_FAST               'original_inames'

 L.1740      2078  LOAD_FAST                'instrument'
             2080  BUILD_LIST_1          1 
             2082  LOAD_FAST                'self'
             2084  STORE_ATTR               inames

 L.1741      2086  LOAD_FAST                'self'
             2088  LOAD_ATTR                generate_lc_model
             2090  LOAD_FAST                'current_parameter_values'
             2092  LOAD_CONST               False
             2094  LOAD_CONST               True
             2096  LOAD_CONST               ('evaluate_global_errors', 'evaluate_lc')
             2098  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2100  POP_TOP          

 L.1742      2102  LOAD_FAST                'original_inames'
             2104  LOAD_FAST                'self'
             2106  STORE_ATTR               inames
             2108  JUMP_FORWARD       2240  'to 2240'
           2110_0  COME_FROM          1910  '1910'

 L.1745      2110  LOAD_FAST                'self'
             2112  LOAD_ATTR                dictionary
             2114  LOAD_FAST                'instrument'
             2116  BINARY_SUBSCR    
             2118  LOAD_STR                 'TransitFit'
             2120  BINARY_SUBSCR    
         2122_2124  POP_JUMP_IF_TRUE   2142  'to 2142'
             2126  LOAD_FAST                'self'
             2128  LOAD_ATTR                dictionary
             2130  LOAD_FAST                'instrument'
             2132  BINARY_SUBSCR    
             2134  LOAD_STR                 'TransitFitCatwoman'
             2136  BINARY_SUBSCR    
         2138_2140  POP_JUMP_IF_FALSE  2172  'to 2172'
           2142_0  COME_FROM          2122  '2122'

 L.1746      2142  LOAD_FAST                'supersample_params'
             2144  LOAD_FAST                'supersample_m'
             2146  ROT_TWO          
             2148  LOAD_FAST                'self'
             2150  LOAD_ATTR                model
             2152  LOAD_FAST                'instrument'
             2154  BINARY_SUBSCR    
             2156  LOAD_STR                 'params'
             2158  STORE_SUBSCR     
             2160  LOAD_FAST                'self'
             2162  LOAD_ATTR                model
             2164  LOAD_FAST                'instrument'
             2166  BINARY_SUBSCR    
             2168  LOAD_STR                 'm'
             2170  STORE_SUBSCR     
           2172_0  COME_FROM          2138  '2138'

 L.1747      2172  LOAD_FAST                'self'
             2174  LOAD_ATTR                lm_boolean
             2176  LOAD_FAST                'instrument'
             2178  BINARY_SUBSCR    
         2180_2182  POP_JUMP_IF_FALSE  2194  'to 2194'

 L.1748      2184  LOAD_FAST                'LMregressors'
             2186  LOAD_FAST                'self'
             2188  LOAD_ATTR                lm_arguments
             2190  LOAD_FAST                'instrument'
             2192  STORE_SUBSCR     
           2194_0  COME_FROM          2180  '2180'

 L.1749      2194  LOAD_GLOBAL              np
             2196  LOAD_METHOD              ones
             2198  LOAD_FAST                'nt'
             2200  CALL_METHOD_1         1  '1 positional argument'
             2202  LOAD_FAST                'self'
             2204  LOAD_ATTR                model
             2206  LOAD_FAST                'instrument'
             2208  BINARY_SUBSCR    
             2210  LOAD_STR                 'ones'
             2212  STORE_SUBSCR     

 L.1750      2214  LOAD_FAST                'nt'
             2216  LOAD_FAST                'self'
             2218  LOAD_ATTR                ndatapoints_per_instrument
             2220  LOAD_FAST                'instrument'
             2222  STORE_SUBSCR     

 L.1752      2224  LOAD_FAST                'self'
             2226  LOAD_ATTR                generate_lc_model
             2228  LOAD_FAST                'current_parameter_values'
             2230  LOAD_CONST               False
             2232  LOAD_CONST               True
             2234  LOAD_CONST               ('evaluate_global_errors', 'evaluate_lc')
             2236  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2238  POP_TOP          
           2240_0  COME_FROM          2108  '2108'
             2240  JUMP_FORWARD       2436  'to 2436'
           2242_0  COME_FROM          1902  '1902'

 L.1755      2242  LOAD_FAST                't'
             2244  LOAD_FAST                'self'
             2246  STORE_ATTR               t

 L.1756      2248  LOAD_FAST                'self'
             2250  LOAD_ATTR                global_model
         2252_2254  POP_JUMP_IF_FALSE  2380  'to 2380'

 L.1760      2256  LOAD_GLOBAL              np
             2258  LOAD_METHOD              ones
             2260  LOAD_GLOBAL              len
             2262  LOAD_FAST                't'
             2264  CALL_FUNCTION_1       1  '1 positional argument'
             2266  CALL_METHOD_1         1  '1 positional argument'
             2268  LOAD_FAST                'self'
             2270  LOAD_ATTR                model
             2272  LOAD_STR                 'global'
             2274  STORE_SUBSCR     

 L.1761      2276  SETUP_LOOP         2338  'to 2338'
             2278  LOAD_FAST                'instruments'
             2280  GET_ITER         
             2282  FOR_ITER           2336  'to 2336'
             2284  STORE_FAST               'ginstrument'

 L.1762      2286  LOAD_FAST                'self'
             2288  LOAD_ATTR                lm_boolean
             2290  LOAD_FAST                'ginstrument'
             2292  BINARY_SUBSCR    
         2294_2296  POP_JUMP_IF_FALSE  2312  'to 2312'

 L.1763      2298  LOAD_FAST                'LMregressors'
             2300  LOAD_FAST                'ginstrument'
             2302  BINARY_SUBSCR    
             2304  LOAD_FAST                'self'
             2306  LOAD_ATTR                lm_arguments
             2308  LOAD_FAST                'ginstrument'
             2310  STORE_SUBSCR     
           2312_0  COME_FROM          2294  '2294'

 L.1764      2312  LOAD_FAST                't'
             2314  LOAD_FAST                'self'
             2316  LOAD_ATTR                times
             2318  LOAD_FAST                'ginstrument'
             2320  STORE_SUBSCR     

 L.1765      2322  LOAD_FAST                'dummy_indexes'
             2324  LOAD_FAST                'self'
             2326  LOAD_ATTR                instrument_indexes
             2328  LOAD_FAST                'ginstrument'
             2330  STORE_SUBSCR     
         2332_2334  JUMP_BACK          2282  'to 2282'
             2336  POP_BLOCK        
           2338_0  COME_FROM_LOOP     2276  '2276'

 L.1767      2338  LOAD_GLOBAL              np
             2340  LOAD_METHOD              copy
             2342  LOAD_FAST                'self'
             2344  LOAD_ATTR                inames
             2346  CALL_METHOD_1         1  '1 positional argument'
             2348  STORE_FAST               'original_inames'

 L.1768      2350  LOAD_FAST                'instrument'
             2352  BUILD_LIST_1          1 
             2354  LOAD_FAST                'self'
             2356  STORE_ATTR               inames

 L.1769      2358  LOAD_FAST                'self'
             2360  LOAD_ATTR                generate_rv_model
             2362  LOAD_FAST                'current_parameter_values'
             2364  LOAD_CONST               False
             2366  LOAD_CONST               ('evaluate_global_errors',)
             2368  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2370  POP_TOP          

 L.1770      2372  LOAD_FAST                'original_inames'
             2374  LOAD_FAST                'self'
             2376  STORE_ATTR               inames
             2378  JUMP_FORWARD       2436  'to 2436'
           2380_0  COME_FROM          2252  '2252'

 L.1772      2380  LOAD_FAST                't'
             2382  LOAD_FAST                'self'
             2384  LOAD_ATTR                times
             2386  LOAD_FAST                'instrument'
             2388  STORE_SUBSCR     

 L.1773      2390  LOAD_FAST                'dummy_indexes'
             2392  LOAD_FAST                'self'
             2394  LOAD_ATTR                instrument_indexes
             2396  LOAD_FAST                'instrument'
             2398  STORE_SUBSCR     

 L.1774      2400  LOAD_FAST                'self'
             2402  LOAD_ATTR                lm_boolean
             2404  LOAD_FAST                'instrument'
             2406  BINARY_SUBSCR    
         2408_2410  POP_JUMP_IF_FALSE  2422  'to 2422'

 L.1775      2412  LOAD_FAST                'LMregressors'
             2414  LOAD_FAST                'self'
             2416  LOAD_ATTR                lm_arguments
             2418  LOAD_FAST                'instrument'
             2420  STORE_SUBSCR     
           2422_0  COME_FROM          2408  '2408'

 L.1777      2422  LOAD_FAST                'self'
             2424  LOAD_ATTR                generate_rv_model
             2426  LOAD_FAST                'current_parameter_values'
             2428  LOAD_CONST               False
             2430  LOAD_CONST               ('evaluate_global_errors',)
             2432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2434  POP_TOP          
           2436_0  COME_FROM          2378  '2378'
           2436_1  COME_FROM          2240  '2240'
           2436_2  COME_FROM          1890  '1890'

 L.1779      2436  LOAD_FAST                'self'
             2438  LOAD_ATTR                global_model
         2440_2442  POP_JUMP_IF_FALSE  2546  'to 2546'

 L.1780      2444  LOAD_FAST                'self'
             2446  LOAD_ATTR                dictionary
             2448  LOAD_STR                 'global_model'
             2450  BINARY_SUBSCR    
             2452  LOAD_STR                 'GPDetrend'
             2454  BINARY_SUBSCR    
         2456_2458  POP_JUMP_IF_FALSE  2518  'to 2518'

 L.1782      2460  LOAD_FAST                'self'
             2462  LOAD_ATTR                get_GP_plus_deterministic_model
             2464  LOAD_FAST                'current_parameter_values'

 L.1783      2466  LOAD_FAST                'instrument'
             2468  LOAD_CONST               ('instrument',)
             2470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2472  UNPACK_SEQUENCE_3     3 
             2474  LOAD_FAST                'output_modelDET_samples'
             2476  LOAD_FAST                'counter'
             2478  LOAD_CONST               None
             2480  LOAD_CONST               None
             2482  BUILD_SLICE_2         2 
             2484  BUILD_TUPLE_2         2 
             2486  STORE_SUBSCR     
             2488  LOAD_FAST                'output_modelGP_samples'
             2490  LOAD_FAST                'counter'
             2492  LOAD_CONST               None
             2494  LOAD_CONST               None
             2496  BUILD_SLICE_2         2 
             2498  BUILD_TUPLE_2         2 
             2500  STORE_SUBSCR     
             2502  LOAD_FAST                'output_model_samples'
             2504  LOAD_FAST                'counter'
             2506  LOAD_CONST               None
             2508  LOAD_CONST               None
             2510  BUILD_SLICE_2         2 
             2512  BUILD_TUPLE_2         2 
             2514  STORE_SUBSCR     
             2516  JUMP_FORWARD       2544  'to 2544'
           2518_0  COME_FROM          2456  '2456'

 L.1785      2518  LOAD_FAST                'self'
             2520  LOAD_ATTR                get_GP_plus_deterministic_model
             2522  LOAD_FAST                'current_parameter_values'

 L.1786      2524  LOAD_FAST                'instrument'
             2526  LOAD_CONST               ('instrument',)
             2528  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2530  LOAD_FAST                'output_model_samples'
             2532  LOAD_FAST                'counter'
             2534  LOAD_CONST               None
             2536  LOAD_CONST               None
             2538  BUILD_SLICE_2         2 
             2540  BUILD_TUPLE_2         2 
             2542  STORE_SUBSCR     
           2544_0  COME_FROM          2516  '2516'
             2544  JUMP_FORWARD       2646  'to 2646'
           2546_0  COME_FROM          2440  '2440'

 L.1788      2546  LOAD_FAST                'self'
             2548  LOAD_ATTR                dictionary
             2550  LOAD_FAST                'instrument'
             2552  BINARY_SUBSCR    
             2554  LOAD_STR                 'GPDetrend'
             2556  BINARY_SUBSCR    
         2558_2560  POP_JUMP_IF_FALSE  2620  'to 2620'

 L.1790      2562  LOAD_FAST                'self'
             2564  LOAD_ATTR                get_GP_plus_deterministic_model
             2566  LOAD_FAST                'current_parameter_values'

 L.1791      2568  LOAD_FAST                'instrument'
             2570  LOAD_CONST               ('instrument',)
             2572  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2574  UNPACK_SEQUENCE_3     3 
             2576  LOAD_FAST                'output_modelDET_samples'
             2578  LOAD_FAST                'counter'
             2580  LOAD_CONST               None
             2582  LOAD_CONST               None
             2584  BUILD_SLICE_2         2 
             2586  BUILD_TUPLE_2         2 
             2588  STORE_SUBSCR     
             2590  LOAD_FAST                'output_modelGP_samples'
             2592  LOAD_FAST                'counter'
             2594  LOAD_CONST               None
             2596  LOAD_CONST               None
             2598  BUILD_SLICE_2         2 
             2600  BUILD_TUPLE_2         2 
             2602  STORE_SUBSCR     
             2604  LOAD_FAST                'output_model_samples'
             2606  LOAD_FAST                'counter'
             2608  LOAD_CONST               None
             2610  LOAD_CONST               None
             2612  BUILD_SLICE_2         2 
             2614  BUILD_TUPLE_2         2 
             2616  STORE_SUBSCR     
             2618  JUMP_FORWARD       2646  'to 2646'
           2620_0  COME_FROM          2558  '2558'

 L.1793      2620  LOAD_FAST                'self'
             2622  LOAD_ATTR                get_GP_plus_deterministic_model
             2624  LOAD_FAST                'current_parameter_values'

 L.1794      2626  LOAD_FAST                'instrument'
             2628  LOAD_CONST               ('instrument',)
             2630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2632  LOAD_FAST                'output_model_samples'
             2634  LOAD_FAST                'counter'
             2636  LOAD_CONST               None
             2638  LOAD_CONST               None
             2640  BUILD_SLICE_2         2 
             2642  BUILD_TUPLE_2         2 
             2644  STORE_SUBSCR     
           2646_0  COME_FROM          2618  '2618'
           2646_1  COME_FROM          2544  '2544'

 L.1799      2646  LOAD_FAST                'return_components'
         2648_2650  POP_JUMP_IF_FALSE  3266  'to 3266'

 L.1800      2652  LOAD_FAST                'self'
             2654  LOAD_ATTR                modeltype
             2656  LOAD_STR                 'lc'
             2658  COMPARE_OP               ==
         2660_2662  POP_JUMP_IF_FALSE  2960  'to 2960'

 L.1801      2664  LOAD_FAST                'self'
             2666  LOAD_ATTR                global_model
         2668_2670  POP_JUMP_IF_FALSE  2830  'to 2830'

 L.1805      2672  SETUP_LOOP         2828  'to 2828'
             2674  LOAD_FAST                'instruments'
             2676  GET_ITER         
             2678  FOR_ITER           2826  'to 2826'
             2680  STORE_FAST               'ginstrument'

 L.1806      2682  LOAD_CONST               0.0
             2684  STORE_FAST               'transit'

 L.1807      2686  SETUP_LOOP         2794  'to 2794'
             2688  LOAD_FAST                'self'
             2690  LOAD_ATTR                numbering
             2692  GET_ITER         
             2694  FOR_ITER           2792  'to 2792'
             2696  STORE_FAST               'i'

 L.1808      2698  LOAD_FAST                'self'
             2700  LOAD_ATTR                model
             2702  LOAD_FAST                'ginstrument'
             2704  BINARY_SUBSCR    
             2706  LOAD_STR                 'p'
             2708  LOAD_GLOBAL              str
             2710  LOAD_FAST                'i'
             2712  CALL_FUNCTION_1       1  '1 positional argument'
             2714  BINARY_ADD       
             2716  BINARY_SUBSCR    
             2718  LOAD_FAST                'components'
             2720  LOAD_STR                 'p'
             2722  LOAD_GLOBAL              str
             2724  LOAD_FAST                'i'
             2726  CALL_FUNCTION_1       1  '1 positional argument'
             2728  BINARY_ADD       
             2730  BINARY_SUBSCR    
             2732  LOAD_FAST                'ginstrument'
             2734  BINARY_SUBSCR    
             2736  LOAD_FAST                'counter'
             2738  LOAD_CONST               None
             2740  LOAD_CONST               None
             2742  BUILD_SLICE_2         2 
             2744  BUILD_TUPLE_2         2 
             2746  STORE_SUBSCR     

 L.1809      2748  LOAD_FAST                'transit'
             2750  LOAD_FAST                'components'
             2752  LOAD_STR                 'p'
             2754  LOAD_GLOBAL              str
             2756  LOAD_FAST                'i'
             2758  CALL_FUNCTION_1       1  '1 positional argument'
             2760  BINARY_ADD       
             2762  BINARY_SUBSCR    
             2764  LOAD_FAST                'ginstrument'
             2766  BINARY_SUBSCR    
             2768  LOAD_FAST                'counter'
             2770  LOAD_CONST               None
             2772  LOAD_CONST               None
             2774  BUILD_SLICE_2         2 
             2776  BUILD_TUPLE_2         2 
             2778  BINARY_SUBSCR    
             2780  LOAD_CONST               1.0
             2782  BINARY_SUBTRACT  
             2784  INPLACE_ADD      
             2786  STORE_FAST               'transit'
         2788_2790  JUMP_BACK          2694  'to 2694'
             2792  POP_BLOCK        
           2794_0  COME_FROM_LOOP     2686  '2686'

 L.1810      2794  LOAD_CONST               1.0
             2796  LOAD_FAST                'transit'
             2798  BINARY_ADD       
             2800  LOAD_FAST                'components'
             2802  LOAD_STR                 'transit'
             2804  BINARY_SUBSCR    
             2806  LOAD_FAST                'ginstrument'
             2808  BINARY_SUBSCR    
             2810  LOAD_FAST                'counter'
             2812  LOAD_CONST               None
             2814  LOAD_CONST               None
             2816  BUILD_SLICE_2         2 
             2818  BUILD_TUPLE_2         2 
             2820  STORE_SUBSCR     
         2822_2824  JUMP_BACK          2678  'to 2678'
             2826  POP_BLOCK        
           2828_0  COME_FROM_LOOP     2672  '2672'
             2828  JUMP_FORWARD       2958  'to 2958'
           2830_0  COME_FROM          2668  '2668'

 L.1812      2830  LOAD_CONST               0.0
             2832  STORE_FAST               'transit'

 L.1813      2834  SETUP_LOOP         2934  'to 2934'
             2836  LOAD_FAST                'self'
             2838  LOAD_ATTR                numbering
             2840  GET_ITER         
             2842  FOR_ITER           2932  'to 2932'
             2844  STORE_FAST               'i'

 L.1814      2846  LOAD_FAST                'self'
             2848  LOAD_ATTR                model
             2850  LOAD_FAST                'instrument'
             2852  BINARY_SUBSCR    
             2854  LOAD_STR                 'p'
             2856  LOAD_GLOBAL              str
             2858  LOAD_FAST                'i'
             2860  CALL_FUNCTION_1       1  '1 positional argument'
             2862  BINARY_ADD       
             2864  BINARY_SUBSCR    
             2866  LOAD_FAST                'components'
             2868  LOAD_STR                 'p'
             2870  LOAD_GLOBAL              str
             2872  LOAD_FAST                'i'
             2874  CALL_FUNCTION_1       1  '1 positional argument'
             2876  BINARY_ADD       
             2878  BINARY_SUBSCR    
             2880  LOAD_FAST                'counter'
             2882  LOAD_CONST               None
             2884  LOAD_CONST               None
             2886  BUILD_SLICE_2         2 
             2888  BUILD_TUPLE_2         2 
             2890  STORE_SUBSCR     

 L.1815      2892  LOAD_FAST                'transit'
             2894  LOAD_FAST                'components'
             2896  LOAD_STR                 'p'
             2898  LOAD_GLOBAL              str
             2900  LOAD_FAST                'i'
             2902  CALL_FUNCTION_1       1  '1 positional argument'
             2904  BINARY_ADD       
             2906  BINARY_SUBSCR    
             2908  LOAD_FAST                'counter'
             2910  LOAD_CONST               None
             2912  LOAD_CONST               None
             2914  BUILD_SLICE_2         2 
             2916  BUILD_TUPLE_2         2 
             2918  BINARY_SUBSCR    
             2920  LOAD_CONST               1.0
             2922  BINARY_SUBTRACT  
             2924  INPLACE_ADD      
             2926  STORE_FAST               'transit'
         2928_2930  JUMP_BACK          2842  'to 2842'
             2932  POP_BLOCK        
           2934_0  COME_FROM_LOOP     2834  '2834'

 L.1816      2934  LOAD_CONST               1.0
             2936  LOAD_FAST                'transit'
             2938  BINARY_ADD       
             2940  LOAD_FAST                'components'
             2942  LOAD_STR                 'transit'
             2944  BINARY_SUBSCR    
             2946  LOAD_FAST                'counter'
             2948  LOAD_CONST               None
             2950  LOAD_CONST               None
             2952  BUILD_SLICE_2         2 
             2954  BUILD_TUPLE_2         2 
             2956  STORE_SUBSCR     
           2958_0  COME_FROM          2828  '2828'
             2958  JUMP_FORWARD       3152  'to 3152'
           2960_0  COME_FROM          2660  '2660'

 L.1818      2960  SETUP_LOOP         3020  'to 3020'
             2962  LOAD_FAST                'self'
             2964  LOAD_ATTR                numbering
             2966  GET_ITER         
             2968  FOR_ITER           3018  'to 3018'
             2970  STORE_FAST               'i'

 L.1819      2972  LOAD_FAST                'self'
             2974  LOAD_ATTR                model
             2976  LOAD_STR                 'p'
             2978  LOAD_GLOBAL              str
             2980  LOAD_FAST                'i'
             2982  CALL_FUNCTION_1       1  '1 positional argument'
             2984  BINARY_ADD       
             2986  BINARY_SUBSCR    
             2988  LOAD_FAST                'components'
             2990  LOAD_STR                 'p'
             2992  LOAD_GLOBAL              str
             2994  LOAD_FAST                'i'
             2996  CALL_FUNCTION_1       1  '1 positional argument'
             2998  BINARY_ADD       
             3000  BINARY_SUBSCR    
             3002  LOAD_FAST                'counter'
             3004  LOAD_CONST               None
             3006  LOAD_CONST               None
             3008  BUILD_SLICE_2         2 
             3010  BUILD_TUPLE_2         2 
             3012  STORE_SUBSCR     
         3014_3016  JUMP_BACK          2968  'to 2968'
             3018  POP_BLOCK        
           3020_0  COME_FROM_LOOP     2960  '2960'

 L.1820      3020  LOAD_FAST                'self'
             3022  LOAD_ATTR                model
             3024  LOAD_STR                 'Keplerian+Trend'
             3026  BINARY_SUBSCR    
             3028  LOAD_FAST                'self'
             3030  LOAD_ATTR                model
             3032  LOAD_STR                 'Keplerian'
             3034  BINARY_SUBSCR    
             3036  BINARY_SUBTRACT  
             3038  LOAD_FAST                'components'
             3040  LOAD_STR                 'trend'
             3042  BINARY_SUBSCR    
             3044  LOAD_FAST                'counter'
             3046  LOAD_CONST               None
             3048  LOAD_CONST               None
             3050  BUILD_SLICE_2         2 
             3052  BUILD_TUPLE_2         2 
             3054  STORE_SUBSCR     

 L.1821      3056  LOAD_FAST                'self'
             3058  LOAD_ATTR                model
             3060  LOAD_STR                 'Keplerian'
             3062  BINARY_SUBSCR    
             3064  LOAD_FAST                'components'
             3066  LOAD_STR                 'keplerian'
             3068  BINARY_SUBSCR    
             3070  LOAD_FAST                'counter'
             3072  LOAD_CONST               None
             3074  LOAD_CONST               None
             3076  BUILD_SLICE_2         2 
             3078  BUILD_TUPLE_2         2 
             3080  STORE_SUBSCR     

 L.1822      3082  LOAD_FAST                'self'
             3084  LOAD_ATTR                global_model
         3086_3088  POP_JUMP_IF_FALSE  3132  'to 3132'

 L.1823      3090  SETUP_LOOP         3152  'to 3152'
             3092  LOAD_FAST                'instruments'
             3094  GET_ITER         
             3096  FOR_ITER           3128  'to 3128'
             3098  STORE_FAST               'ginstrument'

 L.1824      3100  LOAD_FAST                'current_parameter_values'
             3102  LOAD_STR                 'mu_'
             3104  LOAD_FAST                'ginstrument'
             3106  BINARY_ADD       
             3108  BINARY_SUBSCR    
             3110  LOAD_FAST                'components'
             3112  LOAD_STR                 'mu'
             3114  BINARY_SUBSCR    
             3116  LOAD_FAST                'ginstrument'
             3118  BINARY_SUBSCR    
             3120  LOAD_FAST                'counter'
             3122  STORE_SUBSCR     
         3124_3126  JUMP_BACK          3096  'to 3096'
             3128  POP_BLOCK        
             3130  JUMP_FORWARD       3152  'to 3152'
           3132_0  COME_FROM          3086  '3086'

 L.1826      3132  LOAD_FAST                'current_parameter_values'
             3134  LOAD_STR                 'mu_'
             3136  LOAD_FAST                'instrument'
             3138  BINARY_ADD       
             3140  BINARY_SUBSCR    
             3142  LOAD_FAST                'components'
             3144  LOAD_STR                 'mu'
             3146  BINARY_SUBSCR    
             3148  LOAD_FAST                'counter'
             3150  STORE_SUBSCR     
           3152_0  COME_FROM          3130  '3130'
           3152_1  COME_FROM_LOOP     3090  '3090'
           3152_2  COME_FROM          2958  '2958'

 L.1827      3152  LOAD_FAST                'self'
             3154  LOAD_ATTR                global_model
         3156_3158  POP_JUMP_IF_FALSE  3224  'to 3224'

 L.1828      3160  SETUP_LOOP         3266  'to 3266'
             3162  LOAD_FAST                'instruments'
             3164  GET_ITER         
           3166_0  COME_FROM          3178  '3178'
             3166  FOR_ITER           3220  'to 3220'
             3168  STORE_FAST               'ginstrument'

 L.1829      3170  LOAD_FAST                'self'
             3172  LOAD_ATTR                lm_boolean
             3174  LOAD_FAST                'ginstrument'
             3176  BINARY_SUBSCR    
         3178_3180  POP_JUMP_IF_FALSE  3166  'to 3166'

 L.1830      3182  LOAD_FAST                'self'
             3184  LOAD_ATTR                model
             3186  LOAD_FAST                'ginstrument'
             3188  BINARY_SUBSCR    
             3190  LOAD_STR                 'LM'
             3192  BINARY_SUBSCR    
             3194  LOAD_FAST                'components'
             3196  LOAD_STR                 'lm'
             3198  BINARY_SUBSCR    
             3200  LOAD_FAST                'ginstrument'
             3202  BINARY_SUBSCR    
             3204  LOAD_FAST                'counter'
             3206  LOAD_CONST               None
             3208  LOAD_CONST               None
             3210  BUILD_SLICE_2         2 
             3212  BUILD_TUPLE_2         2 
             3214  STORE_SUBSCR     
         3216_3218  JUMP_BACK          3166  'to 3166'
             3220  POP_BLOCK        
             3222  JUMP_FORWARD       3266  'to 3266'
           3224_0  COME_FROM          3156  '3156'

 L.1832      3224  LOAD_FAST                'self'
             3226  LOAD_ATTR                lm_boolean
             3228  LOAD_FAST                'instrument'
             3230  BINARY_SUBSCR    
         3232_3234  POP_JUMP_IF_FALSE  3266  'to 3266'

 L.1833      3236  LOAD_FAST                'self'
             3238  LOAD_ATTR                model
             3240  LOAD_FAST                'instrument'
             3242  BINARY_SUBSCR    
             3244  LOAD_STR                 'LM'
             3246  BINARY_SUBSCR    
             3248  LOAD_FAST                'components'
             3250  LOAD_STR                 'lm'
             3252  BINARY_SUBSCR    
             3254  LOAD_FAST                'counter'
             3256  LOAD_CONST               None
             3258  LOAD_CONST               None
             3260  BUILD_SLICE_2         2 
             3262  BUILD_TUPLE_2         2 
             3264  STORE_SUBSCR     
           3266_0  COME_FROM          3232  '3232'
           3266_1  COME_FROM          3222  '3222'
           3266_2  COME_FROM_LOOP     3160  '3160'
           3266_3  COME_FROM          2648  '2648'

 L.1836      3266  LOAD_FAST                't'
             3268  LOAD_CONST               None
             3270  COMPARE_OP               is-not
         3272_3274  POP_JUMP_IF_FALSE  3638  'to 3638'

 L.1837      3276  LOAD_FAST                'self'
             3278  LOAD_ATTR                global_model
         3280_3282  POP_JUMP_IF_FALSE  3500  'to 3500'

 L.1838      3284  LOAD_FAST                'original_instrument_indexes'
             3286  LOAD_METHOD              copy
             3288  CALL_METHOD_0         0  '0 positional arguments'
             3290  LOAD_FAST                'self'
             3292  STORE_ATTR               instrument_indexes

 L.1839      3294  SETUP_LOOP         3498  'to 3498'
             3296  LOAD_FAST                'instruments'
             3298  GET_ITER         
             3300  FOR_ITER           3496  'to 3496'
             3302  STORE_FAST               'ginstrument'

 L.1840      3304  LOAD_FAST                'original_instrument_times'
             3306  LOAD_FAST                'ginstrument'
             3308  BINARY_SUBSCR    
             3310  LOAD_FAST                'self'
             3312  LOAD_ATTR                times
             3314  LOAD_FAST                'ginstrument'
             3316  STORE_SUBSCR     

 L.1841      3318  LOAD_FAST                'self'
             3320  LOAD_ATTR                modeltype
             3322  LOAD_STR                 'lc'
             3324  COMPARE_OP               ==
         3326_3328  POP_JUMP_IF_FALSE  3452  'to 3452'

 L.1842      3330  LOAD_FAST                'self'
             3332  LOAD_ATTR                dictionary
             3334  LOAD_FAST                'ginstrument'
             3336  BINARY_SUBSCR    
             3338  LOAD_STR                 'TransitFit'
             3340  BINARY_SUBSCR    
         3342_3344  POP_JUMP_IF_TRUE   3362  'to 3362'
             3346  LOAD_FAST                'self'
             3348  LOAD_ATTR                dictionary
             3350  LOAD_FAST                'ginstrument'
             3352  BINARY_SUBSCR    
             3354  LOAD_STR                 'TransitFitCatwoman'
             3356  BINARY_SUBSCR    
         3358_3360  POP_JUMP_IF_FALSE  3400  'to 3400'
           3362_0  COME_FROM          3342  '3342'

 L.1843      3362  LOAD_FAST                'sample_params'
             3364  LOAD_FAST                'ginstrument'
             3366  BINARY_SUBSCR    
             3368  LOAD_FAST                'sample_m'
             3370  LOAD_FAST                'ginstrument'
             3372  BINARY_SUBSCR    
             3374  ROT_TWO          
             3376  LOAD_FAST                'self'
             3378  LOAD_ATTR                model
             3380  LOAD_FAST                'ginstrument'
             3382  BINARY_SUBSCR    
             3384  LOAD_STR                 'params'
             3386  STORE_SUBSCR     
             3388  LOAD_FAST                'self'
             3390  LOAD_ATTR                model
             3392  LOAD_FAST                'ginstrument'
             3394  BINARY_SUBSCR    
             3396  LOAD_STR                 'm'
             3398  STORE_SUBSCR     
           3400_0  COME_FROM          3358  '3358'

 L.1844      3400  LOAD_FAST                'self'
             3402  LOAD_ATTR                lm_boolean
             3404  LOAD_FAST                'ginstrument'
             3406  BINARY_SUBSCR    
         3408_3410  POP_JUMP_IF_FALSE  3426  'to 3426'

 L.1845      3412  LOAD_FAST                'original_lm_arguments'
             3414  LOAD_FAST                'ginstrument'
             3416  BINARY_SUBSCR    
             3418  LOAD_FAST                'self'
             3420  LOAD_ATTR                lm_arguments
             3422  LOAD_FAST                'ginstrument'
             3424  STORE_SUBSCR     
           3426_0  COME_FROM          3408  '3408'

 L.1846      3426  LOAD_GLOBAL              np
             3428  LOAD_METHOD              ones
             3430  LOAD_FAST                'nt_original'
             3432  LOAD_FAST                'ginstrument'
             3434  BINARY_SUBSCR    
             3436  CALL_METHOD_1         1  '1 positional argument'
             3438  LOAD_FAST                'self'
             3440  LOAD_ATTR                model
             3442  LOAD_FAST                'ginstrument'
             3444  BINARY_SUBSCR    
             3446  LOAD_STR                 'ones'
             3448  STORE_SUBSCR     
             3450  JUMP_FORWARD       3478  'to 3478'
           3452_0  COME_FROM          3326  '3326'

 L.1848      3452  LOAD_FAST                'original_t'
             3454  LOAD_FAST                'self'
             3456  STORE_ATTR               t

 L.1849      3458  LOAD_GLOBAL              np
             3460  LOAD_METHOD              ones
             3462  LOAD_GLOBAL              len
             3464  LOAD_FAST                'original_t'
             3466  CALL_FUNCTION_1       1  '1 positional argument'
             3468  CALL_METHOD_1         1  '1 positional argument'
             3470  LOAD_FAST                'self'
             3472  LOAD_ATTR                model
             3474  LOAD_STR                 'global'
             3476  STORE_SUBSCR     
           3478_0  COME_FROM          3450  '3450'

 L.1850      3478  LOAD_FAST                'nt_original'
             3480  LOAD_FAST                'ginstrument'
             3482  BINARY_SUBSCR    
             3484  LOAD_FAST                'self'
             3486  LOAD_ATTR                ndatapoints_per_instrument
             3488  LOAD_FAST                'ginstrument'
             3490  STORE_SUBSCR     
         3492_3494  JUMP_BACK          3300  'to 3300'
             3496  POP_BLOCK        
           3498_0  COME_FROM_LOOP     3294  '3294'
             3498  JUMP_FORWARD       3638  'to 3638'
           3500_0  COME_FROM          3280  '3280'

 L.1852      3500  LOAD_FAST                'original_instrument_times'
             3502  LOAD_FAST                'self'
             3504  LOAD_ATTR                times
             3506  LOAD_FAST                'instrument'
             3508  STORE_SUBSCR     

 L.1853      3510  LOAD_FAST                'self'
             3512  LOAD_ATTR                modeltype
             3514  LOAD_STR                 'lc'
             3516  COMPARE_OP               ==
         3518_3520  POP_JUMP_IF_FALSE  3612  'to 3612'

 L.1854      3522  LOAD_FAST                'self'
             3524  LOAD_ATTR                dictionary
             3526  LOAD_FAST                'instrument'
             3528  BINARY_SUBSCR    
             3530  LOAD_STR                 'TransitFit'
             3532  BINARY_SUBSCR    
         3534_3536  POP_JUMP_IF_FALSE  3568  'to 3568'

 L.1855      3538  LOAD_FAST                'sample_params'
             3540  LOAD_FAST                'sample_m'
             3542  ROT_TWO          
             3544  LOAD_FAST                'self'
             3546  LOAD_ATTR                model
             3548  LOAD_FAST                'instrument'
             3550  BINARY_SUBSCR    
             3552  LOAD_STR                 'params'
             3554  STORE_SUBSCR     
             3556  LOAD_FAST                'self'
             3558  LOAD_ATTR                model
             3560  LOAD_FAST                'instrument'
             3562  BINARY_SUBSCR    
             3564  LOAD_STR                 'm'
             3566  STORE_SUBSCR     
           3568_0  COME_FROM          3534  '3534'

 L.1856      3568  LOAD_FAST                'self'
             3570  LOAD_ATTR                lm_boolean
             3572  LOAD_FAST                'instrument'
             3574  BINARY_SUBSCR    
         3576_3578  POP_JUMP_IF_FALSE  3590  'to 3590'

 L.1857      3580  LOAD_FAST                'original_lm_arguments'
             3582  LOAD_FAST                'self'
             3584  LOAD_ATTR                lm_arguments
             3586  LOAD_FAST                'instrument'
             3588  STORE_SUBSCR     
           3590_0  COME_FROM          3576  '3576'

 L.1858      3590  LOAD_GLOBAL              np
             3592  LOAD_METHOD              ones
             3594  LOAD_FAST                'nt_original'
             3596  CALL_METHOD_1         1  '1 positional argument'
             3598  LOAD_FAST                'self'
             3600  LOAD_ATTR                model
             3602  LOAD_FAST                'instrument'
             3604  BINARY_SUBSCR    
             3606  LOAD_STR                 'ones'
             3608  STORE_SUBSCR     
             3610  JUMP_FORWARD       3628  'to 3628'
           3612_0  COME_FROM          3518  '3518'

 L.1860      3612  LOAD_FAST                'original_t'
             3614  LOAD_FAST                'self'
             3616  STORE_ATTR               t

 L.1861      3618  LOAD_FAST                'original_instrument_index'
             3620  LOAD_FAST                'self'
             3622  LOAD_ATTR                instrument_indexes
             3624  LOAD_FAST                'instrument'
             3626  STORE_SUBSCR     
           3628_0  COME_FROM          3610  '3610'

 L.1862      3628  LOAD_FAST                'nt_original'
             3630  LOAD_FAST                'self'
             3632  LOAD_ATTR                ndatapoints_per_instrument
             3634  LOAD_FAST                'instrument'
             3636  STORE_SUBSCR     
           3638_0  COME_FROM          3498  '3498'
           3638_1  COME_FROM          3272  '3272'

 L.1864      3638  LOAD_FAST                'counter'
             3640  LOAD_CONST               1
             3642  INPLACE_ADD      
             3644  STORE_FAST               'counter'
         3646_3648  JUMP_BACK          1738  'to 1738'
             3650  POP_BLOCK        
           3652_0  COME_FROM_LOOP     1730  '1730'

 L.1866      3652  LOAD_FAST                'return_err'
         3654_3656  POP_JUMP_IF_FALSE  4416  'to 4416'

 L.1867      3658  LOAD_GLOBAL              np
             3660  LOAD_METHOD              zeros
             3662  LOAD_FAST                'output_model_samples'
             3664  LOAD_ATTR                shape
             3666  LOAD_CONST               1
             3668  BINARY_SUBSCR    
             3670  CALL_METHOD_1         1  '1 positional argument'

 L.1868      3672  LOAD_GLOBAL              np
             3674  LOAD_METHOD              zeros
             3676  LOAD_FAST                'output_model_samples'
             3678  LOAD_ATTR                shape
             3680  LOAD_CONST               1
             3682  BINARY_SUBSCR    
             3684  CALL_METHOD_1         1  '1 positional argument'

 L.1869      3686  LOAD_GLOBAL              np
             3688  LOAD_METHOD              zeros
             3690  LOAD_FAST                'output_model_samples'
             3692  LOAD_ATTR                shape
             3694  LOAD_CONST               1
             3696  BINARY_SUBSCR    
             3698  CALL_METHOD_1         1  '1 positional argument'
             3700  ROT_THREE        
             3702  ROT_TWO          
             3704  STORE_FAST               'm_output_model'
             3706  STORE_FAST               'u_output_model'
             3708  STORE_FAST               'l_output_model'

 L.1870      3710  LOAD_FAST                'self'
             3712  LOAD_ATTR                global_model
         3714_3716  POP_JUMP_IF_FALSE  4056  'to 4056'

 L.1871      3718  LOAD_FAST                'self'
             3720  LOAD_ATTR                dictionary
             3722  LOAD_STR                 'global_model'
             3724  BINARY_SUBSCR    
             3726  LOAD_STR                 'GPDetrend'
             3728  BINARY_SUBSCR    
         3730_3732  POP_JUMP_IF_FALSE  3802  'to 3802'

 L.1872      3734  LOAD_GLOBAL              np
             3736  LOAD_METHOD              copy
             3738  LOAD_FAST                'm_output_model'
             3740  CALL_METHOD_1         1  '1 positional argument'
             3742  LOAD_GLOBAL              np
             3744  LOAD_METHOD              copy
             3746  LOAD_FAST                'u_output_model'
             3748  CALL_METHOD_1         1  '1 positional argument'

 L.1873      3750  LOAD_GLOBAL              np
             3752  LOAD_METHOD              copy
             3754  LOAD_FAST                'l_output_model'
             3756  CALL_METHOD_1         1  '1 positional argument'
             3758  ROT_THREE        
             3760  ROT_TWO          
             3762  STORE_FAST               'mDET_output_model'
             3764  STORE_FAST               'uDET_output_model'
             3766  STORE_FAST               'lDET_output_model'

 L.1875      3768  LOAD_GLOBAL              np
             3770  LOAD_METHOD              copy
             3772  LOAD_FAST                'm_output_model'
             3774  CALL_METHOD_1         1  '1 positional argument'
             3776  LOAD_GLOBAL              np
             3778  LOAD_METHOD              copy
             3780  LOAD_FAST                'u_output_model'
             3782  CALL_METHOD_1         1  '1 positional argument'

 L.1876      3784  LOAD_GLOBAL              np
             3786  LOAD_METHOD              copy
             3788  LOAD_FAST                'l_output_model'
             3790  CALL_METHOD_1         1  '1 positional argument'
             3792  ROT_THREE        
             3794  ROT_TWO          
             3796  STORE_FAST               'mGP_output_model'
             3798  STORE_FAST               'uGP_output_model'
             3800  STORE_FAST               'lGP_output_model'
           3802_0  COME_FROM          3730  '3730'

 L.1877      3802  SETUP_LOOP         3970  'to 3970'
             3804  LOAD_GLOBAL              range
             3806  LOAD_FAST                'output_model_samples'
             3808  LOAD_ATTR                shape
             3810  LOAD_CONST               1
             3812  BINARY_SUBSCR    
             3814  CALL_FUNCTION_1       1  '1 positional argument'
             3816  GET_ITER         
           3818_0  COME_FROM          3876  '3876'
             3818  FOR_ITER           3968  'to 3968'
             3820  STORE_FAST               'i'

 L.1878      3822  LOAD_GLOBAL              get_quantiles
             3824  LOAD_FAST                'output_model_samples'
             3826  LOAD_CONST               None
             3828  LOAD_CONST               None
             3830  BUILD_SLICE_2         2 
             3832  LOAD_FAST                'i'
             3834  BUILD_TUPLE_2         2 
             3836  BINARY_SUBSCR    
             3838  LOAD_FAST                'alpha'
             3840  LOAD_CONST               ('alpha',)
             3842  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3844  UNPACK_SEQUENCE_3     3 
             3846  LOAD_FAST                'm_output_model'
             3848  LOAD_FAST                'i'
             3850  STORE_SUBSCR     
             3852  LOAD_FAST                'u_output_model'
             3854  LOAD_FAST                'i'
             3856  STORE_SUBSCR     
             3858  LOAD_FAST                'l_output_model'
             3860  LOAD_FAST                'i'
             3862  STORE_SUBSCR     

 L.1879      3864  LOAD_FAST                'self'
             3866  LOAD_ATTR                dictionary
             3868  LOAD_STR                 'global_model'
             3870  BINARY_SUBSCR    
             3872  LOAD_STR                 'GPDetrend'
             3874  BINARY_SUBSCR    
         3876_3878  POP_JUMP_IF_FALSE  3818  'to 3818'

 L.1880      3880  LOAD_GLOBAL              get_quantiles
             3882  LOAD_FAST                'output_modelDET_samples'
             3884  LOAD_CONST               None
             3886  LOAD_CONST               None
             3888  BUILD_SLICE_2         2 
             3890  LOAD_FAST                'i'
             3892  BUILD_TUPLE_2         2 
             3894  BINARY_SUBSCR    
             3896  LOAD_FAST                'alpha'
             3898  LOAD_CONST               ('alpha',)
             3900  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3902  UNPACK_SEQUENCE_3     3 
             3904  LOAD_FAST                'mDET_output_model'
             3906  LOAD_FAST                'i'
             3908  STORE_SUBSCR     
             3910  LOAD_FAST                'uDET_output_model'
             3912  LOAD_FAST                'i'
             3914  STORE_SUBSCR     
             3916  LOAD_FAST                'lDET_output_model'
             3918  LOAD_FAST                'i'
             3920  STORE_SUBSCR     

 L.1881      3922  LOAD_GLOBAL              get_quantiles
             3924  LOAD_FAST                'output_modelGP_samples'
             3926  LOAD_CONST               None
             3928  LOAD_CONST               None
             3930  BUILD_SLICE_2         2 
             3932  LOAD_FAST                'i'
             3934  BUILD_TUPLE_2         2 
             3936  BINARY_SUBSCR    
             3938  LOAD_FAST                'alpha'
             3940  LOAD_CONST               ('alpha',)
             3942  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3944  UNPACK_SEQUENCE_3     3 
             3946  LOAD_FAST                'mGP_output_model'
             3948  LOAD_FAST                'i'
             3950  STORE_SUBSCR     
             3952  LOAD_FAST                'uGP_output_model'
             3954  LOAD_FAST                'i'
             3956  STORE_SUBSCR     
             3958  LOAD_FAST                'lGP_output_model'
             3960  LOAD_FAST                'i'
             3962  STORE_SUBSCR     
         3964_3966  JUMP_BACK          3818  'to 3818'
             3968  POP_BLOCK        
           3970_0  COME_FROM_LOOP     3802  '3802'

 L.1882      3970  LOAD_FAST                'self'
             3972  LOAD_ATTR                dictionary
             3974  LOAD_STR                 'global_model'
             3976  BINARY_SUBSCR    
             3978  LOAD_STR                 'GPDetrend'
             3980  BINARY_SUBSCR    
         3982_3984  POP_JUMP_IF_FALSE  4414  'to 4414'

 L.1883      3986  LOAD_FAST                'mDET_output_model'
             3988  LOAD_FAST                'mGP_output_model'
             3990  ROT_TWO          
             3992  LOAD_FAST                'self'
             3994  LOAD_ATTR                model
             3996  LOAD_STR                 'deterministic'
             3998  STORE_SUBSCR     
             4000  LOAD_FAST                'self'
             4002  LOAD_ATTR                model
             4004  LOAD_STR                 'GP'
             4006  STORE_SUBSCR     

 L.1884      4008  LOAD_FAST                'uDET_output_model'
             4010  LOAD_FAST                'uGP_output_model'
             4012  ROT_TWO          
             4014  LOAD_FAST                'self'
             4016  LOAD_ATTR                model
             4018  LOAD_STR                 'deterministic_uerror'
             4020  STORE_SUBSCR     
             4022  LOAD_FAST                'self'
             4024  LOAD_ATTR                model
             4026  LOAD_STR                 'GP_uerror'
             4028  STORE_SUBSCR     

 L.1885      4030  LOAD_FAST                'lDET_output_model'
             4032  LOAD_FAST                'lGP_output_model'
             4034  ROT_TWO          
             4036  LOAD_FAST                'self'
             4038  LOAD_ATTR                model
             4040  LOAD_STR                 'deterministic_lerror'
             4042  STORE_SUBSCR     
             4044  LOAD_FAST                'self'
             4046  LOAD_ATTR                model
             4048  LOAD_STR                 'GP_lerror'
             4050  STORE_SUBSCR     
         4052_4054  JUMP_ABSOLUTE      4564  'to 4564'
           4056_0  COME_FROM          3714  '3714'

 L.1887      4056  LOAD_FAST                'self'
             4058  LOAD_ATTR                dictionary
             4060  LOAD_FAST                'instrument'
             4062  BINARY_SUBSCR    
             4064  LOAD_STR                 'GPDetrend'
             4066  BINARY_SUBSCR    
         4068_4070  POP_JUMP_IF_FALSE  4140  'to 4140'

 L.1888      4072  LOAD_GLOBAL              np
             4074  LOAD_METHOD              copy
             4076  LOAD_FAST                'm_output_model'
             4078  CALL_METHOD_1         1  '1 positional argument'
             4080  LOAD_GLOBAL              np
             4082  LOAD_METHOD              copy
             4084  LOAD_FAST                'u_output_model'
             4086  CALL_METHOD_1         1  '1 positional argument'

 L.1889      4088  LOAD_GLOBAL              np
             4090  LOAD_METHOD              copy
             4092  LOAD_FAST                'l_output_model'
             4094  CALL_METHOD_1         1  '1 positional argument'
             4096  ROT_THREE        
             4098  ROT_TWO          
             4100  STORE_FAST               'mDET_output_model'
             4102  STORE_FAST               'uDET_output_model'
             4104  STORE_FAST               'lDET_output_model'

 L.1891      4106  LOAD_GLOBAL              np
             4108  LOAD_METHOD              copy
             4110  LOAD_FAST                'm_output_model'
             4112  CALL_METHOD_1         1  '1 positional argument'
             4114  LOAD_GLOBAL              np
             4116  LOAD_METHOD              copy
             4118  LOAD_FAST                'u_output_model'
             4120  CALL_METHOD_1         1  '1 positional argument'

 L.1892      4122  LOAD_GLOBAL              np
             4124  LOAD_METHOD              copy
             4126  LOAD_FAST                'l_output_model'
             4128  CALL_METHOD_1         1  '1 positional argument'
             4130  ROT_THREE        
             4132  ROT_TWO          
             4134  STORE_FAST               'mGP_output_model'
             4136  STORE_FAST               'uGP_output_model'
             4138  STORE_FAST               'lGP_output_model'
           4140_0  COME_FROM          4068  '4068'

 L.1893      4140  SETUP_LOOP         4308  'to 4308'
             4142  LOAD_GLOBAL              range
             4144  LOAD_FAST                'output_model_samples'
             4146  LOAD_ATTR                shape
             4148  LOAD_CONST               1
             4150  BINARY_SUBSCR    
             4152  CALL_FUNCTION_1       1  '1 positional argument'
             4154  GET_ITER         
           4156_0  COME_FROM          4214  '4214'
             4156  FOR_ITER           4306  'to 4306'
             4158  STORE_FAST               'i'

 L.1894      4160  LOAD_GLOBAL              get_quantiles
             4162  LOAD_FAST                'output_model_samples'
             4164  LOAD_CONST               None
             4166  LOAD_CONST               None
             4168  BUILD_SLICE_2         2 
             4170  LOAD_FAST                'i'
             4172  BUILD_TUPLE_2         2 
             4174  BINARY_SUBSCR    
             4176  LOAD_FAST                'alpha'
             4178  LOAD_CONST               ('alpha',)
             4180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4182  UNPACK_SEQUENCE_3     3 
             4184  LOAD_FAST                'm_output_model'
             4186  LOAD_FAST                'i'
             4188  STORE_SUBSCR     
             4190  LOAD_FAST                'u_output_model'
             4192  LOAD_FAST                'i'
             4194  STORE_SUBSCR     
             4196  LOAD_FAST                'l_output_model'
             4198  LOAD_FAST                'i'
             4200  STORE_SUBSCR     

 L.1895      4202  LOAD_FAST                'self'
             4204  LOAD_ATTR                dictionary
             4206  LOAD_FAST                'instrument'
             4208  BINARY_SUBSCR    
             4210  LOAD_STR                 'GPDetrend'
             4212  BINARY_SUBSCR    
         4214_4216  POP_JUMP_IF_FALSE  4156  'to 4156'

 L.1896      4218  LOAD_GLOBAL              get_quantiles
             4220  LOAD_FAST                'output_modelDET_samples'
             4222  LOAD_CONST               None
             4224  LOAD_CONST               None
             4226  BUILD_SLICE_2         2 
             4228  LOAD_FAST                'i'
             4230  BUILD_TUPLE_2         2 
             4232  BINARY_SUBSCR    
             4234  LOAD_FAST                'alpha'
             4236  LOAD_CONST               ('alpha',)
             4238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4240  UNPACK_SEQUENCE_3     3 
             4242  LOAD_FAST                'mDET_output_model'
             4244  LOAD_FAST                'i'
             4246  STORE_SUBSCR     
             4248  LOAD_FAST                'uDET_output_model'
             4250  LOAD_FAST                'i'
             4252  STORE_SUBSCR     
             4254  LOAD_FAST                'lDET_output_model'
             4256  LOAD_FAST                'i'
             4258  STORE_SUBSCR     

 L.1897      4260  LOAD_GLOBAL              get_quantiles
             4262  LOAD_FAST                'output_modelGP_samples'
             4264  LOAD_CONST               None
             4266  LOAD_CONST               None
             4268  BUILD_SLICE_2         2 
             4270  LOAD_FAST                'i'
             4272  BUILD_TUPLE_2         2 
             4274  BINARY_SUBSCR    
             4276  LOAD_FAST                'alpha'
             4278  LOAD_CONST               ('alpha',)
             4280  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4282  UNPACK_SEQUENCE_3     3 
             4284  LOAD_FAST                'mGP_output_model'
             4286  LOAD_FAST                'i'
             4288  STORE_SUBSCR     
             4290  LOAD_FAST                'uGP_output_model'
             4292  LOAD_FAST                'i'
             4294  STORE_SUBSCR     
             4296  LOAD_FAST                'lGP_output_model'
             4298  LOAD_FAST                'i'
             4300  STORE_SUBSCR     
         4302_4304  JUMP_BACK          4156  'to 4156'
             4306  POP_BLOCK        
           4308_0  COME_FROM_LOOP     4140  '4140'

 L.1898      4308  LOAD_FAST                'self'
             4310  LOAD_ATTR                dictionary
             4312  LOAD_FAST                'instrument'
             4314  BINARY_SUBSCR    
             4316  LOAD_STR                 'GPDetrend'
             4318  BINARY_SUBSCR    
         4320_4322  POP_JUMP_IF_FALSE  4564  'to 4564'

 L.1899      4324  LOAD_FAST                'mDET_output_model'
             4326  LOAD_FAST                'mGP_output_model'
             4328  ROT_TWO          
             4330  LOAD_FAST                'self'
             4332  LOAD_ATTR                model
             4334  LOAD_FAST                'instrument'
             4336  BINARY_SUBSCR    
             4338  LOAD_STR                 'deterministic'
             4340  STORE_SUBSCR     
             4342  LOAD_FAST                'self'
             4344  LOAD_ATTR                model
             4346  LOAD_FAST                'instrument'
             4348  BINARY_SUBSCR    
             4350  LOAD_STR                 'GP'
             4352  STORE_SUBSCR     

 L.1900      4354  LOAD_FAST                'uDET_output_model'
             4356  LOAD_FAST                'uGP_output_model'
             4358  ROT_TWO          
             4360  LOAD_FAST                'self'
             4362  LOAD_ATTR                model
             4364  LOAD_FAST                'instrument'
             4366  BINARY_SUBSCR    
             4368  LOAD_STR                 'deterministic_uerror'
             4370  STORE_SUBSCR     
             4372  LOAD_FAST                'self'
             4374  LOAD_ATTR                model
             4376  LOAD_FAST                'instrument'
             4378  BINARY_SUBSCR    
             4380  LOAD_STR                 'GP_uerror'
             4382  STORE_SUBSCR     

 L.1901      4384  LOAD_FAST                'lDET_output_model'
             4386  LOAD_FAST                'lGP_output_model'
             4388  ROT_TWO          
             4390  LOAD_FAST                'self'
             4392  LOAD_ATTR                model
             4394  LOAD_FAST                'instrument'
             4396  BINARY_SUBSCR    
             4398  LOAD_STR                 'deterministic_lerror'
             4400  STORE_SUBSCR     
             4402  LOAD_FAST                'self'
             4404  LOAD_ATTR                model
             4406  LOAD_FAST                'instrument'
             4408  BINARY_SUBSCR    
             4410  LOAD_STR                 'GP_lerror'
             4412  STORE_SUBSCR     
           4414_0  COME_FROM          3982  '3982'
             4414  JUMP_FORWARD       4564  'to 4564'
           4416_0  COME_FROM          3654  '3654'

 L.1903      4416  LOAD_GLOBAL              np
             4418  LOAD_ATTR                median
             4420  LOAD_FAST                'output_model_samples'
             4422  LOAD_CONST               0
             4424  LOAD_CONST               ('axis',)
             4426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4428  STORE_FAST               'output_model'

 L.1904      4430  LOAD_FAST                'self'
             4432  LOAD_ATTR                global_model
         4434_4436  POP_JUMP_IF_FALSE  4498  'to 4498'

 L.1905      4438  LOAD_FAST                'self'
             4440  LOAD_ATTR                dictionary
             4442  LOAD_STR                 'global_model'
             4444  BINARY_SUBSCR    
             4446  LOAD_STR                 'GPDetrend'
             4448  BINARY_SUBSCR    
         4450_4452  POP_JUMP_IF_FALSE  4564  'to 4564'

 L.1906      4454  LOAD_GLOBAL              np
             4456  LOAD_ATTR                median
             4458  LOAD_FAST                'output_modelDET_samples'
             4460  LOAD_CONST               0
             4462  LOAD_CONST               ('axis',)
             4464  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.1907      4466  LOAD_GLOBAL              np
             4468  LOAD_ATTR                median
             4470  LOAD_FAST                'output_modelGP_samples'
             4472  LOAD_CONST               0
             4474  LOAD_CONST               ('axis',)
             4476  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4478  ROT_TWO          
             4480  LOAD_FAST                'self'
             4482  LOAD_ATTR                model
             4484  LOAD_STR                 'deterministic'
             4486  STORE_SUBSCR     
             4488  LOAD_FAST                'self'
             4490  LOAD_ATTR                model
             4492  LOAD_STR                 'GP'
             4494  STORE_SUBSCR     
             4496  JUMP_FORWARD       4564  'to 4564'
           4498_0  COME_FROM          4434  '4434'

 L.1909      4498  LOAD_FAST                'self'
             4500  LOAD_ATTR                dictionary
             4502  LOAD_FAST                'instrument'
             4504  BINARY_SUBSCR    
             4506  LOAD_STR                 'GPDetrend'
             4508  BINARY_SUBSCR    
         4510_4512  POP_JUMP_IF_FALSE  4564  'to 4564'

 L.1910      4514  LOAD_GLOBAL              np
             4516  LOAD_ATTR                median
             4518  LOAD_FAST                'output_modelDET_samples'
             4520  LOAD_CONST               0
             4522  LOAD_CONST               ('axis',)
             4524  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.1911      4526  LOAD_GLOBAL              np
             4528  LOAD_ATTR                median
             4530  LOAD_FAST                'output_modelGP_samples'
             4532  LOAD_CONST               0
             4534  LOAD_CONST               ('axis',)
             4536  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4538  ROT_TWO          
             4540  LOAD_FAST                'self'
             4542  LOAD_ATTR                model
             4544  LOAD_FAST                'instrument'
             4546  BINARY_SUBSCR    
             4548  LOAD_STR                 'deterministic'
             4550  STORE_SUBSCR     
             4552  LOAD_FAST                'self'
             4554  LOAD_ATTR                model
             4556  LOAD_FAST                'instrument'
             4558  BINARY_SUBSCR    
             4560  LOAD_STR                 'GP'
             4562  STORE_SUBSCR     
           4564_0  COME_FROM          4510  '4510'
           4564_1  COME_FROM          4496  '4496'
           4564_2  COME_FROM          4450  '4450'
           4564_3  COME_FROM          4414  '4414'
           4564_4  COME_FROM          4320  '4320'

 L.1914      4564  LOAD_FAST                'return_components'
         4566_4568  POP_JUMP_IF_FALSE  5662  'to 5662'

 L.1915      4570  LOAD_FAST                'self'
             4572  LOAD_ATTR                modeltype
             4574  LOAD_STR                 'lc'
             4576  COMPARE_OP               ==
         4578_4580  POP_JUMP_IF_FALSE  4702  'to 4702'

 L.1916      4582  LOAD_FAST                'self'
             4584  LOAD_ATTR                global_model
         4586_4588  POP_JUMP_IF_FALSE  4658  'to 4658'

 L.1917      4590  SETUP_LOOP         4700  'to 4700'
             4592  LOAD_FAST                'components'
             4594  LOAD_METHOD              keys
             4596  CALL_METHOD_0         0  '0 positional arguments'
             4598  GET_ITER         
             4600  FOR_ITER           4654  'to 4654'
             4602  STORE_FAST               'k'

 L.1918      4604  SETUP_LOOP         4650  'to 4650'
             4606  LOAD_FAST                'instruments'
             4608  GET_ITER         
             4610  FOR_ITER           4648  'to 4648'
             4612  STORE_FAST               'ginstrument'

 L.1919      4614  LOAD_GLOBAL              np
             4616  LOAD_ATTR                median
             4618  LOAD_FAST                'components'
             4620  LOAD_FAST                'k'
             4622  BINARY_SUBSCR    
             4624  LOAD_FAST                'ginstrument'
             4626  BINARY_SUBSCR    
             4628  LOAD_CONST               0
             4630  LOAD_CONST               ('axis',)
             4632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4634  LOAD_FAST                'components'
             4636  LOAD_FAST                'k'
             4638  BINARY_SUBSCR    
             4640  LOAD_FAST                'ginstrument'
             4642  STORE_SUBSCR     
         4644_4646  JUMP_BACK          4610  'to 4610'
             4648  POP_BLOCK        
           4650_0  COME_FROM_LOOP     4604  '4604'
         4650_4652  JUMP_BACK          4600  'to 4600'
             4654  POP_BLOCK        
             4656  JUMP_FORWARD       4700  'to 4700'
           4658_0  COME_FROM          4586  '4586'

 L.1921      4658  SETUP_LOOP         4876  'to 4876'
             4660  LOAD_FAST                'components'
             4662  LOAD_METHOD              keys
             4664  CALL_METHOD_0         0  '0 positional arguments'
             4666  GET_ITER         
             4668  FOR_ITER           4698  'to 4698'
             4670  STORE_FAST               'k'

 L.1922      4672  LOAD_GLOBAL              np
             4674  LOAD_ATTR                median
             4676  LOAD_FAST                'components'
             4678  LOAD_FAST                'k'
             4680  BINARY_SUBSCR    
             4682  LOAD_CONST               0
             4684  LOAD_CONST               ('axis',)
             4686  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4688  LOAD_FAST                'components'
             4690  LOAD_FAST                'k'
             4692  STORE_SUBSCR     
         4694_4696  JUMP_BACK          4668  'to 4668'
             4698  POP_BLOCK        
           4700_0  COME_FROM_LOOP     4658  '4658'
           4700_1  COME_FROM          4656  '4656'
           4700_2  COME_FROM_LOOP     4590  '4590'
             4700  JUMP_ABSOLUTE      5838  'to 5838'
           4702_0  COME_FROM          4578  '4578'

 L.1924      4702  SETUP_LOOP         4758  'to 4758'
             4704  LOAD_FAST                'self'
             4706  LOAD_ATTR                numbering
             4708  GET_ITER         
             4710  FOR_ITER           4756  'to 4756'
             4712  STORE_FAST               'i'

 L.1925      4714  LOAD_GLOBAL              np
             4716  LOAD_ATTR                median
             4718  LOAD_FAST                'components'
             4720  LOAD_STR                 'p'
             4722  LOAD_GLOBAL              str
             4724  LOAD_FAST                'i'
             4726  CALL_FUNCTION_1       1  '1 positional argument'
             4728  BINARY_ADD       
             4730  BINARY_SUBSCR    
             4732  LOAD_CONST               0
             4734  LOAD_CONST               ('axis',)
             4736  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4738  LOAD_FAST                'components'
             4740  LOAD_STR                 'p'
             4742  LOAD_GLOBAL              str
             4744  LOAD_FAST                'i'
             4746  CALL_FUNCTION_1       1  '1 positional argument'
             4748  BINARY_ADD       
             4750  STORE_SUBSCR     
         4752_4754  JUMP_BACK          4710  'to 4710'
             4756  POP_BLOCK        
           4758_0  COME_FROM_LOOP     4702  '4702'

 L.1926      4758  LOAD_GLOBAL              np
             4760  LOAD_ATTR                median
             4762  LOAD_FAST                'components'
             4764  LOAD_STR                 'trend'
             4766  BINARY_SUBSCR    
             4768  LOAD_CONST               0
             4770  LOAD_CONST               ('axis',)
             4772  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4774  LOAD_FAST                'components'
             4776  LOAD_STR                 'trend'
             4778  STORE_SUBSCR     

 L.1927      4780  LOAD_GLOBAL              np
             4782  LOAD_ATTR                median
             4784  LOAD_FAST                'components'
             4786  LOAD_STR                 'keplerian'
             4788  BINARY_SUBSCR    
             4790  LOAD_CONST               0
             4792  LOAD_CONST               ('axis',)
             4794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4796  LOAD_FAST                'components'
             4798  LOAD_STR                 'keplerian'
             4800  STORE_SUBSCR     

 L.1928      4802  LOAD_FAST                'self'
             4804  LOAD_ATTR                global_model
         4806_4808  POP_JUMP_IF_FALSE  4854  'to 4854'

 L.1929      4810  SETUP_LOOP         4876  'to 4876'
             4812  LOAD_FAST                'instruments'
             4814  GET_ITER         
             4816  FOR_ITER           4850  'to 4850'
             4818  STORE_FAST               'ginstrument'

 L.1930      4820  LOAD_GLOBAL              np
             4822  LOAD_METHOD              median
             4824  LOAD_FAST                'components'
             4826  LOAD_STR                 'mu'
             4828  BINARY_SUBSCR    
             4830  LOAD_FAST                'ginstrument'
             4832  BINARY_SUBSCR    
             4834  CALL_METHOD_1         1  '1 positional argument'
             4836  LOAD_FAST                'components'
             4838  LOAD_STR                 'mu'
             4840  BINARY_SUBSCR    
             4842  LOAD_FAST                'ginstrument'
             4844  STORE_SUBSCR     
         4846_4848  JUMP_BACK          4816  'to 4816'
             4850  POP_BLOCK        
             4852  JUMP_ABSOLUTE      5838  'to 5838'
           4854_0  COME_FROM          4806  '4806'

 L.1932      4854  LOAD_GLOBAL              np
             4856  LOAD_ATTR                median
             4858  LOAD_FAST                'components'
             4860  LOAD_STR                 'mu'
             4862  BINARY_SUBSCR    
             4864  LOAD_CONST               0
             4866  LOAD_CONST               ('axis',)
             4868  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4870  LOAD_FAST                'components'
             4872  LOAD_STR                 'mu'
             4874  STORE_SUBSCR     
           4876_0  COME_FROM_LOOP     4810  '4810'
         4876_4878  JUMP_ABSOLUTE      5838  'to 5838'
           4880_0  COME_FROM           274  '274'

 L.1934      4880  LOAD_FAST                'self'
             4882  LOAD_ATTR                modeltype
             4884  LOAD_STR                 'lc'
             4886  COMPARE_OP               ==
         4888_4890  POP_JUMP_IF_FALSE  4908  'to 4908'

 L.1935      4892  LOAD_FAST                'self'
             4894  LOAD_ATTR                generate_lc_model
             4896  LOAD_FAST                'parameter_values'
             4898  LOAD_CONST               True
             4900  LOAD_CONST               ('evaluate_lc',)
             4902  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4904  POP_TOP          
             4906  JUMP_FORWARD       4918  'to 4918'
           4908_0  COME_FROM          4888  '4888'

 L.1937      4908  LOAD_FAST                'self'
             4910  LOAD_METHOD              generate_rv_model
             4912  LOAD_FAST                'parameter_values'
             4914  CALL_METHOD_1         1  '1 positional argument'
             4916  POP_TOP          
           4918_0  COME_FROM          4906  '4906'

 L.1939      4918  LOAD_FAST                'self'
             4920  LOAD_ATTR                global_model
         4922_4924  POP_JUMP_IF_FALSE  5328  'to 5328'

 L.1940      4926  LOAD_FAST                'self'
             4928  LOAD_ATTR                y
             4930  LOAD_FAST                'self'
             4932  LOAD_ATTR                model
             4934  LOAD_STR                 'global'
             4936  BINARY_SUBSCR    
             4938  BINARY_SUBTRACT  
             4940  LOAD_FAST                'self'
             4942  STORE_ATTR               residuals

 L.1941      4944  LOAD_FAST                'self'
             4946  LOAD_ATTR                model
             4948  LOAD_STR                 'global_variances'
             4950  BINARY_SUBSCR    
             4952  LOAD_FAST                'self'
             4954  STORE_ATTR               variances

 L.1942      4956  LOAD_FAST                'self'
             4958  LOAD_ATTR                dictionary
             4960  LOAD_STR                 'global_model'
             4962  BINARY_SUBSCR    
             4964  LOAD_STR                 'GPDetrend'
             4966  BINARY_SUBSCR    
         4968_4970  POP_JUMP_IF_FALSE  5002  'to 5002'

 L.1943      4972  LOAD_FAST                'self'
             4974  LOAD_METHOD              get_GP_plus_deterministic_model
             4976  LOAD_FAST                'parameter_values'
             4978  CALL_METHOD_1         1  '1 positional argument'
             4980  UNPACK_SEQUENCE_3     3 
             4982  LOAD_FAST                'self'
             4984  LOAD_ATTR                model
             4986  LOAD_STR                 'deterministic'
             4988  STORE_SUBSCR     
             4990  LOAD_FAST                'self'
             4992  LOAD_ATTR                model
             4994  LOAD_STR                 'GP'
             4996  STORE_SUBSCR     
             4998  STORE_FAST               'output_model'
             5000  JUMP_FORWARD       5012  'to 5012'
           5002_0  COME_FROM          4968  '4968'

 L.1945      5002  LOAD_FAST                'self'
             5004  LOAD_METHOD              get_GP_plus_deterministic_model
             5006  LOAD_FAST                'parameter_values'
             5008  CALL_METHOD_1         1  '1 positional argument'
             5010  STORE_FAST               'output_model'
           5012_0  COME_FROM          5000  '5000'

 L.1946      5012  LOAD_FAST                'return_components'
         5014_5016  POP_JUMP_IF_FALSE  5662  'to 5662'

 L.1947      5018  LOAD_FAST                'self'
             5020  LOAD_ATTR                modeltype
             5022  LOAD_STR                 'lc'
             5024  COMPARE_OP               ==
         5026_5028  POP_JUMP_IF_FALSE  5152  'to 5152'

 L.1948      5030  SETUP_LOOP         5274  'to 5274'
             5032  LOAD_FAST                'instruments'
             5034  GET_ITER         
             5036  FOR_ITER           5148  'to 5148'
             5038  STORE_FAST               'ginstrument'

 L.1949      5040  LOAD_CONST               0.0
             5042  STORE_FAST               'transit'

 L.1950      5044  SETUP_LOOP         5128  'to 5128'
             5046  LOAD_FAST                'self'
             5048  LOAD_ATTR                numbering
             5050  GET_ITER         
             5052  FOR_ITER           5126  'to 5126'
             5054  STORE_FAST               'i'

 L.1951      5056  LOAD_FAST                'self'
             5058  LOAD_ATTR                model
             5060  LOAD_FAST                'ginstrument'
             5062  BINARY_SUBSCR    
             5064  LOAD_STR                 'p'
             5066  LOAD_GLOBAL              str
             5068  LOAD_FAST                'i'
             5070  CALL_FUNCTION_1       1  '1 positional argument'
             5072  BINARY_ADD       
             5074  BINARY_SUBSCR    
             5076  LOAD_FAST                'components'
             5078  LOAD_STR                 'p'
             5080  LOAD_GLOBAL              str
             5082  LOAD_FAST                'i'
             5084  CALL_FUNCTION_1       1  '1 positional argument'
             5086  BINARY_ADD       
             5088  BINARY_SUBSCR    
             5090  LOAD_FAST                'ginstrument'
             5092  STORE_SUBSCR     

 L.1952      5094  LOAD_FAST                'transit'
             5096  LOAD_FAST                'components'
             5098  LOAD_STR                 'p'
             5100  LOAD_GLOBAL              str
             5102  LOAD_FAST                'i'
             5104  CALL_FUNCTION_1       1  '1 positional argument'
             5106  BINARY_ADD       
             5108  BINARY_SUBSCR    
             5110  LOAD_FAST                'ginstrument'
             5112  BINARY_SUBSCR    
             5114  LOAD_CONST               1.0
             5116  BINARY_SUBTRACT  
             5118  INPLACE_ADD      
             5120  STORE_FAST               'transit'
         5122_5124  JUMP_BACK          5052  'to 5052'
             5126  POP_BLOCK        
           5128_0  COME_FROM_LOOP     5044  '5044'

 L.1953      5128  LOAD_CONST               1.0
             5130  LOAD_FAST                'transit'
             5132  BINARY_ADD       
             5134  LOAD_FAST                'components'
             5136  LOAD_STR                 'transit'
             5138  BINARY_SUBSCR    
             5140  LOAD_FAST                'ginstrument'
             5142  STORE_SUBSCR     
         5144_5146  JUMP_BACK          5036  'to 5036'
             5148  POP_BLOCK        
             5150  JUMP_FORWARD       5274  'to 5274'
           5152_0  COME_FROM          5026  '5026'

 L.1955      5152  SETUP_LOOP         5200  'to 5200'
             5154  LOAD_FAST                'self'
             5156  LOAD_ATTR                numbering
             5158  GET_ITER         
             5160  FOR_ITER           5198  'to 5198'
             5162  STORE_FAST               'i'

 L.1956      5164  LOAD_FAST                'self'
             5166  LOAD_ATTR                model
             5168  LOAD_STR                 'p'
             5170  LOAD_GLOBAL              str
             5172  LOAD_FAST                'i'
             5174  CALL_FUNCTION_1       1  '1 positional argument'
             5176  BINARY_ADD       
             5178  BINARY_SUBSCR    
             5180  LOAD_FAST                'components'
             5182  LOAD_STR                 'p'
             5184  LOAD_GLOBAL              str
             5186  LOAD_FAST                'i'
             5188  CALL_FUNCTION_1       1  '1 positional argument'
             5190  BINARY_ADD       
             5192  STORE_SUBSCR     
         5194_5196  JUMP_BACK          5160  'to 5160'
             5198  POP_BLOCK        
           5200_0  COME_FROM_LOOP     5152  '5152'

 L.1957      5200  LOAD_FAST                'self'
             5202  LOAD_ATTR                model
             5204  LOAD_STR                 'Keplerian+Trend'
             5206  BINARY_SUBSCR    
             5208  LOAD_FAST                'self'
             5210  LOAD_ATTR                model
             5212  LOAD_STR                 'Keplerian'
             5214  BINARY_SUBSCR    
             5216  BINARY_SUBTRACT  
             5218  LOAD_FAST                'components'
             5220  LOAD_STR                 'trend'
             5222  STORE_SUBSCR     

 L.1958      5224  LOAD_FAST                'self'
             5226  LOAD_ATTR                model
             5228  LOAD_STR                 'Keplerian'
             5230  BINARY_SUBSCR    
             5232  LOAD_FAST                'components'
             5234  LOAD_STR                 'keplerian'
             5236  STORE_SUBSCR     

 L.1959      5238  SETUP_LOOP         5274  'to 5274'
             5240  LOAD_FAST                'instruments'
             5242  GET_ITER         
             5244  FOR_ITER           5272  'to 5272'
             5246  STORE_FAST               'ginstrument'

 L.1960      5248  LOAD_FAST                'parameter_values'
             5250  LOAD_STR                 'mu_'
             5252  LOAD_FAST                'instrument'
             5254  BINARY_ADD       
             5256  BINARY_SUBSCR    
             5258  LOAD_FAST                'components'
             5260  LOAD_STR                 'mu'
             5262  BINARY_SUBSCR    
             5264  LOAD_FAST                'ginstrument'
             5266  STORE_SUBSCR     
         5268_5270  JUMP_BACK          5244  'to 5244'
             5272  POP_BLOCK        
           5274_0  COME_FROM_LOOP     5238  '5238'
           5274_1  COME_FROM          5150  '5150'
           5274_2  COME_FROM_LOOP     5030  '5030'

 L.1961      5274  SETUP_LOOP         5324  'to 5324'
             5276  LOAD_FAST                'instruments'
             5278  GET_ITER         
           5280_0  COME_FROM          5292  '5292'
             5280  FOR_ITER           5322  'to 5322'
             5282  STORE_FAST               'ginstrument'

 L.1962      5284  LOAD_FAST                'self'
             5286  LOAD_ATTR                lm_boolean
             5288  LOAD_FAST                'ginstrument'
             5290  BINARY_SUBSCR    
         5292_5294  POP_JUMP_IF_FALSE  5280  'to 5280'

 L.1963      5296  LOAD_FAST                'self'
             5298  LOAD_ATTR                model
             5300  LOAD_FAST                'ginstrument'
             5302  BINARY_SUBSCR    
             5304  LOAD_STR                 'LM'
             5306  BINARY_SUBSCR    
             5308  LOAD_FAST                'components'
             5310  LOAD_STR                 'lm'
             5312  BINARY_SUBSCR    
             5314  LOAD_FAST                'ginstrument'
             5316  STORE_SUBSCR     
         5318_5320  JUMP_BACK          5280  'to 5280'
             5322  POP_BLOCK        
           5324_0  COME_FROM_LOOP     5274  '5274'
         5324_5326  JUMP_ABSOLUTE      5838  'to 5838'
           5328_0  COME_FROM          4922  '4922'

 L.1965      5328  LOAD_FAST                'self'
             5330  LOAD_ATTR                data
             5332  LOAD_FAST                'instrument'
             5334  BINARY_SUBSCR    
             5336  LOAD_FAST                'self'
             5338  LOAD_ATTR                model
             5340  LOAD_FAST                'instrument'
             5342  BINARY_SUBSCR    
             5344  LOAD_STR                 'deterministic'
             5346  BINARY_SUBSCR    
             5348  BINARY_SUBTRACT  
             5350  LOAD_FAST                'self'
             5352  STORE_ATTR               residuals

 L.1966      5354  LOAD_FAST                'self'
             5356  LOAD_ATTR                dictionary
             5358  LOAD_FAST                'instrument'
             5360  BINARY_SUBSCR    
             5362  LOAD_STR                 'GPDetrend'
             5364  BINARY_SUBSCR    
         5366_5368  POP_JUMP_IF_FALSE  5404  'to 5404'

 L.1967      5370  LOAD_FAST                'self'
             5372  LOAD_ATTR                get_GP_plus_deterministic_model
             5374  LOAD_FAST                'parameter_values'
             5376  LOAD_FAST                'instrument'
             5378  LOAD_CONST               ('instrument',)
             5380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5382  UNPACK_SEQUENCE_3     3 
             5384  LOAD_FAST                'self'
             5386  LOAD_ATTR                model
             5388  LOAD_STR                 'deterministic'
             5390  STORE_SUBSCR     
             5392  LOAD_FAST                'self'
             5394  LOAD_ATTR                model
             5396  LOAD_STR                 'GP'
             5398  STORE_SUBSCR     
             5400  STORE_FAST               'output_model'
             5402  JUMP_FORWARD       5418  'to 5418'
           5404_0  COME_FROM          5366  '5366'

 L.1969      5404  LOAD_FAST                'self'
             5406  LOAD_ATTR                get_GP_plus_deterministic_model
             5408  LOAD_FAST                'parameter_values'
             5410  LOAD_FAST                'instrument'
             5412  LOAD_CONST               ('instrument',)
             5414  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5416  STORE_FAST               'output_model'
           5418_0  COME_FROM          5402  '5402'

 L.1970      5418  LOAD_FAST                'return_components'
         5420_5422  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1971      5424  LOAD_FAST                'self'
             5426  LOAD_ATTR                modeltype
             5428  LOAD_STR                 'lc'
             5430  COMPARE_OP               ==
         5432_5434  POP_JUMP_IF_FALSE  5530  'to 5530'

 L.1973      5436  LOAD_CONST               0.0
             5438  STORE_FAST               'transit'

 L.1974      5440  SETUP_LOOP         5516  'to 5516'
             5442  LOAD_FAST                'self'
             5444  LOAD_ATTR                numbering
             5446  GET_ITER         
             5448  FOR_ITER           5514  'to 5514'
             5450  STORE_FAST               'i'

 L.1975      5452  LOAD_FAST                'self'
             5454  LOAD_ATTR                model
             5456  LOAD_FAST                'instrument'
             5458  BINARY_SUBSCR    
             5460  LOAD_STR                 'p'
             5462  LOAD_GLOBAL              str
             5464  LOAD_FAST                'i'
             5466  CALL_FUNCTION_1       1  '1 positional argument'
             5468  BINARY_ADD       
             5470  BINARY_SUBSCR    
             5472  LOAD_FAST                'components'
             5474  LOAD_STR                 'p'
             5476  LOAD_GLOBAL              str
             5478  LOAD_FAST                'i'
             5480  CALL_FUNCTION_1       1  '1 positional argument'
             5482  BINARY_ADD       
             5484  STORE_SUBSCR     

 L.1976      5486  LOAD_FAST                'transit'
             5488  LOAD_FAST                'components'
             5490  LOAD_STR                 'p'
             5492  LOAD_GLOBAL              str
             5494  LOAD_FAST                'i'
             5496  CALL_FUNCTION_1       1  '1 positional argument'
             5498  BINARY_ADD       
             5500  BINARY_SUBSCR    
             5502  LOAD_CONST               1.0
             5504  BINARY_SUBTRACT  
             5506  INPLACE_ADD      
             5508  STORE_FAST               'transit'
         5510_5512  JUMP_BACK          5448  'to 5448'
             5514  POP_BLOCK        
           5516_0  COME_FROM_LOOP     5440  '5440'

 L.1977      5516  LOAD_CONST               1.0
             5518  LOAD_FAST                'transit'
             5520  BINARY_ADD       
             5522  LOAD_FAST                'components'
             5524  LOAD_STR                 'transit'
             5526  STORE_SUBSCR     
             5528  JUMP_FORWARD       5632  'to 5632'
           5530_0  COME_FROM          5432  '5432'

 L.1979      5530  SETUP_LOOP         5578  'to 5578'
             5532  LOAD_FAST                'self'
             5534  LOAD_ATTR                numbering
             5536  GET_ITER         
             5538  FOR_ITER           5576  'to 5576'
             5540  STORE_FAST               'i'

 L.1980      5542  LOAD_FAST                'self'
             5544  LOAD_ATTR                model
             5546  LOAD_STR                 'p'
             5548  LOAD_GLOBAL              str
             5550  LOAD_FAST                'i'
             5552  CALL_FUNCTION_1       1  '1 positional argument'
             5554  BINARY_ADD       
             5556  BINARY_SUBSCR    
             5558  LOAD_FAST                'components'
             5560  LOAD_STR                 'p'
             5562  LOAD_GLOBAL              str
             5564  LOAD_FAST                'i'
             5566  CALL_FUNCTION_1       1  '1 positional argument'
             5568  BINARY_ADD       
             5570  STORE_SUBSCR     
         5572_5574  JUMP_BACK          5538  'to 5538'
             5576  POP_BLOCK        
           5578_0  COME_FROM_LOOP     5530  '5530'

 L.1981      5578  LOAD_FAST                'self'
             5580  LOAD_ATTR                model
             5582  LOAD_STR                 'Keplerian+Trend'
             5584  BINARY_SUBSCR    
             5586  LOAD_FAST                'self'
             5588  LOAD_ATTR                model
             5590  LOAD_STR                 'Keplerian'
             5592  BINARY_SUBSCR    
             5594  BINARY_SUBTRACT  
             5596  LOAD_FAST                'components'
             5598  LOAD_STR                 'trend'
             5600  STORE_SUBSCR     

 L.1982      5602  LOAD_FAST                'self'
             5604  LOAD_ATTR                model
             5606  LOAD_STR                 'Keplerian'
             5608  BINARY_SUBSCR    
             5610  LOAD_FAST                'components'
             5612  LOAD_STR                 'keplerian'
             5614  STORE_SUBSCR     

 L.1983      5616  LOAD_FAST                'parameter_values'
             5618  LOAD_STR                 'mu_'
             5620  LOAD_FAST                'instrument'
             5622  BINARY_ADD       
             5624  BINARY_SUBSCR    
             5626  LOAD_FAST                'components'
             5628  LOAD_STR                 'mu'
             5630  STORE_SUBSCR     
           5632_0  COME_FROM          5528  '5528'

 L.1984      5632  LOAD_FAST                'self'
             5634  LOAD_ATTR                lm_boolean
             5636  LOAD_FAST                'instrument'
             5638  BINARY_SUBSCR    
         5640_5642  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1985      5644  LOAD_FAST                'self'
             5646  LOAD_ATTR                model
             5648  LOAD_FAST                'instrument'
             5650  BINARY_SUBSCR    
             5652  LOAD_STR                 'LM'
             5654  BINARY_SUBSCR    
             5656  LOAD_FAST                'components'
             5658  LOAD_STR                 'lm'
             5660  STORE_SUBSCR     
           5662_0  COME_FROM          5014  '5014'
           5662_1  COME_FROM          4566  '4566'
             5662  JUMP_FORWARD       5838  'to 5838'
           5664_0  COME_FROM           210  '210'

 L.1988      5664  LOAD_FAST                'self'
             5666  LOAD_ATTR                evaluate_model
             5668  LOAD_FAST                'instrument'
             5670  LOAD_FAST                'self'
             5672  LOAD_ATTR                posteriors
             5674  LOAD_FAST                'resampling'

 L.1989      5676  LOAD_FAST                'nresampling'
             5678  LOAD_FAST                'etresampling'
             5680  LOAD_FAST                'all_samples'

 L.1990      5682  LOAD_FAST                'nsamples'
             5684  LOAD_FAST                'return_samples'
             5686  LOAD_FAST                't'
             5688  LOAD_FAST                'GPregressors'

 L.1991      5690  LOAD_FAST                'LMregressors'
             5692  LOAD_FAST                'return_err'
             5694  LOAD_FAST                'return_components'
             5696  LOAD_FAST                'alpha'
             5698  LOAD_CONST               ('instrument', 'parameter_values', 'resampling', 'nresampling', 'etresampling', 'all_samples', 'nsamples', 'return_samples', 't', 'GPregressors', 'LMregressors', 'return_err', 'return_components', 'alpha')
             5700  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
             5702  STORE_FAST               'x'

 L.1992      5704  LOAD_FAST                'return_samples'
         5706_5708  POP_JUMP_IF_FALSE  5780  'to 5780'

 L.1993      5710  LOAD_FAST                'return_err'
         5712_5714  POP_JUMP_IF_FALSE  5752  'to 5752'

 L.1994      5716  LOAD_FAST                'return_components'
         5718_5720  POP_JUMP_IF_FALSE  5738  'to 5738'

 L.1995      5722  LOAD_FAST                'x'
             5724  UNPACK_SEQUENCE_5     5 
             5726  STORE_FAST               'output_model_samples'
             5728  STORE_FAST               'm_output_model'
             5730  STORE_FAST               'u_output_model'
             5732  STORE_FAST               'l_output_model'
             5734  STORE_FAST               'components'
             5736  JUMP_FORWARD       5750  'to 5750'
           5738_0  COME_FROM          5718  '5718'

 L.1997      5738  LOAD_FAST                'x'
             5740  UNPACK_SEQUENCE_4     4 
             5742  STORE_FAST               'output_model_samples'
             5744  STORE_FAST               'm_output_model'
             5746  STORE_FAST               'u_output_model'
             5748  STORE_FAST               'l_output_model'
           5750_0  COME_FROM          5736  '5736'
             5750  JUMP_FORWARD       5778  'to 5778'
           5752_0  COME_FROM          5712  '5712'

 L.1999      5752  LOAD_FAST                'return_components'
         5754_5756  POP_JUMP_IF_FALSE  5770  'to 5770'

 L.2000      5758  LOAD_FAST                'x'
             5760  UNPACK_SEQUENCE_3     3 
             5762  STORE_FAST               'output_model_samples'
             5764  STORE_FAST               'output_model'
             5766  STORE_FAST               'components'
             5768  JUMP_FORWARD       5778  'to 5778'
           5770_0  COME_FROM          5754  '5754'

 L.2002      5770  LOAD_FAST                'x'
             5772  UNPACK_SEQUENCE_2     2 
             5774  STORE_FAST               'output_model_samples'
             5776  STORE_FAST               'output_model'
           5778_0  COME_FROM          5768  '5768'
           5778_1  COME_FROM          5750  '5750'
             5778  JUMP_FORWARD       5838  'to 5838'
           5780_0  COME_FROM          5706  '5706'

 L.2004      5780  LOAD_FAST                'return_err'
         5782_5784  POP_JUMP_IF_FALSE  5818  'to 5818'

 L.2005      5786  LOAD_FAST                'return_components'
         5788_5790  POP_JUMP_IF_FALSE  5806  'to 5806'

 L.2006      5792  LOAD_FAST                'x'
             5794  UNPACK_SEQUENCE_4     4 
             5796  STORE_FAST               'm_output_model'
             5798  STORE_FAST               'u_output_model'
             5800  STORE_FAST               'l_output_model'
             5802  STORE_FAST               'components'
             5804  JUMP_FORWARD       5816  'to 5816'
           5806_0  COME_FROM          5788  '5788'

 L.2008      5806  LOAD_FAST                'x'
             5808  UNPACK_SEQUENCE_3     3 
             5810  STORE_FAST               'm_output_model'
             5812  STORE_FAST               'u_output_model'
             5814  STORE_FAST               'l_output_model'
           5816_0  COME_FROM          5804  '5804'
             5816  JUMP_FORWARD       5838  'to 5838'
           5818_0  COME_FROM          5782  '5782'

 L.2010      5818  LOAD_FAST                'return_components'
         5820_5822  POP_JUMP_IF_FALSE  5834  'to 5834'

 L.2011      5824  LOAD_FAST                'x'
             5826  UNPACK_SEQUENCE_2     2 
             5828  STORE_FAST               'output_model'
             5830  STORE_FAST               'components'
             5832  JUMP_FORWARD       5838  'to 5838'
           5834_0  COME_FROM          5820  '5820'

 L.2013      5834  LOAD_FAST                'x'
             5836  STORE_FAST               'output_model'
           5838_0  COME_FROM          5832  '5832'
           5838_1  COME_FROM          5816  '5816'
           5838_2  COME_FROM          5778  '5778'
           5838_3  COME_FROM          5662  '5662'
           5838_4  COME_FROM          5640  '5640'
           5838_5  COME_FROM          5420  '5420'

 L.2015      5838  LOAD_FAST                'resampling'
             5840  LOAD_CONST               None
             5842  COMPARE_OP               is-not
         5844_5846  POP_JUMP_IF_FALSE  6014  'to 6014'
             5848  LOAD_FAST                'self'
             5850  LOAD_ATTR                modeltype
             5852  LOAD_STR                 'lc'
             5854  COMPARE_OP               ==
         5856_5858  POP_JUMP_IF_FALSE  6014  'to 6014'
             5860  LOAD_FAST                'instrument'
             5862  LOAD_CONST               None
             5864  COMPARE_OP               is-not
         5866_5868  POP_JUMP_IF_FALSE  6014  'to 6014'

 L.2017      5870  LOAD_FAST                'self'
             5872  LOAD_ATTR                dictionary
             5874  LOAD_FAST                'instrument'
             5876  BINARY_SUBSCR    
             5878  LOAD_STR                 'resampling'
             5880  BINARY_SUBSCR    
         5882_5884  POP_JUMP_IF_FALSE  5964  'to 5964'

 L.2018      5886  LOAD_GLOBAL              init_batman
             5888  LOAD_FAST                'self'
             5890  LOAD_ATTR                times
             5892  LOAD_FAST                'instrument'
             5894  BINARY_SUBSCR    
             5896  LOAD_FAST                'self'
             5898  LOAD_ATTR                dictionary
             5900  LOAD_FAST                'instrument'
             5902  BINARY_SUBSCR    
             5904  LOAD_STR                 'ldlaw'
             5906  BINARY_SUBSCR    

 L.2019      5908  LOAD_FAST                'self'
             5910  LOAD_ATTR                dictionary
             5912  LOAD_FAST                'instrument'
             5914  BINARY_SUBSCR    
             5916  LOAD_STR                 'nresampling'
             5918  BINARY_SUBSCR    

 L.2020      5920  LOAD_FAST                'self'
             5922  LOAD_ATTR                dictionary
             5924  LOAD_FAST                'instrument'
             5926  BINARY_SUBSCR    
             5928  LOAD_STR                 'exptimeresampling'
             5930  BINARY_SUBSCR    
             5932  LOAD_CONST               ('nresampling', 'etresampling')
             5934  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5936  UNPACK_SEQUENCE_2     2 
             5938  LOAD_FAST                'self'
             5940  LOAD_ATTR                model
             5942  LOAD_FAST                'instrument'
             5944  BINARY_SUBSCR    
             5946  LOAD_STR                 'params'
             5948  STORE_SUBSCR     
             5950  LOAD_FAST                'self'
             5952  LOAD_ATTR                model
             5954  LOAD_FAST                'instrument'
             5956  BINARY_SUBSCR    
             5958  LOAD_STR                 'm'
             5960  STORE_SUBSCR     
             5962  JUMP_FORWARD       6014  'to 6014'
           5964_0  COME_FROM          5882  '5882'

 L.2022      5964  LOAD_GLOBAL              init_batman
             5966  LOAD_FAST                'self'
             5968  LOAD_ATTR                times
             5970  LOAD_FAST                'instrument'
             5972  BINARY_SUBSCR    
             5974  LOAD_FAST                'self'
             5976  LOAD_ATTR                dictionary
             5978  LOAD_FAST                'instrument'
             5980  BINARY_SUBSCR    
             5982  LOAD_STR                 'ldlaw'
             5984  BINARY_SUBSCR    
             5986  CALL_FUNCTION_2       2  '2 positional arguments'
             5988  UNPACK_SEQUENCE_2     2 
             5990  LOAD_FAST                'self'
             5992  LOAD_ATTR                model
             5994  LOAD_FAST                'instrument'
             5996  BINARY_SUBSCR    
             5998  LOAD_STR                 'params'
             6000  STORE_SUBSCR     
             6002  LOAD_FAST                'self'
             6004  LOAD_ATTR                model
             6006  LOAD_FAST                'instrument'
             6008  BINARY_SUBSCR    
             6010  LOAD_STR                 'm'
             6012  STORE_SUBSCR     
           6014_0  COME_FROM          5962  '5962'
           6014_1  COME_FROM          5866  '5866'
           6014_2  COME_FROM          5856  '5856'
           6014_3  COME_FROM          5844  '5844'

 L.2024      6014  LOAD_FAST                'self'
             6016  LOAD_ATTR                global_model
         6018_6020  POP_JUMP_IF_TRUE   6028  'to 6028'

 L.2026      6022  LOAD_FAST                'original_inames'
             6024  LOAD_FAST                'self'
             6026  STORE_ATTR               inames
           6028_0  COME_FROM          6018  '6018'

 L.2028      6028  LOAD_FAST                'return_samples'
         6030_6032  POP_JUMP_IF_FALSE  6100  'to 6100'

 L.2029      6034  LOAD_FAST                'return_err'
         6036_6038  POP_JUMP_IF_FALSE  6074  'to 6074'

 L.2030      6040  LOAD_FAST                'return_components'
         6042_6044  POP_JUMP_IF_FALSE  6060  'to 6060'

 L.2031      6046  LOAD_FAST                'output_model_samples'
             6048  LOAD_FAST                'm_output_model'
             6050  LOAD_FAST                'u_output_model'
             6052  LOAD_FAST                'l_output_model'
             6054  LOAD_FAST                'components'
             6056  BUILD_TUPLE_5         5 
             6058  RETURN_VALUE     
           6060_0  COME_FROM          6042  '6042'

 L.2033      6060  LOAD_FAST                'output_model_samples'
             6062  LOAD_FAST                'm_output_model'
             6064  LOAD_FAST                'u_output_model'
             6066  LOAD_FAST                'l_output_model'
             6068  BUILD_TUPLE_4         4 
             6070  RETURN_VALUE     
             6072  JUMP_FORWARD       6098  'to 6098'
           6074_0  COME_FROM          6036  '6036'

 L.2035      6074  LOAD_FAST                'return_components'
         6076_6078  POP_JUMP_IF_FALSE  6090  'to 6090'

 L.2036      6080  LOAD_FAST                'output_model_samples'
             6082  LOAD_FAST                'output_model'
             6084  LOAD_FAST                'components'
             6086  BUILD_TUPLE_3         3 
             6088  RETURN_VALUE     
           6090_0  COME_FROM          6076  '6076'

 L.2038      6090  LOAD_FAST                'output_model_samples'
             6092  LOAD_FAST                'output_model'
             6094  BUILD_TUPLE_2         2 
             6096  RETURN_VALUE     
           6098_0  COME_FROM          6072  '6072'
             6098  JUMP_FORWARD       6154  'to 6154'
           6100_0  COME_FROM          6030  '6030'

 L.2040      6100  LOAD_FAST                'return_err'
         6102_6104  POP_JUMP_IF_FALSE  6136  'to 6136'

 L.2041      6106  LOAD_FAST                'return_components'
         6108_6110  POP_JUMP_IF_FALSE  6124  'to 6124'

 L.2042      6112  LOAD_FAST                'm_output_model'
             6114  LOAD_FAST                'u_output_model'
             6116  LOAD_FAST                'l_output_model'
             6118  LOAD_FAST                'components'
             6120  BUILD_TUPLE_4         4 
             6122  RETURN_VALUE     
           6124_0  COME_FROM          6108  '6108'

 L.2044      6124  LOAD_FAST                'm_output_model'
             6126  LOAD_FAST                'u_output_model'
             6128  LOAD_FAST                'l_output_model'
             6130  BUILD_TUPLE_3         3 
             6132  RETURN_VALUE     
             6134  JUMP_FORWARD       6154  'to 6154'
           6136_0  COME_FROM          6102  '6102'

 L.2046      6136  LOAD_FAST                'return_components'
         6138_6140  POP_JUMP_IF_FALSE  6150  'to 6150'

 L.2047      6142  LOAD_FAST                'output_model'
             6144  LOAD_FAST                'components'
             6146  BUILD_TUPLE_2         2 
             6148  RETURN_VALUE     
           6150_0  COME_FROM          6138  '6138'

 L.2049      6150  LOAD_FAST                'output_model'
             6152  RETURN_VALUE     
           6154_0  COME_FROM          6134  '6134'
           6154_1  COME_FROM          6098  '6098'

Parse error at or near `COME_FROM_LOOP' instruction at offset 4876_0

    def generate_lc_model--- This code section failed: ---

 L.2052         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               modelOK

 L.2055         6  LOAD_FAST                'self'
                8  LOAD_ATTR                Tflag
            10_12  POP_JUMP_IF_FALSE   428  'to 428'

 L.2056        14  BUILD_MAP_0           0 
               16  BUILD_MAP_0           0 
               18  ROT_TWO          
               20  STORE_FAST               'planet_t0'
               22  STORE_FAST               'planet_P'

 L.2057        24  BUILD_MAP_0           0 
               26  BUILD_MAP_0           0 
               28  ROT_TWO          
               30  STORE_FAST               'all_Ts'
               32  STORE_FAST               'all_ns'

 L.2058     34_36  SETUP_LOOP          428  'to 428'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                numbering
               42  GET_ITER         
             44_0  COME_FROM            58  '58'
            44_46  FOR_ITER            426  'to 426'
               48  STORE_FAST               'i'

 L.2059        50  LOAD_FAST                'self'
               52  LOAD_ATTR                Tparametrization
               54  LOAD_FAST                'i'
               56  BINARY_SUBSCR    
               58  POP_JUMP_IF_FALSE    44  'to 44'

 L.2060        60  LOAD_GLOBAL              np
               62  LOAD_METHOD              array
               64  BUILD_LIST_0          0 
               66  CALL_METHOD_1         1  '1 positional argument'
               68  LOAD_GLOBAL              np
               70  LOAD_METHOD              array
               72  BUILD_LIST_0          0 
               74  CALL_METHOD_1         1  '1 positional argument'
               76  ROT_TWO          
               78  LOAD_FAST                'all_Ts'
               80  LOAD_FAST                'i'
               82  STORE_SUBSCR     
               84  LOAD_FAST                'all_ns'
               86  LOAD_FAST                'i'
               88  STORE_SUBSCR     

 L.2061        90  SETUP_LOOP          214  'to 214'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                inames
               96  GET_ITER         
               98  FOR_ITER            212  'to 212'
              100  STORE_FAST               'instrument'

 L.2062       102  SETUP_LOOP          210  'to 210'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                dictionary
              108  LOAD_FAST                'instrument'
              110  BINARY_SUBSCR    
              112  LOAD_STR                 'TTVs'
              114  BINARY_SUBSCR    
              116  LOAD_GLOBAL              int
              118  LOAD_FAST                'i'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  BINARY_SUBSCR    
              124  LOAD_STR                 'transit_number'
              126  BINARY_SUBSCR    
              128  GET_ITER         
              130  FOR_ITER            208  'to 208'
              132  STORE_FAST               'transit_number'

 L.2063       134  LOAD_GLOBAL              np
              136  LOAD_METHOD              append
              138  LOAD_FAST                'all_Ts'
              140  LOAD_FAST                'i'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'parameter_values'
              146  LOAD_STR                 'T_p'
              148  LOAD_GLOBAL              str
              150  LOAD_FAST                'i'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  BINARY_ADD       
              156  LOAD_STR                 '_'
              158  BINARY_ADD       
              160  LOAD_FAST                'instrument'
              162  BINARY_ADD       
              164  LOAD_STR                 '_'
              166  BINARY_ADD       
              168  LOAD_GLOBAL              str
              170  LOAD_FAST                'transit_number'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  BINARY_ADD       
              176  BINARY_SUBSCR    
              178  CALL_METHOD_2         2  '2 positional arguments'
              180  LOAD_FAST                'all_Ts'
              182  LOAD_FAST                'i'
              184  STORE_SUBSCR     

 L.2064       186  LOAD_GLOBAL              np
              188  LOAD_METHOD              append
              190  LOAD_FAST                'all_ns'
              192  LOAD_FAST                'i'
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'transit_number'
              198  CALL_METHOD_2         2  '2 positional arguments'
              200  LOAD_FAST                'all_ns'
              202  LOAD_FAST                'i'
              204  STORE_SUBSCR     
              206  JUMP_BACK           130  'to 130'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      102  '102'
              210  JUMP_BACK            98  'to 98'
              212  POP_BLOCK        
            214_0  COME_FROM_LOOP       90  '90'

 L.2068       214  LOAD_FAST                'evaluate_lc'
          216_218  POP_JUMP_IF_TRUE    382  'to 382'

 L.2069       220  LOAD_GLOBAL              np
              222  LOAD_METHOD              sum
              224  LOAD_FAST                'all_Ts'
              226  LOAD_FAST                'i'
              228  BINARY_SUBSCR    
              230  LOAD_FAST                'all_ns'
              232  LOAD_FAST                'i'
              234  BINARY_SUBSCR    
              236  BINARY_MULTIPLY  
              238  CALL_METHOD_1         1  '1 positional argument'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                N_TTVs
              244  LOAD_FAST                'i'
              246  BINARY_SUBSCR    
              248  BINARY_TRUE_DIVIDE
              250  LOAD_GLOBAL              np
              252  LOAD_METHOD              sum
              254  LOAD_FAST                'all_Ts'
              256  LOAD_FAST                'i'
              258  BINARY_SUBSCR    
              260  CALL_METHOD_1         1  '1 positional argument'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                N_TTVs
              266  LOAD_FAST                'i'
              268  BINARY_SUBSCR    
              270  BINARY_TRUE_DIVIDE
              272  LOAD_GLOBAL              np
              274  LOAD_METHOD              sum
              276  LOAD_FAST                'all_ns'
              278  LOAD_FAST                'i'
              280  BINARY_SUBSCR    
              282  CALL_METHOD_1         1  '1 positional argument'
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                N_TTVs
              288  LOAD_FAST                'i'
              290  BINARY_SUBSCR    
              292  BINARY_TRUE_DIVIDE
              294  LOAD_GLOBAL              np
              296  LOAD_METHOD              sum
              298  LOAD_FAST                'all_ns'
              300  LOAD_FAST                'i'
              302  BINARY_SUBSCR    
              304  LOAD_CONST               2
              306  BINARY_POWER     
              308  CALL_METHOD_1         1  '1 positional argument'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                N_TTVs
              314  LOAD_FAST                'i'
              316  BINARY_SUBSCR    
              318  BINARY_TRUE_DIVIDE
              320  BUILD_TUPLE_4         4 
              322  UNPACK_SEQUENCE_4     4 
              324  STORE_FAST               'XY'
              326  STORE_FAST               'Y'
              328  STORE_FAST               'X'
              330  STORE_FAST               'X2'

 L.2071       332  LOAD_FAST                'XY'
              334  LOAD_FAST                'X'
              336  LOAD_FAST                'Y'
              338  BINARY_MULTIPLY  
              340  BINARY_SUBTRACT  
              342  LOAD_FAST                'X2'
              344  LOAD_FAST                'X'
              346  LOAD_CONST               2
              348  BINARY_POWER     
              350  BINARY_SUBTRACT  
              352  BINARY_TRUE_DIVIDE
              354  LOAD_FAST                'planet_P'
              356  LOAD_FAST                'i'
              358  STORE_SUBSCR     

 L.2073       360  LOAD_FAST                'Y'
              362  LOAD_FAST                'planet_P'
              364  LOAD_FAST                'i'
              366  BINARY_SUBSCR    
              368  LOAD_FAST                'X'
              370  BINARY_MULTIPLY  
              372  BINARY_SUBTRACT  
              374  LOAD_FAST                'planet_t0'
              376  LOAD_FAST                'i'
              378  STORE_SUBSCR     
              380  JUMP_BACK            44  'to 44'
            382_0  COME_FROM           216  '216'

 L.2075       382  LOAD_FAST                'parameter_values'
              384  LOAD_STR                 't0_p'
              386  LOAD_GLOBAL              str
              388  LOAD_FAST                'i'
              390  CALL_FUNCTION_1       1  '1 positional argument'
              392  BINARY_ADD       
              394  BINARY_SUBSCR    
              396  LOAD_FAST                'parameter_values'
              398  LOAD_STR                 'P_p'
              400  LOAD_GLOBAL              str
              402  LOAD_FAST                'i'
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  BINARY_ADD       
              408  BINARY_SUBSCR    
              410  ROT_TWO          
              412  LOAD_FAST                'planet_t0'
              414  LOAD_FAST                'i'
              416  STORE_SUBSCR     
              418  LOAD_FAST                'planet_P'
              420  LOAD_FAST                'i'
              422  STORE_SUBSCR     
              424  JUMP_BACK            44  'to 44'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP       34  '34'
            428_1  COME_FROM            10  '10'

 L.2079   428_430  SETUP_LOOP         3564  'to 3564'
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                inames
              436  GET_ITER         
            438_0  COME_FROM          3498  '3498'
            438_1  COME_FROM          3462  '3462'
          438_440  FOR_ITER           3562  'to 3562'
              442  STORE_FAST               'instrument'

 L.2081       444  LOAD_GLOBAL              np
              446  LOAD_METHOD              copy
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                model
              452  LOAD_FAST                'instrument'
              454  BINARY_SUBSCR    
              456  LOAD_STR                 'ones'
              458  BINARY_SUBSCR    
              460  CALL_METHOD_1         1  '1 positional argument'
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                model
              466  LOAD_FAST                'instrument'
              468  BINARY_SUBSCR    
              470  LOAD_STR                 'M'
              472  STORE_SUBSCR     

 L.2083       474  LOAD_FAST                'self'
              476  LOAD_ATTR                dictionary
              478  LOAD_FAST                'instrument'
              480  BINARY_SUBSCR    
              482  LOAD_STR                 'TransitFit'
              484  BINARY_SUBSCR    
          486_488  POP_JUMP_IF_FALSE  3138  'to 3138'

 L.2085       490  LOAD_FAST                'self'
              492  LOAD_ATTR                dictionary
              494  LOAD_FAST                'instrument'
              496  BINARY_SUBSCR    
              498  LOAD_STR                 'ldlaw'
              500  BINARY_SUBSCR    
              502  LOAD_STR                 'linear'
              504  COMPARE_OP               !=
          506_508  POP_JUMP_IF_FALSE   566  'to 566'

 L.2086       510  LOAD_GLOBAL              reverse_ld_coeffs
              512  LOAD_FAST                'self'
              514  LOAD_ATTR                dictionary
              516  LOAD_FAST                'instrument'
              518  BINARY_SUBSCR    
              520  LOAD_STR                 'ldlaw'
              522  BINARY_SUBSCR    
              524  LOAD_FAST                'parameter_values'
              526  LOAD_STR                 'q1_'
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                ld_iname
              532  LOAD_FAST                'instrument'
              534  BINARY_SUBSCR    
              536  BINARY_ADD       
              538  BINARY_SUBSCR    

 L.2087       540  LOAD_FAST                'parameter_values'
              542  LOAD_STR                 'q2_'
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                ld_iname
              548  LOAD_FAST                'instrument'
              550  BINARY_SUBSCR    
              552  BINARY_ADD       
              554  BINARY_SUBSCR    
              556  CALL_FUNCTION_3       3  '3 positional arguments'
              558  UNPACK_SEQUENCE_2     2 
              560  STORE_FAST               'coeff1'
              562  STORE_FAST               'coeff2'
              564  JUMP_FORWARD        584  'to 584'
            566_0  COME_FROM           506  '506'

 L.2089       566  LOAD_FAST                'parameter_values'
              568  LOAD_STR                 'q1_'
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                ld_iname
              574  LOAD_FAST                'instrument'
              576  BINARY_SUBSCR    
              578  BINARY_ADD       
              580  BINARY_SUBSCR    
              582  STORE_FAST               'coeff1'
            584_0  COME_FROM           564  '564'

 L.2094       584  BUILD_MAP_0           0 
              586  BUILD_MAP_0           0 
              588  ROT_TWO          
              590  STORE_FAST               'cP'
              592  STORE_FAST               'ct0'

 L.2095   594_596  SETUP_LOOP         1186  'to 1186'
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                numbering
              602  GET_ITER         
          604_606  FOR_ITER           1184  'to 1184'
              608  STORE_FAST               'i'

 L.2097       610  LOAD_FAST                'self'
              612  LOAD_ATTR                dictionary
              614  LOAD_FAST                'instrument'
              616  BINARY_SUBSCR    
              618  LOAD_STR                 'TTVs'
              620  BINARY_SUBSCR    
              622  LOAD_FAST                'i'
              624  BINARY_SUBSCR    
              626  LOAD_STR                 'status'
              628  BINARY_SUBSCR    
          630_632  POP_JUMP_IF_TRUE    690  'to 690'

 L.2098       634  LOAD_FAST                'parameter_values'
              636  LOAD_STR                 't0_p'
              638  LOAD_GLOBAL              str
              640  LOAD_FAST                'i'
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  BINARY_ADD       
              646  BINARY_SUBSCR    
              648  LOAD_FAST                'parameter_values'
              650  LOAD_STR                 'P_p'
              652  LOAD_GLOBAL              str
              654  LOAD_FAST                'i'
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  BINARY_ADD       
              660  BINARY_SUBSCR    
              662  ROT_TWO          
              664  STORE_FAST               't0'
              666  STORE_FAST               'P'

 L.2099       668  LOAD_FAST                'P'
              670  LOAD_FAST                't0'
              672  ROT_TWO          
              674  LOAD_FAST                'cP'
              676  LOAD_FAST                'i'
              678  STORE_SUBSCR     
              680  LOAD_FAST                'ct0'
              682  LOAD_FAST                'i'
              684  STORE_SUBSCR     
          686_688  JUMP_BACK           604  'to 604'
            690_0  COME_FROM           630  '630'

 L.2107       690  LOAD_GLOBAL              np
              692  LOAD_METHOD              copy
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                times
              698  LOAD_FAST                'instrument'
              700  BINARY_SUBSCR    
              702  CALL_METHOD_1         1  '1 positional argument'
              704  STORE_FAST               'dummy_time'

 L.2108       706  LOAD_FAST                'self'
              708  LOAD_ATTR                dictionary
              710  LOAD_FAST                'instrument'
              712  BINARY_SUBSCR    
              714  LOAD_STR                 'TTVs'
              716  BINARY_SUBSCR    
              718  LOAD_FAST                'i'
              720  BINARY_SUBSCR    
              722  LOAD_STR                 'parametrization'
              724  BINARY_SUBSCR    
              726  LOAD_STR                 'dt'
              728  COMPARE_OP               ==
          730_732  POP_JUMP_IF_FALSE   966  'to 966'

 L.2109       734  LOAD_FAST                'parameter_values'
              736  LOAD_STR                 't0_p'
              738  LOAD_GLOBAL              str
              740  LOAD_FAST                'i'
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  BINARY_ADD       
              746  BINARY_SUBSCR    
              748  LOAD_FAST                'parameter_values'
              750  LOAD_STR                 'P_p'
              752  LOAD_GLOBAL              str
              754  LOAD_FAST                'i'
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  BINARY_ADD       
              760  BINARY_SUBSCR    
              762  ROT_TWO          
              764  STORE_FAST               't0'
              766  STORE_FAST               'P'

 L.2110       768  LOAD_FAST                'P'
              770  LOAD_FAST                't0'
              772  ROT_TWO          
              774  LOAD_FAST                'cP'
              776  LOAD_FAST                'i'
              778  STORE_SUBSCR     
              780  LOAD_FAST                'ct0'
              782  LOAD_FAST                'i'
              784  STORE_SUBSCR     

 L.2111       786  SETUP_LOOP          964  'to 964'
              788  LOAD_FAST                'self'
              790  LOAD_ATTR                dictionary
              792  LOAD_FAST                'instrument'
              794  BINARY_SUBSCR    
              796  LOAD_STR                 'TTVs'
              798  BINARY_SUBSCR    
              800  LOAD_GLOBAL              int
              802  LOAD_FAST                'i'
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  BINARY_SUBSCR    
              808  LOAD_STR                 'transit_number'
              810  BINARY_SUBSCR    
              812  GET_ITER         
              814  FOR_ITER            962  'to 962'
              816  STORE_FAST               'transit_number'

 L.2112       818  LOAD_FAST                't0'
              820  LOAD_FAST                'transit_number'
              822  LOAD_FAST                'P'
              824  BINARY_MULTIPLY  
              826  BINARY_ADD       
              828  LOAD_FAST                'parameter_values'
              830  LOAD_STR                 'dt_p'
              832  LOAD_GLOBAL              str
              834  LOAD_FAST                'i'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  BINARY_ADD       
              840  LOAD_STR                 '_'
              842  BINARY_ADD       
              844  LOAD_FAST                'instrument'
              846  BINARY_ADD       
              848  LOAD_STR                 '_'
              850  BINARY_ADD       
              852  LOAD_GLOBAL              str
              854  LOAD_FAST                'transit_number'
              856  CALL_FUNCTION_1       1  '1 positional argument'
              858  BINARY_ADD       
              860  BINARY_SUBSCR    
              862  BINARY_ADD       
              864  STORE_FAST               'transit_time'

 L.2114       866  LOAD_GLOBAL              np
              868  LOAD_METHOD              where
              870  LOAD_GLOBAL              np
              872  LOAD_METHOD              abs
              874  LOAD_FAST                'self'
              876  LOAD_ATTR                times
              878  LOAD_FAST                'instrument'
              880  BINARY_SUBSCR    
              882  LOAD_FAST                'transit_time'
              884  BINARY_SUBTRACT  
              886  CALL_METHOD_1         1  '1 positional argument'
              888  LOAD_FAST                'P'
              890  LOAD_CONST               4.0
              892  BINARY_TRUE_DIVIDE
              894  COMPARE_OP               <
              896  CALL_METHOD_1         1  '1 positional argument'
              898  LOAD_CONST               0
              900  BINARY_SUBSCR    
              902  STORE_FAST               'idx'

 L.2115       904  LOAD_FAST                'self'
              906  LOAD_ATTR                times
              908  LOAD_FAST                'instrument'
              910  BINARY_SUBSCR    
              912  LOAD_FAST                'idx'
              914  BINARY_SUBSCR    
              916  LOAD_FAST                'parameter_values'
              918  LOAD_STR                 'dt_p'
              920  LOAD_GLOBAL              str
              922  LOAD_FAST                'i'
              924  CALL_FUNCTION_1       1  '1 positional argument'
              926  BINARY_ADD       
              928  LOAD_STR                 '_'
              930  BINARY_ADD       
              932  LOAD_FAST                'instrument'
              934  BINARY_ADD       
              936  LOAD_STR                 '_'
              938  BINARY_ADD       
              940  LOAD_GLOBAL              str
              942  LOAD_FAST                'transit_number'
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  BINARY_ADD       
              948  BINARY_SUBSCR    
              950  BINARY_SUBTRACT  
              952  LOAD_FAST                'dummy_time'
              954  LOAD_FAST                'idx'
              956  STORE_SUBSCR     
          958_960  JUMP_BACK           814  'to 814'
              962  POP_BLOCK        
            964_0  COME_FROM_LOOP      786  '786'
              964  JUMP_BACK           604  'to 604'
            966_0  COME_FROM           730  '730'

 L.2117       966  LOAD_FAST                'planet_t0'
              968  LOAD_FAST                'i'
              970  BINARY_SUBSCR    
              972  LOAD_FAST                'planet_P'
              974  LOAD_FAST                'i'
              976  BINARY_SUBSCR    
              978  ROT_TWO          
              980  STORE_FAST               't0'
              982  STORE_FAST               'P'

 L.2118       984  SETUP_LOOP         1162  'to 1162'
              986  LOAD_FAST                'self'
              988  LOAD_ATTR                dictionary
              990  LOAD_FAST                'instrument'
              992  BINARY_SUBSCR    
              994  LOAD_STR                 'TTVs'
              996  BINARY_SUBSCR    
              998  LOAD_GLOBAL              int
             1000  LOAD_FAST                'i'
             1002  CALL_FUNCTION_1       1  '1 positional argument'
             1004  BINARY_SUBSCR    
             1006  LOAD_STR                 'transit_number'
             1008  BINARY_SUBSCR    
             1010  GET_ITER         
             1012  FOR_ITER           1160  'to 1160'
             1014  STORE_FAST               'transit_number'

 L.2119      1016  LOAD_FAST                'parameter_values'
             1018  LOAD_STR                 'T_p'
             1020  LOAD_GLOBAL              str
             1022  LOAD_FAST                'i'
             1024  CALL_FUNCTION_1       1  '1 positional argument'
             1026  BINARY_ADD       
             1028  LOAD_STR                 '_'
             1030  BINARY_ADD       
             1032  LOAD_FAST                'instrument'
             1034  BINARY_ADD       
             1036  LOAD_STR                 '_'
             1038  BINARY_ADD       
             1040  LOAD_GLOBAL              str
             1042  LOAD_FAST                'transit_number'
             1044  CALL_FUNCTION_1       1  '1 positional argument'
             1046  BINARY_ADD       
             1048  BINARY_SUBSCR    
             1050  LOAD_FAST                't0'
             1052  LOAD_FAST                'transit_number'
             1054  LOAD_FAST                'P'
             1056  BINARY_MULTIPLY  
             1058  BINARY_ADD       
             1060  BINARY_SUBTRACT  
             1062  STORE_FAST               'dt'

 L.2121      1064  LOAD_GLOBAL              np
             1066  LOAD_METHOD              where
             1068  LOAD_GLOBAL              np
             1070  LOAD_METHOD              abs
             1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                times
             1076  LOAD_FAST                'instrument'
             1078  BINARY_SUBSCR    
             1080  LOAD_FAST                'parameter_values'
             1082  LOAD_STR                 'T_p'
             1084  LOAD_GLOBAL              str
             1086  LOAD_FAST                'i'
             1088  CALL_FUNCTION_1       1  '1 positional argument'
             1090  BINARY_ADD       
             1092  LOAD_STR                 '_'
             1094  BINARY_ADD       
             1096  LOAD_FAST                'instrument'
             1098  BINARY_ADD       
             1100  LOAD_STR                 '_'
             1102  BINARY_ADD       
             1104  LOAD_GLOBAL              str
             1106  LOAD_FAST                'transit_number'
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  BINARY_ADD       
             1112  BINARY_SUBSCR    
             1114  BINARY_SUBTRACT  
             1116  CALL_METHOD_1         1  '1 positional argument'
             1118  LOAD_FAST                'P'
             1120  LOAD_CONST               4.0
             1122  BINARY_TRUE_DIVIDE
             1124  COMPARE_OP               <
             1126  CALL_METHOD_1         1  '1 positional argument'
             1128  LOAD_CONST               0
             1130  BINARY_SUBSCR    
             1132  STORE_FAST               'idx'

 L.2122      1134  LOAD_FAST                'self'
             1136  LOAD_ATTR                times
             1138  LOAD_FAST                'instrument'
             1140  BINARY_SUBSCR    
             1142  LOAD_FAST                'idx'
             1144  BINARY_SUBSCR    
             1146  LOAD_FAST                'dt'
             1148  BINARY_SUBTRACT  
             1150  LOAD_FAST                'dummy_time'
             1152  LOAD_FAST                'idx'
             1154  STORE_SUBSCR     
         1156_1158  JUMP_BACK          1012  'to 1012'
             1160  POP_BLOCK        
           1162_0  COME_FROM_LOOP      984  '984'

 L.2123      1162  LOAD_FAST                'P'
             1164  LOAD_FAST                't0'
             1166  ROT_TWO          
             1168  LOAD_FAST                'cP'
             1170  LOAD_FAST                'i'
             1172  STORE_SUBSCR     
             1174  LOAD_FAST                'ct0'
             1176  LOAD_FAST                'i'
             1178  STORE_SUBSCR     
         1180_1182  JUMP_BACK           604  'to 604'
             1184  POP_BLOCK        
           1186_0  COME_FROM_LOOP      594  '594'

 L.2126      1186  LOAD_CONST               True
             1188  STORE_FAST               'first_time'

 L.2127      1190  SETUP_LOOP         1262  'to 1262'
             1192  LOAD_FAST                'self'
             1194  LOAD_ATTR                numbering
             1196  GET_ITER         
             1198  FOR_ITER           1260  'to 1260'
             1200  STORE_FAST               'i'

 L.2128      1202  LOAD_FAST                'first_time'
         1204_1206  POP_JUMP_IF_FALSE  1222  'to 1222'

 L.2129      1208  LOAD_FAST                'cP'
             1210  LOAD_FAST                'i'
             1212  BINARY_SUBSCR    
             1214  STORE_FAST               'ccP'

 L.2130      1216  LOAD_CONST               False
             1218  STORE_FAST               'first_time'
             1220  JUMP_BACK          1198  'to 1198'
           1222_0  COME_FROM          1204  '1204'

 L.2132      1222  LOAD_FAST                'ccP'
             1224  LOAD_FAST                'cP'
             1226  LOAD_FAST                'i'
             1228  BINARY_SUBSCR    
             1230  COMPARE_OP               <
         1232_1234  POP_JUMP_IF_FALSE  1246  'to 1246'

 L.2133      1236  LOAD_FAST                'cP'
             1238  LOAD_FAST                'i'
             1240  BINARY_SUBSCR    
             1242  STORE_FAST               'ccP'
             1244  JUMP_BACK          1198  'to 1198'
           1246_0  COME_FROM          1232  '1232'

 L.2135      1246  LOAD_CONST               False
             1248  LOAD_FAST                'self'
             1250  STORE_ATTR               modelOK

 L.2136      1252  LOAD_CONST               False
             1254  RETURN_VALUE     
         1256_1258  JUMP_BACK          1198  'to 1198'
             1260  POP_BLOCK        
           1262_0  COME_FROM_LOOP     1190  '1190'

 L.2139  1262_1264  SETUP_LOOP         3138  'to 3138'
             1266  LOAD_FAST                'self'
             1268  LOAD_ATTR                numbering
             1270  GET_ITER         
         1272_1274  FOR_ITER           3136  'to 3136'
             1276  STORE_FAST               'i'

 L.2140      1278  LOAD_FAST                'cP'
             1280  LOAD_FAST                'i'
             1282  BINARY_SUBSCR    
             1284  LOAD_FAST                'ct0'
             1286  LOAD_FAST                'i'
             1288  BINARY_SUBSCR    
             1290  ROT_TWO          
             1292  STORE_FAST               'P'
             1294  STORE_FAST               't0'

 L.2141      1296  LOAD_FAST                'self'
             1298  LOAD_ATTR                dictionary
             1300  LOAD_STR                 'efficient_bp'
             1302  BINARY_SUBSCR    
             1304  LOAD_FAST                'i'
             1306  BINARY_SUBSCR    
         1308_1310  POP_JUMP_IF_FALSE  1622  'to 1622'

 L.2142      1312  LOAD_FAST                'self'
             1314  LOAD_ATTR                dictionary
             1316  LOAD_STR                 'fitrho'
             1318  BINARY_SUBSCR    
         1320_1322  POP_JUMP_IF_TRUE   1378  'to 1378'

 L.2143      1324  LOAD_FAST                'parameter_values'
             1326  LOAD_STR                 'a_p'
             1328  LOAD_GLOBAL              str
             1330  LOAD_FAST                'i'
             1332  CALL_FUNCTION_1       1  '1 positional argument'
             1334  BINARY_ADD       
             1336  BINARY_SUBSCR    
             1338  LOAD_FAST                'parameter_values'
             1340  LOAD_STR                 'r1_p'
             1342  LOAD_GLOBAL              str
             1344  LOAD_FAST                'i'
             1346  CALL_FUNCTION_1       1  '1 positional argument'
             1348  BINARY_ADD       
             1350  BINARY_SUBSCR    

 L.2144      1352  LOAD_FAST                'parameter_values'
             1354  LOAD_STR                 'r2_p'
             1356  LOAD_GLOBAL              str
             1358  LOAD_FAST                'i'
             1360  CALL_FUNCTION_1       1  '1 positional argument'
             1362  BINARY_ADD       
             1364  BINARY_SUBSCR    
             1366  ROT_THREE        
             1368  ROT_TWO          
             1370  STORE_FAST               'a'
             1372  STORE_FAST               'r1'
             1374  STORE_FAST               'r2'
             1376  JUMP_FORWARD       1460  'to 1460'
           1378_0  COME_FROM          1320  '1320'

 L.2146      1378  LOAD_FAST                'parameter_values'
             1380  LOAD_STR                 'rho'
             1382  BINARY_SUBSCR    
             1384  LOAD_FAST                'parameter_values'
             1386  LOAD_STR                 'r1_p'
             1388  LOAD_GLOBAL              str
             1390  LOAD_FAST                'i'
             1392  CALL_FUNCTION_1       1  '1 positional argument'
             1394  BINARY_ADD       
             1396  BINARY_SUBSCR    

 L.2147      1398  LOAD_FAST                'parameter_values'
             1400  LOAD_STR                 'r2_p'
             1402  LOAD_GLOBAL              str
             1404  LOAD_FAST                'i'
             1406  CALL_FUNCTION_1       1  '1 positional argument'
             1408  BINARY_ADD       
             1410  BINARY_SUBSCR    
             1412  ROT_THREE        
             1414  ROT_TWO          
             1416  STORE_FAST               'rho'
             1418  STORE_FAST               'r1'
             1420  STORE_FAST               'r2'

 L.2148      1422  LOAD_FAST                'rho'
             1424  LOAD_GLOBAL              G
             1426  BINARY_MULTIPLY  
             1428  LOAD_FAST                'P'
             1430  LOAD_CONST               24.0
             1432  BINARY_MULTIPLY  
             1434  LOAD_CONST               3600.0
             1436  BINARY_MULTIPLY  
             1438  LOAD_CONST               2
             1440  BINARY_POWER     
             1442  BINARY_MULTIPLY  
             1444  LOAD_CONST               3.0
             1446  LOAD_GLOBAL              np
             1448  LOAD_ATTR                pi
             1450  BINARY_MULTIPLY  
             1452  BINARY_TRUE_DIVIDE
             1454  LOAD_CONST               0.3333333333333333
             1456  BINARY_POWER     
             1458  STORE_FAST               'a'
           1460_0  COME_FROM          1376  '1376'

 L.2149      1460  LOAD_FAST                'r1'
             1462  LOAD_FAST                'self'
             1464  LOAD_ATTR                Ar
             1466  COMPARE_OP               >
         1468_1470  POP_JUMP_IF_FALSE  1532  'to 1532'

 L.2150      1472  LOAD_CONST               1
             1474  LOAD_FAST                'self'
             1476  LOAD_ATTR                pl
             1478  BINARY_ADD       
             1480  LOAD_CONST               1.0
             1482  LOAD_FAST                'r1'
             1484  LOAD_CONST               1.0
             1486  BINARY_SUBTRACT  
             1488  LOAD_CONST               1.0
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                Ar
             1494  BINARY_SUBTRACT  
             1496  BINARY_TRUE_DIVIDE
             1498  BINARY_ADD       
             1500  BINARY_MULTIPLY  

 L.2151      1502  LOAD_CONST               1
             1504  LOAD_FAST                'r2'
             1506  BINARY_SUBTRACT  
             1508  LOAD_FAST                'self'
             1510  LOAD_ATTR                pl
             1512  BINARY_MULTIPLY  
             1514  LOAD_FAST                'r2'
             1516  LOAD_FAST                'self'
             1518  LOAD_ATTR                pu
             1520  BINARY_MULTIPLY  
             1522  BINARY_ADD       
             1524  ROT_TWO          
             1526  STORE_FAST               'b'
             1528  STORE_FAST               'p'
             1530  JUMP_FORWARD       1994  'to 1994'
           1532_0  COME_FROM          1468  '1468'

 L.2153      1532  LOAD_CONST               1.0
             1534  LOAD_FAST                'self'
             1536  LOAD_ATTR                pl
             1538  BINARY_ADD       
             1540  LOAD_GLOBAL              np
             1542  LOAD_METHOD              sqrt
             1544  LOAD_FAST                'r1'
             1546  LOAD_FAST                'self'
             1548  LOAD_ATTR                Ar
             1550  BINARY_TRUE_DIVIDE
             1552  CALL_METHOD_1         1  '1 positional argument'
             1554  LOAD_FAST                'r2'
             1556  BINARY_MULTIPLY  
             1558  LOAD_FAST                'self'
             1560  LOAD_ATTR                pu
             1562  LOAD_FAST                'self'
             1564  LOAD_ATTR                pl
             1566  BINARY_SUBTRACT  
             1568  BINARY_MULTIPLY  
             1570  BINARY_ADD       

 L.2154      1572  LOAD_FAST                'self'
             1574  LOAD_ATTR                pu
             1576  LOAD_FAST                'self'
             1578  LOAD_ATTR                pl
             1580  LOAD_FAST                'self'
             1582  LOAD_ATTR                pu
             1584  BINARY_SUBTRACT  
             1586  LOAD_GLOBAL              np
             1588  LOAD_METHOD              sqrt
             1590  LOAD_FAST                'r1'
             1592  LOAD_FAST                'self'
             1594  LOAD_ATTR                Ar
             1596  BINARY_TRUE_DIVIDE
             1598  CALL_METHOD_1         1  '1 positional argument'
             1600  BINARY_MULTIPLY  
             1602  LOAD_CONST               1.0
             1604  LOAD_FAST                'r2'
             1606  BINARY_SUBTRACT  
             1608  BINARY_MULTIPLY  
             1610  BINARY_ADD       
             1612  ROT_TWO          
             1614  STORE_FAST               'b'
             1616  STORE_FAST               'p'
         1618_1620  JUMP_FORWARD       1994  'to 1994'
           1622_0  COME_FROM          1308  '1308'

 L.2156      1622  LOAD_FAST                'self'
             1624  LOAD_ATTR                dictionary
             1626  LOAD_STR                 'fitrho'
             1628  BINARY_SUBSCR    
         1630_1632  POP_JUMP_IF_TRUE   1804  'to 1804'

 L.2157      1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                dictionary
             1638  LOAD_FAST                'instrument'
             1640  BINARY_SUBSCR    
             1642  LOAD_STR                 'TransitFitCatwoman'
             1644  BINARY_SUBSCR    
         1646_1648  POP_JUMP_IF_TRUE   1704  'to 1704'

 L.2158      1650  LOAD_FAST                'parameter_values'
             1652  LOAD_STR                 'a_p'
             1654  LOAD_GLOBAL              str
             1656  LOAD_FAST                'i'
             1658  CALL_FUNCTION_1       1  '1 positional argument'
             1660  BINARY_ADD       
             1662  BINARY_SUBSCR    
             1664  LOAD_FAST                'parameter_values'
             1666  LOAD_STR                 'b_p'
             1668  LOAD_GLOBAL              str
             1670  LOAD_FAST                'i'
             1672  CALL_FUNCTION_1       1  '1 positional argument'
             1674  BINARY_ADD       
             1676  BINARY_SUBSCR    

 L.2159      1678  LOAD_FAST                'parameter_values'
             1680  LOAD_STR                 'p_p'
             1682  LOAD_GLOBAL              str
             1684  LOAD_FAST                'i'
             1686  CALL_FUNCTION_1       1  '1 positional argument'
             1688  BINARY_ADD       
             1690  BINARY_SUBSCR    
             1692  ROT_THREE        
             1694  ROT_TWO          
             1696  STORE_FAST               'a'
             1698  STORE_FAST               'b'
             1700  STORE_FAST               'p'
             1702  JUMP_FORWARD       1802  'to 1802'
           1704_0  COME_FROM          1646  '1646'

 L.2161      1704  LOAD_FAST                'parameter_values'
             1706  LOAD_STR                 'a_p'
             1708  LOAD_GLOBAL              str
             1710  LOAD_FAST                'i'
             1712  CALL_FUNCTION_1       1  '1 positional argument'
             1714  BINARY_ADD       
             1716  BINARY_SUBSCR    
             1718  LOAD_FAST                'parameter_values'
             1720  LOAD_STR                 'b_p'
             1722  LOAD_GLOBAL              str
             1724  LOAD_FAST                'i'
             1726  CALL_FUNCTION_1       1  '1 positional argument'
             1728  BINARY_ADD       
             1730  BINARY_SUBSCR    

 L.2162      1732  LOAD_FAST                'parameter_values'
             1734  LOAD_STR                 'p1_p'
             1736  LOAD_GLOBAL              str
             1738  LOAD_FAST                'i'
             1740  CALL_FUNCTION_1       1  '1 positional argument'
             1742  BINARY_ADD       
             1744  BINARY_SUBSCR    
             1746  LOAD_FAST                'parameter_values'
             1748  LOAD_STR                 'p2_p'
             1750  LOAD_GLOBAL              str
             1752  LOAD_FAST                'i'
             1754  CALL_FUNCTION_1       1  '1 positional argument'
             1756  BINARY_ADD       
             1758  BINARY_SUBSCR    

 L.2163      1760  LOAD_FAST                'parameter_values'
             1762  LOAD_STR                 'phi_p'
             1764  LOAD_GLOBAL              str
             1766  LOAD_FAST                'i'
             1768  CALL_FUNCTION_1       1  '1 positional argument'
             1770  BINARY_ADD       
             1772  BINARY_SUBSCR    
             1774  BUILD_TUPLE_5         5 
             1776  UNPACK_SEQUENCE_5     5 
             1778  STORE_FAST               'a'
             1780  STORE_FAST               'b'
             1782  STORE_FAST               'p1'
             1784  STORE_FAST               'p2'
             1786  STORE_FAST               'phi'

 L.2164      1788  LOAD_GLOBAL              np
             1790  LOAD_METHOD              min
             1792  LOAD_FAST                'p1'
             1794  LOAD_FAST                'p2'
             1796  BUILD_LIST_2          2 
             1798  CALL_METHOD_1         1  '1 positional argument'
             1800  STORE_FAST               'p'
           1802_0  COME_FROM          1702  '1702'
             1802  JUMP_FORWARD       1994  'to 1994'
           1804_0  COME_FROM          1630  '1630'

 L.2166      1804  LOAD_FAST                'self'
             1806  LOAD_ATTR                dictionary
             1808  LOAD_FAST                'instrument'
             1810  BINARY_SUBSCR    
             1812  LOAD_STR                 'TransitFitCatwoman'
             1814  BINARY_SUBSCR    
         1816_1818  POP_JUMP_IF_TRUE   1866  'to 1866'

 L.2167      1820  LOAD_FAST                'parameter_values'
             1822  LOAD_STR                 'rho'
             1824  BINARY_SUBSCR    
             1826  LOAD_FAST                'parameter_values'
             1828  LOAD_STR                 'b_p'
             1830  LOAD_GLOBAL              str
             1832  LOAD_FAST                'i'
             1834  CALL_FUNCTION_1       1  '1 positional argument'
             1836  BINARY_ADD       
             1838  BINARY_SUBSCR    

 L.2168      1840  LOAD_FAST                'parameter_values'
             1842  LOAD_STR                 'p_p'
             1844  LOAD_GLOBAL              str
             1846  LOAD_FAST                'i'
             1848  CALL_FUNCTION_1       1  '1 positional argument'
             1850  BINARY_ADD       
             1852  BINARY_SUBSCR    
             1854  ROT_THREE        
             1856  ROT_TWO          
             1858  STORE_FAST               'rho'
             1860  STORE_FAST               'b'
             1862  STORE_FAST               'p'
             1864  JUMP_FORWARD       1956  'to 1956'
           1866_0  COME_FROM          1816  '1816'

 L.2170      1866  LOAD_FAST                'parameter_values'
             1868  LOAD_STR                 'rho'
             1870  BINARY_SUBSCR    
             1872  LOAD_FAST                'parameter_values'
             1874  LOAD_STR                 'b_p'
             1876  LOAD_GLOBAL              str
             1878  LOAD_FAST                'i'
             1880  CALL_FUNCTION_1       1  '1 positional argument'
             1882  BINARY_ADD       
             1884  BINARY_SUBSCR    

 L.2171      1886  LOAD_FAST                'parameter_values'
             1888  LOAD_STR                 'p1_p'
             1890  LOAD_GLOBAL              str
             1892  LOAD_FAST                'i'
             1894  CALL_FUNCTION_1       1  '1 positional argument'
             1896  BINARY_ADD       
             1898  BINARY_SUBSCR    
             1900  LOAD_FAST                'parameter_values'
             1902  LOAD_STR                 'p2_p'
           1904_0  COME_FROM          1530  '1530'
             1904  LOAD_GLOBAL              str
             1906  LOAD_FAST                'i'
             1908  CALL_FUNCTION_1       1  '1 positional argument'
             1910  BINARY_ADD       
             1912  BINARY_SUBSCR    

 L.2172      1914  LOAD_FAST                'parameter_values'
             1916  LOAD_STR                 'phi_p'
             1918  LOAD_GLOBAL              str
             1920  LOAD_FAST                'i'
             1922  CALL_FUNCTION_1       1  '1 positional argument'
             1924  BINARY_ADD       
             1926  BINARY_SUBSCR    
             1928  BUILD_TUPLE_5         5 
             1930  UNPACK_SEQUENCE_5     5 
             1932  STORE_FAST               'rho'
             1934  STORE_FAST               'b'
             1936  STORE_FAST               'p1'
             1938  STORE_FAST               'p2'
             1940  STORE_FAST               'phi'

 L.2173      1942  LOAD_GLOBAL              np
             1944  LOAD_METHOD              min
             1946  LOAD_FAST                'p1'
             1948  LOAD_FAST                'p2'
             1950  BUILD_LIST_2          2 
             1952  CALL_METHOD_1         1  '1 positional argument'
             1954  STORE_FAST               'p'
           1956_0  COME_FROM          1864  '1864'

 L.2174      1956  LOAD_FAST                'rho'
             1958  LOAD_GLOBAL              G
             1960  BINARY_MULTIPLY  
             1962  LOAD_FAST                'P'
             1964  LOAD_CONST               24.0
             1966  BINARY_MULTIPLY  
             1968  LOAD_CONST               3600.0
             1970  BINARY_MULTIPLY  
             1972  LOAD_CONST               2
             1974  BINARY_POWER     
             1976  BINARY_MULTIPLY  
             1978  LOAD_CONST               3.0
             1980  LOAD_GLOBAL              np
             1982  LOAD_ATTR                pi
             1984  BINARY_MULTIPLY  
             1986  BINARY_TRUE_DIVIDE
             1988  LOAD_CONST               0.3333333333333333
             1990  BINARY_POWER     
             1992  STORE_FAST               'a'
           1994_0  COME_FROM          1802  '1802'
           1994_1  COME_FROM          1618  '1618'

 L.2177      1994  LOAD_FAST                'self'
             1996  LOAD_ATTR                dictionary
             1998  LOAD_STR                 'ecc_parametrization'
             2000  BINARY_SUBSCR    
             2002  LOAD_FAST                'i'
             2004  BINARY_SUBSCR    
             2006  LOAD_CONST               0
             2008  COMPARE_OP               ==
         2010_2012  POP_JUMP_IF_FALSE  2050  'to 2050'

 L.2178      2014  LOAD_FAST                'parameter_values'
             2016  LOAD_STR                 'ecc_p'
             2018  LOAD_GLOBAL              str
             2020  LOAD_FAST                'i'
             2022  CALL_FUNCTION_1       1  '1 positional argument'
             2024  BINARY_ADD       
             2026  BINARY_SUBSCR    
             2028  LOAD_FAST                'parameter_values'
             2030  LOAD_STR                 'omega_p'
             2032  LOAD_GLOBAL              str
             2034  LOAD_FAST                'i'
             2036  CALL_FUNCTION_1       1  '1 positional argument'
             2038  BINARY_ADD       
             2040  BINARY_SUBSCR    
             2042  ROT_TWO          
             2044  STORE_FAST               'ecc'
             2046  STORE_FAST               'omega'
             2048  JUMP_FORWARD       2250  'to 2250'
           2050_0  COME_FROM          2010  '2010'

 L.2179      2050  LOAD_FAST                'self'
             2052  LOAD_ATTR                dictionary
             2054  LOAD_STR                 'ecc_parametrization'
             2056  BINARY_SUBSCR    
             2058  LOAD_FAST                'i'
             2060  BINARY_SUBSCR    
             2062  LOAD_CONST               1
             2064  COMPARE_OP               ==
         2066_2068  POP_JUMP_IF_FALSE  2164  'to 2164'

 L.2180      2070  LOAD_GLOBAL              np
             2072  LOAD_METHOD              sqrt
             2074  LOAD_FAST                'parameter_values'
             2076  LOAD_STR                 'ecosomega_p'
             2078  LOAD_GLOBAL              str
             2080  LOAD_FAST                'i'
             2082  CALL_FUNCTION_1       1  '1 positional argument'
             2084  BINARY_ADD       
             2086  BINARY_SUBSCR    
             2088  LOAD_CONST               2
             2090  BINARY_POWER     
             2092  LOAD_FAST                'parameter_values'
             2094  LOAD_STR                 'esinomega_p'
             2096  LOAD_GLOBAL              str
             2098  LOAD_FAST                'i'
             2100  CALL_FUNCTION_1       1  '1 positional argument'
             2102  BINARY_ADD       
             2104  BINARY_SUBSCR    
             2106  LOAD_CONST               2
             2108  BINARY_POWER     
             2110  BINARY_ADD       
             2112  CALL_METHOD_1         1  '1 positional argument'
             2114  STORE_FAST               'ecc'

 L.2181      2116  LOAD_GLOBAL              np
             2118  LOAD_METHOD              arctan2
             2120  LOAD_FAST                'parameter_values'
             2122  LOAD_STR                 'esinomega_p'
             2124  LOAD_GLOBAL              str
             2126  LOAD_FAST                'i'
             2128  CALL_FUNCTION_1       1  '1 positional argument'
             2130  BINARY_ADD       
             2132  BINARY_SUBSCR    
             2134  LOAD_FAST                'parameter_values'
             2136  LOAD_STR                 'ecosomega_p'
             2138  LOAD_GLOBAL              str
             2140  LOAD_FAST                'i'
             2142  CALL_FUNCTION_1       1  '1 positional argument'
             2144  BINARY_ADD       
             2146  BINARY_SUBSCR    
             2148  CALL_METHOD_2         2  '2 positional arguments'
             2150  LOAD_CONST               180.0
             2152  BINARY_MULTIPLY  
             2154  LOAD_GLOBAL              np
             2156  LOAD_ATTR                pi
             2158  BINARY_TRUE_DIVIDE
             2160  STORE_FAST               'omega'
             2162  JUMP_FORWARD       2250  'to 2250'
           2164_0  COME_FROM          2066  '2066'

 L.2183      2164  LOAD_FAST                'parameter_values'
             2166  LOAD_STR                 'secosomega_p'
             2168  LOAD_GLOBAL              str
             2170  LOAD_FAST                'i'
             2172  CALL_FUNCTION_1       1  '1 positional argument'
             2174  BINARY_ADD       
             2176  BINARY_SUBSCR    
             2178  LOAD_CONST               2
             2180  BINARY_POWER     
             2182  LOAD_FAST                'parameter_values'
             2184  LOAD_STR                 'sesinomega_p'
             2186  LOAD_GLOBAL              str
             2188  LOAD_FAST                'i'
             2190  CALL_FUNCTION_1       1  '1 positional argument'
             2192  BINARY_ADD       
             2194  BINARY_SUBSCR    
             2196  LOAD_CONST               2
             2198  BINARY_POWER     
             2200  BINARY_ADD       
             2202  STORE_FAST               'ecc'

 L.2184      2204  LOAD_GLOBAL              np
             2206  LOAD_METHOD              arctan2
             2208  LOAD_FAST                'parameter_values'
             2210  LOAD_STR                 'sesinomega_p'
             2212  LOAD_GLOBAL              str
             2214  LOAD_FAST                'i'
             2216  CALL_FUNCTION_1       1  '1 positional argument'
             2218  BINARY_ADD       
             2220  BINARY_SUBSCR    
             2222  LOAD_FAST                'parameter_values'
             2224  LOAD_STR                 'secosomega_p'
             2226  LOAD_GLOBAL              str
             2228  LOAD_FAST                'i'
             2230  CALL_FUNCTION_1       1  '1 positional argument'
             2232  BINARY_ADD       
             2234  BINARY_SUBSCR    
             2236  CALL_METHOD_2         2  '2 positional arguments'
             2238  LOAD_CONST               180.0
             2240  BINARY_MULTIPLY  
             2242  LOAD_GLOBAL              np
             2244  LOAD_ATTR                pi
             2246  BINARY_TRUE_DIVIDE
             2248  STORE_FAST               'omega'
           2250_0  COME_FROM          2162  '2162'
           2250_1  COME_FROM          2048  '2048'

 L.2187      2250  LOAD_FAST                'ecc'
             2252  LOAD_FAST                'self'
             2254  LOAD_ATTR                ecclim
             2256  COMPARE_OP               >
         2258_2260  POP_JUMP_IF_FALSE  2272  'to 2272'

 L.2188      2262  LOAD_CONST               False
             2264  LOAD_FAST                'self'
             2266  STORE_ATTR               modelOK

 L.2189      2268  LOAD_CONST               False
             2270  RETURN_VALUE     
           2272_0  COME_FROM          2258  '2258'

 L.2191      2272  LOAD_CONST               1.0
             2274  LOAD_FAST                'ecc'
             2276  LOAD_GLOBAL              np
             2278  LOAD_METHOD              sin
             2280  LOAD_FAST                'omega'
             2282  LOAD_GLOBAL              np
             2284  LOAD_ATTR                pi
             2286  BINARY_MULTIPLY  
             2288  LOAD_CONST               180.0
             2290  BINARY_TRUE_DIVIDE
             2292  CALL_METHOD_1         1  '1 positional argument'
             2294  BINARY_MULTIPLY  
             2296  BINARY_ADD       
             2298  LOAD_CONST               1.0
             2300  LOAD_FAST                'ecc'
             2302  LOAD_CONST               2
             2304  BINARY_POWER     
             2306  BINARY_SUBTRACT  
             2308  BINARY_TRUE_DIVIDE
             2310  STORE_FAST               'ecc_factor'

 L.2192      2312  LOAD_FAST                'b'
             2314  LOAD_FAST                'a'
             2316  BINARY_TRUE_DIVIDE
             2318  LOAD_FAST                'ecc_factor'
             2320  BINARY_MULTIPLY  
             2322  STORE_FAST               'inc_inv_factor'

 L.2193      2324  LOAD_FAST                'b'
             2326  LOAD_CONST               1.0
             2328  LOAD_FAST                'p'
             2330  BINARY_ADD       
             2332  COMPARE_OP               >
         2334_2336  POP_JUMP_IF_TRUE   3122  'to 3122'
             2338  LOAD_FAST                'inc_inv_factor'
             2340  LOAD_CONST               1.0
             2342  COMPARE_OP               >=
         2344_2346  POP_JUMP_IF_TRUE   3122  'to 3122'

 L.2194      2348  LOAD_FAST                't0'
             2350  LOAD_FAST                'self'
             2352  LOAD_ATTR                model
             2354  LOAD_FAST                'instrument'
             2356  BINARY_SUBSCR    
             2358  LOAD_STR                 'params'
             2360  BINARY_SUBSCR    
             2362  STORE_ATTR               t0

 L.2195      2364  LOAD_FAST                'P'
             2366  LOAD_FAST                'self'
             2368  LOAD_ATTR                model
             2370  LOAD_FAST                'instrument'
             2372  BINARY_SUBSCR    
             2374  LOAD_STR                 'params'
             2376  BINARY_SUBSCR    
             2378  STORE_ATTR               per

 L.2196      2380  LOAD_FAST                'a'
             2382  LOAD_FAST                'self'
             2384  LOAD_ATTR                model
             2386  LOAD_FAST                'instrument'
             2388  BINARY_SUBSCR    
             2390  LOAD_STR                 'params'
             2392  BINARY_SUBSCR    
             2394  STORE_ATTR               a

 L.2197      2396  LOAD_GLOBAL              np
             2398  LOAD_METHOD              arccos
             2400  LOAD_FAST                'inc_inv_factor'
             2402  CALL_METHOD_1         1  '1 positional argument'
             2404  LOAD_CONST               180.0
             2406  BINARY_MULTIPLY  
             2408  LOAD_GLOBAL              np
             2410  LOAD_ATTR                pi
             2412  BINARY_TRUE_DIVIDE
             2414  LOAD_FAST                'self'
             2416  LOAD_ATTR                model
             2418  LOAD_FAST                'instrument'
             2420  BINARY_SUBSCR    
             2422  LOAD_STR                 'params'
             2424  BINARY_SUBSCR    
             2426  STORE_ATTR               inc

 L.2198      2428  LOAD_FAST                'ecc'
             2430  LOAD_FAST                'self'
             2432  LOAD_ATTR                model
             2434  LOAD_FAST                'instrument'
             2436  BINARY_SUBSCR    
             2438  LOAD_STR                 'params'
             2440  BINARY_SUBSCR    
             2442  STORE_ATTR               ecc

 L.2199      2444  LOAD_FAST                'omega'
             2446  LOAD_FAST                'self'
             2448  LOAD_ATTR                model
             2450  LOAD_FAST                'instrument'
             2452  BINARY_SUBSCR    
             2454  LOAD_STR                 'params'
             2456  BINARY_SUBSCR    
             2458  STORE_ATTR               w

 L.2200      2460  LOAD_FAST                'self'
             2462  LOAD_ATTR                dictionary
             2464  LOAD_FAST                'instrument'
             2466  BINARY_SUBSCR    
             2468  LOAD_STR                 'TransitFitCatwoman'
             2470  BINARY_SUBSCR    
         2472_2474  POP_JUMP_IF_TRUE   2494  'to 2494'

 L.2201      2476  LOAD_FAST                'p'
             2478  LOAD_FAST                'self'
             2480  LOAD_ATTR                model
             2482  LOAD_FAST                'instrument'
             2484  BINARY_SUBSCR    
             2486  LOAD_STR                 'params'
             2488  BINARY_SUBSCR    
             2490  STORE_ATTR               rp
             2492  JUMP_FORWARD       2542  'to 2542'
           2494_0  COME_FROM          2472  '2472'

 L.2203      2494  LOAD_FAST                'p1'
             2496  LOAD_FAST                'self'
             2498  LOAD_ATTR                model
             2500  LOAD_FAST                'instrument'
             2502  BINARY_SUBSCR    
             2504  LOAD_STR                 'params'
             2506  BINARY_SUBSCR    
             2508  STORE_ATTR               rp

 L.2204      2510  LOAD_FAST                'p2'
             2512  LOAD_FAST                'self'
             2514  LOAD_ATTR                model
             2516  LOAD_FAST                'instrument'
             2518  BINARY_SUBSCR    
             2520  LOAD_STR                 'params'
             2522  BINARY_SUBSCR    
             2524  STORE_ATTR               rp2

 L.2205      2526  LOAD_FAST                'phi'
             2528  LOAD_FAST                'self'
             2530  LOAD_ATTR                model
             2532  LOAD_FAST                'instrument'
             2534  BINARY_SUBSCR    
             2536  LOAD_STR                 'params'
             2538  BINARY_SUBSCR    
             2540  STORE_ATTR               phi
           2542_0  COME_FROM          2492  '2492'

 L.2206      2542  LOAD_FAST                'self'
             2544  LOAD_ATTR                dictionary
             2546  LOAD_FAST                'instrument'
             2548  BINARY_SUBSCR    
             2550  LOAD_STR                 'ldlaw'
             2552  BINARY_SUBSCR    
             2554  LOAD_STR                 'linear'
             2556  COMPARE_OP               !=
         2558_2560  POP_JUMP_IF_FALSE  2584  'to 2584'

 L.2207      2562  LOAD_FAST                'coeff1'
             2564  LOAD_FAST                'coeff2'
             2566  BUILD_LIST_2          2 
             2568  LOAD_FAST                'self'
             2570  LOAD_ATTR                model
             2572  LOAD_FAST                'instrument'
             2574  BINARY_SUBSCR    
             2576  LOAD_STR                 'params'
             2578  BINARY_SUBSCR    
             2580  STORE_ATTR               u
             2582  JUMP_FORWARD       2602  'to 2602'
           2584_0  COME_FROM          2558  '2558'

 L.2209      2584  LOAD_FAST                'coeff1'
             2586  BUILD_LIST_1          1 
             2588  LOAD_FAST                'self'
             2590  LOAD_ATTR                model
             2592  LOAD_FAST                'instrument'
             2594  BINARY_SUBSCR    
             2596  LOAD_STR                 'params'
             2598  BINARY_SUBSCR    
             2600  STORE_ATTR               u
           2602_0  COME_FROM          2582  '2582'

 L.2214      2602  LOAD_FAST                'self'
             2604  LOAD_ATTR                dictionary
             2606  LOAD_FAST                'instrument'
             2608  BINARY_SUBSCR    
             2610  LOAD_STR                 'TTVs'
             2612  BINARY_SUBSCR    
             2614  LOAD_FAST                'i'
             2616  BINARY_SUBSCR    
             2618  LOAD_STR                 'status'
             2620  BINARY_SUBSCR    
         2622_2624  POP_JUMP_IF_TRUE   2784  'to 2784'

 L.2216      2626  LOAD_FAST                'self'
             2628  LOAD_ATTR                log_like_calc
         2630_2632  POP_JUMP_IF_FALSE  2688  'to 2688'

 L.2217      2634  LOAD_FAST                'self'
             2636  LOAD_ATTR                model
             2638  LOAD_FAST                'instrument'
             2640  BINARY_SUBSCR    
             2642  LOAD_STR                 'M'
             2644  DUP_TOP_TWO      
             2646  BINARY_SUBSCR    
             2648  LOAD_FAST                'self'
             2650  LOAD_ATTR                model
             2652  LOAD_FAST                'instrument'
             2654  BINARY_SUBSCR    
             2656  LOAD_STR                 'm'
             2658  BINARY_SUBSCR    
             2660  LOAD_METHOD              light_curve
             2662  LOAD_FAST                'self'
             2664  LOAD_ATTR                model
             2666  LOAD_FAST                'instrument'
             2668  BINARY_SUBSCR    
             2670  LOAD_STR                 'params'
             2672  BINARY_SUBSCR    
             2674  CALL_METHOD_1         1  '1 positional argument'
             2676  LOAD_CONST               1.0
             2678  BINARY_SUBTRACT  
             2680  INPLACE_ADD      
             2682  ROT_THREE        
             2684  STORE_SUBSCR     
             2686  JUMP_ABSOLUTE      3132  'to 3132'
           2688_0  COME_FROM          2630  '2630'

 L.2219      2688  LOAD_FAST                'self'
             2690  LOAD_ATTR                model
             2692  LOAD_FAST                'instrument'
             2694  BINARY_SUBSCR    
             2696  LOAD_STR                 'm'
             2698  BINARY_SUBSCR    
             2700  LOAD_METHOD              light_curve
             2702  LOAD_FAST                'self'
             2704  LOAD_ATTR                model
             2706  LOAD_FAST                'instrument'
             2708  BINARY_SUBSCR    
             2710  LOAD_STR                 'params'
             2712  BINARY_SUBSCR    
             2714  CALL_METHOD_1         1  '1 positional argument'
             2716  LOAD_FAST                'self'
             2718  LOAD_ATTR                model
             2720  LOAD_FAST                'instrument'
             2722  BINARY_SUBSCR    
             2724  LOAD_STR                 'p'
             2726  LOAD_GLOBAL              str
             2728  LOAD_FAST                'i'
             2730  CALL_FUNCTION_1       1  '1 positional argument'
             2732  BINARY_ADD       
             2734  STORE_SUBSCR     

 L.2220      2736  LOAD_FAST                'self'
             2738  LOAD_ATTR                model
             2740  LOAD_FAST                'instrument'
             2742  BINARY_SUBSCR    
             2744  LOAD_STR                 'M'
             2746  DUP_TOP_TWO      
             2748  BINARY_SUBSCR    
             2750  LOAD_FAST                'self'
             2752  LOAD_ATTR                model
             2754  LOAD_FAST                'instrument'
             2756  BINARY_SUBSCR    
             2758  LOAD_STR                 'p'
             2760  LOAD_GLOBAL              str
             2762  LOAD_FAST                'i'
             2764  CALL_FUNCTION_1       1  '1 positional argument'
             2766  BINARY_ADD       
             2768  BINARY_SUBSCR    
             2770  LOAD_CONST               1.0
             2772  BINARY_SUBTRACT  
             2774  INPLACE_ADD      
             2776  ROT_THREE        
             2778  STORE_SUBSCR     
         2780_2782  JUMP_ABSOLUTE      3132  'to 3132'
           2784_0  COME_FROM          2622  '2622'

 L.2222      2784  LOAD_FAST                'self'
             2786  LOAD_ATTR                dictionary
             2788  LOAD_FAST                'instrument'
             2790  BINARY_SUBSCR    
             2792  LOAD_STR                 'TransitFitCatwoman'
             2794  BINARY_SUBSCR    
         2796_2798  POP_JUMP_IF_TRUE   2894  'to 2894'

 L.2223      2800  LOAD_FAST                'self'
             2802  LOAD_ATTR                dictionary
             2804  LOAD_FAST                'instrument'
             2806  BINARY_SUBSCR    
             2808  LOAD_STR                 'resampling'
             2810  BINARY_SUBSCR    
         2812_2814  POP_JUMP_IF_FALSE  2868  'to 2868'

 L.2224      2816  LOAD_GLOBAL              init_batman
             2818  LOAD_FAST                'dummy_time'
             2820  LOAD_FAST                'self'
             2822  LOAD_ATTR                dictionary
             2824  LOAD_FAST                'instrument'
             2826  BINARY_SUBSCR    
             2828  LOAD_STR                 'ldlaw'
             2830  BINARY_SUBSCR    

 L.2225      2832  LOAD_FAST                'self'
             2834  LOAD_ATTR                dictionary
             2836  LOAD_FAST                'instrument'
             2838  BINARY_SUBSCR    
             2840  LOAD_STR                 'nresampling'
             2842  BINARY_SUBSCR    

 L.2226      2844  LOAD_FAST                'self'
             2846  LOAD_ATTR                dictionary
             2848  LOAD_FAST                'instrument'
             2850  BINARY_SUBSCR    
             2852  LOAD_STR                 'exptimeresampling'
             2854  BINARY_SUBSCR    
             2856  LOAD_CONST               ('nresampling', 'etresampling')
             2858  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2860  UNPACK_SEQUENCE_2     2 
             2862  STORE_FAST               'pm'
             2864  STORE_FAST               'm'
             2866  JUMP_FORWARD       2892  'to 2892'
           2868_0  COME_FROM          2812  '2812'

 L.2228      2868  LOAD_GLOBAL              init_batman
             2870  LOAD_FAST                'dummy_time'
             2872  LOAD_FAST                'self'
             2874  LOAD_ATTR                dictionary
             2876  LOAD_FAST                'instrument'
             2878  BINARY_SUBSCR    
             2880  LOAD_STR                 'ldlaw'
             2882  BINARY_SUBSCR    
             2884  CALL_FUNCTION_2       2  '2 positional arguments'
             2886  UNPACK_SEQUENCE_2     2 
             2888  STORE_FAST               'pm'
             2890  STORE_FAST               'm'
           2892_0  COME_FROM          2866  '2866'
             2892  JUMP_FORWARD       2986  'to 2986'
           2894_0  COME_FROM          2796  '2796'

 L.2230      2894  LOAD_FAST                'self'
             2896  LOAD_ATTR                dictionary
             2898  LOAD_FAST                'instrument'
             2900  BINARY_SUBSCR    
             2902  LOAD_STR                 'resampling'
             2904  BINARY_SUBSCR    
         2906_2908  POP_JUMP_IF_FALSE  2962  'to 2962'

 L.2231      2910  LOAD_GLOBAL              init_catwoman
             2912  LOAD_FAST                'dummy_time'
             2914  LOAD_FAST                'self'
             2916  LOAD_ATTR                dictionary
             2918  LOAD_FAST                'instrument'
             2920  BINARY_SUBSCR    
             2922  LOAD_STR                 'ldlaw'
             2924  BINARY_SUBSCR    

 L.2232      2926  LOAD_FAST                'self'
             2928  LOAD_ATTR                dictionary
             2930  LOAD_FAST                'instrument'
             2932  BINARY_SUBSCR    
             2934  LOAD_STR                 'nresampling'
             2936  BINARY_SUBSCR    

 L.2233      2938  LOAD_FAST                'self'
             2940  LOAD_ATTR                dictionary
             2942  LOAD_FAST                'instrument'
             2944  BINARY_SUBSCR    
             2946  LOAD_STR                 'exptimeresampling'
             2948  BINARY_SUBSCR    
             2950  LOAD_CONST               ('nresampling', 'etresampling')
             2952  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2954  UNPACK_SEQUENCE_2     2 
             2956  STORE_FAST               'pm'
             2958  STORE_FAST               'm'
             2960  JUMP_FORWARD       2986  'to 2986'
           2962_0  COME_FROM          2906  '2906'

 L.2235      2962  LOAD_GLOBAL              init_catwoman
             2964  LOAD_FAST                'dummy_time'
             2966  LOAD_FAST                'self'
             2968  LOAD_ATTR                dictionary
             2970  LOAD_FAST                'instrument'
             2972  BINARY_SUBSCR    
             2974  LOAD_STR                 'ldlaw'
             2976  BINARY_SUBSCR    
             2978  CALL_FUNCTION_2       2  '2 positional arguments'
             2980  UNPACK_SEQUENCE_2     2 
             2982  STORE_FAST               'pm'
             2984  STORE_FAST               'm'
           2986_0  COME_FROM          2960  '2960'
           2986_1  COME_FROM          2892  '2892'

 L.2237      2986  LOAD_FAST                'self'
             2988  LOAD_ATTR                log_like_calc
         2990_2992  POP_JUMP_IF_FALSE  3038  'to 3038'

 L.2238      2994  LOAD_FAST                'self'
             2996  LOAD_ATTR                model
             2998  LOAD_FAST                'instrument'
             3000  BINARY_SUBSCR    
             3002  LOAD_STR                 'M'
             3004  DUP_TOP_TWO      
             3006  BINARY_SUBSCR    
             3008  LOAD_FAST                'm'
             3010  LOAD_METHOD              light_curve
             3012  LOAD_FAST                'self'
             3014  LOAD_ATTR                model
             3016  LOAD_FAST                'instrument'
             3018  BINARY_SUBSCR    
             3020  LOAD_STR                 'params'
             3022  BINARY_SUBSCR    
             3024  CALL_METHOD_1         1  '1 positional argument'
             3026  LOAD_CONST               1.0
             3028  BINARY_SUBTRACT  
             3030  INPLACE_ADD      
             3032  ROT_THREE        
             3034  STORE_SUBSCR     
             3036  JUMP_FORWARD       3120  'to 3120'
           3038_0  COME_FROM          2990  '2990'

 L.2240      3038  LOAD_FAST                'm'
             3040  LOAD_METHOD              light_curve
             3042  LOAD_FAST                'self'
             3044  LOAD_ATTR                model
             3046  LOAD_FAST                'instrument'
             3048  BINARY_SUBSCR    
             3050  LOAD_STR                 'params'
             3052  BINARY_SUBSCR    
             3054  CALL_METHOD_1         1  '1 positional argument'
             3056  LOAD_FAST                'self'
             3058  LOAD_ATTR                model
             3060  LOAD_FAST                'instrument'
             3062  BINARY_SUBSCR    
             3064  LOAD_STR                 'p'
             3066  LOAD_GLOBAL              str
             3068  LOAD_FAST                'i'
             3070  CALL_FUNCTION_1       1  '1 positional argument'
             3072  BINARY_ADD       
             3074  STORE_SUBSCR     

 L.2241      3076  LOAD_FAST                'self'
             3078  LOAD_ATTR                model
             3080  LOAD_FAST                'instrument'
             3082  BINARY_SUBSCR    
             3084  LOAD_STR                 'M'
             3086  DUP_TOP_TWO      
             3088  BINARY_SUBSCR    
             3090  LOAD_FAST                'self'
             3092  LOAD_ATTR                model
             3094  LOAD_FAST                'instrument'
             3096  BINARY_SUBSCR    
             3098  LOAD_STR                 'p'
             3100  LOAD_GLOBAL              str
             3102  LOAD_FAST                'i'
             3104  CALL_FUNCTION_1       1  '1 positional argument'
             3106  BINARY_ADD       
             3108  BINARY_SUBSCR    
             3110  LOAD_CONST               1.0
             3112  BINARY_SUBTRACT  
             3114  INPLACE_ADD      
             3116  ROT_THREE        
             3118  STORE_SUBSCR     
           3120_0  COME_FROM          3036  '3036'
             3120  JUMP_BACK          1272  'to 1272'
           3122_0  COME_FROM          2344  '2344'
           3122_1  COME_FROM          2334  '2334'

 L.2244      3122  LOAD_CONST               False
             3124  LOAD_FAST                'self'
             3126  STORE_ATTR               modelOK

 L.2245      3128  LOAD_CONST               False
             3130  RETURN_VALUE     
         3132_3134  JUMP_BACK          1272  'to 1272'
             3136  POP_BLOCK        
           3138_0  COME_FROM_LOOP     1262  '1262'
           3138_1  COME_FROM           486  '486'

 L.2249      3138  LOAD_FAST                'parameter_values'
             3140  LOAD_STR                 'mdilution_'
             3142  LOAD_FAST                'self'
             3144  LOAD_ATTR                mdilution_iname
             3146  LOAD_FAST                'instrument'
             3148  BINARY_SUBSCR    
             3150  BINARY_ADD       
             3152  BINARY_SUBSCR    
             3154  LOAD_FAST                'parameter_values'
             3156  LOAD_STR                 'mflux_'
             3158  LOAD_FAST                'instrument'
             3160  BINARY_ADD       
             3162  BINARY_SUBSCR    
             3164  ROT_TWO          
             3166  STORE_FAST               'D'
             3168  STORE_FAST               'M'

 L.2250      3170  LOAD_FAST                'self'
             3172  LOAD_ATTR                model
             3174  LOAD_FAST                'instrument'
             3176  BINARY_SUBSCR    
             3178  LOAD_STR                 'M'
             3180  BINARY_SUBSCR    
             3182  LOAD_FAST                'D'
             3184  BINARY_MULTIPLY  
             3186  LOAD_CONST               1.0
             3188  LOAD_FAST                'D'
             3190  BINARY_SUBTRACT  
             3192  BINARY_ADD       
             3194  LOAD_CONST               1.0
             3196  LOAD_CONST               1.0
             3198  LOAD_FAST                'D'
             3200  LOAD_FAST                'M'
             3202  BINARY_MULTIPLY  
             3204  BINARY_ADD       
             3206  BINARY_TRUE_DIVIDE
             3208  BINARY_MULTIPLY  
             3210  LOAD_FAST                'self'
             3212  LOAD_ATTR                model
             3214  LOAD_FAST                'instrument'
             3216  BINARY_SUBSCR    
             3218  LOAD_STR                 'M'
             3220  STORE_SUBSCR     

 L.2253      3222  LOAD_FAST                'self'
             3224  LOAD_ATTR                lm_boolean
             3226  LOAD_FAST                'instrument'
             3228  BINARY_SUBSCR    
         3230_3232  POP_JUMP_IF_FALSE  3390  'to 3390'

 L.2254      3234  LOAD_GLOBAL              np
             3236  LOAD_METHOD              zeros
             3238  LOAD_FAST                'self'
             3240  LOAD_ATTR                ndatapoints_per_instrument
             3242  LOAD_FAST                'instrument'
             3244  BINARY_SUBSCR    
             3246  CALL_METHOD_1         1  '1 positional argument'
             3248  LOAD_FAST                'self'
             3250  LOAD_ATTR                model
             3252  LOAD_FAST                'instrument'
             3254  BINARY_SUBSCR    
             3256  LOAD_STR                 'LM'
             3258  STORE_SUBSCR     

 L.2255      3260  SETUP_LOOP         3350  'to 3350'
             3262  LOAD_GLOBAL              range
             3264  LOAD_FAST                'self'
             3266  LOAD_ATTR                lm_n
             3268  LOAD_FAST                'instrument'
             3270  BINARY_SUBSCR    
             3272  CALL_FUNCTION_1       1  '1 positional argument'
             3274  GET_ITER         
             3276  FOR_ITER           3348  'to 3348'
             3278  STORE_FAST               'i'

 L.2256      3280  LOAD_FAST                'self'
             3282  LOAD_ATTR                model
             3284  LOAD_FAST                'instrument'
             3286  BINARY_SUBSCR    
             3288  LOAD_STR                 'LM'
             3290  DUP_TOP_TWO      
             3292  BINARY_SUBSCR    
             3294  LOAD_FAST                'parameter_values'
             3296  LOAD_STR                 'theta'
             3298  LOAD_GLOBAL              str
             3300  LOAD_FAST                'i'
             3302  CALL_FUNCTION_1       1  '1 positional argument'
             3304  BINARY_ADD       
             3306  LOAD_STR                 '_'
             3308  BINARY_ADD       
             3310  LOAD_FAST                'instrument'
             3312  BINARY_ADD       
             3314  BINARY_SUBSCR    
             3316  LOAD_FAST                'self'
             3318  LOAD_ATTR                lm_arguments
             3320  LOAD_FAST                'instrument'
             3322  BINARY_SUBSCR    
             3324  LOAD_CONST               None
             3326  LOAD_CONST               None
             3328  BUILD_SLICE_2         2 
             3330  LOAD_FAST                'i'
             3332  BUILD_TUPLE_2         2 
             3334  BINARY_SUBSCR    
             3336  BINARY_MULTIPLY  
             3338  INPLACE_ADD      
             3340  ROT_THREE        
             3342  STORE_SUBSCR     
         3344_3346  JUMP_BACK          3276  'to 3276'
             3348  POP_BLOCK        
           3350_0  COME_FROM_LOOP     3260  '3260'

 L.2257      3350  LOAD_FAST                'self'
             3352  LOAD_ATTR                model
             3354  LOAD_FAST                'instrument'
             3356  BINARY_SUBSCR    
             3358  LOAD_STR                 'M'
             3360  BINARY_SUBSCR    
             3362  LOAD_FAST                'self'
             3364  LOAD_ATTR                model
             3366  LOAD_FAST                'instrument'
             3368  BINARY_SUBSCR    
             3370  LOAD_STR                 'LM'
             3372  BINARY_SUBSCR    
             3374  BINARY_ADD       
             3376  LOAD_FAST                'self'
             3378  LOAD_ATTR                model
             3380  LOAD_FAST                'instrument'
             3382  BINARY_SUBSCR    
             3384  LOAD_STR                 'deterministic'
             3386  STORE_SUBSCR     
             3388  JUMP_FORWARD       3414  'to 3414'
           3390_0  COME_FROM          3230  '3230'

 L.2259      3390  LOAD_FAST                'self'
             3392  LOAD_ATTR                model
             3394  LOAD_FAST                'instrument'
             3396  BINARY_SUBSCR    
             3398  LOAD_STR                 'M'
             3400  BINARY_SUBSCR    
             3402  LOAD_FAST                'self'
             3404  LOAD_ATTR                model
             3406  LOAD_FAST                'instrument'
             3408  BINARY_SUBSCR    
             3410  LOAD_STR                 'deterministic'
             3412  STORE_SUBSCR     
           3414_0  COME_FROM          3388  '3388'

 L.2260      3414  LOAD_FAST                'self'
             3416  LOAD_ATTR                errors
             3418  LOAD_FAST                'instrument'
             3420  BINARY_SUBSCR    
             3422  LOAD_CONST               2
             3424  BINARY_POWER     
             3426  LOAD_FAST                'parameter_values'
             3428  LOAD_STR                 'sigma_w_'
             3430  LOAD_FAST                'instrument'
             3432  BINARY_ADD       
             3434  BINARY_SUBSCR    
             3436  LOAD_CONST               1e-06
             3438  BINARY_MULTIPLY  
             3440  LOAD_CONST               2
             3442  BINARY_POWER     
             3444  BINARY_ADD       
             3446  LOAD_FAST                'self'
             3448  LOAD_ATTR                model
             3450  LOAD_FAST                'instrument'
             3452  BINARY_SUBSCR    
             3454  LOAD_STR                 'deterministic_variances'
             3456  STORE_SUBSCR     

 L.2262      3458  LOAD_FAST                'self'
             3460  LOAD_ATTR                global_model
         3462_3464  POP_JUMP_IF_FALSE   438  'to 438'

 L.2263      3466  LOAD_FAST                'self'
             3468  LOAD_ATTR                model
             3470  LOAD_FAST                'instrument'
             3472  BINARY_SUBSCR    
             3474  LOAD_STR                 'deterministic'
             3476  BINARY_SUBSCR    
             3478  LOAD_FAST                'self'
             3480  LOAD_ATTR                model
             3482  LOAD_STR                 'global'
             3484  BINARY_SUBSCR    
             3486  LOAD_FAST                'self'
             3488  LOAD_ATTR                instrument_indexes
             3490  LOAD_FAST                'instrument'
             3492  BINARY_SUBSCR    
             3494  STORE_SUBSCR     

 L.2264      3496  LOAD_FAST                'evaluate_global_errors'
         3498_3500  POP_JUMP_IF_FALSE   438  'to 438'

 L.2265      3502  LOAD_FAST                'self'
             3504  LOAD_ATTR                yerr
             3506  LOAD_FAST                'self'
             3508  LOAD_ATTR                instrument_indexes
             3510  LOAD_FAST                'instrument'
             3512  BINARY_SUBSCR    
             3514  BINARY_SUBSCR    
             3516  LOAD_CONST               2
             3518  BINARY_POWER     

 L.2266      3520  LOAD_FAST                'parameter_values'
             3522  LOAD_STR                 'sigma_w_'
             3524  LOAD_FAST                'instrument'
             3526  BINARY_ADD       
             3528  BINARY_SUBSCR    
             3530  LOAD_CONST               1e-06
             3532  BINARY_MULTIPLY  
             3534  LOAD_CONST               2
             3536  BINARY_POWER     
             3538  BINARY_ADD       
             3540  LOAD_FAST                'self'
             3542  LOAD_ATTR                model
             3544  LOAD_STR                 'global_variances'
             3546  BINARY_SUBSCR    
             3548  LOAD_FAST                'self'
             3550  LOAD_ATTR                instrument_indexes
             3552  LOAD_FAST                'instrument'
             3554  BINARY_SUBSCR    
             3556  STORE_SUBSCR     
         3558_3560  JUMP_BACK           438  'to 438'
             3562  POP_BLOCK        
           3564_0  COME_FROM_LOOP      428  '428'

Parse error at or near `COME_FROM' instruction at offset 1904_0

    def gaussian_log_likelihood(self, residuals, variances):
        taus = 1.0 / variances
        return -0.5 * (len(residuals) * log2pi + np.sum(-np.log(taus) + taus * residuals ** 2))

    def get_log_likelihood(self, parameter_values):
        if self.global_model:
            residuals = self.y - self.model['global']
            if self.dictionary['global_model']['GPDetrend']:
                self.dictionary['global_model']['noise_model'].set_parameter_vector(parameter_values)
                self.dictionary['global_model']['noise_model'].yerr = np.sqrt(self.model['global_variances'])
                self.dictionary['global_model']['noise_model'].compute_GP()
                return self.dictionary['global_model']['noise_model'].GP.log_likelihood(residuals)
            self.gaussian_log_likelihood(residuals, self.model['global_variances'])
        else:
            log_like = 0.0
            for instrument in self.inames:
                residuals = self.data[instrument] - self.model[instrument]['deterministic']
                if self.dictionary[instrument]['GPDetrend']:
                    self.dictionary[instrument]['noise_model'].set_parameter_vector(parameter_values)
                    try:
                        log_like += self.dictionary[instrument]['noise_model'].GP.log_likelihood(residuals)
                    except:
                        log_like = -np.inf
                        break

                else:
                    log_like += self.gaussian_log_likelihood(residuals, self.model[instrument]['deterministic_variances'])

            return log_like

    def set_posterior_samples(self, posterior_samples):
        self.posteriors = posterior_samples
        self.median_posterior_samples = {}
        for parameter in self.posteriors.keys():
            if parameter is not 'unnamed':
                self.median_posterior_samples[parameter] = np.median(self.posteriors[parameter])

        for parameter in self.priors:
            if self.priors[parameter]['distribution'] == 'fixed':
                self.median_posterior_samples[parameter] = self.priors[parameter]['hyperparameters']

        try:
            self.generate(self.median_posterior_samples)
        except:
            print('Warning: model evaluated at the posterior median did not compute properly.')

    def __init__(self, data, modeltype, pl=0.0, pu=1.0, ecclim=1.0, ta=2458460.0, log_like_calc=False):
        self.priors = data.priors
        self.ecclim = ecclim
        self.ta = ta
        self.log_like_calc = log_like_calc
        self.modelOK = True
        self.posteriors = None
        self.median_posterior_samples = None
        self.ndatapoints_per_instrument = {}
        if modeltype == 'lc':
            self.modeltype = 'lc'
            self.t = data.t_lc
            self.y = data.y_lc
            self.yerr = data.yerr_lc
            self.times = data.times_lc
            self.data = data.data_lc
            self.errors = data.errors_lc
            self.instruments = data.instruments_lc
            self.ninstruments = data.ninstruments_lc
            self.inames = data.inames_lc
            self.instrument_indexes = data.instrument_indexes_lc
            self.lm_boolean = data.lm_lc_boolean
            self.lm_arguments = data.lm_lc_arguments
            self.lm_n = {}
            self.pl = pl
            self.pu = pu
            self.Ar = (self.pu - self.pl) / (2.0 + self.pl + self.pu)
            self.global_model = data.global_lc_model
            self.dictionary = data.lc_options
            self.numbering = data.numbering_transiting_planets
            self.numbering.sort()
            self.nplanets = len(self.numbering)
            self.model = {}
            if self.global_model:
                self.model['global'] = np.zeros(len(self.t))
                self.model['global_variances'] = np.zeros(len(self.t))
                self.model['deterministic'] = np.zeros(len(self.t))
            self.ld_iname = {}
            self.mdilution_iname = {}
            self.ndatapoints_all_instruments = 0.0
            self.Tflag = False
            self.N_TTVs = {}
            self.Tparametrization = {}
            for pi in self.numbering:
                self.N_TTVs[pi] = 0.0

            for instrument in self.inames:
                for pi in self.numbering:
                    if self.dictionary[instrument]['TTVs'][pi]['status']:
                        if self.dictionary[instrument]['TTVs'][pi]['parametrization'] == 'T':
                            self.Tparametrization[pi] = True
                            self.Tflag = True
                        self.N_TTVs[pi] += self.dictionary[instrument]['TTVs'][pi]['totalTTVtransits']

                self.model[instrument] = {}
                self.ndatapoints_per_instrument[instrument] = len(self.instrument_indexes[instrument])
                self.ndatapoints_all_instruments += self.ndatapoints_per_instrument[instrument]
                if self.lm_boolean[instrument]:
                    self.lm_n[instrument] = self.lm_arguments[instrument].shape[1]
                self.model[instrument]['ones'] = np.ones(len(self.instrument_indexes[instrument]))
                self.model[instrument]['M'] = np.ones(len(self.instrument_indexes[instrument]))
                self.model[instrument]['LM'] = np.zeros(len(self.instrument_indexes[instrument]))
                self.model[instrument]['deterministic'] = np.zeros(len(self.instrument_indexes[instrument]))
                self.model[instrument]['deterministic_errors'] = np.zeros(len(self.instrument_indexes[instrument]))
                if self.dictionary[instrument]['TransitFit']:
                    if self.dictionary[instrument]['resampling']:
                        if not self.dictionary[instrument]['TransitFitCatwoman']:
                            self.model[instrument]['params'], self.model[instrument]['m'] = init_batman((self.times[instrument]), (self.dictionary[instrument]['ldlaw']), nresampling=(self.dictionary[instrument]['nresampling']),
                              etresampling=(self.dictionary[instrument]['exptimeresampling']))
                        else:
                            self.model[instrument]['params'], self.model[instrument]['m'] = init_catwoman((self.times[instrument]), (self.dictionary[instrument]['ldlaw']), nresampling=(self.dictionary[instrument]['nresampling']),
                              etresampling=(self.dictionary[instrument]['exptimeresampling']))
                    else:
                        if not self.dictionary[instrument]['TransitFitCatwoman']:
                            self.model[instrument]['params'], self.model[instrument]['m'] = init_batman(self.times[instrument], self.dictionary[instrument]['ldlaw'])
                        else:
                            self.model[instrument]['params'], self.model[instrument]['m'] = init_catwoman(self.times[instrument], self.dictionary[instrument]['ldlaw'])
                    for i in self.numbering:
                        self.model[instrument]['p' + str(i)] = np.ones(len(self.instrument_indexes[instrument]))

                    for pname in self.priors.keys():
                        if pname[0:2] == 'q1':
                            vec = pname.split('_')
                            if len(vec) > 2:
                                if instrument in vec:
                                    self.ld_iname[instrument] = '_'.join(vec[1:])
                            elif instrument in vec:
                                self.ld_iname[instrument] = vec[1]
                            if pname[0:9] == 'mdilution':
                                vec = pname.split('_')
                                if len(vec) > 2:
                                    if instrument in vec:
                                        self.mdilution_iname[instrument] = '_'.join(vec[1:])
                                else:
                                    self.mdilution_iname[instrument] = vec[1]

                else:
                    for pname in self.priors.keys():
                        if pname[0:9] == 'mdilution':
                            vec = pname.split('_')
                            if len(vec) > 2:
                                if instrument in vec:
                                    self.mdilution_iname[instrument] = '_'.join(vec[1:])
                            else:
                                self.mdilution_iname[instrument] = vec[1]

            self.evaluate = self.evaluate_model
            self.generate = self.generate_lc_model
        else:
            if modeltype == 'rv':
                self.modeltype = 'rv'
                self.t = data.t_rv
                self.y = data.y_rv
                self.yerr = data.yerr_rv
                self.times = data.times_rv
                self.data = data.data_rv
                self.errors = data.errors_rv
                self.instruments = data.instruments_rv
                self.ninstruments = data.ninstruments_rv
                self.inames = data.inames_rv
                self.instrument_indexes = data.instrument_indexes_rv
                self.lm_boolean = data.lm_rv_boolean
                self.lm_arguments = data.lm_rv_arguments
                self.lm_n = {}
                self.global_model = data.global_rv_model
                self.dictionary = data.rv_options
                self.numbering = data.numbering_rv_planets
                self.numbering.sort()
                self.nplanets = len(self.numbering)
                self.model = {}
                self.ndatapoints_all_instruments = 0.0
                if self.global_model:
                    self.model['global'] = np.zeros(len(self.t))
                    self.model['global_variances'] = np.zeros(len(self.t))
                self.model['radvel'] = init_radvel(nplanets=(self.nplanets))
                for i in self.numbering:
                    self.model['p' + str(i)] = np.ones(len(self.t))

                self.model['Keplerian'] = np.ones(len(self.t))
                self.model['Keplerian+Trend'] = np.ones(len(self.t))
                for instrument in self.inames:
                    self.model[instrument] = {}
                    self.ndatapoints_per_instrument[instrument] = len(self.instrument_indexes[instrument])
                    self.ndatapoints_all_instruments += self.ndatapoints_per_instrument[instrument]
                    if self.lm_boolean[instrument]:
                        self.lm_n[instrument] = self.lm_arguments[instrument].shape[1]
                    self.model[instrument]['M'] = np.ones(len(self.instrument_indexes[instrument]))
                    self.model[instrument]['LM'] = np.zeros(len(self.instrument_indexes[instrument]))
                    self.model[instrument]['deterministic'] = np.zeros(len(self.instrument_indexes[instrument]))
                    self.model[instrument]['deterministic_errors'] = np.zeros(len(self.instrument_indexes[instrument]))
                    for i in self.numbering:
                        self.model[instrument]['p' + str(i)] = np.ones(len(self.instrument_indexes[instrument]))

                    self.model[instrument]['ones'] = np.ones(len(self.t[self.instrument_indexes[instrument]]))

                self.evaluate = self.evaluate_model
                self.generate = self.generate_rv_model
            else:
                raise Exception('Model type "' + lc + '" not recognized. Currently it can only be "lc" for a light-curve model or "rv" for radial-velocity model.')


class gaussian_process(object):
    __doc__ = "\n    Given a juliet data object (created via juliet.load), a model type (i.e., is this a GP for a RV or lightcurve dataset) and \n    an instrument name, this object generates a Gaussian Process (GP) object to use within the juliet library. Example usage:\n\n               >>> GPmodel = juliet.gaussian_process(data, model_type = 'lc', instrument = 'TESS')\n\n    :param data (juliet.load object)\n        Object containing all the information about the current dataset. This will help in determining the type of kernel \n        the input instrument has and also if the instrument has any errors associated with it to initialize the kernel.\n\n    :param model_type: (string)\n        A string defining the type of data the GP will be modelling. Can be either ``lc`` (for photometry) or ``rv`` (for radial-velocities).\n\n    :param instrument: (string)\n        A string indicating the name of the instrument the GP is being applied to. This string simplifies cross-talk with juliet's ``posteriors`` \n        dictionary.\n\n    :param george_hodlr: (optional, boolean)\n        If True, this uses George's HODLR solver (faster).\n\n    "

    def get_kernel_name(self, priors):
        variables_that_match = []
        for pname in priors.keys():
            vec = pname.split('_')
            if vec[0] == 'GP' and self.instrument in vec:
                variables_that_match = variables_that_match + [vec[1]]

        n_variables_that_match = len(variables_that_match)
        if n_variables_that_match == 0:
            raise Exception('Input error: it seems instrument ' + self.instrument + ' has no defined priors in the prior file for a Gaussian Process. Check the prior file and try again.')
        for kernel_name in self.all_kernel_variables.keys():
            counter = 0
            for variable_name in self.all_kernel_variables[kernel_name]:
                if variable_name in variables_that_match:
                    counter += 1

            if n_variables_that_match == counter and len(self.all_kernel_variables[kernel_name]) == n_variables_that_match:
                return kernel_name

    def init_GP(self):
        if self.use_celerite:
            self.GP = celerite.GP((self.kernel), mean=0.0)
        else:
            if self.global_GP:
                if self.george_hodlr:
                    self.GP = george.GP((self.kernel), mean=0.0, fit_mean=False, fit_white_noise=False,
                      solver=(george.HODLRSolver))
                else:
                    self.GP = george.GP((self.kernel), mean=0.0, fit_mean=False, fit_white_noise=False)
            else:
                jitter_term = george.modeling.ConstantModel(1.0)
                if self.george_hodlr:
                    self.GP = george.GP((self.kernel), mean=0.0, fit_mean=False, white_noise=jitter_term, fit_white_noise=True,
                      solver=(george.HODLRSolver))
                else:
                    self.GP = george.GP((self.kernel), mean=0.0, fit_mean=False, white_noise=jitter_term, fit_white_noise=True)
        self.compute_GP()

    def compute_GP(self, X=None):
        if self.yerr is not None:
            if X is None:
                self.GP.compute((self.X), yerr=(self.yerr))
            else:
                self.GP.compute(X, yerr=(self.yerr))
        elif X is None:
            self.GP.compute(self.X)
        else:
            self.GP.compute(X)

    def set_input_instrument(self, input_variables):
        for i in range(len(self.variables)):
            GPvariable = self.variables[i]
            for pnames in input_variables.keys():
                vec = pnames.split('_')
                if vec[0] == 'GP' and GPvariable in vec[1] and self.instrument in vec:
                    self.input_instrument.append('_'.join(vec[2:]))

    def set_parameter_vector(self, parameter_values):
        base_index = 0
        if self.kernel_name == 'SEKernel':
            if not self.global_GP:
                self.parameter_vector[base_index] = np.log((parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor) ** 2)
                base_index += 1
            self.parameter_vector[base_index] = np.log((parameter_values[('GP_sigma_' + self.input_instrument[0])] * self.sigma_factor) ** 2.0)
            for i in range(self.nX):
                self.parameter_vector[base_index + 1 + i] = np.log(1.0 / parameter_values[('GP_alpha' + str(i) + '_' + self.input_instrument[(1 + i)])])

        else:
            if self.kernel_name == 'ExpSineSquaredSEKernel':
                if not self.global_GP:
                    self.parameter_vector[base_index] = np.log((parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor) ** 2)
                    base_index += 1
                self.parameter_vector[base_index] = np.log((parameter_values[('GP_sigma_' + self.input_instrument[0])] * self.sigma_factor) ** 2.0)
                self.parameter_vector[base_index + 1] = np.log(1.0 / parameter_values[('GP_alpha_' + self.input_instrument[1])])
                self.parameter_vector[base_index + 2] = parameter_values[('GP_Gamma_' + self.input_instrument[2])]
                self.parameter_vector[base_index + 3] = np.log(parameter_values[('GP_Prot_' + self.input_instrument[3])])
            else:
                if self.kernel_name == 'CeleriteQPKernel':
                    self.parameter_vector[0] = np.log(parameter_values[('GP_B_' + self.input_instrument[0])])
                    self.parameter_vector[1] = np.log(parameter_values[('GP_L_' + self.input_instrument[1])])
                    self.parameter_vector[2] = np.log(parameter_values[('GP_Prot_' + self.input_instrument[2])])
                    self.parameter_vector[3] = np.log(parameter_values[('GP_C_' + self.input_instrument[3])])
                    self.parameter_vector[4] = self.global_GP or np.log(parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor)
                else:
                    if self.kernel_name == 'CeleriteExpKernel':
                        self.parameter_vector[0] = np.log(parameter_values[('GP_sigma_' + self.input_instrument[0])])
                        self.parameter_vector[1] = np.log(parameter_values[('GP_timescale_' + self.input_instrument[1])])
                        self.parameter_vector[2] = self.global_GP or np.log(parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor)
                    else:
                        if self.kernel_name == 'CeleriteMaternKernel':
                            self.parameter_vector[0] = np.log(parameter_values[('GP_sigma_' + self.input_instrument[0])])
                            self.parameter_vector[1] = np.log(parameter_values[('GP_rho_' + self.input_instrument[1])])
                            self.parameter_vector[2] = self.global_GP or np.log(parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor)
                        else:
                            if self.kernel_name == 'CeleriteMaternExpKernel':
                                self.parameter_vector[0] = np.log(parameter_values[('GP_sigma_' + self.input_instrument[0])])
                                self.parameter_vector[1] = np.log(parameter_values[('GP_timescale_' + self.input_instrument[1])])
                                self.parameter_vector[3] = np.log(parameter_values[('GP_rho_' + self.input_instrument[2])])
                                self.parameter_vector[4] = self.global_GP or np.log(parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor)
                            else:
                                if self.kernel_name == 'CeleriteSHOKernel':
                                    self.parameter_vector[0] = np.log(parameter_values[('GP_S0_' + self.input_instrument[0])])
                                    self.parameter_vector[1] = np.log(parameter_values[('GP_Q_' + self.input_instrument[1])])
                                    self.parameter_vector[2] = np.log(parameter_values[('GP_omega0_' + self.input_instrument[2])])
                                    if not self.global_GP:
                                        self.parameter_vector[3] = np.log(parameter_values[('sigma_w_' + self.instrument)] * self.sigma_factor)
                                self.GP.set_parameter_vector(self.parameter_vector)

    def __init__(self, data, model_type, instrument, george_hodlr=True, matern_eps=0.01):
        self.isInit = False
        self.model_type = model_type.lower()
        if self.model_type == 'lc':
            if instrument is None:
                instrument = 'lc'
            self.sigma_factor = 1e-06
        else:
            if self.model_type == 'rv':
                if instrument is None:
                    instrument = 'rv'
                self.sigma_factor = 1.0
            else:
                raise Exception('Model type ' + model_type + ' currently not supported. Only "lc" or "rv" can serve as inputs for now.')
        self.instrument = instrument
        self.global_GP = False
        if self.model_type == 'lc':
            if instrument == 'lc':
                self.X = data.GP_lc_arguments['lc']
                self.global_GP = True
            else:
                self.X = data.GP_lc_arguments[instrument]
            if data.yerr_lc is not None:
                if instrument != 'lc':
                    self.yerr = data.yerr_lc[data.instrument_indexes_lc[instrument]]
                else:
                    self.yerr = data.yerr_lc
            else:
                self.yerr = None
        else:
            if self.model_type == 'rv':
                if instrument == 'rv':
                    self.X = data.GP_rv_arguments['rv']
                    self.global_GP = True
                else:
                    self.X = data.GP_rv_arguments[instrument]
                if data.yerr_rv is not None:
                    if instrument != 'rv':
                        self.yerr = data.yerr_rv[data.instrument_indexes_rv[instrument]]
                    else:
                        self.yerr = data.yerr_rv
                else:
                    self.yerr = None
            else:
                if len(self.X.shape) == 2:
                    if self.X.shape[1] != 1:
                        self.nX = self.X.shape[1]
                    else:
                        self.X = self.X[:, 0]
                        self.nX = 1
                else:
                    self.nX = 1
                self.all_kernel_variables = {}
                self.all_kernel_variables['SEKernel'] = [
                 'sigma']
                for i in range(self.nX):
                    self.all_kernel_variables['SEKernel'] = self.all_kernel_variables['SEKernel'] + ['alpha' + str(i)]

                self.all_kernel_variables['ExpSineSquaredSEKernel'] = [
                 'sigma', 'alpha', 'Gamma', 'Prot']
                self.all_kernel_variables['CeleriteQPKernel'] = ['B', 'L', 'Prot', 'C']
                self.all_kernel_variables['CeleriteExpKernel'] = ['sigma', 'timescale']
                self.all_kernel_variables['CeleriteMaternKernel'] = ['sigma', 'rho']
                self.all_kernel_variables['CeleriteMaternExpKernel'] = ['sigma', 'timescale', 'rho']
                self.all_kernel_variables['CeleriteSHOKernel'] = ['S0', 'Q', 'omega0']
                self.kernel_name = self.get_kernel_name(data.priors)
                self.GP = None
                self.use_celerite = False
                if george_hodlr:
                    self.george_hodlr = True
                else:
                    self.george_hodlr = False
            self.input_instrument = []
            self.variables = self.all_kernel_variables[self.kernel_name]
            phantomvariable = 0
        if self.kernel_name == 'SEKernel':
            self.kernel = 1.0 * george.kernels.ExpSquaredKernel((np.ones(self.nX)), ndim=(self.nX), axes=(range(self.nX)))
        else:
            if self.kernel_name == 'ExpSineSquaredSEKernel':
                K1 = 1.0 * george.kernels.ExpSquaredKernel(metric=1.0)
                K2 = george.kernels.ExpSine2Kernel(gamma=1.0, log_period=1.0)
                self.kernel = K1 * K2
            else:
                if self.kernel_name == 'CeleriteQPKernel':
                    rot_kernel = terms.TermSum(RotationTerm(log_amp=(np.log(10.0)), log_timescale=(np.log(10.0)),
                      log_period=(np.log(3.0)),
                      log_factor=(np.log(1.0))))
                    kernel_jitter = terms.JitterTerm(np.log(9.999999999999999e-05))
                    if self.instrument in ('rv', 'lc'):
                        self.kernel = rot_kernel
                    else:
                        self.kernel = rot_kernel + kernel_jitter
                    self.use_celerite = True
                else:
                    if self.kernel_name == 'CeleriteExpKernel':
                        exp_kernel = terms.RealTerm(log_a=(np.log(10.0)), log_c=(np.log(10.0)))
                        kernel_jitter = terms.JitterTerm(np.log(9.999999999999999e-05))
                        if self.instrument in ('rv', 'lc'):
                            self.kernel = exp_kernel
                        else:
                            self.kernel = exp_kernel + kernel_jitter
                        self.use_celerite = True
                    else:
                        if self.kernel_name == 'CeleriteMaternKernel':
                            matern_kernel = terms.Matern32Term(log_sigma=(np.log(10.0)), log_rho=(np.log(10.0)), eps=matern_eps)
                            kernel_jitter = terms.JitterTerm(np.log(9.999999999999999e-05))
                            if self.instrument in ('rv', 'lc'):
                                self.kernel = matern_kernel
                            else:
                                self.kernel = matern_kernel + kernel_jitter
                            self.use_celerite = True
                        else:
                            if self.kernel_name == 'CeleriteMaternExpKernel':
                                matern_kernel = terms.Matern32Term(log_sigma=(np.log(10.0)), log_rho=(np.log(10.0)), eps=matern_eps)
                                exp_kernel = terms.RealTerm(log_a=(np.log(10.0)), log_c=(np.log(10.0)))
                                kernel_jitter = terms.JitterTerm(np.log(9.999999999999999e-05))
                                if self.instrument in ('rv', 'lc'):
                                    self.kernel = exp_kernel * matern_kernel
                                else:
                                    self.kernel = exp_kernel * matern_kernel + kernel_jitter
                                phantomvariable = 1
                                self.use_celerite = True
                            else:
                                if self.kernel_name == 'CeleriteSHOKernel':
                                    sho_kernel = terms.SHOTerm(log_S0=(np.log(10.0)), log_Q=(np.log(10.0)), log_omega0=(np.log(10.0)))
                                    kernel_jitter = terms.JitterTerm(np.log(9.999999999999999e-05))
                                    if self.instrument in ('rv', 'lc'):
                                        self.kernel = sho_kernel
                                    else:
                                        self.kernel = sho_kernel + kernel_jitter
                                    self.use_celerite = True
                                elif self.use_celerite:
                                    idx_sorted = np.argsort(self.X)
                                    lX = len(self.X)
                                    diff1 = np.count_nonzero(self.X - self.X[idx_sorted])
                                    diff2 = np.count_nonzero(self.X - self.X[idx_sorted[::-1]])
                                    if diff1 == 0 or diff2 == 0:
                                        self.init_GP()
                                        self.isInit = True
                                    else:
                                        self.init_GP()
                                        self.isInit = True
                                    if self.global_GP:
                                        self.parameter_vector = np.zeros(len(self.variables) + phantomvariable)
                                else:
                                    self.parameter_vector = np.zeros(len(self.variables) + 1 + phantomvariable)
                                self.set_input_instrument(data.priors)