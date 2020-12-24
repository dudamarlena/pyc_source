# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_demographics.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 10789 bytes
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from typing import List as _List
from typing import Dict as _Dict
import os as _os, pathlib as _pathlib
from ._demographic import Demographic
from ._network import Network
__all__ = [
 'Demographics']
_default_demographics_path = _os.path.join(_pathlib.Path.home(), 'GitHub', 'MetaWardsData')
_default_folder_name = 'demographics'

def _get_value(value):
    """Extract a numeric value from the passed value - this is used
       to allow the demographics.json file to store numbers is
       a variety of formats
    """
    from metawards.utils import safe_eval_float
    if value is None:
        return 0.0
    if isinstance(value, list):
        lst = []
        for v in value:
            lst.append(safe_eval_float(v))

        return lst
    if isinstance(value, dict):
        d = []
        for k, v in value.items():
            d[k] = safe_eval_float(v)

        return d
    return safe_eval_float(value)


@_dataclass(eq=False)
class Demographics:
    __doc__ = 'This class holds metadata about all of the demographics\n       being modelled\n    '
    demographics = _field(default_factory=list)
    demographics: _List[Demographic]
    interaction_matrix = None
    interaction_matrix: _List[_List[int]]
    _names = _field(default_factory=dict)
    _names: _Dict[(str, int)]
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
        d = '\n  '.join([str(x) for x in self.demographics])
        return f"Demographics {self._name}\nloaded from {self._filename}\nversion: {self._version}\nauthor(s): {self._authors}\ncontact(s): {self._contacts}\nreferences(s): {self._references}\nrepository: {self._repository}\nrepository_branch: {self._repository_branch}\nrepository_version: {self._repository_version}\ndemographics = [\n  {d}\n]"

    def __len__(self):
        return len(self.demographics)

    def __eq__(self, other):
        if not isinstance(other, Demographics):
            return False
        if len(self) != len(other):
            return False
        for name, index in self._names.items():
            if other._names.get(name, None) != index:
                return False
                if self.demographics[index] != other.demographics[index]:
                    return False

        return True

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.demographics[self._names[item]]
        return self.demographics[item]

    def copy(self):
        """Return a copy of this demographics object that should
           allow a safe reset between runs. This deepcopies things
           that may change, while shallow copying things that won't
        """
        from copy import copy, deepcopy
        demographics = copy(self)
        demographics.interaction_matrix = deepcopy(self.interaction_matrix)
        demographics.demographics = copy(self.demographics)
        return demographics

    def add(self, demographic: Demographic):
        """Add a demographic to the set to be modelled"""
        if demographic.name is None:
            raise ValueError('You can only add named demographics to the set.')
        if demographic.name in self._names:
            raise ValueError(f"There is already a demographic called {demographic.name} in this set. Please rename and try again.")
        self.demographics.append(demographic)
        self._names[demographic.name] = len(self.demographics) - 1

    def get_name(self, item):
        """Return the name of the demographic at 'item'"""
        return self.demographics[self.get_index(item)].name

    def get_index(self, item):
        """Return the index of the passed item"""
        try:
            item = int(item)
        except Exception:
            pass

        if isinstance(item, str):
            try:
                return self._names[item]
            except Exception:
                pass

        else:
            if isinstance(item, int):
                try:
                    if self.demographics[item] is not None:
                        return item
                except Exception:
                    pass

            else:
                if isinstance(item, Demographic):
                    for i, d in enumerate(self.demographics):
                        if item == d:
                            return i

        raise KeyError(f"There is no demographic is this set that matches {item}.")

    @staticmethod
    def load(name: str=None, repository: str=None, folder: str=_default_folder_name, filename: str=None):
        """Load the parameters for the specified set of demographics.
           This will look for a file called f"{name}.json"
           in the directory f"{repository}/{folder}/{name}.json"

           By default this will load nothing.

           Alternatively you can provide the full path to the
           json file via the "filename" argument

           Parameters
           ----------
           name: str
             The name of the demographics to load. This is the name that
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
           demographics: Demographics
             The constructed and validated demographics
        """
        repository_version = None
        repository_branch = None
        if filename is None:
            import os
            if os.path.exists(name):
                filename = name
            else:
                if os.path.exists(f"{name}.json"):
                    filename = f"{name}.json"
        import os
        if filename is None:
            if repository is None:
                repository = os.getenv('METAWARDSDATA')
                if repository is None:
                    repository = _default_demographics_path
            filename = os.path.join(repository, folder, f"{name}.json")
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
                print(f"Could not find the demographics file {json_file}")
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

        demographics = data.get('demographics', [])
        work_ratios = data.get('work_ratios', [])
        play_ratios = data.get('play_ratios', [])
        if len(demographics) != len(work_ratios) or len(demographics) != len(play_ratios):
            raise ValueError(f"The number of work_ratios ({len(work_ratios)}) must equal to number of play_ratios ({len(play_ratios)}) which must equal the number of demographics ({len(demographics)})")
        demos = Demographics(_name=name, _authors=(data.get('author(s)', 'unknown')),
          _contacts=(data.get('contact(s)', 'unknown')),
          _references=(data.get('reference(s)', 'none')),
          _filename=json_file,
          _repository=repository,
          _repository_branch=repository_branch,
          _repository_version=repository_version)
        for i in range(0, len(demographics)):
            demographic = Demographic(name=(demographics[i]), work_ratio=(_get_value(work_ratios[i])),
              play_ratio=(_get_value(play_ratios[i])))
            demos.add(demographic)

        return demos

    def specialise(self, network: Network, profiler=None, nthreads: int=1):
        """Build the set of networks that will model this set
           of demographics applied to the passed Network.

           Parameters
           ----------
           network: Network
             The overall population model - this contains the base
             parameters, wards, work and play links that define
             the model outbreak
           profiler: Profiler
             Profiler used to profile the specialisation
           nthreads: int
             Number of threads over which to parallelise the work

           Returns
           -------
           networks: Networks
             The set of Networks that represent the model run over the
             full set of different demographics
        """
        if len(self) == 0:
            return network
        from ._networks import Networks
        return Networks.build(network=network, demographics=self, profiler=profiler,
          nthreads=nthreads)