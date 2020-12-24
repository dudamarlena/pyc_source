# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/io/GetData.py
# Compiled at: 2018-11-05 17:00:12
# Size of source mod 2**32: 4031 bytes
from cmlreaders import CMLReader, get_data_index
from ptsa.data.readers import JsonIndexReader, TalReader
import os
__all__ = [
 'get_subjects',
 'get_sessions',
 'get_ram_experiments',
 'get_sub_tal']

def get_subjects(experiment):
    """Returns an array of all subjects who participated in the experiment

    Parameters
    ----------
    experiment: str, must be 'CatFR1', 'FR1', 'pyFR' or 'ltpFR2'

    Returns
    -------
    All valid subjects
    """
    if experiment.lower() in ('catfr1', 'fr1'):
        dataframe = get_data_index('r1')
    elif experiment.lower() in 'pyfr':
        dataframe = get_data_index('pyfr')
    elif experiment.lower() in ('ltp', 'ltpfr2'):
        dataframe = get_data_index('ltp')
    else:
        try:
            dataframe = get_data_index(experiment)
        except ValueError as e:
            try:
                print(e)
                return
            finally:
                e = None
                del e

    return dataframe[(dataframe['experiment'] == experiment)]['subject'].unique()


def get_sessions(subject, experiment):
    """For a given subject and experiment return an array of all valid sessions

    Parameters
    ----------
    subject: str, must be a valid pyFR or FR1 or catFR1 subject
    experiment: str, must be a valid experiment.
                Currently implemented experiments:
                FR1, catFR1, pyFR

    Returns
    -------

    """
    RAM = [
     'catFR1', 'FR1']
    if experiment in RAM:
        dataframe = get_data_index('r1')
        return dataframe[((dataframe['experiment'] == experiment) & (dataframe['subject'] == subject))]['session'].unique()
    if experiment == 'pyFR':
        dataframe = get_data_index('pyfr')
        return dataframe[((dataframe['experiment'] == experiment) & (dataframe['subject'] == subject))]['session'].unique()


def get_ram_experiments(subject):
    """Given a subject from RAM returns the experiments

    Parameters
    ----------
    subject: str, RAM subject id to get experiments for

    Returns
    -------
    all valid experiments for the subject
    """
    dataframe = get_data_index('r1')
    return dataframe[(dataframe['subject'] == subject)]['experiment'].unique()


def get_sub_tal(subject, experiment, return_channels=False):
    """Returns a subject's talairach using TalReader and JsonIndexReader
    -----
    INPUTS:
    -----
    subject: str, subject ID, e.g. 'R1111M'
    experiment: str, experiment, e.g. 'FR1', 'catFR1'
    return_channels: bool, default = False, whether to return arrays of
                     monopolar and bipolar channels used for EEGReader
    ------
    OUTPUTS if return_channels is False:
    ------
    tal_reader.read(): np.recarray, an array containing relevant values
                       for electrode localization
    ------
    OUTPUTS if return_channels is True:
    ------
    mp: np.recarray, monopolar channels used for EEGReader
    bp: np.recarray, bipolar channels used for EEGReader
    tal_reader.read(): np.recarray, an array containing relevant values
                       for electrode localization
    """
    cwd = os.getcwd()
    local = '' if cwd.split('/')[1][:4] == 'home' else '/Volumes/rhino'
    protocol = local + '/protocols/r1.json'
    jr = JsonIndexReader(protocol)
    pairs_path = jr.get_value('pairs', subject=subject, experiment=experiment)
    tal_reader = TalReader(filename=pairs_path)
    if return_channels:
        mp = tal_reader.get_monopolar_channels()
        bp = tal_reader.get_bipolar_pairs()
        return (
         mp, bp, tal_reader.read())
    return tal_reader.read()


if __name__ == '__main__':
    mp, bp, bp_tal = get_sub_tal(subject='R1207J', experiment='FR1', return_channels=True)