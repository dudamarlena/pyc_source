# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/luigine/abc.py
# Compiled at: 2019-08-27 02:38:05
# Size of source mod 2**32: 10014 bytes
__author__ = 'Hiroshi Kajino, Takeshi Teshima'
__copyright__ = '(c) Copyright IBM Corp. 2019'
__version__ = '1.0'
from abc import abstractmethod
from copy import deepcopy
from collections import OrderedDict
from datetime import datetime
import errno, gzip, hashlib, logging, luigi, numpy as np, optuna, os, pickle, pprint
from .utils import sort_dict, dict_to_str
logger = logging.getLogger('luigi-interface')

@luigi.Task.event_handler(luigi.Event.FAILURE)
@luigi.Task.event_handler(luigi.Event.BROKEN_TASK)
def curse_failure(*kwargs):
    if os.path.exists('engine_status.progress'):
        os.rename('engine_status.progress', 'engine_status.error')
    with open('engine_status.error', 'a') as (f):
        f.write('error: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    with open(os.path.join('ENGLOG', 'engine.log'), 'a') as (f):
        f.write('{}'.format(kwargs))
    raise RuntimeError('error occurs and halt.')


def main():
    if not os.path.exists(os.path.join('INPUT', 'luigi.cfg')):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join('INPUT', 'luigi.cfg'))
    elif not os.path.exists(os.path.join('INPUT', 'logging.conf')):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join('INPUT', 'luigi.cfg'))
    else:
        if not os.path.exists(os.path.join('ENGLOG')):
            os.mkdir(os.path.join('ENGLOG'))
        if not os.path.exists(os.path.join('OUTPUT')):
            os.mkdir(os.path.join('OUTPUT'))
        os.rename('engine_status.ready', 'engine_status.progress')
        with open('engine_status.progress', 'a') as (f):
            f.write('progress: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        try:
            is_success = luigi.run(local_scheduler=True)
            if not is_success:
                raise RuntimeError('task fails')
            if os.path.exists('engine_status.progress'):
                os.rename('engine_status.progress', 'engine_status.complete')
        except:
            import traceback
            if os.path.exists('engine_status.progress'):
                os.rename('engine_status.progress', 'engine_status.error')
            with open('engine_status.error', 'a') as (f):
                f.write('error: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
            with open(os.path.join('ENGLOG', 'engine.log'), 'a') as (f):
                f.write(traceback.format_exc())


class MainTask(luigi.Task):
    __doc__ = '\n    A main task should inherit this class.\n    '
    working_dir = luigi.Parameter()

    def load_output(self):
        """Interface to load and return the output object."""
        pass


class MainWrapperTask(luigi.WrapperTask):
    __doc__ = '\n    A main wrapper task should inherit this class.\n    '
    working_dir = luigi.Parameter()

    def load_output(self):
        """Interface to load and return the output object."""
        pass


class AutoNamingTask(luigi.Task):
    __doc__ = '\n    This task defines the output name automatically from task parameters.\n\n    Attributes\n    ----------\n    hash_num : int\n        the number of characters used for hashing\n    working_subdir : str\n        the name of directory where the output of this task is stored\n    output_ext : str\n        extension of the output file\n    '
    __no_hash_keys__ = []
    hash_num = luigi.IntParameter(default=10)
    working_subdir = luigi.Parameter()
    output_ext = luigi.Parameter(default='pklz')

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        self.param_name = ''
        param_kwargs = deepcopy(self.__dict__['param_kwargs'])
        if 'working_subdir' in param_kwargs:
            param_kwargs.pop('working_subdir')
        for each_key in self.__no_hash_keys__:
            if len(each_key) == 2:
                self.param_name = self.param_name + str(param_kwargs[each_key[0]][each_key[1]]) + '_'
                param_kwargs[each_key[0]] = dict(param_kwargs[each_key[0]])
                param_kwargs[each_key[0]].pop(each_key[1])
            else:
                self.param_name = self.param_name + str(param_kwargs[each_key]) + '_'
                param_kwargs.pop(each_key)

        for each_key in sorted(param_kwargs.keys()):
            if isinstance(param_kwargs[each_key], (dict, OrderedDict, luigi.parameter._FrozenOrderedDict)):
                self.param_name = self.param_name + hashlib.md5(dict_to_str(sort_dict(param_kwargs[each_key])).encode('utf-8')).hexdigest()[:self.hash_num] + '_'
            else:
                self.param_name = self.param_name + hashlib.md5(str(param_kwargs[each_key]).encode('utf-8')).hexdigest()[:self.hash_num] + '_'

        self.param_name = self.param_name[:-1]

    def output(self):
        if not os.path.exists('OUTPUT'):
            os.mkdir('OUTPUT')
        if not os.path.exists(os.path.join('OUTPUT', self.working_subdir)):
            os.mkdir(os.path.join('OUTPUT', self.working_subdir))
        return luigi.LocalTarget(os.path.join('OUTPUT', self.working_subdir, '{}.{}'.format(self.param_name, self.output_ext)))

    def load_output(self):
        with gzip.open(self.output().path, 'rb') as (f):
            res = pickle.load(f)
        return res


class OptunaTask(AutoNamingTask):
    __doc__ = " Parameter optimization task using Optuna.\n    Given a task that receives parameters and outputs a loss to be minimized,\n    this task can find better parameters that will achieve lower loss.\n\n    Attributes\n    ----------\n    OptunaTask_params : DictParameters\n        Dictionary of Dictionaries, where each dictionary corresponds to each task's `DictParameter`\n        A key starting from `@` will get suggestion from optuna.\n        For example, if the user would like to choose better regularization parameter `C` from [0, 1], instead of specifying {'C': 1.0}, specify it as {'@C': ['uniform', [0, 1]]}.\n        The first element of the value is used to choose `suggest_{}` method, and the second element (list) is used as args for the suggestion method.\n    n_trials : int\n        the number of trials in optuna.\n    "
    output_ext = luigi.Parameter(default='db')
    OptunaTask_params = luigi.DictParameter()
    n_trials = luigi.IntParameter(default=100)
    working_subdir = luigi.Parameter(default='optuna')

    def obj_task(self):
        """ return a `luigi.Task` instance, which, given a set of parameters in dict, returns a `loss` to be minimized.
        """
        raise NotImplementedError

    def run(self):
        study_name = os.path.splitext(os.path.basename(self.output().path))[0]
        study = optuna.create_study(study_name=study_name, storage=f"sqlite:///{self.output().path}")
        study.optimize((self.objective), n_trials=(self.n_trials), n_jobs=1)
        best_params_str = pprint.pformat(study.best_params)
        logger.info(f"\n=====================================\nbest_params:\n{best_params_str}\nbest_value:\t{study.best_value}\n=====================================\n        ")

    def create_params(self, trial):
        """ create a dictionary of parameters for `obj_task` given a trial

        Parameters
        ----------
        trial : optuna.trial.Trial
            trial object

        Returns
        -------
        dict
            parameters for `obj_task`
        """

        def _create_subparams(trial, param_dict):
            out_param_dict = dict()
            for each_key, each_val in param_dict.items():
                if isinstance(each_val, (dict, OrderedDict, luigi.parameter._FrozenOrderedDict)):
                    out_param_dict[each_key] = _create_subparams(trial, each_val)
                elif each_key.startswith('@'):
                    out_param_dict[each_key[1:]] = (getattr(trial, 'suggest_{}'.format(each_val[0])))(each_key[1:], *each_val[1])
                else:
                    out_param_dict[each_key] = each_val

            return out_param_dict

        return _create_subparams(trial, self.OptunaTask_params)

    def objective(self, trial):
        """ objective function

        Parameters
        ----------
        trial : optuna.trial.Trial
            trial object

        Returns
        -------
        float
            loss to be minimized. if a task fails, it returns `np.inf`
        """
        param_dict = self.create_params(trial)
        res = (self.obj_task)(**param_dict)
        luigi.build([res])
        try:
            val = float(res.output().open('r').read())
        except:
            val = np.inf

        return val

    def load_output(self):
        study_name = os.path.splitext(os.path.basename(self.output().path))[0]
        study = optuna.load_study(study_name=study_name, storage=f"sqlite:///{self.output().path}")
        return study

    def get_best_params(self):
        study = self.load_output()

        def _create_subparams(study, param_dict):
            out_param_dict = dict()
            for each_key, each_val in param_dict.items():
                if isinstance(each_val, (dict, OrderedDict, luigi.parameter._FrozenOrderedDict)):
                    out_param_dict[each_key] = _create_subparams(study, each_val)
                elif each_key.startswith('@'):
                    out_param_dict[each_key[1:]] = study.best_params[each_key[1:]]
                else:
                    out_param_dict[each_key] = each_val

            return out_param_dict

        return _create_subparams(study, self.OptunaTask_params)