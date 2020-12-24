# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/base/photon_elements.py
# Compiled at: 2019-11-21 09:20:09
# Size of source mod 2**32: 50697 bytes
import importlib, importlib.util, inspect
from copy import deepcopy
import os, numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection._search import ParameterGrid
from photonai.base.photon_pipeline import PhotonPipeline
from photonai.base.registry.element_dictionary import ElementDictionary
from photonai.helper.helper import PhotonDataHelper
from photonai.optimization.config_grid import create_global_config_grid, create_global_config_dict
import photonai.photonlogger.logger as logger

class PhotonNative:
    __doc__ = 'only for checking if code is meeting requirements'


class PipelineElement(BaseEstimator):
    __doc__ = '\n    Photon wrapper class for any transformer or predictor element in the pipeline.\n\n    1. Saves the hyperparameters that are to be tested and creates a grid of all hyperparameter configurations\n    2. Enables fast and rapid instantiation of pipeline elements per string identifier,\n         e.g \'svc\' creates an sklearn.svm.SVC object.\n    3. Attaches a "disable" switch to every element in the pipeline in order to test a complete disable\n\n\n    Parameters\n    ----------\n    * `name` [str]:\n       A string literal encoding the class to be instantiated\n    * `hyperparameters` [dict]:\n       Which values/value range should be tested for the hyperparameter.\n       In form of "Hyperparameter_name: [array of parameter values to be tested]"\n    * `test_disabled` [bool]:\n        If the hyperparameter search should evaluate a complete disabling of the element\n    * `disabled` [bool]:\n        If true, the element is currently disabled and does nothing except return the data it received\n    * `kwargs` [dict]:\n        Any parameters that should be passed to the object to be instantiated, default parameters\n\n    '
    ELEMENT_DICTIONARY = ElementDictionary.get_package_info()

    def __init__(self, name, hyperparameters: dict=None, test_disabled: bool=False, disabled: bool=False, base_element=None, batch_size=0, **kwargs):
        """
        Takes a string literal and transforms it into an object of the associated class (see PhotonCore.JSON)

        Returns
        -------
        instantiated class object
        """
        if hyperparameters is None:
            hyperparameters = {}
        else:
            if base_element is None:
                if name in PipelineElement.ELEMENT_DICTIONARY:
                    try:
                        desired_class_info = PipelineElement.ELEMENT_DICTIONARY[name]
                        desired_class_home = desired_class_info[0]
                        desired_class_name = desired_class_info[1]
                        imported_module = importlib.import_module(desired_class_home)
                        desired_class = getattr(imported_module, desired_class_name)
                        self.base_element = desired_class(**kwargs)
                    except AttributeError as ae:
                        try:
                            logger.error('ValueError: Could not find according class:' + str(PipelineElement.ELEMENT_DICTIONARY[name]))
                            raise ValueError('Could not find according class:', PipelineElement.ELEMENT_DICTIONARY[name])
                        finally:
                            ae = None
                            del ae

                else:
                    logger.error('Element not supported right now:' + name)
                    raise NameError('Element not supported right now:', name)
            else:
                self.base_element = base_element
            self.is_transformer = hasattr(self.base_element, 'transform')
            self.is_estimator = hasattr(self.base_element, 'predict')
            self._name = name
            self.initial_name = str(name)
            self.kwargs = kwargs
            self.current_config = None
            self.batch_size = batch_size
            self.test_disabled = test_disabled
            self.initial_hyperparameters = dict(hyperparameters)
            self._sklearn_disabled = self.name + '__disabled'
            self._hyperparameters = hyperparameters
            if len(hyperparameters) > 0:
                key_0 = next(iter(hyperparameters))
                if self.name not in key_0:
                    self.hyperparameters = hyperparameters
            else:
                self.hyperparameters = hyperparameters
            if not self.is_transformer:
                if self.is_estimator:
                    self._check_hyperparameters(BaseEstimator)
                self.disabled = disabled
                if hasattr(self.base_element, 'needs_y'):
                    self.needs_y = self.base_element.needs_y
                else:
                    self.needs_y = False
                if hasattr(self.base_element, 'needs_covariates'):
                    self.needs_covariates = self.base_element.needs_covariates
            else:
                self.needs_covariates = False
        self._random_state = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.generate_sklearn_hyperparameters(self.initial_hyperparameters)

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, value: dict):
        self.generate_sklearn_hyperparameters(value)

    def _check_hyperparameters(self, BaseEstimator):
        not_supported_hyperparameters = list(set([key.split('__')[(-1)] for key in self._hyperparameters.keys() if key.split('__')[(-1)] != 'disabled']) - set(BaseEstimator.get_params(self.base_element).keys()))
        if not_supported_hyperparameters:
            error_message = 'ValueError: Set of hyperparameters are not valid, check hyperparameters:' + str(not_supported_hyperparameters)
            logger.error(error_message)
            raise ValueError(error_message)

    def generate_sklearn_hyperparameters(self, value: dict):
        """
        Generates a dictionary according to the sklearn convention of element_name__parameter_name: parameter_value
        """
        self._hyperparameters = {}
        for attribute, value_list in value.items():
            self._hyperparameters[self.name + '__' + attribute] = value_list

        if self.test_disabled:
            self._hyperparameters[self._sklearn_disabled] = [
             False, True]

    @property
    def random_state(self):
        return self._random_state

    @random_state.setter
    def random_state(self, random_state):
        self._random_state = random_state
        if hasattr(self, 'elements'):
            for el in self.elements:
                if hasattr(el, 'random_state'):
                    el.random_state = self._random_state

        if hasattr(self, 'base_element'):
            if hasattr(self.base_element, 'random_state'):
                self.base_element.random_state = random_state

    @property
    def _estimator_type(self):
        if hasattr(self.base_element, '_estimator_type'):
            est_type = getattr(self.base_element, '_estimator_type')
            if est_type is not 'classifier':
                if est_type is not 'regressor':
                    raise NotImplementedError('Currently, we only support type classifier or regressor. Is {}.'.format(est_type))
            if not hasattr(self.base_element, 'predict'):
                raise NotImplementedError('Estimator does not implement predict() method.')
            return est_type
            if hasattr(self.base_element, 'predict'):
                raise NotImplementedError('Element has predict() method but does not specify whether it is a regressor or classifier. Remember to inherit from ClassifierMixin or RegressorMixin.')
        else:
            return

    def __iadd__(self, pipe_element):
        """
        Add an element to the element list
        Returns self

        Parameters
        ----------
        * `pipe_element` [PipelineElement or Hyperpipe]:
            The object to add, being either a transformer or an estimator.

        """
        PipelineElement.sanity_check_element_type_for_building_photon_pipes(pipe_element, type(self))
        already_added_objects = len([i for i in self.elements if i is pipe_element])
        if already_added_objects > 0:
            error_msg = 'Cannot add the same instance twice to ' + self.name + ' - ' + str(type(self))
            logger.error(error_msg)
            raise ValueError(error_msg)
        already_existing_element_with_that_name = len([i for i in self.elements if i.name == pipe_element.name])
        if already_existing_element_with_that_name > 0:
            error_msg = 'Already added a pipeline element with the name ' + pipe_element.name + ' to ' + self.name
            logger.warn(error_msg)
            nr_of_existing_elements_with_that_name = len([i for i in self.elements if i.name.startswith(pipe_element.name)])
            new_name = pipe_element.name + str(nr_of_existing_elements_with_that_name + 1)
            while len([i for i in self.elements if i.name == new_name]) > 0:
                nr_of_existing_elements_with_that_name += 1
                new_name = pipe_element.name + str(nr_of_existing_elements_with_that_name + 1)

            logger.warn('Renaming ' + pipe_element.name + ' in ' + self.name + ' to ' + new_name + ' in ' + self.name)
            pipe_element.name = new_name
        self.elements.append(pipe_element)
        return self

    def copy_me(self):
        if self.name in self.ELEMENT_DICTIONARY:
            copy = PipelineElement(self.initial_name, {}, test_disabled=self.test_disabled, disabled=self.disabled, 
             batch_size=self.batch_size, **self.kwargs)
            copy.initial_hyperparameters = self.initial_hyperparameters
            copy.name = self.name
        else:
            if hasattr(self.base_element, 'copy_me'):
                new_base_element = self.base_element.copy_me()
            else:
                try:
                    new_base_element = deepcopy(self.base_element)
                except Exception as e:
                    try:
                        error_msg = 'Cannot copy custom element ' + self.name + '. Please specify a copy_me() method returning a copy of the object'
                        logger.error(error_msg)
                        raise e
                    finally:
                        e = None
                        del e

                copy = (PipelineElement.create)(self.name, new_base_element, hyperparameters=self.hyperparameters, test_disabled=self.test_disabled, 
                 disabled=self.disabled, 
                 batch_size=self.batch_size, **self.kwargs)
        if self.current_config is not None:
            (copy.set_params)(**self.current_config)
        copy._random_state = self._random_state
        return copy

    @classmethod
    def create(cls, name, base_element, hyperparameters: dict, test_disabled=False, disabled=False, **kwargs):
        """
        Takes an instantiated object and encapsulates it into the PHOTON structure,
        add the disabled function and attaches information about the hyperparameters that should be tested
        """
        if isinstance(base_element, type):
            raise ValueError('Base element should be an instance but is a class.')
        return PipelineElement(name, hyperparameters, test_disabled, disabled, base_element=base_element, **kwargs)

    @property
    def feature_importances_(self):
        if hasattr(self.base_element, 'feature_importances_'):
            return self.base_element.feature_importances_.tolist()
        if hasattr(self.base_element, 'coef_'):
            return self.base_element.coef_.tolist()

    def generate_config_grid(self):
        config_dict = create_global_config_dict([self])
        if len(config_dict) > 0:
            if self.test_disabled:
                config_dict.pop(self._sklearn_disabled)
            config_list = list(ParameterGrid(config_dict))
            if self.test_disabled:
                for item in config_list:
                    item[self._sklearn_disabled] = False

                config_list.append({self._sklearn_disabled: True})
                if len(config_list) < 2:
                    config_list.append({self._sklearn_disabled: False})
            return config_list
        return []

    def get_params(self, deep: bool=True):
        """
        Forwards the get_params request to the wrapped base element
        """
        if hasattr(self.base_element, 'get_params'):
            params = self.base_element.get_params(deep)
            params['name'] = self.name
            return params
        return

    def set_params(self, **kwargs):
        """
        Forwards the set_params request to the wrapped base element
        Takes care of the disabled parameter which is additionally attached by the PHOTON wrapper
        """
        self.current_config = kwargs
        if self._sklearn_disabled in kwargs:
            self.disabled = kwargs[self._sklearn_disabled]
            del kwargs[self._sklearn_disabled]
        else:
            if 'disabled' in kwargs:
                self.disabled = kwargs['disabled']
                del kwargs['disabled']
        (self.base_element.set_params)(**kwargs)
        return self

    def fit(self, X, y=None, **kwargs):
        """
        Calls the fit function of the base element

        Returns
        ------
        self
        """
        if not self.disabled:
            obj = self.base_element
            arg_list = inspect.signature(obj.fit)
            if len(arg_list.parameters) > 2:
                vals = arg_list.parameters.values()
                kwargs_param = list(vals)[(-1)]
                if kwargs_param.kind == kwargs_param.VAR_KEYWORD:
                    (obj.fit)(X, y, **kwargs)
                    return self
            obj.fit(X, y)
        return self

    def __batch_predict(self, delegate, X, **kwargs):
        if not isinstance(X, list):
            if not isinstance(X, np.ndarray):
                logger.warn('Cannot do batching on a single entity.')
                return delegate(X, **kwargs)
        processed_y = None
        nr = PhotonDataHelper.find_n(X)
        batch_idx = 0
        for start, stop in PhotonDataHelper.chunker(nr, self.batch_size):
            batch_idx += 1
            logger.debug(self.name + ' is predicting batch ' + str(batch_idx))
            X_batched, y_batched, kwargs_dict_batched = PhotonDataHelper.split_data(X, None, kwargs, start, stop)
            y_pred = delegate(X_batched, **kwargs_dict_batched)
            processed_y = PhotonDataHelper.stack_data_vertically(processed_y, y_pred)

        return processed_y

    def __predict(self, X, **kwargs):
        if not self.disabled:
            if hasattr(self.base_element, 'predict'):
                return (self.adjusted_predict_call)((self.base_element.predict), X, **kwargs)
            logger.error('BaseException. base Element should have function predict.')
            raise BaseException('base Element should have function predict.')
        else:
            return X

    def predict(self, X, **kwargs):
        """
        Calls predict function on the base element.
        """
        if self.batch_size == 0:
            return (self._PipelineElement__predict)(X, **kwargs)
        return (self._PipelineElement__batch_predict)((self._PipelineElement__predict), X, **kwargs)

    def predict_proba(self, X, **kwargs):
        if self.batch_size == 0:
            return (self._PipelineElement__predict_proba)(X, **kwargs)
        return (self._PipelineElement__batch_predict)((self._PipelineElement__predict_proba), X, **kwargs)

    def __predict_proba(self, X, **kwargs):
        """
        Predict probabilities
        base element needs predict_proba() function, otherwise throw
        base exception.
        """
        if not self.disabled:
            if hasattr(self.base_element, 'predict_proba'):
                return (self.adjusted_predict_call)((self.base_element.predict_proba), X, **kwargs)
            return
        return X

    def __transform(self, X, y=None, **kwargs):
        if not self.disabled:
            if hasattr(self.base_element, 'transform'):
                return (self.adjusted_delegate_call)((self.base_element.transform), X, y, **kwargs)
            if hasattr(self.base_element, 'predict'):
                return (
                 (self.predict)(X, **kwargs), y, kwargs)
            logger.error('BaseException: transform-predict-mess')
            raise BaseException('transform-predict-mess')
        else:
            return (
             X, y, kwargs)

    def transform(self, X, y=None, **kwargs):
        """
        Calls transform on the base element.

        IN CASE THERE IS NO TRANSFORM METHOD, CALLS PREDICT.
        This is used if we are using an estimator as a preprocessing step.
        """
        if self.batch_size == 0:
            return (self._PipelineElement__transform)(X, y, **kwargs)
        return (self._PipelineElement__batch_transform)(X, y, **kwargs)

    def inverse_transform(self, X, y=None, **kwargs):
        if hasattr(self.base_element, 'inverse_transform'):
            X, y, kwargs = (self.adjusted_delegate_call)((self.base_element.inverse_transform), X, y, **kwargs)
        return (
         X, y, kwargs)

    def __batch_transform(self, X, y=None, **kwargs):
        if not isinstance(X, list):
            if not isinstance(X, np.ndarray):
                logger.warn('Cannot do batching on a single entity.')
                return (self._PipelineElement__transform)(X, y, **kwargs)
        processed_X = None
        processed_y = None
        processed_kwargs = dict()
        nr = PhotonDataHelper.find_n(X)
        batch_idx = 0
        for start, stop in PhotonDataHelper.chunker(nr, self.batch_size):
            batch_idx += 1
            X_batched, y_batched, kwargs_dict_batched = PhotonDataHelper.split_data(X, y, kwargs, start, stop)
            actual_batch_size = PhotonDataHelper.find_n(X_batched)
            logger.debug(self.name + ' is transforming batch ' + str(batch_idx) + ' with ' + str(actual_batch_size) + ' items.')
            X_new, y_new, kwargs_new = (self.adjusted_delegate_call)((self.base_element.transform), X_batched, y_batched, **kwargs_dict_batched)
            processed_X, processed_y, processed_kwargs = PhotonDataHelper.join_data(processed_X, X_new, processed_y, y_new, processed_kwargs, kwargs_new)

        return (processed_X, processed_y, processed_kwargs)

    def adjusted_delegate_call(self, delegate, X, y, **kwargs):
        if self.needs_y:
            if isinstance(self, (Switch, Branch, Preprocessing)):
                X, y, kwargs = delegate(X, y, **kwargs)
            elif y is not None:
                if self.needs_covariates:
                    X, y, kwargs = delegate(X, y, **kwargs)
                else:
                    X, y = delegate(X, y)
        elif self.needs_covariates:
            X, kwargs = delegate(X, **kwargs)
        else:
            X = delegate(X)
        return (X, y, kwargs)

    def adjusted_predict_call(self, delegate, X, **kwargs):
        if self.needs_covariates:
            return delegate(X, **kwargs)
        return delegate(X)

    def score(self, X_test, y_test):
        """
        Calls the score function on the base element:
        Returns a goodness of fit measure or a likelihood of unseen data:
        """
        return self.base_element.score(X_test, y_test)

    def prettify_config_output(self, config_name: str, config_value, return_dict: bool=False):
        """Make hyperparameter combinations human readable """
        if config_name == 'disabled' and config_value is False:
            if return_dict:
                return {'disabled': False}
            return 'disabled = False'
        else:
            if return_dict:
                return {config_name: config_value}
            return config_name + '=' + str(config_value)

    @staticmethod
    def sanity_check_element_type_for_building_photon_pipes--- This code section failed: ---

 L. 545         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'pipe_element'
                4  LOAD_GLOBAL              PipelineElement
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'pipe_element'
               14  LOAD_GLOBAL              PhotonNative
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_FALSE    30  'to 30'
             20_0  COME_FROM             8  '8'
               20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'pipe_element'
               24  LOAD_GLOBAL              Preprocessing
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_FALSE    58  'to 58'
             30_0  COME_FROM            18  '18'

 L. 546        30  LOAD_GLOBAL              TypeError
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'type_of_self'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_STR                 ' only accepts PHOTON elements. Cannot add element of type '
               40  BINARY_ADD       
               42  LOAD_GLOBAL              str
               44  LOAD_GLOBAL              type
               46  LOAD_FAST                'pipe_element'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  BINARY_ADD       
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            28  '28'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 56


