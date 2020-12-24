# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/PyGS/PyGS.py
# Compiled at: 2013-11-06 06:45:28
"""
Created on May 22, 2012

@author: Steven Murray and Jake Hebert

    PyGS (Python Galaxy Survey) is designed to be an interactive class to deal with large-scale redshift surveys.
    
    Its ideal is to make the run-of-the-mill operations as simple as possible, but to provide enough flexibility
    in the background to be of real usefulness. While intended as an interactive class, for use with the python
    shell or IPython, it can of course also be scripted.
    
    Many of the more intensive routines are written in Fortran and made available through F2PY.
    
    Instantiating the class requires a filename, or folder, which contains the survey information (redshifts,
    angles, magnitudes etc.). Once the import of the data has been successful, a directory structure will be
    created which is intended to allow speed-of-access and computation, and ease-of-reuse for future 
    calculations. See the documentation for __init__ for detailed explanations.
    
    Most calculations have default options which will be used in the absence of user-specified options, and these
    are deemed to be the most common usages of the method. However, there is always the opportunity to tweak these
    as needed. Generally there are 'convenience' functions for performing a series of calculations, where it is
    common to do these together.

"""
history = "\n0.5.0 - 06/11/2013\n        MANY MANY CHANGES - I haven't been updating the history for most of them\n        Mostly now there is working luminosity functions and selection functions\n        Non-interactive Import is still a bit buggy.\n        \n0.4.2 - 02/05/2013\n        Minor updates and bugfixes\n        Convert pandas series to numpy array for FD_bins function.\n        \n0.4.1 - 30/05/2013\n        Re-organised code so that external modules have intrinsic functions which\n        are USED by PyGS but not automatically classes - makes it easier to trace\n        bugs.\n        Re-wrote lumfunc code.\n        \n0.4.0 - 15/05/13 (final)\n        Made DFT multi-threaded for performance\n        Modified Power Spectra functions to be easier to call and takes weights        \n        Added dependencies to setup script.\n        Made it possible to have non-interactive Import\n        \n0.4.0 - 07/05/13 (alpha)\n        Major (backwards-incompatible) update.\n        Now the project file is in HDF5 format, eliciting faster read-in.\n        numpy recarrays replaced with pandas DataFrame\n        Extreme simplification of __init__ method logic\n        Made most units smaller and more manageable.\n        \n0.3.3 - 08/04/13\n        Added clean() method to PyGS object which gets rid of 'stupid' data\n        Severely changed lumfunct.f90 to be cleaner\n        \n0.3.2 - 05/03/13\n        Jake Hebert wrote fortran code to calculate EEP luminosity function\n        Integrated this code into the PyGS package.\n        Fixed a typo which made the whole program useless\n        Fixed a bug with _LumDistance()\n        \n0.3.1 - 22/01/13\n        Added an empty 'Cosmology' module/class which will be used to output cosmology plots\n        Put correct units on many of the power spectra plots\n        Added a uniqueness test based on ID to the import.\n        \n0.3.0 - 4/12/12\n        Major re-organization of code to be much more modular. \n        Each type of calculation has a separate module containing a subclass of PyGS.\n        Not much difference to the interface.\n        \n0.2.5 - 13/11/12\n        Now calculates the K-Correction, the luminosity distance, absolute magnitude, and luminosity\n        Author: Jake Hebert\n        \n0.2.4 - 12/11/12\n        Cleaned up column-specifying behaviour. \n        \n0.2.3 - 8/11/12\n        Thanks to Jake Hebert, fixed a bug on importing. \n        Now imports g-band apparent magnitudes ready for K-corrections.\n        \n0.2.2 - 17/09/12\n        Now can calculate selection function upon import and deals with weight values more homogeneously\n        Added support for power spectra (fixed) and histograms to receive the weights.\n        NOTE: selection function calculated for data stopping before z=0.25 seems to be inaccurate.\n        \n0.2.1 - 17/09/12\n        Updated the radial power spectra calculations to involve an optional weighting form the selection function.\n        \n0.2.0 - 17/09/12\n        Added simple selection function routines, to define AND create samples from the analytic selection function.\n        \n0.1.5 - 14/09/12\n        Imports sample cuts from file when starting from a sample file for more homogeneous usage.\n        \n0.1.4 - 13/09/12\n        Changed default bounds of 1D power spectra to be more useful.\n        Fixed bug which made program hang if 'no' was selected when asked to overwrite project folder.\n        Fixed bug where setting a cut to 0 would render it useless.\n        \n0.1.3 - Hid LuminosityFromAppMag method from user\n        Cleaned up a lot of input/raw_input statements\n        Fixed a bug that meant angles weren't converting to radians\n        Cut specification overhaul with range now indicated and if a cut removes all data it is flagged and you must re-specify.\n        \n0.1.2 - Hid unwanted methods and variables from end user (6/09/12)\n0.1.1 - Fixed import when importing from scratch. Now creates sample directory properly. (6/09/12)\n0.1.0 - All power spectra implemented, and importing of data roughly implemented.\n"
import sys, os, errno, time, pandas
from cosmolopy import *
try:
    import numpy as np
