# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_parameters.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 15975 bytes
from dataclasses import dataclass as _dataclass
from typing import List as _List, Dict as _Dict
from copy import deepcopy as _deepcopy
import pathlib as _pathlib, os as _os, json as _json
from ._inputfiles import InputFiles
from ._disease import Disease
from ._variableset import VariableSets, VariableSet
__all__ = [
 'Parameters', 'get_repository_version']
_default_parameters_path = _os.path.join(_pathlib.Path.home(), 'GitHub', 'MetaWardsData')
_default_folder_name = 'parameters'
_repositories = {}

def generate_repository_version(repository):
    """Try to run the './version' script within the passed repository,
       to generate the required 'version.txt' file
    """
    import subprocess
    script = _os.path.join(repository, 'version')
    print(f"Regenerating version information using {script}")
    subprocess.run(script, cwd=repository)


def get_repository_version(repository: str):
    """Read and return the Git version of the passed repository

       Parameters
       ----------
       repository: str
         The full path to the repository whose version should be obtained

       Returns
       -------
       version_data: dict
         A dictionary containing version information for the repository
    """
    global _repositories
    if repository in _repositories:
        return _repositories[repository]
    filename = _os.path.join(repository, 'version.txt')
    try:
        with open(filename) as (FILE):
            version = _json.load(FILE)
            _repositories[repository] = version
            return version
    except Exception:
        pass

    try:
        generate_repository_version(repository)
        with open(filename) as (FILE):
            version = _json.load(FILE)
            _repositories[repository] = version
            return version
    except Exception:
        print(f"Could not find the repository version info in {filename}.Please make sure that you have run './version' in that repository to generate the version info.")
        _repositories[repository] = {'repository':'unknown', 
         'version':'unknown', 
         'branch':'unknown'}
        return _repositories[repository]