class Branch(PipelineElement):
    __doc__ = '\n     A substream of pipeline elements that is encapsulated e.g. for parallelization\n\n     Parameters\n     ----------\n        * `name` [str]:\n            Name of the encapsulated item and/or summary of the encapsulated element`s functions\n\n        '

    def __init__(self, name, elements=None):
        super().__init__(name, {}, test_disabled=False, disabled=False, base_element=True)
        self.needs_y = True
        self.needs_covariates = True
        self.elements = []
        self.has_hyperparameters = True
        self.skip_caching = True
        self.fix_fold_id = False
        self.do_not_delete_cache_folder = False
        if elements:
            for element in elements:
                self.add(element)

    def fit(self, X, y=None, **kwargs):
        self.base_element = Branch.sanity_check_pipeline(self.base_element)
        return (super().fit)(X, y, **kwargs)

    def transform(self, X, y=None, **kwargs):
        if self._estimator_type == 'classifier' or self._estimator_type == 'regressor':
            return (
             super().predict(X), y, kwargs)
        return (super().transform)(X, y, **kwargs)

    def predict(self, X, **kwargs):
        return (super().predict)(X, **kwargs)

    def __iadd__(self, pipe_element):
        super(Branch, self).__iadd__(pipe_element)
        self._prepare_pipeline()
        return self

    def add(self, pipe_element):
        """
           Add an element to the sub pipeline
           Returns self

           Parameters
           ----------
           * `pipe_element` [PipelineElement or Hyperpipe]:
               The object to add, being either a transformer or an estimator.

           """
        self.__iadd__(pipe_element)

    @staticmethod
    def prepare_photon_pipe(elements):
        pipeline_steps = list()
        for item in elements:
            pipeline_steps.append((item.name, item))

        return PhotonPipeline(pipeline_steps)

    @staticmethod
    def sanity_check_pipeline(pipe):
        if isinstance(pipe.elements[(-1)][1], CallbackElement):
            raise Warning('Last element of pipeline cannot be callback element, would be mistaken for estimator. Removing it.')
            Logger().warn('Last element of pipeline cannot be callback element, would be mistaken for estimator. Removing it.')
            del pipeline_steps[-1]
        return pipe

    def _prepare_pipeline(self):
        """ Generates sklearn pipeline with all underlying elements """
        self._hyperparameters = {item.name:item.hyperparameters for item in self.elements if hasattr(item, 'hyperparameters') if hasattr(item, 'hyperparameters')}
        if self.has_hyperparameters:
            self.generate_sklearn_hyperparameters()
        new_pipe = Branch.prepare_photon_pipe(self.elements)
        new_pipe._fix_fold_id = self.fix_fold_id
        new_pipe._do_not_delete_cache_folder = self.do_not_delete_cache_folder
        self.base_element = new_pipe

    def copy_me(self):
        new_copy_of_me = self.__class__(self.name)
        for item in self.elements:
            if hasattr(item, 'copy_me'):
                copy_item = item.copy_me()
            else:
                copy_item = deepcopy(item)
            new_copy_of_me += copy_item

        if self.current_config is not None:
            (new_copy_of_me.set_params)(**self.current_config)
        new_copy_of_me._random_state = self._random_state
        return new_copy_of_me

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, value):
        """
        Setting hyperparameters does not make sense, only the items that added can be optimized, not the container (self)
        """
        pass

    @property
    def _estimator_type(self):
        return getattr(self.elements[(-1)], '_estimator_type')

    def generate_config_grid(self):
        if self.has_hyperparameters:
            tmp_grid = create_global_config_grid(self.elements, self.name)
            return tmp_grid
        return []

    def generate_sklearn_hyperparameters(self):
        """
        Generates a dictionary according to the sklearn convention of element_name__parameter_name: parameter_value
        """
        self._hyperparameters = {}
        for element in self.elements:
            for attribute, value_list in element.hyperparameters.items():
                self._hyperparameters[self.name + '__' + attribute] = value_list

    def _check_hyper(self, BaseEstimator):
        pass

    @property
    def feature_importances_(self):
        if hasattr(self.elements[(-1)], 'feature_importances_'):
            return getattr(self.elements[(-1)], 'feature_importances_')


