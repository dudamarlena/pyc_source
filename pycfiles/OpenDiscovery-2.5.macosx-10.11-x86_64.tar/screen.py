# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/OpenDiscovery/screen.py
# Compiled at: 2016-03-23 21:32:35
from . import *
from . import OD_VERSION
import os, sys, glob, json
from Vina import *
from runProcess import runProcess
import matplotlib.pyplot as plt, pandas as pd, numpy as np, math, pkg_resources, argparse
__version__ = OD_VERSION

def run(options=[]):
    directory = os.path.abspath(os.path.expanduser(options['directory']))
    receptor_folder = directory + '/receptors/*.pdbqt'
    for i, receptor in enumerate(glob.glob(receptor_folder)):
        receptor_name, receptor_extension = os.path.splitext(os.path.basename(os.path.normpath(receptor)))
        s = Screen(parse=tryForKeyInDict('parse', options, False), directory=tryForKeyInDict('directory', options, '~'), exhaustiveness=tryForKeyInDict('exhaustiveness', options, 20), verbose=tryForKeyInDict('verbose', options, False), header=True if i == 0 else False, receptor=receptor_name)
        s.run()

    try:
        return s
    except Exception as e:
        log('Are you sure there is a valid PDBQT file for each receptor, with a conf file too?')
        sys.exit()


def tryForKeyInDict(needle, haystack, fallback):
    try:
        return haystack[needle]
    except Exception as e:
        return fallback


def cli():
    parser = argparse.ArgumentParser(description='Open Discovery Screening Protocol')
    parser.add_argument('-d', '--directory', help='Path to the ligand directory. Required!', required=True)
    parser.add_argument('-e', '--exhaustiveness', help='Exhaustiveness. Default = 20.', type=int, default=20)
    parser.add_argument('-v', '--verbose', help='Enable verbose output. Default = False.', action='store_true', default=False)
    parsed = vars(parser.parse_args())
    options = {}
    options['directory'] = parsed['directory']
    options['exhaustiveness'] = parsed['exhaustiveness']
    options['verbose'] = parsed['verbose']
    run(options)


