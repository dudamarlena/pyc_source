# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_multinest_catalogue.py
# Compiled at: 2019-07-16 04:25:49
import numpy as np, os, logging, cPickle
from beagle_utils import prepare_data_saving, BeagleDirectories, get_files_list

class MultiNestMode(object):

    def __init__(self, logEvidence, post_mean, max_likelihood, max_a_post):
        self.logEvidence = logEvidence
        self.post_mean = np.array(post_mean)
        self.max_likelihood = max_likelihood
        self.max_a_post = max_a_post


class MultiNestObject(object):

    def __init__(self, ID, logEvidence):
        self.ID = ID
        self.logEvidence = logEvidence
        self.mode = list()

    def add_mode(self, logEvidence, post_mean, max_likelihood, max_a_post):
        newMode = MultiNestMode(logEvidence, post_mean, max_likelihood, max_a_post)
        self.mode.append(newMode)


class MultiNestCatalogue(object):

    def load(self, file_name=None, n_par=None, file_list=None):
        """ 
        Load a 'MultiNest catalogue'.

        Parameters
        ----------
        file_name : str
            Name of the file containing the catalogue.

        Notes
        -----
        You then access the data for each object and each mode as
        self.MNObjects[0].mode[0].post_mean  ---> posterior mean values for
        the different parameters for object 0 and mode 0

        self.MNObjects[2].mode[1].max_likelihood ---> max_likelihood likelihood
        values for the different parameters for object 2 and mode 1
        """
        if file_name is None:
            try:
                tmp = BeagleDirectories.param_file
                file_name = tmp.split('.')[(-2)] + '_MultiNest.cat'
            except:
                pass

        name = file_name
        if os.path.dirname(name) is None:
            name = os.path.join(BeagleDirectories.results_dir, BeagleDirectories.pypbeagle_data, file_name)
        if os.path.isfile(name):
            logging.info('Loading the `MultiNestCatalogue`: ' + name)
            file = open(name, 'rb')
            self.MNObjects = cPickle.load(file)
            file.close()
            return
        else:
            name = prepare_data_saving(file_name)
            if n_par is not None:
                try:
                    self.compute(n_par, file_list=file_list)
                    return
                except:
                    return

            return

    def compute(self, n_par, file_list=None, file_name=None):
        """ 
        Compute a 'MultiNest catalogue'

        Parameters
        ----------
        n_par : int
            Number of free parameters in the BEAGLE run.

        file_list : iterable 
            Contains the list of MultiNest output files '*MNstats.dat'.

        file_name : str
            Name of the output 'MultiNest' catalogue.

        Notes
        -----
        You then access the data for each object and each mode as
        self.MNObjects[0].mode[0].post_mean  ---> posterior mean values for
        the different parameters for object 0 and mode 0

        self.MNObjects[2].mode[1].max_likelihood ---> max_likelihood likelihood
        values for the different parameters for object 2 and mode 1
        """
        if file_name is None:
            try:
                tmp = BeagleDirectories.param_file
                file_name = tmp.split('.')[(-2)] + '_MultiNest.cat'
            except:
                pass

        if file_list is None:
            try:
                file_list, IDs = get_files_list(suffix=BeagleDirectories.MN_suffix)
            except:
                return

        self.MNObjects = list()
        for j, file in enumerate(file_list):
            end = file.find('_BEAGLE')
            objID = os.path.basename(file[:end])
            f = open(os.path.join(BeagleDirectories.results_dir, file), 'r')
            for i, line in enumerate(f):
                if i == 0:
                    logEvidence = float(line.split()[5])
                if i == 5:
                    n_modes = int(line.split()[3])

            f.close()
            n_lines_per_mode = 8 + n_par * 3
            first_line = 10
            post_mean = list()
            max_likelihood = list()
            max_a_post = list()
            mode = list()
            MNObj = MultiNestObject(objID, logEvidence)
            f = open(os.path.join(BeagleDirectories.results_dir, file), 'r')
            for i, line in enumerate(f):
                if i == first_line:
                    logEv = float(line.split()[2])
                elif i >= first_line + 3 and i < first_line + 3 + n_par:
                    post_mean.append(float(line.split()[1]))
                elif i >= first_line + 6 + n_par and i < first_line + 6 + 2 * n_par:
                    max_likelihood.append(float(line.split()[1]))
                elif i >= first_line + 9 + 2 * n_par and i < first_line + 9 + 3 * n_par:
                    max_a_post.append(float(line.split()[1]))
                if i == first_line + n_lines_per_mode:
                    MNObj.add_mode(logEv, post_mean, max_likelihood, max_a_post)
                    post_mean = list()
                    max_likelihood = list()
                    max_a_post = list()
                    first_line += n_lines_per_mode + 5

            f.close()
            self.MNObjects.append(MNObj)

        if file_name is not None:
            name = prepare_data_saving(file_name)
            fOut = open(name, 'w')
            cPickle.dump(self.MNObjects, fOut, cPickle.HIGHEST_PROTOCOL)
            fOut.close()
        return