class Preprocessing(Branch):
    __doc__ = '\n        If a preprocessing pipe is added to a PHOTON Hyperpipe, all transformers are applied to the data ONCE\n        BEFORE cross validation starts in order to prepare the data.\n        Every added element should be a transformer PipelineElement.\n    '

    def __init__(self):
        super().__init__('Preprocessing')
        self.has_hyperparameters = False
        self.needs_y = True
        self.needs_covariates = True
        self._name = 'Preprocessing'
        self.is_transformer = True
        self.is_estimator = False

    def __iadd__(self, pipe_element):
        if hasattr(pipe_element, 'transform'):
            super(Preprocessing, self).__iadd__(pipe_element)
            if len(pipe_element.hyperparameters) > 0:
                raise ValueError('A preprocessing transformer must not have any hyperparameter because it is not part of the optimization and cross validation procedure')
        else:
            raise ValueError('Pipeline Element must have transform function')
        return self

    def predict(self, data, **kwargs):
        raise Warning('There is no predict function of the preprocessing pipe, it is a transformer only.')

    @property
    def _estimator_type(self):
        pass


class Stack(PipelineElement):
    __doc__ = '\n    Creates a vertical stacking/parallelization of pipeline items.\n\n    The object acts as single pipeline element and encapsulates several vertically stacked other pipeline elements, each\n    child receiving the same input data. The data is iteratively distributed to all children, the results are collected\n    and horizontally concatenated.\n\n    '

    def __init__(self, name, elements=None, use_probabilities=False):
        """
        Creates a new Stack element.
        Collects all possible hyperparameter combinations of the children

        Parameters
        ----------
        * `name` [str]:
            Give the pipeline element a name
        * `elements` [list, optional]:
            List of pipeline elements that should run in parallel
        * `voting` [bool]:
            If true, the predictions of the encapsulated pipeline elements are joined to a single prediction
        """
        super(Stack, self).__init__(name, hyperparameters={}, test_disabled=False, disabled=False, base_element=True)
        self._hyperparameters = {}
        self.elements = list()
        if elements is not None:
            for item_to_stack in elements:
                self.__iadd__(item_to_stack)

        self.needs_y = False
        self.needs_covariates = True
        self.use_probabilities = use_probabilities

    def __iadd__(self, item):
        self.check_if_needs_y(item)
        super(Stack, self).__iadd__(item)
        tmp_dict = dict(item.hyperparameters)
        for key, element in tmp_dict.items():
            self._hyperparameters[self.name + '__' + key] = tmp_dict[key]

        return self

    def check_if_needs_y(self, item):
        if isinstance(item, (Branch, Stack, Switch)):
            for child_item in item.elements:
                self.check_if_needs_y(child_item)

        else:
            if isinstance(item, PipelineElement) and item.needs_y:
                raise NotImplementedError('Elements in Stack must not transform y because the number of samples in every element of the stack might differ. Then, it will not be possible to concatenate those data and target matrices. Please use the transformer that is using y before or after the stack.')

    def add(self, item):
        self.__iadd__(item)

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, value):
        """
        Setting hyperparameters does not make sense, only the items that added can be optimized, not the container (self)
        """
        pass

    def generate_config_grid(self):
        tmp_grid = create_global_config_grid(self.elements, self.name)
        return tmp_grid

    def get_params(self, deep=True):
        all_params = {}
        for element in self.elements:
            all_params[element.name] = element.get_params(deep)

        return all_params

    def set_params(self, **kwargs):
        """
        Find the particular child and distribute the params to it
        """
        spread_params_dict = {}
        for k, val in kwargs.items():
            splitted_k = k.split('__')
            item_name = splitted_k[0]
            if item_name not in spread_params_dict:
                spread_params_dict[item_name] = {}
            dict_entry = {'__'.join(splitted_k[1:]): val}
            spread_params_dict[item_name].update(dict_entry)

        for name, params in spread_params_dict.items():
            missing_element = (
             name, params)
            for element in self.elements:
                if element.name == name:
                    (element.set_params)(**params)
                    missing_element = None

            if missing_element:
                raise ValueError("Couldn't set hyperparameter for element {} -> {}".format(missing_element[0], missing_element[1]))

        return self

    def fit(self, X, y=None, **kwargs):
        """
        Calls fit iteratively on every child
        """
        for element in self.elements:
            (element.fit)(X, y, **kwargs)

        return self

    def predict(self, X, **kwargs):
        if not self.use_probabilities:
            return (self._predict)(X, **kwargs)
        return (self.predict_proba)(X, **kwargs)

    def _predict(self, X, **kwargs):
        """
        Iteratively calls predict on every child.
        """
        predicted_data = np.array([])
        for element in self.elements:
            element_transform = (element.predict)(X, **kwargs)
            predicted_data = PhotonDataHelper.stack_data_horizontally(predicted_data, element_transform)

        return predicted_data

    def predict_proba(self, X, y=None, **kwargs):
        """
        Predict probabilities for every pipe element and stack them together.
        """
        predicted_data = np.array([])
        for element in self.elements:
            element_transform = element.predict_proba(X)
            if element_transform is None:
                element_transform = element.predict(X)
            predicted_data = PhotonDataHelper.stack_data_horizontally(predicted_data, element_transform)

        return predicted_data

    def transform(self, X, y=None, **kwargs):
        """
        Calls transform on every child.

        If the encapsulated child is a hyperpipe, also calls predict on the last element in the pipeline.
        """
        transformed_data = np.array([])
        for element in self.elements:
            element_transform, _, _ = (element.transform)(X, y, **kwargs)
            transformed_data = PhotonDataHelper.stack_data_horizontally(transformed_data, element_transform)

        return (transformed_data, y, kwargs)

    def copy_me(self):
        ps = Stack(self.name)
        for element in self.elements:
            new_element = element.copy_me()
            ps += new_element

        ps.base_element = self.base_element
        ps._random_state = self._random_state
        return ps

    def inverse_transform(self, X, y=None, **kwargs):
        raise NotImplementedError('Inverse Transform is not yet implemented for a Stacking Element in PHOTON')

    @property
    def _estimator_type(self):
        pass

    def _check_hyper(self, BaseEstimator):
        pass

    @property
    def feature_importances_(self):
        pass