@_dataclass
class Parameters:
    __doc__ = 'The full set of Parameters that are used to control the model\n       outbreak over a Network. The combination of a Network and\n       a Parameters defines the model outbreak.\n\n       Load the Parameters using the Parameters.load function, and\n       then add extra data using the various "set" and "add" functions,\n       e.g.\n\n       Examples\n       --------\n       >>> params = Parameters.load("march29")\n       >>> params.set_disease("ncov")\n       >>> params.set_input_files("2011Data")\n       >>> params.add_seeds("ExtraSeedsBrighton.dat")\n    '
    input_files = None
    input_files: InputFiles
    uv_filename = None
    uv_filename: str
    disease_params = None
    disease_params: Disease
    additional_seeds = None
    additional_seeds: _List[str]
    length_day = 0.7
    length_day: float
    plength_day = 0.5
    plength_day: float
    initial_inf = 5
    initial_inf: int
    static_play_at_home = 0.0
    static_play_at_home: float
    dyn_play_at_home = 0.0
    dyn_play_at_home: float
    data_dist_cutoff = 10000000.0
    data_dist_cutoff: float
    dyn_dist_cutoff = 10000000.0
    dyn_dist_cutoff: float
    play_to_work = 0.0
    play_to_work: float
    work_to_play = 0.0
    work_to_play: float
    local_vaccination_thresh = 4
    local_vaccination_thresh: int
    global_detection_thresh = 4
    global_detection_thresh: int
    daily_ward_vaccination_capacity = 5
    daily_ward_vaccination_capacity: int
    neighbour_weight_threshold = 0.0
    neighbour_weight_threshold: float
    daily_imports = 0.0
    daily_imports: float
    UV = 0.0
    UV: float
    user_params = None
    user_params: _Dict[(str, float)]
    _name = None
    _name: str
    _version = None
    _version: str
    _authors = None
    _authors: str
    _contacts = None
    _contacts: str
    _references = None
    _references: str
    _filename = None
    _filename: str
    _repository = None
    _repository: str
    _repository_version = None
    _repository_version: str
    _repository_branch = None
    _repository_branch: str
    _repository_dir = None
    _repository_dir: str

    def __str__(self):
        return f"Parameters {self._name}\nloaded from {self._filename}\nversion: {self._version}\nauthor(s): {self._authors}\ncontact(s): {self._contacts}\nreferences(s): {self._references}\nrepository: {self._repository}\nrepository_branch: {self._repository_branch}\nrepository_version: {self._repository_version}\n\nlength_day = {self.length_day}\nplength_day = {self.plength_day}\ninitial_inf = {self.initial_inf}\nstatic_play_at_home = {self.static_play_at_home}\ndyn_play_at_home = {self.dyn_play_at_home}\ndata_dist_cutoff = {self.data_dist_cutoff}\ndyn_dist_cutoff = {self.dyn_dist_cutoff}\nplay_to_work = {self.play_to_work}\nwork_to_play = {self.work_to_play}\nlocal_vaccination_thresh = {self.local_vaccination_thresh}\nglobal_detection_thresh = {self.global_detection_thresh}\ndaily_ward_vaccination_capacity = {self.daily_ward_vaccination_capacity}\nneighbour_weight_threshold = {self.neighbour_weight_threshold}\ndaily_imports = {self.daily_imports}\nUV = {self.UV}\nadditional_seeds = {self.additional_seeds}\n\n"

    @staticmethod
    def get_repository(repository: str=None):
        """Return the repository location and version information
           for the passed repository

           Parameters
           ----------
           repository: str
             Location on the filesystem of the repository. If this
             is None then it will be searched for using first
             the environment variable METAWARDSDATA, then
             $HOME/GitHub/MetaWardsData, then ./METAWARDSDATA

           Returns
           -------
           (repository, version): tuple
             A tuple of the location on disk of the repository,
             plus the version information (git ID etc)
        """
        if repository is None:
            repository = _os.getenv('METAWARDSDATA')
            if repository is None:
                repository = _default_parameters_path
        else:
            from pathlib import Path
            import os
            repository = os.path.expanduser(os.path.expandvars(repository))
            repository = Path(repository).absolute().resolve()
            if not os.path.exists(repository):
                raise FileNotFoundError(f"Cannot find the MetaWardsData repository at {repository}")
            assert os.path.isdir(repository), f"Expected {repository} to be a directory containing the MetaWardsData repository. It isn't?"
        v = get_repository_version(repository)
        return (repository, v)

    @staticmethod
    def load(parameters: str='march29', repository: str=None, folder: str=_default_folder_name, filename: str=None):
        """This will return a Parameters object containing all of the
           parameters loaded from the parameters found in file
           f"{repository}/{folder}/{parameters}.json"

           By default this will load the march29 parameters from
           $HOME/GitHub/model_data/2011Data/parameters/march29.json

           Alternatively, you can provide the exact path to the
           filename via the 'filename' argument

           Parameters
           ----------
           parameters: str
             The name of the parameters to load. This is the name that
             will be searched for in the METAWARDSDATA parameters directory
           repository: str
             The location of the cloned METAWARDSDATA repository
           folder: str
             The name of the folder within the METAWARDSDATA repository
             that contains the parameters
           filename: str
             The name of the file to load the parameters from - this directly
             loads this file without searching through the METAWARDSDATA
             repository

           Returns
           -------
           params: Parameters
             The constructed and validated parameters
        """
        repository_version = None
        repository_branch = None
        repository_dir = None
        if filename is None:
            repository, v = Parameters.get_repository(repository)
            filename = _os.path.join(repository, folder, f"{parameters}.json")
            repository_dir = repository
            repository = v['repository']
            repository_branch = v['branch']
            repository_version = v['version']
        json_file = filename
        try:
            with open(json_file, 'r') as (FILE):
                import json
                data = json.load(FILE)
        except Exception as e:
            try:
                print(f"Could not find the parameters file {json_file}")
                print('Either it does not exist of was corrupted.')
                print(f"Error was {e.__class__} {e}")
                print('To download the parameters type the command:')
                print('  git clone https://github.com/metawards/MetaWardsData')
                print('and then re-run this function passing in the full')
                print('path to where you downloaded this directory')
                raise FileNotFoundError(f"Could not find or read {json_file}: {e.__class__} {e}")
            finally:
                e = None
                del e

        par = Parameters(length_day=(data.get('length_day', 0.7)),
          plength_day=(data.get('plength_day', 0.5)),
          initial_inf=(data.get('initial_inf', 0)),
          static_play_at_home=(data.get('static_play_at_home', 0.0)),
          dyn_play_at_home=(data.get('dyn_play_at_home', 0.0)),
          data_dist_cutoff=(data.get('data_dist_cutoff', 10000000.0)),
          dyn_dist_cutoff=(data.get('dyn_dist_cutoff', 10000000.0)),
          play_to_work=(data.get('play_to_work', 0.0)),
          work_to_play=(data.get('work_to_play', 0.0)),
          local_vaccination_thresh=(data.get('local_vaccination_threshold', 4)),
          global_detection_thresh=(data.get('global_detection_threshold', 4)),
          daily_ward_vaccination_capacity=(data.get('daily_ward_vaccination_capacity', 5)),
          neighbour_weight_threshold=(data.get('neighbour_weight_threshold', 0.0)),
          daily_imports=(data.get('daily_imports', 0)),
          UV=(data.get('UV', 0.0)),
          _name=(data.get('name', parameters)),
          _authors=(data.get('author(s)', 'unknown')),
          _version=(data.get('version', 'unknown')),
          _contacts=(data.get('contact(s)', 'unknown')),
          _references=(data.get('reference(s)', 'none')),
          _filename=json_file,
          _repository=repository,
          _repository_dir=repository_dir,
          _repository_branch=repository_branch,
          _repository_version=repository_version)
        print('Using parameters:')
        print(par)
        return par

    def add_seeds(self, filename: str):
        """Add an 'additional seeds' file that can be used to
           seed wards with new infections at different times and
           locations. Several additional_seed files can be added

           Parameters
           ----------
           filename: str
             Name of the file containing the additional seeds
        """
        if self.additional_seeds is None:
            self.additional_seeds = []
        elif not _os.path.exists(filename):
            f = _os.path.join(self._repository_dir, 'extra_seeds', filename)
            if _os.path.exists(f):
                filename = f
            else:
                raise FileExistsError(f"Unable to find extra seeds file {filename} in the current directory or in {f}")
        self.additional_seeds.append(filename)

    def set_input_files(self, input_files: InputFiles):
        """Set the input files that are used to initialise the
           simulation

           Parameters
           ----------
           input_files: InputFiles
             The set of input files that will be used to load the Network.
             If a string is passed then the InputFiles will be loaded
             based on that string.
        """
        if isinstance(input_files, str):
            input_files = InputFiles.load(input_files, repository=(self._repository_dir))
        print('Using input files:')
        print(input_files)
        self.input_files = _deepcopy(input_files)

    def set_disease(self, disease: Disease):
        """"Set the disease that will be modelled

            Parameters:
              disease: The disease to be modelled. If a string is passed
              then the disease will be loaded using that string
        """
        if isinstance(disease, str):
            disease = Disease.load(disease, repository=(self._repository_dir))
        print('Using disease')
        print(disease)
        self.disease_params = _deepcopy(disease)

    def set_variables(self, variables: VariableSet):
        """This function sets the adjustable variable values to those
           specified in 'variables' in A COPY OF THIS PARAMETERS OBJECT.
           This returns the copy. It does not change this object

           Parameters
           ----------
           variables: VariableSet
             The variables that will be adjusted before the model run.
             This adjusts the parameters and returns them in a deep copy

           Returns
           -------
           params: Parameters
             A copy of this set of parameters with the variables adjusted
        """
        params = _deepcopy(self)
        if isinstance(variables, dict):
            variables = VariableSet(variables)
        variables.adjust(params)
        return params

    @staticmethod
    def read_variables(filename: str, line_numbers: _List[int]):
        """Read in extra variable parameters from the specified line number(s)
           of the specified file, returning the list
           of the dictionaries of variables that have been
           read. You can then apply those variable parameters
           using the 'set_variables' function

           Parameters
           ----------
           filename: str
             The file from which to read the adjustable variables
           line_numbers: List[int]
             All of the line numbers from which to read. If this is
             None then all lines will be read.

           Returns
           -------
           variables: VariableSets
             The VariableSets containing all of the adjustable variables
        """
        return VariableSets.read(filename, line_numbers)