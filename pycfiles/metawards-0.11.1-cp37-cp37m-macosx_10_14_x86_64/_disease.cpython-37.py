# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_disease.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 8380 bytes
from dataclasses import dataclass as _dataclass
from typing import List as _List
import pathlib as _pathlib, os as _os
__all__ = [
 'Disease']
_default_disease_path = _os.path.join(_pathlib.Path.home(), 'GitHub', 'MetaWardsData')
_default_folder_name = 'diseases'

@_dataclass
class Disease:
    __doc__ = 'This class holds the parameters about a single disease\n\n       A disease is characterised as a serious of stages, each\n       with their own values of the beta, progress, too_ill_to_move\n       and contrib_foi parameters. To load a disease use\n       the Disease.load function, e.g.\n\n       Examples\n       --------\n       >>> disease = Disease.load("ncov")\n       >>> print(disease)\n       Disease ncov\n       repository: https://github.com/metawards/MetaWardsData\n       repository_branch: master\n       repository_version: 0.2.0\n       beta = [0.0, 0.0, 0.95, 0.95, 0.0]\n       progress = [1.0, 0.1923, 0.909091, 0.909091, 0.0]\n       too_ill_to_move = [0.0, 0.0, 0.0, 0.0, 0.0]\n       contrib_foi = [1.0, 1.0, 1.0, 1.0, 0.0]\n    '
    beta = None
    beta: _List[float]
    progress = None
    progress: _List[float]
    too_ill_to_move = None
    too_ill_to_move: _List[float]
    contrib_foi = None
    contrib_foi: _List[float]
    start_symptom = None
    start_symptom: int
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

    def __str__(self):
        return f"Disease {self._name}\nloaded from {self._filename}\nversion: {self._version}\nauthor(s): {self._authors}\ncontact(s): {self._contacts}\nreferences(s): {self._references}\nrepository: {self._repository}\nrepository_branch: {self._repository_branch}\nrepository_version: {self._repository_version}\n\nbeta = {self.beta}\nprogress = {self.progress}\ntoo_ill_to_move = {self.too_ill_to_move}\ncontrib_foi = {self.contrib_foi}\nstart_symptom = {self.start_symptom}\n\n"

    def __eq__(self, other):
        return self.beta == other.beta and self.progress == other.progress and self.too_ill_to_move == other.too_ill_to_move and self.contrib_foi == other.contrib_foi and self.start_symptom == other.start_symptom

    def __len__(self):
        if self.beta:
            return len(self.beta)
        return 0

    def N_INF_CLASSES(self):
        """Return the number of stages of the disease"""
        return len(self.beta)

    def _validate(self):
        """Check that the loaded parameters make sense"""
        try:
            n = len(self.beta)
            assert len(self.progress) == n
            assert len(self.too_ill_to_move) == n
            assert len(self.contrib_foi) == n
        except Exception as e:
            try:
                raise AssertionError(f"Data read for disease {self._name} is corrupted! {e.__class__}: {e}")
            finally:
                e = None
                del e

        if self.start_symptom is None or self.start_symptom < 0 or self.start_symptom >= n:
            raise AssertionError(f"start_symptom {self.start_symptom} is invalid for a disease with {n} stages")
        self.start_symptom = int(self.start_symptom)
        from utils._safe_eval_float import safe_eval_float
        for i in range(0, n):
            try:
                self.progress[i] = safe_eval_float(self.progress[i])
                self.too_ill_to_move[i] = safe_eval_float(self.too_ill_to_move[i])
                self.beta[i] = safe_eval_float(self.beta[i])
                self.contrib_foi[i] = safe_eval_float(self.contrib_foi[i])
            except Exception as e:
                try:
                    raise AssertionError(f"Invalid disease parameter at index {i}: {e.__class__} {e}")
                finally:
                    e = None
                    del e

    @staticmethod
    def load(disease: str='ncov', repository: str=None, folder: str=_default_folder_name, filename: str=None):
        """Load the disease parameters for the specified disease.
           This will look for a file called f"{disease}.json"
           in the directory f"{repository}/{folder}/{disease}.json"

           By default this will load the ncov (SARS-Cov-2)
           parameters from
           $HOME/GitHub/model_data/diseases/ncov.json

           Alternatively you can provide the full path to the
           json file via the "filename" argument

           Parameters
           ----------
           disease: str
             The name of the disease to load. This is the name that
             will be searched for in the METAWARDSDATA diseases directory
           repository: str
             The location of the cloned METAWARDSDATA repository
           folder: str
             The name of the folder within the METAWARDSDATA repository
             that contains the diseases
           filename: str
             The name of the file to load the disease from - this directly
             loads this file without searching through the METAWARDSDATA
             repository

           Returns
           -------
           disease: Disease
             The constructed and validated disease
        """
        repository_version = None
        repository_branch = None
        if filename is None:
            import os
            if os.path.exists(disease):
                filename = disease
            else:
                if os.path.exists(f"{disease}.json"):
                    filename = f"{disease}.json"
        if filename is None:
            if repository is None:
                repository = _os.getenv('METAWARDSDATA')
                if repository is None:
                    repository = _default_disease_path
            filename = _os.path.join(repository, folder, f"{disease}.json")
            from ._parameters import get_repository_version
            v = get_repository_version(repository)
            repository = v['repository']
            repository_version = v['version']
            repository_branch = v['branch']
        json_file = filename
        try:
            with open(json_file, 'r') as (FILE):
                import json
                data = json.load(FILE)
        except Exception as e:
            try:
                print(f"Could not find the disease file {json_file}")
                print('Either it does not exist of was corrupted.')
                print(f"Error was {e.__class__} {e}")
                print('To download the disease data type the command:')
                print('  git clone https://github.com/metawards/MetaWardsData')
                print('and then re-run this function passing in the full')
                print('path to where you downloaded this directory')
                raise FileNotFoundError(f"Could not find or read {json_file}: {e.__class__} {e}")
            finally:
                e = None
                del e

        disease = Disease(beta=(data.get('beta', [])), progress=(data.get('progress', [])),
          too_ill_to_move=(data.get('too_ill_to_move', [])),
          contrib_foi=(data.get('contrib_foi', [])),
          start_symptom=(data.get('start_symptom', 3)),
          _name=disease,
          _authors=(data.get('author(s)', 'unknown')),
          _contacts=(data.get('contact(s)', 'unknown')),
          _references=(data.get('reference(s)', 'none')),
          _filename=json_file,
          _repository=repository,
          _repository_branch=repository_branch,
          _repository_version=repository_version)
        disease._validate()
        return disease