class Switch(PipelineElement):
    __doc__ = "\n    This class encapsulates several pipeline elements that belong at the same step of the pipeline,\n    competing for being the best choice.\n\n    If for example you want to find out if preprocessing A or preprocessing B is better at this position in the pipe.\n    Or you want to test if a tree outperforms the good old SVM.\n\n    ATTENTION: This class is a construct that may be convenient but is not suitable for any complex optimizations.\n    Currently it only works for grid_search and the derived optimization strategies.\n    USE THIS ONLY FOR RAPID PROTOTYPING AND PRELIMINARY RESULTS\n\n    The class acts as if it is a single entity. Tt joins the hyperparamater combinations of each encapsulated element to\n    a single, big combination grid. Each hyperparameter combination from that grid gets a number. Then the Switch\n    object publishes the numbers to be chosen as the object's hyperparameter. When a new number is chosen from the\n    optimizer, it internally activates the belonging element and sets the element's parameter to the hyperparameter\n    combination. In that way, each of the elements is tested in all its configurations at the same position in the\n    pipeline. From the outside, the process and the optimizer only sees one parameter of the Switch, that is\n    the an integer indicating which item of the hyperparameter combination grid is currently active.\n\n    "

    def __init__(self, name: str, elements: list=None):
        """
        Creates a new Switch object and generated the hyperparameter combination grid

        Parameters
        ----------
        * `name` [str]:
            How the element is called in the pipeline
        * `elements` [list, optional]:
            The competing pipeline elements
        * `_estimator_type:
            Used for validation purposes, either classifier or regressor

        """
        self._name = name
        self.sklearn_name = self.name + '__current_element'
        self._hyperparameters = {}
        self._current_element = (1, 1)
        self.pipeline_element_configurations = []
        self.base_element = None
        self.disabled = False
        self.test_disabled = False
        self.batch_size = 0
        self.needs_y = True
        self.needs_covariates = True
        self.is_estimator = True
        self.is_transformer = True
        self._random_state = False
        self.elements_dict = {}
        if elements:
            self.elements = elements
            self.generate_private_config_grid()
            for p_element in elements:
                self.elements_dict[p_element.name] = p_element

        else:
            self.elements = []

    def __iadd__(self, pipeline_element):
        super(Switch, self).__iadd__(pipeline_element)
        self.elements_dict[pipeline_element.name] = pipeline_element
        self.generate_private_config_grid()
        return self

    def add(self, pipeline_element):
        """
        Add a new estimator or transformer object to the switch container. All items change positions during testing.

        Parameters
        ----------
        * `pipeline_element` [PipelineElement]:
            Item that should be tested against other competing elements at that position in the pipeline.
        """
        self.__iadd__(pipeline_element)

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, value):
        pass

    def generate_private_config_grid(self):
        self.pipeline_element_configurations = []
        hyperparameters = []
        for i, pipe_element in enumerate(self.elements):
            if hasattr(pipe_element, 'generate_config_grid'):
                element_configurations = pipe_element.generate_config_grid()
                final_configuration_list = []
                if len(element_configurations) == 0:
                    final_configuration_list.append({})
                for dict_item in element_configurations:
                    final_configuration_list.append(dict(dict_item))

            self.pipeline_element_configurations.append(final_configuration_list)
            hyperparameters += [(i, nr) for nr in range(len(final_configuration_list))]

        self._hyperparameters = {self.sklearn_name: hyperparameters}

    @property
    def current_element(self):
        return self._current_element

    @current_element.setter
    def current_element(self, value):
        self._current_element = value
        self.base_element = self.elements[self.current_element[0]]

    def get_params(self, deep: bool=True):
        if self.base_element:
            return self.base_element.get_params(deep)
        return {}

    def set_params(self, **kwargs):
        """
        The optimization process sees the amount of possible combinations and chooses one of them.
        Then this class activates the belonging element and prepared the element with the particular chosen configuration.

        """
        config_nr = None
        config = None
        if self.sklearn_name in kwargs:
            config_nr = kwargs[self.sklearn_name]
        else:
            if 'current_element' in kwargs:
                config_nr = kwargs['current_element']
            elif config_nr is None:
                if kwargs is not None:
                    config = kwargs
                    for kwargs_key, kwargs_value in kwargs.items():
                        first_element_name = kwargs_key.split('__')[0]
                        self.base_element = self.elements_dict[first_element_name]
                        break

            else:
                if not isinstance(config_nr, (tuple, list)):
                    logger.error('ValueError: current_element must be of type Tuple')
                    raise ValueError('current_element must be of type Tuple')
                self.current_element = config_nr
                config = self.pipeline_element_configurations[config_nr[0]][config_nr[1]]
            if config:
                unnamed_config = {}
                for config_key, config_value in config.items():
                    key_split = config_key.split('__')
                    unnamed_config['__'.join(key_split[1:])] = config_value

                (self.base_element.set_params)(**unnamed_config)
            return self

    def copy_me(self):
        ps = Switch(self.name)
        ps._random_state = self._random_state
        for element in self.elements:
            new_element = element.copy_me()
            ps += new_element

        ps._current_element = self._current_element
        return ps

    def prettify_config_output(self, config_name, config_value, return_dict=False):
        """
        Makes the sklearn configuration dictionary human readable

        Returns
        -------
        * `prettified_configuration_string` [str]:
            configuration as prettified string or configuration as dict with prettified keys
        """
        if isinstance(config_value, tuple):
            output = self.pipeline_element_configurations[config_value[0]][config_value[1]]
            if not output:
                if return_dict:
                    return {self.elements[config_value[0]].name: None}
                return self.elements[config_value[0]].name
            else:
                if return_dict:
                    return output
                return str(output)
        else:
            return super(Switch, self).prettify_config_output(config_name, config_value)

    def predict_proba(self, X, **kwargs):
        """
        Predict probabilities
        base element needs predict_proba() function, otherwise throw
        base exception.
        """
        if not self.disabled:
            if hasattr(self.base_element.base_element, 'predict_proba'):
                return self.base_element.predict_proba(X)
            return
        return X

    def _check_hyper(self, BaseEstimator):
        pass

    def inverse_transform(self, X, y=None, **kwargs):
        if hasattr(self.base_element, 'inverse_transform'):
            X, y, kwargs = (self.adjusted_delegate_call)((self.base_element.inverse_transform), X, y, **kwargs)
        return (
         X, y, kwargs)

    @property
    def _estimator_type(self):
        estimator_types = list()
        for element in self.elements:
            estimator_types.append(getattr(element, '_estimator_type'))

        unique_types = set(estimator_types)
        if len(unique_types) > 1:
            raise NotImplementedError('Switch should only contain elements of a single type (transformer, classifier, regressor). Found multiple types: {}'.format(unique_types))
        else:
            if len(unique_types) == 1:
                return list(unique_types)[0]
            return

    @property
    def feature_importances_(self):
        if hasattr(self.base_element, 'feature_importances_'):
            return getattr(self.base_element, 'feature_importances_')