except:
    sys.exit('Please install Numpy')

try:
    import matplotlib.pyplot as plt
except:
    sys.exit('Please install matplotlib')

import LuminosityFunction as lf, PowerSpectra as ps, Correlations as cf, utils, SelectionFunction as sf

class Import(object):

    def __init__(self, filename, radians=True, cosmology=fidcosmo, sample_name=None, sample_cuts=None, clobber=None, verbose=True):
        """
        Imports the survey and creates a project directory and internal structure. 
        
        Instantiating the class requires a filename or directory in which is kept (solely) the survey information.
        This step is designed to be as seamless as possible. To this end, note the following:
        
        The default expected input is one ascii file with columns as data fields.
        
        If the survey information is in a completely different format, then the best thing to to do is reformat it 
        yourself and try again. And email me the problem and I'll try to update the class to deal with it.
        
        Once the information is read in, a project directory is automatically created. This serves to speed up future
        calculations and simplify the layout of results from your survey. The project folder is named
        <survey_filename>_project/ and included is an empty file "_PyLSSproject_" which serves to tell this class that
        the folder is in fact formatted in the default way. Within this folder the directory structure looks like:
        
        <my_survey>.[dat,csv, etc.]
        <my_survey>_project/
            _PyLSSproject_
            <my_survey>.h5   #Correctly formatted (HDF5) survey
            All/
                _PyLSSsample_
                <plot_varieties>/
                    plot.pdf
                    another_plot.pdf
                    ...
                ...
            <other_sample_name>/
                _PyLSSsample_
                <plot_varieties>/
                    plot.pdf
                    another_plot.pdf
                    ...
                ...
            
        A note on cosmologies: changing the fiducial cosmology will potentially change many of the calculations
        for a given survey (especially those relying on distances). This is reflected in the "Sample" directory
        level. That is, two identical samples of the main survey will be called different samples if their
        cosmology is specified differently.
        
        INPUT:
            radians [True] bool
            #Whether the data is in radians to begin with.

            cosmology [fidcosmo] dict  
            #A dictionary of cosmological parameters. Default is cosmolopy's default.

            sample_name [None] string
            #Which sample to use (can always be 'all', otherwise will make one)
                 
            sample_cuts [None] dict
            #Cuts to apply to the sample, takes the form
            sample_cuts = {"redshift":[min_z,max_z],"ra":[min_z,max_z]...}
   
            clobber [None] bool
            # Whether to overwrite project directory if appropriate
                
        """
        self.cosmology = cosmology
        self.sample_name = sample_name
        self.sample_cuts = sample_cuts
        self._clobber = clobber
        self.verbose = verbose
        self.plottype = 'png'
        self._raw_columns = [
         'redshift', 'ra', 'dec', 'mag_r', 'mag_g', 'id', 'extinction_r', 'extinction_g']
        is_project_file, self._project_dir, filename = self._determine_if_project(filename)
        if not is_project_file:
            self._initial_file_import(filename, radians)
            self._create_project_dir(filename)
            os.chdir(self._project_dir)
            self._write_project_file(filename)
            filename = os.path.join(self._project_dir, os.path.split(filename)[1].split('.')[0] + '.h5')
        self.sample_name, self.sample_cuts, query = self._define_sample(filename)
        print query
        self._create_sample_dir(self.sample_name)
        self._sample_dir = os.path.join(self._project_dir, self.sample_name)
        self._make_result_dirs()
        self._write_sample_cuts_cosmo(filename, self.sample_name, self.sample_cuts)
        self._project_file_import(filename, query)
        self._cut_data(self.sample_cuts)
        self.survey_data['c_dist'] = cd.comoving_distance(self.survey_data['redshift'], **self.cosmology)
        lum_dist = lf.lum_dist(self.survey_data['redshift'], self.survey_data['c_dist'])
        gr = self.survey_data['mag_g'] - self.survey_data['mag_r'] - self.survey_data['extinction_g'] - self.survey_data['extinction_r']
        self.survey_data['kcorr'] = lf.k_correct(self.survey_data['redshift'], gr)
        self.survey_data['absmag'] = lf.absolute_mag(self.survey_data['mag_r'], lum_dist, self.survey_data['kcorr'], self.survey_data['extinction_r'])
        self.survey_data['lum'] = lf.absmag_to_lum(self.survey_data['absmag'])
        self.clean()
        self.N = self.survey_data.shape[0]
        self.survey_name = os.path.split(self._project_dir)[1].replace('_Project', '')
        self._define_z_from_dist()

    def _determine_if_project(self, filename):
        """
        Determines if the input file is a project file or not
        """
        project_dir = filename.partition('.')[0] + '_Project'
        if '_PyLSSProject_' in os.listdir(os.path.split(filename)[0]):
            is_project_file = True
            project_dir = os.path.split(filename)[0]
        elif os.path.isdir(project_dir):
            if self._clobber is None:
                do_continue = raw_input('A project folder for this survey has ' + 'already been created, would you like ' + 'to overwrite it (y) or use its ' + 'contents (n)?')
                while do_continue[0] not in 'yn':
                    do_continue = raw_input('Overwrite? Please type y or n: ')

                do_continue = do_continue[0]
            elif self._clobber:
                do_continue = 'y'
            else:
                do_continue = 'n'
            if do_continue is 'n' and os.path.isfile(project_dir + '/' + os.path.split(filename)[1].split('.')[0] + '.h5'):
                is_project_file = True
                filename = project_dir + '/' + os.path.split(filename)[1].split('.')[0] + '.h5'
            elif do_continue is 'n':
                print 'Apparently the actual survey in the project folder has been deleted.'
                is_project_file = False
            elif do_continue is 'y':
                is_project_file = False
        else:
            is_project_file = False
        return (is_project_file, project_dir, filename)

    def _mkdir(self, foldername):
        """
        A utility function to make directories under the sample directory
        """
        try:
            os.makedirs(self._dirs[foldername])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def _make_result_dirs(self):
        """
        Simply makes the directories under the sample directory that will hold the results
        """
        plot_dirs = [
         'SurveyPlots', 'PowerSpecs_1D', 'PowerSpecs_2D', 'FilteredData',
         'CorrelationFunctions', 'LuminosityFunction', 'SelectionFunction']
        self._dirs = {}
        for folder in plot_dirs:
            self._dirs[folder] = self._sample_dir + '/' + folder + '/'
            self._mkdir(folder)

    def _initial_file_import(self, filename, radians=True):
        """
        This method imports the file for the first time (the hard part...)
        """
        if os.path.isfile(filename):
            self.survey_data = pandas.read_csv(filename)
        else:
            sys.exit('Your filename was not a true filename. Filename: ' + filename)
        for col in self.survey_data.columns:
            self.survey_data.rename(columns={col: col.lower()}, inplace=True)

        print 'This survey contains ', len(self.survey_data), ' galaxies'
        print 'The field names of the data just read are: '
        print self.survey_data.columns
        got_all = True
        for col in self._raw_columns:
            got_all = col in self.survey_data.columns and got_all

        if got_all:
            self.survey_data = self.survey_data[self._raw_columns]
            return
        print 'Attempting automatic conversion to PyGS format... ',
        aliases = {'redshift': ['z'], 'mag_r': [
                   'modelmag_r', 'cmodelmag_r'], 
           'mag_g': [
                   'modelmag_g', 'cmodelmag_g'], 
           'id': [
                'specobjid', 'specobj_id', 'objid']}
        for key, val in aliases.iteritems():
            for col in self.survey_data.columns:
                if col in val:
                    self.survey_data.rename(columns={col: key}, inplace=True)

        got_all = True
        for col in self._raw_columns:
            got_all = col in self.survey_data.columns and got_all

        if got_all:
            print 'succeeded.'
        else:
            if self.col_mapping:
                print 'failed.'
                self.survey_data.rename(columns=self.col_mapping, inplace=True)
            else:
                print 'failed. '
                print 'Please input column names manually - Modified (current) field names are: '
                print self.survey_data.columns
                for col in self._raw_columns:
                    passed_none = False
                    while col not in self.survey_data.columns and not passed_none:
                        col_name = raw_input('Which column name contains ' + col + ' info? (Press RETURN if none): ')

                    if col_name:
                        self.survey_data.rename(columns={col_name: col}, inplace=True)
                    else:
                        passed_none = True

                for col in ['redshift', 'ra', 'dec', 'mag_r']:
                    if col not in self.survey_data.columns:
                        sys.exit('You need to have specified a column for ' + col)

            if 'id' in self.survey_data.columns:
                print 'Testing for Uniqueness:'
                unique, indices = np.unique(np.array(self.survey_data['id']), return_index=True)
                print 'Deleting ', len(self.survey_data) - len(unique), ' duplicate values'
                self.survey_data = self.survey_data.iloc[indices]
                del unique
                del indices
                del self.survey_data['id']
            restriction = []
            for column in self._raw_columns:
                if column in self.survey_data.columns:
                    restriction = restriction + [column]

        self.survey_data = self.survey_data[restriction]
        if np.max(self.survey_data['ra'] > 2 * np.pi) or np.min(self.survey_data['dec']) < -np.pi / 2 or np.max(self.survey_data['dec']) > -np.pi / 2:
            radians = False
        if not radians:
            self.survey_data['ra'] = self.survey_data['ra'] * np.pi / 180.0
            self.survey_data['dec'] = self.survey_data['dec'] * np.pi / 180.0

    def _create_project_dir(self, filename):
        """
        Creates the directory structure into which all calculations will be placed.
        """
        try:
            os.makedirs(self._project_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        os.chdir(self._project_dir)

    def _write_project_file(self, filename):
        project_file = open('_PyLSSProject_', 'w')
        project_file.close()
        store = pandas.HDFStore(os.path.split(filename)[1].split('.')[0] + '.h5')
        store['survey'] = self.survey_data
        all_cuts = pandas.DataFrame(index=[0, 1])
        for col in self._raw_columns:
            all_cuts[col] = [
             None, None]

        store['all_cuts'] = all_cuts
        cosmo = pandas.DataFrame(index=[0])
        for key, val in self.cosmology.iteritems():
            cosmo[key] = [
             val]

        store['all_cosmo'] = cosmo
        self._create_sample_dir('all')
        store.close()
        return

    def _write_sample_cuts_cosmo(self, filename, sample_name, sample_cuts):
        store = pandas.HDFStore(filename)
        store[sample_name + '_cuts'] = sample_cuts
        cosmo = pandas.DataFrame(index=[0])
        for key, val in self.cosmology.iteritems():
            cosmo[key] = [
             val]

        store[sample_name + '_cosmo'] = cosmo

    def _project_file_import(self, filename, query):
        """
        A simple function to import the project data
        """
        store = pandas.HDFStore(filename)
        if query is not None:
            self.survey_data = store.select('survey', query)
            print 'Using query'
        else:
            self.survey_data = store['survey']
        return

    def _cut_data(self, sample_cuts):
        """
        Cuts the data with the provided sample cuts.. only here because store.select() doesn't work??
        """
        for key, val in sample_cuts.iteritems():
            if val[0] is not None:
                self.survey_data = self.survey_data[(self.survey_data[key] > val[0])]
                if len(self.survey_data) == 0:
                    raise Exception('Cuts left data with no galaxies!')
            if val[1] is not None:
                self.survey_data = self.survey_data[(self.survey_data[key] < val[1])]
                if len(self.survey_data) == 0:
                    raise Exception('Cuts left data with no galaxies!')

        return

    def _define_sample(self, filename):
        """
        A convenience method which will let the user choose a pre-made sample or make one themselves
        """
        store = pandas.HDFStore(filename)
        print os.getcwd()
        print self._project_dir
        sample_names = os.walk(self._project_dir).next()[1]
        if not self.sample_name:
            print 'Current defined samples are: '
            for name in sample_names:
                print name

            sample_name = 'aegnoarg'
            while sample_name not in sample_names + ['']:
                sample_name = raw_input('Choose a defined sample or press <return> to define a new one: ')

        else:
            sample_name = self.sample_name
            print 'The sample name: ', sample_name
        if sample_name in sample_names:
            sample_cuts = store[(sample_name + '_cuts')]
            cosmo = store[(sample_name + '_cosmo')]
            for key in self.cosmology:
                self.cosmology[key] = cosmo[key][0]

        else:
            if not self.sample_cuts:
                sample_cuts = self._specify_sample_cuts()
            else:
                sample_cuts = self._convert_sample_cuts()
            sample_name = str(raw_input('Please choose a name for the sample: '))
        query = self._make_query(sample_cuts)
        return (
         sample_name, sample_cuts, query)

    def _make_query(self, sample_cuts):
        """
        Turns a dataframe of min/max cuts into a SQL query string for importing data
        """
        final_term = []
        for col in sample_cuts.columns:
            if sample_cuts[col][0] != None:
                final_term.append(pandas.Term(col, '>', sample_cuts[col][0]))
            if sample_cuts[col][1] != None:
                final_term.append(pandas.Term(col, '<', sample_cuts[col][1]))

        return final_term

    def _convert_sample_cuts(self):
        """ Converts sample cuts in form of dict to writable form"""
        sample_cuts = pandas.DataFrame(index=['min', 'max'])
        for col in self._raw_columns:
            try:
                sample_cuts[col] = self.sample_cuts[col]
            except:
                sample_cuts[col] = [
                 None, None]

        return sample_cuts

    def _create_sample_dir(self, sample_name):
        """
        Creates a directory for the sample
        """
        sample_dir = os.path.join(self._project_dir, sample_name)
        try:
            os.makedirs(sample_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        os.chdir(sample_dir)
        sample_file = open('_PyLSSSample_', 'w')
        sample_file.close()
        return sample_dir

    def _specify_sample_cuts(self):
        """
        Specifies sample cuts and makes those cuts to current data
        """
        sample_cuts = pandas.DataFrame(index=['min', 'max'])
        for col in self._raw_columns:
            if col != 'id':
                try:
                    min_input = input('What is the minimum ' + col + ' preferred? [' + str(min(self.survey_data[col])) + ',' + str(max(self.survey_data[col])) + ']: ')
                except SyntaxError:
                    min_input = None
                    print ''

                try:
                    max_input = input('What is the maximum ' + col + ' preferred? [' + str(min(self.survey_data[col])) + ',' + str(max(self.survey_data[col])) + ']: ')
                except SyntaxError:
                    max_input = None
                    print ''

                sample_cuts[col] = [min_input, max_input]

        return sample_cuts

    def _define_z_from_dist(self):
        """
        Defines a function that gets redshift from comoving distance
        """
        c_distance, self.c_z = cd.quick_distance_function(cd.comoving_distance, return_inverse=True, **self.cosmology)

    def clean(self):
        """
        Cleans the data according to a set of rules (inbuilt)
        """
        print 'Deleting ', np.sum(self.survey_data['absmag'] > 0), ' entries whose absmag is greater than 0'
        self.survey_data = self.survey_data[(self.survey_data['absmag'] < 0)]
        print 'Deleting ', np.sum(self.survey_data['absmag'] < -30), ' entries whose absmag is less than -30'
        self.survey_data = self.survey_data[(self.survey_data['absmag'] > -30)]

    def write_individual_files(self, prefix='', exclude=[]):
        """
        Write out an ascii file for each column in the survey_data to prefix
        
        e.g. if prefix = "/home/user/" then you'll get the files /home/user/z.dat,
        /home/user/absmag.dat etc.
        
        Not specifying prefix by default writes the files in the current directory
        (which should be the sample directory).
        """
        for col in self.survey_data.columns:
            if col not in exclude:
                self.survey_data[col].to_csv(os.path.join(prefix, col + '.dat'), index=False, header=False)

    def lum_func(self, Np, method='vmax', min_acceptable=1, eps=0.01, max_iter=10, new=True):
        """
        Calculates the luminosity function of galaxies in Np bins.
        
        Can use either the EEP method or the Vmax method currently.
        
        INPUT PARAMETERS
        Np                 -- The number of bins to use
        method ["vmax"]    -- A string indicating which method to use (EEP or vmax)
        min_acceptable [1] -- Minimum acceptable galaxies in a bin
        eps [0.01]         -- for EEP, target convergence
        max_iter [10]      -- for EEP, maximum iterations
        new [True]         -- whether to force re-calculation even if previous results are available
        
        OUTPUT
        M   -- Array of absolute magnitude bin centres
        phi -- Array of luminosity function values
        """
        if not new:
            try:
                lfunc = np.genfromtxt(self._dirs['LuminosityFunction'] + method + '.dat')
                M = lfunc[:, 0]
                phi = lfunc[:, 1]
                return (M, phi)
            except IOError:
                pass

        if method == 'EEP':
            phi, iteration = lf.EEP(absmag=self.survey_data['absmag'], apmag=self.survey_data['mag_r'], Np=Np, min_acceptable=min_acceptable, eps=eps, max_iter=max_iter, verbose=self.verbose)
            phi.plot(logy=True, marker='o')
            plt.show()
            plt.savefig(self._dirs['LuminosityFunction'] + 'allEEP.' + self.plottype)
            M = np.array(phi.index)
            phi = np.array(phi[iteration])
            plt.clf()
            plt.plot(M, phi)
            plt.xlabel('Absolute Magnitude')
            plt.ylabel('Unnormalised Luminosity Function')
            plt.yscale('log')
            plt.savefig(self._dirs['LuminosityFunction'] + 'finalEEP.' + self.plottype)
        elif method == 'vmax':
            phi, M = lf.vmax_method(absmag=self.survey_data['absmag'], appmag=self.survey_data['mag_r'], c_dist=self.survey_data['c_dist'], redshift=self.survey_data['redshift'], bins=Np)
            plt.clf()
            plt.plot(M, phi)
            plt.yscale('log')
            plt.savefig(self._dirs['LuminosityFunction'] + 'vmax.' + self.plottype)
        output = np.vstack((M, phi)).T
        np.savetxt(self._dirs['LuminosityFunction'] + method + '.dat', output)
        return (
         M, phi)

    def power_spec(self, quantity='redshift', bins=None, min_wave=0.0001, max_wave=0.02, n_waves=1000, pad=1, in_wavelength=True, weight=True, slow=True, yscale='linear', xscale='linear'):
        """
        Computes the 1D power spectrum and plots it.
    
        This method uses the numpy fft algorithm to calculate the real to real 
        DFT of any quantity in the GS data, then converts this to a power
        spectrum (merely squares it). As such, it needs what I call 'density 
        values' as its input, which here are merely histogram values. It will 
        only calculate as many DFT points as there are bins in the histogram, 
        which is fine for frequency-based plots, but makes wavelength (inverse 
        frequency) plots very angular. To increase the number of points you can
        pad the original data with zeroes on either end, but even this does not
        ensure a smooth wavelength plot. To get a very nice looking wavelength 
        plot, use PowerSpec_1d_slow().
        
        
        INPUT PARAMETERS:
        quantity    [redshift]    : the quantity type used for the dft. Generally 'redshift', 'c_dist', 'ra' or 'dec'
        bins        [None]        : the number of bins to use in the histogram to get 'densities'. 
                                    If none, an 'optimal' bin number is used.
        min_wave    [0.0001]      : The minimum wavelength to plot.
        max_wave    [0.02]        : The maximum wavelength to plot
        pad         [1]           : How much the original data length is multiplied by (zeroes padded in the extra space).
                                    The higher the padding, the longer the calculation, but the better the resolution.
        wavelength  [True]        : Whether to plot the power against wavelength. If False, plots against frequency.
        weight      [None]        :  An optional setting allowing a further weight to be applied to the bin densities before calculation.
                                    0 - No extra weighting (each bin will be its number)
                                    'weights_1' - Inverse of selection function (simple)
                                    'weights_2' - Inverse of selection function +1 (simple)
        
        OUTPUT PARAMETERS:
        ps                        : array of power spectrum values
        freq                      : array of frequencies
        wvl                       : array of wavelengths
        """
        if quantity is 'c_dist' and max_wave < 2:
            min_wave = 10
            max_wave = 180
        elif quantity is 'ra' and min_wave == 0.0001 and max_wave == 0.02:
            min_wave = 0.01
            max_wave = 2 * np.pi
        elif quantity is 'dec' and min_wave == 0.0001 and max_wave == 0.02:
            min_wave = 0.01
            max_wave = np.pi
        if quantity != 'redshift' and quantity != 'c_dist':
            weight = False
        if weight:
            if 'weight' not in self.survey_data.columns:
                self.do_selection_and_weighting()
            weight = self.survey_data['weight']
        else:
            weight = None
        if not slow:
            power, freq, wavelength = ps.power_spec_1d_fast(quantity=self.survey_data[quantity], bins=bins, min_wave=min_wave, max_wave=max_wave, pad=pad, weight=weight)
        else:
            power, freq, wavelength = ps.power_spec_1d_slow(quantity=self.survey_data[quantity], bins=bins, min_wave=min_wave, max_wave=max_wave, n_waves=n_waves, weight=weight)
        plt.clf()
        plt.title('1D P.S. for ' + quantity + ' of sample ' + self.sample_name.partition('.')[0] + ' from ' + self.survey_name)
        if in_wavelength:
            plt.plot(wavelength[((wavelength < max_wave) & (wavelength > min_wave))], power[((wavelength < max_wave) & (wavelength > min_wave))], 'b-')
            if quantity == 'redshift':
                plt.xlabel('Wavelength, (z)')
            elif quantity == 'c_dist':
                plt.xlabel('Wavelength, Mpc $h^{-1}$s')
        else:
            plt.plot(freq[((wavelength < max_wave) & (wavelength > min_wave))] * 2 * np.pi, power[((wavelength < max_wave) & (wavelength > min_wave))], 'b-')
            plt.xlabel('Frequency (radians)')
        plt.ylabel('Power')
        plt.xscale(xscale)
        plt.yscale(yscale)
        if in_wavelength:
            plt.savefig(self._dirs['PowerSpecs_1D'] + quantity + '_bins' + str(bins) + '_wavelength.eps')
        else:
            plt.savefig(self._dirs['PowerSpecs_1D'] + quantity + '_bins' + str(bins) + '_frequency.eps')
        plt.show()
        return

    def selection_function(self, method='EEP', bins=None, new_lumfunc=False, min_acceptable=1, eps=0.01, max_iter=10, selbins=100):
        """
        Calculate a selection function value for each galaxy.
        
        INPUT PARAMETERS
        method ["EEP"]        -- A method with which to calculate the lumfunc. If None,
                                 will use a simple parametrisation for the N(z) distribution.                    
        bins [None]           -- How many bins to use in the given method
        new_lumfunc [False]   -- Whether to force a new lumfunc calculation even if previous
                                 results exist
        new_selection [False] -- Whether to force a new selection function calcualtion even
                                 if previous results exit.
        min_acceptable        -- Lowest acceptable number of galaxies per bin
        eps                   -- Target uncertainty for convergence in EEP
        max_iter              -- Maximum iterations for EEP
                            
        """
        if method is None:
            A, g, t = sf.fit_selection_simple(self.survey_data['c_dist'], bins=bins, verbose=self.verbose)
            self.survey_data['weight'] = 1.0 / sf.get_sel_from_nd(A, g, t)(self.survey_data['c_dist'])
            if not bins:
                bins = utils.FD_bins(self.survey_data['c_dist'])
            plt.clf()
            plt.title('N(d) with selection function for Sample ' + self.sample_name + ' from ' + self.survey_name)
            hist, edges = np.histogram(self.survey_data['c_dist'], density=True, bins=bins)
            centres = edges[:-1] + (edges[1] - edges[0]) / 2.0
            plt.plot(centres, hist)
            plt.plot(centres, sf.selection_simple(centres, A, g, t))
            plt.xlabel('Comoving Distance')
            plt.ylabel('Normalised Count')
            plt.savefig(self._dirs['SelectionFunction'] + 'N(d)_' + str(bins) + 'bins.eps')
            plt.show()
            self.selection_params = {'A': A, 'g': g, 't': t}
        else:
            M, phi = self.lum_func(Np=bins, method=method, new=new_lumfunc, min_acceptable=min_acceptable, eps=eps, max_iter=max_iter)
            if selbins is None:
                self.survey_data['weight'] = 1.0 / sf.selection_of_galaxies(phi, M, self.survey_data['mag_r'], self.survey_data['absmag'])
                plt.clf()
                plt.plot(self.survey_data['redshift'], 1.0 / self.survey_data['weight'], linestyle='None', marker='.', markersize=1)
                plt.xlabel('Redshift')
                plt.ylabel('Selection Function')
                plt.yscale('log')
                plt.savefig(self._dirs['SelectionFunction'] + 'SelectionFunction_' + method + '_' + str(bins) + '.' + self.plottype)
            else:
                s_of_z = sf.selection_of_z(selbins, phi, M, self.survey_data['mag_r'], self.survey_data['absmag'], self.survey_data['redshift'])
                self.survey_data['weight'] = 1.0 / np.exp(s_of_z(self.survey_data['redshift']))
                z = np.linspace(self.survey_data['redshift'].min(), self.survey_data['redshift'].max(), 1000)
                plt.clf()
                plt.plot(z, np.exp(s_of_z(z)))
                plt.yscale('log')
                plt.xlabel('Redshift')
                plt.ylabel('Selection Function')
                plt.savefig(self._dirs['SelectionFunction'] + 'SelectionFunctionAve_' + method + '_L' + str(bins) + '_S' + str(selbins) + '.' + self.plottype)
        return

    def radial_mock(self, method='EEP', N=None, bins=100, new_lumfunc=False, min_acceptable=1, eps=0.01, max_iter=10, selbins=100):
        """
        Creates a random catalogue of particles based on a defined selection function. Only radial co-ords.
        
        Ouput: radii :: length N vector (default length of survey) of radii        
        """
        z_min = self.survey_data['redshift'].min()
        z_max = self.survey_data['redshift'].max()
        if N is None:
            N = self.N
        if method is None:
            radii = sf.create_radial_selection_simple(z_min, z_max, N)
        else:
            M, phi = self.lum_func(Np=bins, method=method, new=new_lumfunc, min_acceptable=min_acceptable, eps=eps, max_iter=max_iter)
            s_of_z = sf.selection_of_z(selbins, phi, M, self.survey_data['mag_r'], self.survey_data['absmag'], self.survey_data['redshift'])
            radii = sf.create_mock(s_of_z, z_min, z_max, N)
        plt.clf()
        plt.hist(radii, bins=100, normed=True, label='Mock')
        plt.hist(self.survey_data['redshift'], bins=100, normed=True, label='Data')
        plt.legend()
        plt.savefig(self._dirs['SelectionFunction'] + 'N(z)_' + method + '_L' + str(bins) + '_S' + str(selbins) + '.' + self.plottype)
        return radii

    def corr_one_d(self, quantity='redshift', end_s=0.02, ns=15, n_randoms=1, n_cores=1):
        """
        Calculates the correlation function in 1d for the given quantity
        """
        if quantity == 'c_dist' and end_s == 0.02:
            end_s = 120
        if quantity == 'redshift':
            min_cut = self.sample_cuts['redshift'][0]
            max_cut = self.sample_cuts['redshift'][1]
        elif quantity == 'c_dist':
            min_cut = cd.comoving_distance(self.sample_cuts['redshift'][0], **self.cosmology)
            max_cut = cd.comoving_distance(self.sample_cuts['redshift'][1], **self.cosmology)
        else:
            raise ValueError('Quantity not supported: ', quantity)
        s_bins, corr = cf._1d_correlation(self.survey_data[quantity], min_cut, max_cut, end_s, ns, n_randoms, n_cores)
        print s_bins, corr
        plt.clf()
        plt.plot(s_bins, corr)
        plt.title('Correlation Function for $' + quantity + '$ of sample ' + self.sample_name.partition('.')[0] + ' from ' + self.survey_name)
        print 'made title'
        if quantity == 'c_dist':
            plt.xlabel('Separation, Mpc $h^{-1}$s')
        elif quantity == 'redshift':
            plt.xlabel('Separation, [z]')
        print 'plotted'
        plt.ylabel('$\\xi(r)$')
        plt.savefig(self._dirs['CorrelationFunctions'] + 'CorrelationFunction_' + quantity + '_NS' + str(ns) + '_Nrand' + str(n_randoms) + '.eps')
        print 'saved first fig'
        plt.clf()
        plt.plot(s_bins, corr * s_bins ** 2)
        plt.title('Correlation Function by $s^2$ for $' + quantity + '$ of sample ' + self.sample_name.partition('.')[0] + ' from ' + self.survey_name)
        if quantity == 'c_dist':
            plt.xlabel('Separation, Mpc $h^{-1}$s')
        elif quantity == 'redshift':
            plt.xlabel('Separation, [z]')
        plt.ylabel('$r^2\\xi(r)$')
        plt.savefig(self._dirs['CorrelationFunctions'] + 'CorrelationFunction_s2_' + quantity + '_NS' + str(ns) + '_Nrand' + str(n_randoms) + '.eps')
        return (
         s_bins, corr)

    def PlotHist(self, quantity='redshift', bins=None, weight=None):
        """
        Plots a Histogram of the data for any quantity
        """
        if not bins:
            bins = utils.FD_bins(self.survey_data[quantity])
        plt.clf()
        plt.title('Histogram of ' + quantity + ' values for Sample ' + self.sample_name + ' from ' + self.survey_name)
        if not weight:
            plt.hist(self.survey_data[quantity], bins)
        else:
            plt.hist(self.survey_data[quantity], bins, weights=self.survey_data['weight'])
        plt.xlabel(quantity)
        plt.ylabel('Number')
        plt.savefig(self._dirs['SurveyPlots'] + 'Histogram_' + quantity + '_' + str(bins) + 'bins.eps')
        plt.show()

    def PlotPolarDot(self, distance=False):
        """
        Makes a polar plot of the data, TODO: with an optional filter condition
            
        If distance is true, plots against comoving distance rather than redshift.
        """
        plt.clf()
        plt.title('Polar Plot of sample ' + self.sample_name + ' from ' + self.survey_name)
        if not distance:
            plt.polar(self.survey_data['ra'], self.survey_data['redshift'], '.', markersize=1)
            plt.savefig(self._dirs['SurveyPlots'] + 'PolarPlot_Redshift.eps')
        else:
            plt.polar(self.survey_data['ra'], self.survey_data['c_dist'], '.', markersize=1)
            plt.savefig(self._dirs['SurveyPlots'] + 'PolarPlot_Distance.eps')
        plt.show()

    def PlotPolarSmooth(self, bins=None):
        """
        Makes a polar plot of the data smoothed by a filter., TODO: with an optional filter condition
            
        If distance is true, plots against comoving distance rather than redshift.
        """
        x_p = self.survey_data['c_dist'] * np.cos(self.survey_data['ra'])
        y_p = self.survey_data['c_dist'] * np.sin(self.survey_data['ra'])
        if not bins:
            bins = np.ceil(np.sqrt(self.N / 10000))
            if bins < 30:
                bins = 30
        smooth = np.histogram2d(x_p, y_p, (bins, bins))[0]
        plt.clf()
        plt.title('Smoothed Polar Plot of sample ' + self.sample_name + ' from ' + self.survey_name)
        plt.imshow(smooth, interpolation='Gaussian', aspect='equal')
        plt.tick_params(axis='both', labelbottom=False, labelleft=False)
        plt.savefig(self._dirs['SurveyPlots'] + 'PolarPlot_Smooth.eps')
        plt.show()

    def PlotSkyDot(self):
        """
        Makes a 2-D flat sky-plot of the data points.
        """
        plt.clf()
        plt.title('Sky Plot of sample ' + self.sample_name + ' from ' + self.survey_name)
        plt.plot(self.survey_data['ra'], self.survey_data['dec'], '.', markersize=1)
        plt.xlabel('Right Ascension')
        plt.ylabel('Declination')
        plt.savefig(self._dirs['SurveyPlots'] + 'SkyPlot.eps')
        plt.show()

    def PlotSkySmooth(self, bins=None):
        """
        Makes a 2-D flat sky-plot of the data points, smoothed by Gaussian filter.
        """
        plt.clf()
        plt.title('Smoothed Sky Plot of sample ' + self.sample_name + ' from ' + self.survey_name)
        if not bins:
            bins = np.ceil(np.sqrt(self.N / 10000))
            if bins < 30:
                bins = 30
        smooth = np.histogram2d(self.survey_data['ra'], self.survey_data['dec'], (bins, bins))[0]
        plt.clf()
        plt.imshow(smooth, interpolation=None, aspect='equal', extent=(np.min(self.survey_data['ra']),
         np.max(self.survey_data['ra']), np.min(self.survey_data['dec']), np.max(self.survey_data['dec'])))
        plt.tick_params(axis='both')
        plt.savefig(self._dirs['SurveyPlots'] + 'SkyPlot_Smooth.eps')
        plt.show()
        return