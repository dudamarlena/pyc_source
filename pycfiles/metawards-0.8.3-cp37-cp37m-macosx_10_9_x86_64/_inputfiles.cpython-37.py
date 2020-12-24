# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/_inputfiles.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 8858 bytes
from dataclasses import dataclass as _dataclass
import os as _os, pathlib as _pathlib
__all__ = [
 'InputFiles']
_inputfiles = {}
_default_model_path = _os.path.join(_pathlib.Path.home(), 'GitHub', 'MetaWardsData')
_default_folder_name = 'model_data'

@_dataclass
class InputFiles:
    __doc__ = 'This class holds all of the input files that must be loaded\n       from METAWARDSDATA to construct the network of wards\n       and links between them\n\n       Load using the InputFiles.load function e.g.\n\n       Examples\n       --------\n       >>> infiles = InputFiles.load("2011Data")\n       >>> print(infiles)\n       Model 2011Data version March 29 2020\n       repository: https://github.com/metawards/MetaWardsData\n       repository_branch: master\n       repository_version: 0.2.0\n       etc.\n    '
    work = None
    work: str
    play = None
    play: str
    identifier = None
    identifier: str
    identifier2 = None
    identifier2: str
    weekend = None
    weekend: str
    play_size = None
    play_size: str
    position = None
    position: str
    seed = None
    seed: str
    nodes_to_track = None
    nodes_to_track: str
    uv = None
    uv: str
    _filename = None
    _filename: str
    _model_name = None
    _model_name: str
    _model_path = None
    _model_path: str
    _model_version = None
    _model_version: str
    _authors = None
    _authors: str
    _contacts = None
    _contacts: str
    _references = None
    _references: str
    _repository = None
    _repository: str
    _repository_version = None
    _repository_version: str
    _repository_branch = None
    _repository_branch: str

    def model_name(self):
        """Return the name of this model"""
        return self._model_name

    def model_path(self):
        """Return the path to the directory containing this model"""
        return self._model_path

    def model_version(self):
        """Return the version of the data in this model"""
        return self._model_version

    def __str__(self):
        return f"Model {self._model_name} version {self._model_version}\nloaded from {self._filename}\nroot directory {self._model_path}\nauthor(s): {self._authors}\ncontact(s): {self._contacts}\nreferences(s): {self._references}\nrepository: {self._repository}\nrepository_branch: {self._repository_branch}\nrepository_version: {self._repository_version}\n\nwork = {self.work}\nplay = {self.play}\nidentifier = {self.identifier}\nidentifier2 = {self.identifier2}\nweekend = {self.weekend}\nplay_size = {self.play_size}\nposition = {self.position}\nseed = {self.seed}\nnodes_to_track = {self.nodes_to_track}\n\n"

    def _localise(self):
        """Localise the filenames in this input files set. This will
           prepend model_path/model to every filename and will also
           double-check that all files exist and are readable
        """
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) if not attr.startswith('_')]
        for member in members:
            filename = getattr(self, member)
            if filename:
                filename = _os.path.join(self._model_path, filename)
                if not (_os.path.exists(filename) and _os.path.isfile(filename)):
                    raise FileNotFoundError(f"Cannot find input file {member} = {filename}")
                setattr(self, member, filename)

    @staticmethod
    def load(model: str='2011Data', repository: str=_default_model_path, folder: str=_default_folder_name, description: str='description.json', filename: str=None):
        """Load the parameters associated with the passed model.
           This will look for the parameters specified in
           the json file called f"{repository}/{folder}/{model}/{description}"

           By default this will load the 2011Data parameters
           from $HOME/GitHub/model_data/2011Data/description.json

           Alternatively you can provide the full path to the
           description json file usng the 'filename' argument.
           All files within this description will be searched
           for using the directory that contains that file
           as a base

           Parameters
           ----------
           model: str
             The name of the model data to load. This is the name that
             will be searched for in the METAWARDSDATA model_data directory
           repository: str
             The location of the cloned METAWARDSDATA repository
           folder: str
             The name of the folder within the METAWARDSDATA repository
             that contains the model data
           filename: str
             The name of the file to load the model data from - this directly
             loads this file without searching through the METAWARDSDATA
             repository

           Returns
           -------
           input_files: InputFiles
             The constructed and validated set of input files
        """
        repository_version = None
        repository_branch = None
        if filename is None:
            if repository is None:
                repository = _os.getenv('METAWARDSDATA')
                if repository is None:
                    repository = _default_model_path
            filename = _os.path.join(repository, folder, model, description)
            from ._parameters import get_repository_version
            v = get_repository_version(repository)
            repository = v['repository']
            repository_version = v['version']
            repository_branch = v['branch']
        json_file = filename
        model_path = _os.path.dirname(filename)
        try:
            with open(json_file, 'r') as (FILE):
                import json
                files = json.load(FILE)
        except Exception as e:
            try:
                print(f"Could not find the model file {json_file}")
                print('Either it does not exist of was corrupted.')
                print(f"Error was {e.__class__} {e}")
                print('To download the model data type the command:')
                print('  git clone https://github.com/metawards/MetaWardsData')
                print('and then re-run this function passing in the full')
                print('path to where you downloaded this directory')
                raise FileNotFoundError(f"Could not find or read {json_file}: {e.__class__} {e}")
            finally:
                e = None
                del e

        model = InputFiles(work=(files['work']), play=(files['play']),
          identifier=(files['identifier']),
          identifier2=(files['identifier2']),
          weekend=(files['weekend']),
          play_size=(files['play_size']),
          position=(files['position']),
          seed=(files['seed']),
          nodes_to_track=(files['nodes_to_track']),
          uv=(files['uv']),
          _filename=json_file,
          _model_path=model_path,
          _model_name=(files['name']),
          _model_version=(files['version']),
          _references=(files['reference(s)']),
          _authors=(files['author(s)']),
          _contacts=(files['contact(s)']),
          _repository=repository,
          _repository_version=repository_version,
          _repository_branch=repository_branch)
        model._localise()
        return model