class DataFilter(BaseEstimator, PhotonNative):
    __doc__ = '\n    Helper Class to split the data e.g. for stacking.\n    '

    def __init__(self, indices):
        self.name = 'DataFilter'
        self.hyperparameters = {}
        self.indices = indices
        self.needs_covariates = False
        self.needs_y = False

    def fit(self, X, y=None, **kwargs):
        return self

    def transform(self, X, y=None, **kwargs):
        """
        Returns only part of the data, column-wise filtered by self.indices
        """
        return (
         X[:, self.indices], y, kwargs)

    def copy_me(self):
        return self.__class__(indices=(self.indices))

    @property
    def _estimator_type(self):
        pass


class CallbackElement(PhotonNative):

    def __init__(self, name, delegate_function, method_to_monitor='transform'):
        self.needs_covariates = True
        self.needs_y = True
        self.name = name
        self.delegate_function = delegate_function
        self.method_to_monitor = method_to_monitor
        self.hyperparameters = {}
        self.is_transformer = True
        self.is_estimator = False

    def fit(self, X, y=None, **kwargs):
        if self.method_to_monitor == 'fit':
            (self.delegate_function)(X, y, **kwargs)
        return self

    def transform(self, X, y=None, **kwargs):
        if self.method_to_monitor == 'transform':
            (self.delegate_function)(X, y, **kwargs)
        return (
         X, y, kwargs)

    def copy_me(self):
        return self.__class__(self.name, self.delegate_function, self.method_to_monitor)

    def inverse_transform(self, X, y=None, **kwargs):
        return (
         X, y, kwargs)

    @property
    def _estimator_type(self):
        pass

    @property
    def feature_importances_(self):
        pass