class Screen(object):
    """ A Screening object that can be used to perform docking of ligands to a receptor.

        Instantiates variables variables and runs methods that perform the screening.
    """

    def __init__(self, parse=False, directory='', receptor='', exhaustiveness='20', driver='vina', verbose=False, header=False):
        self.options = {}
        self.options['pretty_header'] = header
        self.ligands = {}
        self.minimised = []
        self.results = {}
        self.total = 0
        self.sorted_results = []
        self.options['directory'] = directory
        self.options['receptor'] = receptor
        self.options['exhaustiveness'] = exhaustiveness
        self.options['driver'] = driver
        self.options['verbose'] = verbose
        self.protocol_dir = os.path.abspath(os.path.split(sys.argv[0])[0])
        self.ligand_dir = os.path.abspath(os.path.expanduser(self.options['directory']))
        self.cmd = runProcess()
        self.cmd.verbose = verbose
        self.__checkStart()
        self.determineTypeOfScreening()
        self.load()
        self.total = self.__scanDirectoryAndUpdateLigandState()
        if self.options['receptor'] not in self.results:
            self.results[self.options['receptor']] = {}
        self.save()

    def run(self):
        self.__header()
        self.convertToPDB()
        self.minimisePDBs()
        self.preparePDBQTs()
        self.performScreening()
        self.extractModels()
        self.gatherResults()
        self.save()
        self.writeCompleteSummary()

    def load(self):
        """ Loads data from a saved od.json into the current instance. """
        if os.path.isfile(self.ligand_dir + '/od.json'):
            try:
                data = json.load(open(self.ligand_dir + '/od.json'))
                self.ligands = data['ligands']
                self.minimised = data['minimised']
                self.results = data['results']
            except:
                pass

    def save(self):
        """ Saves the current state of the Screen class to od.json. """
        data = {'ligands': self.ligands, 'minimised': self.minimised, 
           'results': self.results}
        json.dump(data, open(self.ligand_dir + '/od.json', 'wb'), indent=4)

    def __checkStart(self):
        """ Checks if all is well before continuing the screening.

            Looks for a ligands,receptors and confs folder.
        """
        if (os.path.isdir(self.ligand_dir + '/ligands') or os.path.isdir(self.ligand_dir + '/receptors') or os.path.isdir(self.ligand_dir + '/confs')) is not True:
            log('There is an error in folder setup. Exiting now.', colour='red')
            sys.exit()

    def __scanDirectoryAndUpdateLigandState(self):
        """ Updates ligand state, returning the number of ligands to iterate over"""
        for cmpnd in glob.glob(('{ld}/ligands/*').format(ld=self.ligand_dir)):
            f = os.path.splitext(os.path.basename(cmpnd))
            lig_name = f[0]
            lig_ext = f[1]
            if lig_name not in self.ligands:
                self.ligands[lig_name] = lig_ext
            if lig_ext == '.pdb' and self.ligands[lig_name] != '.pdb':
                self.ligands[lig_name] = lig_ext
            if lig_ext == '.pdbqt' and self.ligands[lig_name] != '.pdbqt':
                self.ligands[lig_name] = lig_ext

        return len(self.ligands)

    def __getConfsForReceptor(self, rec):
        return [ conf for conf in glob.glob(self.ligand_dir + '/confs/' + rec + '*') ]

    def __header(self):
        """ Simply presents a pretty header to the user. """
        if self.options['pretty_header']:
            import platform, datetime
            log('\n\n\n  `-:-.   ,-;"`-:-.   ,-;"`-:-.   ,-;"`-:-.   ,-;"\n     `=`,\'=/     `=`,\'=/     `=`,\'=/     `=`,\'=/\n       y==/        y==/        y==/        y==/\n     ,=,-<=`.    ,=,-<=`.    ,=,-<=`.    ,=,-<=`.\n  ,-\'-\'   `-=_,-\'-\'   `-=_,-\'-\'   `-=_,-\'-\'   `-=_\n\n')
            log(('  OpenDiscovery {v}').format(v=__version__), bold=True, colour='white')
            log(('  Time started: {d}').format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')), colour='black')
            log(('  Platform: {p}').format(p=platform.platform()), colour='black')
            log(('  Ligand Dir: {l}').format(l=self.ligand_dir), colour='black')
            log(('  Exhaustiveness: {e}').format(e=self.options['exhaustiveness']), colour='black')
            log(('  Driver: {d}').format(d=self.options['driver']), colour='black')
        log('')
        log(('  {receptor}').format(receptor=self.options['receptor']), bold=True, colour='yellow')

    def __getFileNameFromPath(self, path):
        return os.path.splitext(os.path.basename(path))[0]

    def __getDirNameFromPath(self, path):
        return os.path.basename(os.path.normpath(path))

    def determineTypeOfScreening(self):
        self.count = {}
        self.count['ligands'], self.count['receptors'], self.count['confs'] = (0, 0,
                                                                               0)
        self.count['ligands'] = self.numberOfLigands()
        self.count['receptors'] = self.numberOfReceptors()
        self.count['confs'] = self.numberOfConfs()
        l, r, c = self.count['ligands'], self.count['receptors'], self.count['confs']
        self.screening_type = []
        if c > 1:
            self.screening_type.append('multi-conf')
        if l > 1:
            self.screening_type.append('multi-ligand')
        if r > 1:
            self.screening_type.append('multi-receptor')
        return self.screening_type

    def convertToPDB(self):
        """ Converts the ligands into a PDB file using obabel, if currently not a PDB. """
        for index, cmpnd in enumerate(self.ligands):
            ProgressBar(index, self.total, 'Converting to PDBs: ', newline=False)
            extension = self.ligands[cmpnd]
            full_name = self.ligand_dir + '/ligands/' + cmpnd + extension
            if not (self.ligands[cmpnd] == '.pdb' or self.ligands[cmpnd] == '.pdbqt'):
                self.cmd.run(('obabel {compound} -O {ld}/ligands/{name}.pdb --gen3d --conformer --systematic -p').format(compound=full_name, ld=self.ligand_dir, name=cmpnd))
                self.ligands[cmpnd] = '.pdb'

        self.save()

    def minimisePDBs(self):
        """ Minimises the ligand PDBs using obabel. """
        for index, cmpnd in enumerate(self.ligands):
            ProgressBar(index, self.total, 'Minimising Ligands: ')
            extension = self.ligands[cmpnd]
            full_name = self.ligand_dir + '/ligands/' + cmpnd + extension
            if cmpnd not in self.minimised and not self.ligands[cmpnd] == '.pdbqt':
                self.cmd.run(('obminimize -sd -c 1e-5 {ld}/ligands/{name}.pdb').format(ld=self.ligand_dir, name=cmpnd))
                self.minimised.append(cmpnd)

        self.save()

    def preparePDBQTs(self):
        """ Converts the minimised ligands to PDBQT for Vina use. """
        for index, cmpnd in enumerate(self.ligands):
            ProgressBar(index, self.total, 'Preparing PDBQTs: ')
            extension = self.ligands[cmpnd]
            full_name = self.ligand_dir + '/ligands/' + cmpnd + extension
            if self.ligands[cmpnd] == '.pdbqt':
                continue
            if self.ligands[cmpnd] == '.pdb':
                pythonsh = pkg_resources.resource_filename('OpenDiscovery', 'lib/pythonsh')
                prepareligand4 = pkg_resources.resource_filename('OpenDiscovery', 'lib/prepare_ligand4.py')
                os.chdir(os.path.abspath(self.ligand_dir + '/ligands'))
                self.cmd.run(('{psh} {pl4} -l {ld}/ligands/{name}.pdb').format(psh=pythonsh, pl4=prepareligand4, ld=self.ligand_dir, name=cmpnd))
                os.chdir(os.path.abspath(self.ligand_dir))
                self.ligands[cmpnd] = '.pdbqt'

        self.save()

    def performScreening(self):
        """ Use the docking driver to perform the actual docking. """
        confsArray = glob.glob(self.ligand_dir + '/confs/' + self.options['receptor'] + '*.txt')
        ligandsArray = glob.glob(self.ligand_dir + '/ligands/*.pdbqt')
        total_screenings = len(confsArray) * len(ligandsArray)
        screened = 0
        for conf in confsArray:
            conf_name = self.__getFileNameFromPath(conf)
            for ligand in self.ligands:
                ProgressBar(screened, total_screenings, 'Perform Screening: ')
                screened += 1
                if self.options['driver'].lower() == 'vina':
                    Vina(screen=self, ligand=ligand, conf=conf_name).run()
                else:
                    sys.exit()

    def extractModels(self):
        """ Extracts separate models from a multi-model PDB/PDBQT file. Uses an awk script. """
        lf = []
        self.confs = []
        for conf in glob.glob(self.ligand_dir + '/confs/' + self.options['receptor'] + '*'):
            self.confs.append(self.__getFileNameFromPath(conf))

        for screened in glob.glob(self.ligand_dir + '/results-' + self.options['receptor'] + '/*/*.pdbqt'):
            lf.append(screened)

        for index, l in enumerate(lf):
            os.chdir(os.path.abspath(os.path.join(l, os.pardir)))
            lig_name = self.__getFileNameFromPath(l)
            ProgressBar(index, self.numberOfConfs(), 'Extracting Models: ')
            awk_location = pkg_resources.resource_filename('OpenDiscovery', 'lib/extract.awk')
            self.cmd.run(('awk -f {awk} < {results}').format(awk=awk_location, results=lig_name + '.pdbqt'))
            makeFolder(lig_name)
            for mode in glob.glob('mode_*.pdb'):
                os.rename(mode, ('{0}/{0}_{1}').format(lig_name, mode))

            try:
                os.rename(lig_name + '.txt', lig_name + '/' + lig_name + '.txt')
                os.rename(lig_name + '.pdbqt', lig_name + '/' + lig_name + '.pdbqt')
            except:
                pass

    def gatherResults(self):
        """ Extracts the energy information from vina logs, and adds it to a sorted csv. """
        self.results[self.options['receptor']] = {}
        confsArray = glob.glob(self.ligand_dir + '/confs/' + self.options['receptor'] + '*.txt')
        ligandsArray = glob.glob(self.ligand_dir + '/ligands/*.pdbqt')
        total_screenings = len(confsArray) * len(ligandsArray)
        results_folder = []
        for conf_file in glob.glob(self.ligand_dir + '/confs/' + self.options['receptor'] + '*'):
            short = os.path.splitext(os.path.basename(conf_file))[0]
            results = self.ligand_dir + '/results-' + self.options['receptor'] + '/' + short
            results_folder.append(results)
            self.results[self.options['receptor']][short] = {}

        current = 0
        for rf in results_folder:
            short = os.path.splitext(os.path.basename(rf))[0]
            open(rf + '/summary.csv', 'w').close()
            for index, result in enumerate(glob.glob(rf + '/*/')):
                lig_name = os.path.basename(os.path.normpath(result))
                conf_file = os.path.basename(os.path.abspath(os.path.join(result, os.pardir)))
                with open(('{0}/{1}.txt').format(result, lig_name)) as (file):
                    for line in file:
                        if line.find('0.000') != -1:
                            energy = line.split()[1]
                            with open(rf + '/summary.csv', 'a') as (summary):
                                summary.write(('{0},{1}\n').format(lig_name, float(energy)))

                ProgressBar(current, total_screenings, 'Gathering Results: ')
                current = current + 1
                self.results[self.options['receptor']][conf_file][lig_name] = energy

        log('')

    def writeCompleteSummary(self):
        receptors = []
        results = []
        ligands = []
        res = []
        for r in self.results:
            receptors.append(r)
            results.append(self.results[r])

        self.receptor_array = receptors
        printHeader('Analysing Results.')
        self.receptor_results = {}
        for receptor in receptors:
            confs, short_confs = [], []
            df = []
            print receptor
            for conf in glob.glob(self.ligand_dir + '/results-' + receptor + '/*/'):
                confs.append(conf + '/summary.csv')
                short_confs.append(self.__getDirNameFromPath(conf))
                df.append(pd.read_csv(conf + '/summary.csv', names=[
                 'ligand', self.__getDirNameFromPath(conf)], index_col=0))

            self.receptor_results[receptor] = pd.concat(df, axis=1)
            self.receptor_results[receptor].to_csv(self.ligand_dir + '/results-' + receptor + '/receptor-summary.csv')

        return self.receptor_results

    def plot(self, show=True, save=False):
        number_of_subplots = self.numberOfReceptors()
        nrows = int(math.ceil(number_of_subplots / 2.0))
        fig, axs = plt.subplots(2, nrows)
        for ax, receptor in zip(axs.flat, self.receptor_array):
            data = self.receptor_results[receptor]
            heatmap = ax.pcolor(data.T, cmap=plt.cm.autumn)
            ax.set_title(receptor)
            ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
            ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
            ax.set_yticklabels(data.columns.values.tolist(), minor=False)
            ax.set_xticklabels(data.index, minor=False)
            ax.invert_yaxis()

        plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        plt.colorbar(heatmap, cax=cbar_ax)
        if save:
            plt.savefig(self.ligand_dir + '/heatmap.pdf')
        if show:
            plt.show()

    def numberOfLigands(self):
        """ Utility function to return the number of ligands to convert. """
        self.count['ligands'] = 0
        for receptor in glob.glob(('{ld}/ligands/*.pdbqt').format(ld=self.ligand_dir)):
            self.count['ligands'] += 1

        return int(self.count['ligands'])

    def numberOfReceptors(self):
        """ Utility function to return the number of receptors. """
        self.count['receptors'] = 0
        for receptor in glob.glob(('{ld}/receptors/*.pdbqt').format(ld=self.ligand_dir)):
            self.count['receptors'] += 1

        return self.count['receptors']

    def numberOfConfs(self):
        """ Utility function to return the number of conf files. """
        self.count['confs'] = 0
        for receptor in glob.glob(('{ld}/confs/*.txt').format(ld=self.ligand_dir)):
            self.count['confs'] += 1

        return self.count['confs']


class ScreenTests(object):
    """ A class intended for testing. """

    def __init__(self, args):
        self.passed = args

    def checkSetup(self):
        return self.passed