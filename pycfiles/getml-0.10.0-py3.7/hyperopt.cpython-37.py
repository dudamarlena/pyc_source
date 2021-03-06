# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/hyperopt.py
# Compiled at: 2019-12-09 07:12:30
# Size of source mod 2**32: 73787 bytes
"""Automatically find the best combination of parameters for both the
feature engineerers and predictors.

To use the hyperparameter optimization, you first have to construct
and provide a base `model` (of type
:class:`~getml.models.MultirelModel` or
:class:`~getml.models.RelboostModel`) as well as a parameter space
`param_space` from which new hyperparameter combinations will be
drawn. The actual algorithm to pick the next combination is chosen via
the particular class to construct the hyperparameter optimization
from. For now :class:`~getml.hyperopt.RandomSearch` and
:class:`~getml.hyperopt.LatinHypercubeSearch` are available.

In each iteration of the hyperparameter optimization a new combination
of hyperparameters are drawn from `param_space` and assigned to
`model`. The resulting model will be stored in the getML engine,
fitted and scored. The whole process is triggered by invoking the
:meth:`~getml.hyperopt._BaseSearch.fit` method and results can be
access using :meth:`~getml.hyperopt._BaseSearch.get_models` and
:meth:`~getml.hyperopt._BaseSearch.get_scores`.

A working example can be found in :ref:`hyperparameter-optimization`.

"""
import datetime, json, numbers, warnings, numpy as np
import getml.communication as comm
import getml.engine as engine
import getml.models as models

class _BaseSearch(object):
    __doc__ = '\n    Base class - not meant to be called by the user.\n    '

    def __init__(self, model, param_space=None):
        """Constructor function.

        Uses the :meth:`~getml.hyperopt._BaseSearch.set_param_space`
        function to add `param_space` to the constructed instance.

        Args:

            model (:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`) 
                Base model used
                to derive all models fitted and scored during the
                hyperparameter optimization. Be careful in
                constructing it since only those parameters present in
                `param_space` too will be overwritten. It defines the
                data schema, the loss function and any hyperparameters
                that are not optimized.
            param_space (dict, optional): Dictionary containing lists
                of length two holding the lower and upper bounds of
                all hyperparameters which will be altered in `model`
                during the hyperparameter optimization as values. To
                keep a specific hyperparameter fixed, you have two
                options. Either ensure it is not present in
                `param_space` (but in `model`), or set both the lower
                and upper bound to the same value. If None, the
                default parameters will be determined for the
                particular combination of model, predictor, and
                feature selector using the
                :meth:`~getml.hyperopt._BaseSearch.__default_param_space_*`
                member functions of this class. Default is None.

        Raises:
            Exception: If not predictor is present in the provided
                `model`.
            TypeError: If the predictor is neither
                :class:`~getml.predictors.LinearRegression`,
                :class:`~getml.predictors.LogisticRegression`,
                :class:`~getml.predictors.XGBoostClassifier` or
                :class:`~getml.predictors.XGBoostRegressor` (in
                :meth:`~getml.hyperopt._BaseSearch.set_param_space`).
            TypeError: If the model is neither
                :class:`~getml.models.MultirelModel` nor
                :class:`~getml.models.RelboostModel`.
            ValueError: If at least one of the keys in `param_space`
                does not exist in the corresponding default space (in
                :meth:`~getml.hyperopt._BaseSearch.set_param_space`).

        """
        if param_space is None:
            use_default_param_space = True
        else:
            use_default_param_space = False
        if use_default_param_space:
            param_space = _BaseSearch__default_param_space_Multirel()
        elif type(model) is models.MultirelModel:
            self.model_type = 'Multirel'
            if use_default_param_space:
                param_space = _BaseSearch__default_param_space_Multirel()
        elif type(model) is models.RelboostModel:
            self.model_type = 'Relboost'
            if use_default_param_space:
                param_space = _BaseSearch__default_param_space_Relboost()
        else:
            raise TypeError('Unknown model class.')
        self.model = model
        if model.params['predictor'] is None:
            raise Exception('No predictor present in supplied model!')
        self.params = {'n_iter':100, 
         'ratio_iter':0.75, 
         'optimization_algorithm':'nelderMead', 
         'optimization_burn_in_algorithm':'latinHypercube', 
         'optimization_burn_ins':15, 
         'surrogate_burn_in_algorithm':'latinHypercube', 
         'gaussian__kernel':'matern52', 
         'gaussian__optimization_algorithm':'nelderMead', 
         'gaussian__optimization_burn_in_algorithm':'latinHypercube', 
         'gaussian__optimization_burn_ins':50}
        if use_default_param_space:
            if model.params['predictor']['type_'] == 'LinearRegression':
                param_space.update(self._BaseSearch__default_param_space_LinearRegression())
            if model.params['predictor']['type_'] == 'LogisticRegression':
                param_space.update(self._BaseSearch__default_param_space_LogisticRegression())
            if model.params['predictor']['type_'] == 'XGBoostPredictor':
                param_space.update(self._BaseSearch__default_param_space_XGBoost())
        self.set_param_space(param_space)

    def __default_param_space_Multirel(self):
        """Default parameter space for optimizing the
        :class:`~getml.models.MultirelModel`.

        Returns:
            dict: 
                Default parameter space for optimizing the Multirel
                model.

        """
        param_space = {'grid_factor':[
          1.0, 16.0], 
         'max_length':[
          1, 10], 
         'min_num_samples':[
          100, 500], 
         'num_features':[
          10, 500], 
         'regularization':[
          0.0, 0.01], 
         'share_aggregations':[
          0.01, 1.0], 
         'share_selected_features':[
          0.1, 1.0], 
         'shrinkage':[
          0.01, 0.4]}
        return param_space

    def __default_param_space_LinearRegression(self):
        """Default parameter space for the
        :class:`~getml.predictors.LinearRegression`.

        Returns:
            dict: 
                Default parameter space for
                :class:`~getml.predictors.LinearRegression` predictor.

        """
        param_space = {'predictor__learning_rate':[
          0.5, 1.0], 
         'predictor__lambda':[
          0.0, 1.0]}
        return param_space

    def __default_param_space_LogisticRegression(self):
        """Default parameter space for the
        :class:`~getml.predictors.LogisticRegression`.

        Returns:
            dict: 
                Default parameter space for
                :class:`~getml.predictors.LogisticRegression` predictor.

        """
        param_space = {'predictor__learning_rate':[
          0.0, 1.0], 
         'predictor__lambda':[
          0.0, 1.0]}
        return param_space

    def __default_param_space_Relboost(self):
        """Default parameter space for optimizing the Relboost model.
        """
        param_space = {'max_depth':[
          1, 10], 
         'min_num_samples':[
          100, 500], 
         'num_features':[
          10, 500], 
         'reg_lambda':[
          0.0, 0.1], 
         'share_selected_features':[
          0.1, 1.0], 
         'shrinkage':[
          0.01, 0.4]}
        return param_space

    def __default_param_space_XGBoost(self):
        """Default parameter space for
        :class:`~getml.predictors.XGBoostClassifier` and
        :class:`~getml.predictors.XGBoostRegressor`.

        Returns:
            dict:  
                Default parameter space.

        """
        param_space = {'predictor__n_estimators':[
          10, 500], 
         'predictor__learning_rate':[
          0.0, 1.0], 
         'predictor__max_depth':[
          3, 15], 
         'predictor__reg_lambda':[
          0.0, 10.0]}
        return param_space

    def __validate_colnames(self, names_table1, names_table2, description):
        """Makes sure that the colnames of two tables provided in
        `names_table1` and `names_table2` do match.

        Args:
            names_table1 (list[string]): List of strings specifying a
                set of columns in one table.
            names_table2 (list[string]): List of strings specifying a
                set of columns in another table.
            description (string): Should specify the particular set of
                column to allow for more informative exceptions
                raised.

        Raises:
            Exception: If the length of `names_table1` and
                `names_table2` do not match.
            Exception: If one string in `names_table1` is not present
                in `names_table2` or the other way around.

        """
        if len(names_table1) != len(names_table2):
            raise Exception('Number of ' + description + ' columns does not match')
        for nname in names_table1:
            if nname not in names_table2:
                raise Exception('Missing column in ' + description + ":'" + nname + "'")

        for nname in names_table1:
            if nname not in names_table2:
                raise Exception('Missing column in ' + description + ":'" + nname + "'")

    def __validate_ensure_param_space_bounds(self, param_space, key, bounds):
        """Checks whether a particular hyperparameter of the `param_space`
        does lie within the provided `bounds`.

        It ensures the second element of the list in the corresponding
        value of `param_space` - the upper bound - is larger than the
        first - the lower bound. In addition, it checks that both
        elements are within the provided `bounds`.

        In both cases the function will overwrite the provided
        dictionary using
        :meth:`~getml.hyperopt._BaseSearch.__validate_set_param_space_with_warning`
        to ensure the correct ordering and that either of the two
        bounds are not exceeded. Whenever this happens a warning
        message will be printed.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.
            key (string): Specifies a particular hyperparameter in
                `param_space`.
            bounds (list[numeric]): Numerical list of length 2
                specifying the lower and upper bound (in that order)
                of a particular hyperparameter determined by `key` in
                `param_space`.

        Returns:
            dict:  
                Validated version of `param_space`.

        Raises:
            TypeError: If the object in `param_space` referenced by
                `key` is not a list, is not of length two or does not
                exclusively contain real numbers.

        """
        if type(param_space[key]) is not list:
            raise TypeError('Please provide a numerical list of length two for [{0:s}]'.format(key))
        else:
            if len(param_space[key]) is not 2:
                raise TypeError('Please provide a numerical list of length two for [{0:s}]'.format(key))
            if not all((isinstance(eelement, numbers.Real) for eelement in param_space[key])):
                raise TypeError('Please provide a numerical list of length two for [{0:s}]'.format(key))
            if param_space[key][0] > param_space[key][1]:
                aux = param_space[key][0]
                param_space[key][0] = param_space[key][1]
                param_space[key][1] = aux
            if param_space[key][0] < bounds[0]:
                if param_space[key][1] < bounds[0]:
                    param_space = self._BaseSearch__validate_set_param_space_with_warning(param_space, key, [bounds[0], bounds[0]])
                else:
                    param_space = self._BaseSearch__validate_set_param_space_with_warning(param_space, key, [bounds[0], param_space[key][1]])
        if param_space[key][0] > bounds[1]:
            param_space = self._BaseSearch__validate_set_param_space_with_warning(param_space, key, [bounds[1], bounds[1]])
        if param_space[key][0] < bounds[0]:
            param_space = self._BaseSearch__validate_set_param_space_with_warning(param_space, key, [bounds[0], bounds[0]])
        if param_space[key][1] > bounds[1]:
            param_space = self._BaseSearch__validate_set_param_space_with_warning(param_space, key, [param_space[key][0], bounds[1]])
        return param_space

    def __validate_param_space_Multirel(self, param_space):
        """Checks whether the hyperparameters provided in `param_space` are
        valid and can be properly handled by the engine using
        :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`. If
        any of them does not match the constraints, it will be
        overwritten and the user will be informed via a warning
        message.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.

        Returns:
            dict:  
                Validated version of `param_space`.

        Raises:
            TypeError: If `param_space` is not a dictionary.
            TypeError: If one of the values in `param_space` validated
                during the function call ` is not a list, is not of
                length two or does not exclusively contain real
                numbers (in
                :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds).

        """
        if type(param_space) is not dict:
            raise TypeError('Provided param_space argument is not a dict!.')
        if 'grid_factor' in param_space.keys():
            bounds = [
             np.finfo(np.float64).resolution, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'grid_factor', bounds)
        if 'max_length' in param_space.keys():
            bounds = [
             0, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'max_length', bounds)
        if 'min_num_samples' in param_space.keys():
            bounds = [
             1, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'min_num_samples', bounds)
        if 'num_features' in param_space.keys():
            bounds = [
             1, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'num_features', bounds)
        if 'regularization' in param_space.keys():
            bounds = [
             0.0, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'regularization', bounds)
        if 'share_aggregations' in param_space.keys():
            bounds = [
             np.finfo(np.float64).resolution, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'share_aggregations', bounds)
        if 'share_selected_features' in param_space.keys():
            bounds = [
             0.0, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'share_selected_features', bounds)
        if 'shrinkage' in param_space.keys():
            bounds = [
             0.0, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'shrinkage', bounds)
        return param_space

    def __validate_param_space_LinearRegression(self, param_space):
        """Checks whether the hyperparameters provided in `param_space` are
        valid and can be properly handled by the engine using
        :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`. If
        any of them does not match the constraints, it will be
        overwritten and the user will be informed via a warning
        message.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.

        Returns:
            dict:  
                Validated version of `param_space`.

        Raises:
            TypeError: If `param_space` is not a dictionary.
            TypeError: If one of the values in `param_space` validated
                during the function call ` is not a list, is not of
                length two or does not exclusively contain real
                numbers (in
                :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`).

        """
        if type(param_space) is not dict:
            raise TypeError('Provided param_space argument is not a dict!.')
        if 'predictor__learning_rate' in param_space.keys():
            bounds = [
             np.finfo(np.float64).resolution, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__learning_rate', bounds)
        if 'predictor__lambda' in param_space.keys():
            bounds = [
             0.0, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__lambda', bounds)
        return param_space

    def __validate_param_space_LogisticRegression(self, param_space):
        """Checks whether the hyperparameters provided in `param_space` are
        valid and can be properly handled by the engine using
        :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`. If
        any of them does not match the constraints, it will be
        overwritten and the user will be informed via a warning
        message.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.

        Returns:
            dict:  
                Validated version of `param_space`.

        Raises:
            TypeError: If `param_space` is not a dictionary.
            TypeError: If one of the values in `param_space` validated
                during the function call ` is not a list, is not of
                length two or does not exclusively contain real
                numbers (in
                :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`).

        """
        if type(param_space) is not dict:
            raise TypeError('Provided param_space argument is not a dict!.')
        if 'predictor__learning_rate' in param_space.keys():
            bounds = [
             np.finfo(np.float64).resolution, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__learning_rate', bounds)
        if 'predictor__lambda' in param_space.keys():
            bounds = [
             0.0, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__lambda', bounds)
        return param_space

    def __validate_param_space_Relboost(self, param_space):
        """Checks whether the parameter space provided in the param_space
        argument are valid and can be properly handled by the
        engine. If any does not match the constrained, it will be
        overwritten.

        """
        if type(param_space) is not dict:
            raise TypeError('Provided param_space argument is not a dict!.')
        if 'max_depth' in param_space.keys():
            bounds = [
             0, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'max_depth', bounds)
        if 'min_num_samples' in param_space.keys():
            bounds = [
             1, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'min_num_samples', bounds)
        if 'num_features' in param_space.keys():
            bounds = [
             1, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'num_features', bounds)
        if 'share_selected_features' in param_space.keys():
            bounds = [
             0.0, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'share_selected_features', bounds)
        if 'reg_lambda' in param_space.keys():
            bounds = [
             0.0, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'reg_lambda', bounds)
        if 'shrinkage' in param_space.keys():
            bounds = [
             0.0, 1.0]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'shrinkage', bounds)
        return param_space

    def __validate_param_space_XGBoost(self, param_space):
        """Checks whether the hyperparameters provided in `param_space` are
        valid and can be properly handled by the engine using
        :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`. If
        any of them does not match the constraints, it will be
        overwritten and the user will be informed via a warning
        message.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.

        Returns:
            dict:  
                Validated version of `param_space`.

        Raises:
            TypeError: If `param_space` is not a dictionary.
            TypeError: If one of the values in `param_space` validated
                during the function call ` is not a list, is not of
                length two or does not exclusively contain real
                numbers (in
                :meth:`~getml.hyperopt._BaseSearch.__validate_ensure_param_space_bounds`).

        """
        if type(param_space) is not dict:
            raise TypeError('Provided param_space argument is not a dict!.')
        if 'predictor__n_estimators' in param_space.keys():
            bounds = [
             10, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__n_estimators', bounds)
        if 'predictor__learning_rate' in param_space.keys():
            bounds = [
             0.0, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__learning_rate', bounds)
        if 'predictor__max_depth' in param_space.keys():
            bounds = [
             1, np.iinfo(np.int32).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__max_depth', bounds)
        if 'predictor__reg_lambda' in param_space.keys():
            bounds = [
             0.0, np.finfo(np.float64).max]
            param_space = self._BaseSearch__validate_ensure_param_space_bounds(param_space, 'predictor__reg_lambda', bounds)
        return param_space

    def __validate_params(self, params):
        """Checks whether the options of the hyperparameter optimization
        provided in `params` are valid and can be properly handled by
        the engine. 

        It does so using
        :meth:`~getml.hyperopt._BaseSearch.__validate_set_params_with_warning`. If
        any does not match the constrained, it will be overwritten and
        the user will be informed via a warning message.

        Args:
            params (dict): Dictionary containing the different options
                to stir the hyperparameter optimization.

        Returns:
            dict:  
                Validated version of `params`.

        Raises:
            TypeError: If `params` is not a dictionary.
            TypeError: If one of the values in `params` does not match
                its associated type.

        """
        if type(params) is not dict:
            raise TypeError('Provided params argument is not a dict!.')
        else:
            if 'n_iter' in params.keys():
                if not isinstance(params['n_iter'], numbers.Real):
                    raise TypeError("Parameter 'n_iter' only supports numerical values!")
                else:
                    if params['n_iter'] < 2:
                        params = self._BaseSearch__validate_set_params_with_warning(params, 'n_iter', 2)
                    else:
                        if 'ratio_iter' in params.keys():
                            if not isinstance(params['ratio_iter'], numbers.Real):
                                raise TypeError("Parameter 'ratio_iter' only supports numerical values!")
                        elif params['ratio_iter'] < 0:
                            params = self._BaseSearch__validate_set_params_with_warning(params, 'ratio_iter', 0)
                        else:
                            if params['ratio_iter'] > 1:
                                params = self._BaseSearch__validate_set_params_with_warning(params, 'ratio_iter', 1)
                            elif 'optimization_algorithm' in params.keys():
                                if type(params['optimization_algorithm']) is not str:
                                    raise TypeError("Parameter 'optimization_algorithm' only supports strings!")
                                if params['optimization_algorithm'] not in ('nelderMead',
                                                                            'bfgs'):
                                    params = self._BaseSearch__validate_set_params_with_warning(params, 'optimization_algorithm', 'nelderMead')
                            if 'optimization_burn_in_algorithm' in params.keys():
                                if type(params['optimization_burn_in_algorithm']) is not str:
                                    raise TypeError("Parameter 'optimization_burn_in_algorithm' only supports strings!")
                                if params['optimization_burn_in_algorithm'] not in ('random',
                                                                                    'latinHypercube'):
                                    params = self._BaseSearch__validate_set_params_with_warning(params, 'optimization_burn_in_algorithm', 'latinHypercube')
                        if 'optimization_burn_ins' in params.keys():
                            if not isinstance(params['optimization_burn_ins'], numbers.Real):
                                raise TypeError("Parameter 'optimization_burn_ins' only supports numerical values!")
                            if params['optimization_burn_ins'] < 1:
                                params = self._BaseSearch__validate_set_params_with_warning(params, 'optimization_burn_ins', 1)
                    if 'surrogate_burn_in_algorithm' in params.keys():
                        if type(params['surrogate_burn_in_algorithm']) is not str:
                            raise TypeError("Parameter 'surrogate_burn_in_algorithm' only supports strings!")
                        if params['surrogate_burn_in_algorithm'] not in ('random',
                                                                         'latinHypercube'):
                            params = self._BaseSearch__validate_set_params_with_warning(params, 'surrogate_burn_in_algorithm', 'latinHypercube')
                if 'gaussian__kernel' in params.keys():
                    if type(params['gaussian__kernel']) is not str:
                        raise TypeError("Parameter 'gaussian__kernel' only supports strings!")
                    if params['gaussian__kernel'] not in ('matern32', 'matern52', 'gauss',
                                                          'exp'):
                        params = self._BaseSearch__validate_set_params_with_warning(params, 'gaussian__kernel', 'matern52')
                        params['gaussian__kernel'] = 'matern52'
            else:
                if 'gaussian__optimization_algorithm' in params.keys():
                    if type(params['gaussian__optimization_burn_in_algorithm']) is not str:
                        raise TypeError("Parameter 'gaussian__optimization_burn_in_algorithm' only supports strings!")
                    if params['gaussian__optimization_algorithm'] not in ('nelderMead',
                                                                          'bfgs'):
                        params = self._BaseSearch__validate_set_params_with_warning(params, 'gaussian__optimization_algorithm', 'nelderMead')
                if 'gaussian__optimization_burn_in_algorithm' in params.keys():
                    if type(params['gaussian__optimization_burn_in_algorithm']) is not str:
                        raise TypeError("Parameter 'gaussian__optimization_burn_in_algorithm' only supports strings!")
                    if params['gaussian__optimization_burn_in_algorithm'] not in ('random',
                                                                                  'latinHypercube'):
                        params = self._BaseSearch__validate_set_params_with_warning(params, 'gaussian__optimization_burn_in_algorithm', 'latinHypercube')
            if 'gaussian__optimization_burn_ins' in params.keys():
                if not isinstance(params['gaussian__optimization_burn_ins'], numbers.Real):
                    raise TypeError("Parameter 'gaussian__optimization_burn_ins' only supports numerical values!")
                if params['gaussian__optimization_burn_ins'] < 1:
                    params = self._BaseSearch__validate_set_params_with_warning(params, 'gaussian__optimization_burn_ins', 1)
        return params

    def __validate_set_param_space_with_warning(self, param_space, key, new_list):
        """Replaces the value corresponding to `key` in `param_space` with
        `new_list` and prints an appropriate warning to the user.

        Note: Only numerical dimensions are supported.

        Args:
            param_space (dict): Dictionary containing lists of length
                two holding the lower and upper bound for all
                hyperparameters to be altered during the
                hyperparameter optimization.
            key (string): Specifies a particular hyperparameter in
                `param_space`.
            new_list (list[numeric]): Numerical list of length 2
                specifying the new lower and upper bound (in that
                order) of a particular hyperparameter determined by
                `key` in `param_space`.

        Returns:
            dict:  
                Updated version of `param_space`.

        """
        warnings.warn('Replacing invalid value [{0:g},{1:g}] in key [{2:s}] with new value [{3:g},{4:g}]'.format(param_space[key][0], param_space[key][1], key, new_list[0], new_list[1]))
        param_space[key] = new_list
        return param_space

    def __validate_set_params_with_warning(self, params, key, new_value):
        """Replaces the value corresponding to `key` in `param_space` with
        `new_value` and prints an appropriate warning to the user.

        Args:
            params (dict): Dictionary containing the different options
                to stir the hyperparameter optimization.
            key (string): Specifies a particular option in `params`.
            new_value: New value for a particular option determined by
                `key` in `params`.

        Returns:
            dict:  
                Updated version of `params`.

        """
        if type(new_value) is str:
            warnings.warn('Replacing invalid value [{0:s}] in key [{1:s}] with new value [{2:s}]'.format(params[key], key, new_value))
        else:
            warnings.warn('Replacing invalid value [{0:g}] in key [{1:s}] with new value [{2:g}]'.format(params[key], key, new_value))
        params[key] = new_value
        return params

    def fit(self, population_table_training, population_table_validation, peripheral_tables, score=None):
        """Launches the hyperparameter optimization.

        The optimization itself will be done by the getML software and
        this function returns immediately after constructing the
        request and checking whether `population_table_training` and
        `population_table_validation` do hold the same column names
        using :meth:`~getml.hyperopt._BaseSearch.__validate_colnames`.
        
        In every iteration of the hyperparameter optimization a new
        set of hyperparameters will be drawn from the `param_space`
        member of the class, those particular parameters will be
        overwritten in the base model and it will be renamed, fitted,
        and scored. How the hyperparameters themselves are drawn
        depends on the particular class of hyperparameter
        optimization.

        The provided :class:`~getml.engine.DataFrame`s
        `population_table_training`, `population_table_validation` and
        `peripheral_tables` must be consistent with the
        :class:`~getml.engine.Placeholders` provided when constructing
        the base model.

        Args:
            population_table_training(:class:`~getml.engine.DataFrame`):
                The population table that models will be trained on.
            population_table_validation(:class:`~getml.engine.DataFrame`):
                The population table that models will be evaluated on.
            peripheral_tables(:class:`~getml.engine.DataFrame`): The
                peripheral tables used to provide additional
                information for the population tables.
            score (string, optional): The score with respect to whom
                the hyperparameters are going to be optimized.
        
                Possible values for a regression problem are:
                - "rmse"
                - "mae"
                - "rsquared" (default)

                Possible values for a classification problem are:
                "cross_entropy" (default), "auc" and "accuracy".
                - "cross entropy" (default)
                - "auc"
                - "accuracy"

        Raises:
            TypeError: If any of `population_table_training`,
                `population_table_validation` or `peripheral_tables`
                is not of type :class:`~getml.engine.DataFrame`.
            TypeError: If the model is neither
                :class:`~getml.models.MultirelModel` nor
                :class:`~getml.models.RelboostModel`.
            Exception: If the value of the 'loss_function' key stored
                in the `params` dictionary of the base model is
                neither :class:`~getml.loss_functions.SquareLoss` or
                :class:`~getml.loss_functions.CrossEntropyLoss`.
            Exception: If either the base model was not transmitted to
                the engine yet - using its
                :class:`~getml.models.MultirelModel.send` method - or
                the later reports back that the operation - starting
                the hyperparameter optimization - was not successful.

        """
        if type(population_table_training) is not engine.DataFrame or type(population_table_validation) is not engine.DataFrame or any((type(pp) is not engine.DataFrame for pp in peripheral_tables)):
            raise TypeError('Only engine.DataFrame are supported by the hyperparameter search!')
        self._BaseSearch__validate_colnames(population_table_training.target_names, population_table_validation.target_names, 'targets')
        self._BaseSearch__validate_colnames(population_table_training.join_key_names, population_table_validation.join_key_names, 'join keys')
        self._BaseSearch__validate_colnames(population_table_training.time_stamp_names, population_table_validation.time_stamp_names, 'time stamps')
        self._BaseSearch__validate_colnames(population_table_training.categorical_names, population_table_validation.categorical_names, 'categorical')
        self._BaseSearch__validate_colnames(population_table_training.numerical_names, population_table_validation.numerical_names, 'numerical')
        self._BaseSearch__validate_colnames(population_table_training.discrete_names, population_table_validation.discrete_names, 'discrete')
        if score is not None:
            if score[(-1)] != '_':
                score += '_'
        if self.model.params['loss_function'] == 'SquareLoss' and not score is None:
            if score not in ('rmse_', 'mae_', 'rsquared_'):
                score = 'rmse_'
        else:
            if self.model.params['loss_function'] == 'CrossEntropyLoss':
                if score is None or score not in ('cross_entropy_', 'auc_', 'accuracy_'):
                    score = 'cross_entropy_'
                else:
                    raise Exception('Unknown loss function')
            else:
                self.params['score'] = score
                cmd = dict()
                if type(self.model) is models.MultirelModel:
                    cmd['type_'] = 'MultirelModel.launch_hyperopt'
                else:
                    if type(self.model) is models.RelboostModel:
                        cmd['type_'] = 'RelboostModel.launch_hyperopt'
                    else:
                        raise TypeError('Unknown model class.')
            cmd['name_'] = self.model.name
            s = comm.send_and_receive_socket(cmd)
            msg = comm.recv_string(s)
            if msg != 'Found!':
                s.close()
                raise Exception(msg)
            cmd['peripheral_names_'] = [df.name for df in peripheral_tables]
            cmd['population_training_name_'] = population_table_training.name
            cmd['population_validation_name_'] = population_table_validation.name
            cmd['session_name_'] = self.session_name
            cmd['param_space_'] = self.param_space
            cmd['params_'] = self.params
            comm.send_string(s, json.dumps(cmd))
            print('Launched hyperparameter optimization...')
            msg = comm.recv_string(s)
            if msg != 'Success!':
                s.close()
                raise Exception(msg)
            s.close()

    def get_models(self):
        """Get a list of all models fitted during the hyperparameter
        optimization.

        Returns:
            list:  
                List of all models fitted during the hyperparameter
                optimization.

        Raises:
            TypeError: If the model is neither
                :class:`~getml.models.MultirelModel` nor
                :class:`~getml.models.RelboostModel`.
            Exception: If the engine yet reports back that the
                operation was not successful.

        """
        cmd = dict()
        if type(self.model) is models.MultirelModel:
            cmd['type_'] = 'MultirelModel.get_hyperopt_names'
        else:
            if type(self.model) is models.RelboostModel:
                cmd['type_'] = 'RelboostModel.get_hyperopt_names'
            else:
                raise TypeError('Unknown model class.')
        cmd['name_'] = self.session_name
        s = comm.send_and_receive_socket(cmd)
        msg = comm.recv_string(s)
        if msg != 'Success!':
            s.close()
            raise Exception(msg)
        names = comm.recv_string(s)
        s.close()
        names = json.loads(names)['names_']
        model_list = [type(self.model)(name=name).refresh() for name in names]
        return model_list

    def get_scores(self):
        """Get a dictionary of the score corresponding to all models fitted
        during the hyperparamer optimization.

        Returns:
            dict: 
                All score fitted during the hyperparameter
                optimization.

        Raises:
            TypeError: If the model is neither
                :class:`~getml.models.MultirelModel` nor
                :class:`~getml.models.RelboostModel`.
            Exception: If the engine yet reports back that the
                operation was not successful.

        """
        cmd = dict()
        if type(self.model) is models.MultirelModel:
            cmd['type_'] = 'MultirelModel.get_hyperopt_scores'
        else:
            if type(self.model) is models.RelboostModel:
                cmd['type_'] = 'RelboostModel.get_hyperopt_scores'
            else:
                raise TypeError('Unknown model class.')
        cmd['name_'] = self.session_name
        s = comm.send_and_receive_socket(cmd)
        msg = comm.recv_string(s)
        if msg != 'Success!':
            s.close()
            raise Exception(msg)
        scores = comm.recv_string(s)
        s.close()
        return json.loads(scores)

    def get_param_space(self):
        """Returns the `param_space` member of the instance.

        Returns:
            dict:  
                Dictionary containing lists of length two holding
                the lower and upper bound for all hyperparameters to
                be altered during the hyperparameter
                optimization.

        """
        return self.param_space

    def get_params(self):
        """Returns the `params` member of the instance.

        Returns:
            params (dict):  
                Dictionary containing the different options
                to stir the hyperparameter optimization.
        """
        return self.params

    def set_param_space(self, param_space=None, **kwargs):
        r"""Sets the parameter space the hyperparameter optimization will take
        place in. Please note that the boundary of the space will also be used
        as a hard boundary during the optimization. Therefore, only parameter
        combination within this space will be feasible.

        To keep a specific hyperparameter fixed, you have two
        options. Either ensure it is neither present in `param_space`
        nor `\*\*kwargs` (but in the base model), or set both the
        lower and upper bound to the same value.

        Args:
            param_space (dict, optional): Dictionary containing lists
                of length two holding the lower and upper bound of all
                hyperparameters which will be altered in the base
                model during the hyperparameter optimization as
                values. If None, the inline input arguments stored in
                `\*\*kwargs` will be used instead. Default is None.
            **kwargs: Alternative way to specify the individual
                key-value pairs of `param_space`. Each of them must be
                a list of length two specifying the lower and upper
                limit of a particular hyperparameter.

        Returns:
            :class:`~getml.hyperopt._BaseSearch`:  
                The current instance
                of the hyperparameter optimization class.

        Raises:
            TypeError: If the predictor is neither
                :class:`~getml.predictors.LinearRegression`,
                :class:`~getml.predictors.LogisticRegression`,
                :class:`~getml.predictors.XGBoostClassifier` nor
                :class:`~getml.predictors.XGBoostRegressor` (in
                :meth:`~getml.hyperopt._BaseSearch.set_param_space`).
            TypeError: If the model is neither
                :class:`~getml.models.MultirelModel` nor
                :class:`~getml.models.RelboostModel`.
            ValueError: If at least one of the keys in `param_space`
                does not exist in the corresponding default space.

        """
        if param_space is None:
            param_space = kwargs
        else:
            if self.model_type is 'Multirel':
                param_space = self._BaseSearch__validate_param_space_Multirel(param_space)
                default_param_space = self._BaseSearch__default_param_space_Multirel()
            else:
                if self.model_type is 'Relboost':
                    param_space = self._BaseSearch__validate_param_space_Relboost(param_space)
                    default_param_space = self._BaseSearch__default_param_space_Relboost()
                else:
                    raise TypeError('Unknown model_type')
            if self.model.params['predictor']['type_'] == 'LinearRegression':
                param_space = self._BaseSearch__validate_param_space_LinearRegression(param_space)
                default_param_space.update(self._BaseSearch__default_param_space_LinearRegression())
            else:
                if self.model.params['predictor']['type_'] == 'LogisticRegression':
                    param_space = self._BaseSearch__validate_param_space_LogisticRegression(param_space)
                    default_param_space.update(self._BaseSearch__default_param_space_LogisticRegression())
                else:
                    if self.model.params['predictor']['type_'] == 'XGBoostPredictor':
                        param_space = self._BaseSearch__validate_param_space_XGBoost(param_space)
                        default_param_space.update(self._BaseSearch__default_param_space_XGBoost())
                    else:
                        raise TypeError('Unknown predictor')
        for key, value in param_space.items():
            if key not in default_param_space.keys():
                raise ValueError('Invalid parameter %s. Please use only the following ones: %s' % (
                 key, default_param_space.keys()))

        self.param_space = param_space
        return self

    def set_params(self, params=None, **kwargs):
        r"""Sets the parameters customizing the hyperparameter
        optimization.

        Args:
            params (dict, optional): Dictionary containing the
                different options to stir the hyperparameter
                optimization. If None, the inline input arguments
                stored in `\*\*kwargs` will be used instead. Default
                is None.
            **kwargs: Alternative way to specify the individual
                key-value pairs of `params`.

        Returns:
            :class:`~getml.hyperopt._BaseSearch`:  
                The current instance
                of the hyperparameter optimization class.

        Raises:
            ValueError: If at least one of the keys in `params`
                does not exist in the corresponding defaults.

        """
        if params is not None:
            params = self._BaseSearch__validate_params(params)
            items = params.items()
        else:
            kwargs = self._BaseSearch__validate_params(kwargs)
            items = kwargs.items()
        valid_params = self.get_params()
        for key, value in items:
            if key[(-1)] == '_':
                key = key[:-1]
            if key not in valid_params:
                raise ValueError('Invalid parameter %s. ' % key)
            self.params[key] = value

        return self


class RandomSearch(_BaseSearch):
    __doc__ = 'Uniformly distributed sampling of the hyperparameters.\n\n    At each iteration a new set of hyperparameters is chosen at random\n    by uniformly drawing a random value in between the lower and upper\n    bound for each dimension of `param_space` independently.\n    \n    Args:\n        model (:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`): \n            Base model used to\n            derive all models fitted and scored during the\n            hyperparameter optimization. Be careful in constructing it\n            since only those parameters present in `param_space` too\n            will be overwritten. It defines the data schema, the loss\n            function and any hyperparameters that are not optimized.\n        param_space (dict): Dictionary containing lists of length two\n            holding the lower and upper bounds of all hyperparameters\n            which will be altered in `model` during the hyperparameter\n            optimization as values. To keep a specific hyperparameter\n            fixed, you have two options. Either ensure it is not\n            present in `param_space` (but in `model`), or set both the\n            lower and upper bound to the same value. If None, the\n            default parameters will be determined for the particular\n            combination of model, predictor, and feature selector\n            using the\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Multirel`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LinearRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LogisticRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Relboost`,\n            or\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_XGBoost`,\n            member functions of this class. Default is None.\n        session_name (string, optional): Prefix which will be used for\n            all models fitted during the hyperparameter\n            optimization. It will also be used as a handle to\n            load/restore the constructed class from data saved in\n            getML. Thus, it has to be unique.\n        n_iter (numeric, optional): Number of hyperparameter\n            combinations to draw and evaluate.\n\n    Raises:\n        Exception: If not predictor is present in the provided\n            `model`.\n        TypeError: If the model is neither\n            :class:`~getml.models.MultirelModel` nor\n            :class:`~getml.models.RelboostModel`.\n        TypeError: If the predictor is neither\n            :class:`~getml.predictors.LinearRegression`,\n            :class:`~getml.predictors.LogisticRegression`,\n            :class:`~getml.predictors.XGBoostClassifier` or\n            :class:`~getml.predictors.XGBoostRegressor` (in\n            :meth:`~getml.hyperopt._BaseSearch.set_param_space`).\n        ValueError: If at least one of the keys in `param_space` does\n            not exist in the corresponding default space (in\n            :meth:`~getml.hyperopt._BaseSearch.set_param_space`).\n\n    '

    def __init__(self, model, param_space, session_name='', n_iter=30):
        super().__init__(model=model,
          param_space=param_space)
        params = dict()
        params['ratio_iter'] = 1
        params['surrogate_burn_in_algorithm'] = 'random'
        params['n_iter'] = n_iter
        self.set_params(params=params)
        if session_name == '':
            self.session_name = datetime.datetime.now().isoformat().split('.')[0].replace(':', '-') + '-hyperopt-random' + '-' + self.model_type.lower()
            self.params['session_name'] = self.session_name
        else:
            self.session_name = session_name
            self.params['session_name'] = session_name


class LatinHypercubeSearch(_BaseSearch):
    __doc__ = 'Latin hypercube sampling of the hyperparameters.\n\n    Uses a multidimensional, uniform cumulative distribution function\n    to drawn the random numbers from. For drawing M samples, the\n    distribution will be divided in hypercubes of equal size. M of\n    them will be selected in such a way only one per dimension is used\n    and an independent and identically-distributed (iid) random number\n    is drawn within the boundaries of the hypercube.\n    \n    Args:\n        model (:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`): \n            Base model used to\n            derive all models fitted and scored during the\n            hyperparameter optimization. Be careful in constructing it\n            since only those parameters present in `param_space` too\n            will be overwritten. It defines the data schema, the loss\n            function and any hyperparameters that are not optimized.\n        param_space (dict): Dictionary containing lists of length two\n            holding the lower and upper bounds of all hyperparameters\n            which will be altered in `model` during the hyperparameter\n            optimization as values. To keep a specific hyperparameter\n            fixed, you have two options. Either ensure it is not\n            present in `param_space` (but in `model`), or set both the\n            lower and upper bound to the same value. If None, the\n            default parameters will be determined for the particular\n            combination of model, predictor, and feature selector\n            using the\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Multirel`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LinearRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LogisticRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Relboost`,\n            or\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_XGBoost`,\n            member functions of this class. Default is None.\n        session_name (string, optional): Prefix which will be used for\n            all models fitted during the hyperparameter\n            optimization. It will also be used as a handle to\n            load/restore the constructed class from data saved in\n            getML. Thus, it has to be unique.\n        n_iter (numeric, optional): Number of hyperparameter\n            combinations to draw and evaluate.\n\n    Raises:\n        Exception: If not predictor is present in the provided\n            `model`.\n        TypeError: If the model is neither\n            :class:`~getml.models.MultirelModel` nor\n            :class:`~getml.models.RelboostModel`.\n        TypeError: If the predictor is neither\n            :class:`~getml.predictors.LinearRegression`,\n            :class:`~getml.predictors.LogisticRegression`,\n            :class:`~getml.predictors.XGBoostClassifier` or\n            :class:`~getml.predictors.XGBoostRegressor` (in\n            :meth:`~getml.hyperopt._BaseSearch.set_param_space`).\n        ValueError: If at least one of the keys in `param_space` does\n            not exist in the corresponding default space (in\n            :meth:`~getml.hyperopt._BaseSearch.set_param_space`).\n\n    '

    def __init__(self, model, param_space, session_name='', n_iter=30):
        super().__init__(model=model,
          param_space=param_space)
        params = dict()
        params['ratio_iter'] = 1
        params['surrogate_burn_in_algorithm'] = 'latinHypercube'
        params['n_iter'] = n_iter
        self.set_params(params=params)
        if session_name == '':
            self.session_name = datetime.datetime.now().isoformat().split('.')[0].replace(':', '-') + '-hyperopt-latin' + '-' + self.model_type.lower()
            self.params['session_name'] = self.session_name
        else:
            self.session_name = session_name
            self.params['session_name'] = session_name


class GaussianHyperparameterSearch(_BaseSearch):
    __doc__ = 'Bayesian hyperparameter optimization using a Gaussian Process.\n\n    Args:\n        model (:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`): \n            Base model used to\n            derive all models fitted and scored during the\n            hyperparameter optimization. Be careful in constructing it\n            since only those parameters present in `param_space` too\n            will be overwritten. It defines the data schema, the loss\n            function and any hyperparameters that are not optimized.\n        param_space (dict): Dictionary containing lists of length two\n            holding the lower and upper bounds of all hyperparameters\n            which will be altered in `model` during the hyperparameter\n            optimization as values. To keep a specific hyperparameter\n            fixed, you have two options. Either ensure it is not\n            present in `param_space` (but in `model`), or set both the\n            lower and upper bound to the same value. If None, the\n            default parameters will be determined for the particular\n            combination of model, predictor, and feature selector\n            using the\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Multirel`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LinearRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_LogisticRegression`,\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_Relboost`,\n            or\n            :meth:`~getml.hyperopt._BaseSearch.__default_param_space_XGBoost`,\n            member functions of this class. Default is None.\n        session_name (string, optional): Prefix which will be used for\n            all models fitted during the hyperparameter\n            optimization. It will also be used as a handle to\n            load/restore the constructed class from data saved in\n            getML. Thus, it has to be unique.\n        n_iter (numeric, optional): Number of hyperparameter\n            combinations to draw and evaluate.\n\n        ratio_iter (numeric, optional): Number of hyperparameter\n            combinations to draw and evaluate.\n\n        optimization_algorithm (string, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n        optimization_burn_in_algorithm (string, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n        optimization_burn_ins (numeric, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n        surrogate_burn_in_algorithm (string, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n        gaussian__kernel (string, optional): Number of hyperparameter\n            combinations to draw and evaluate.\n\n        gaussian__optimization_algorithm (string, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n        gaussian__optimization_burn_in_algorithm (string, optional):\n            Number of hyperparameter combinations to draw and\n            evaluate.\n\n        gaussian__optimization_burn_ins (numeric, optional): Number of\n            hyperparameter combinations to draw and evaluate.\n\n    '

    def __init__(self, model, param_space, session_name='', n_iter=100, ratio_iter=0.75, optimization_algorithm='nelderMead', optimization_burn_in_algorithm='latinHypercube', optimization_burn_ins=15, surrogate_burn_in_algorithm='latinHypercube', gaussian__kernel='matern52', gaussian__optimization_algorithm='nelderMead', gaussian__optimization_burn_in_algorithm='latinHypercube', gaussian__optimization_burn_ins=50):
        super().__init__(model=model,
          param_space=param_space)
        params = dict()
        params['n_iter'] = n_iter
        params['ratio_iter'] = ratio_iter
        params['optimization_algorithm'] = optimization_algorithm
        params['optimization_burn_in_algorithm'] = optimization_burn_in_algorithm
        params['optimization_burn_ins'] = optimization_burn_ins
        params['surrogate_burn_in_algorithm'] = surrogate_burn_in_algorithm
        params['gaussian__kernel'] = gaussian__kernel
        params['gaussian__optimization_algorithm'] = gaussian__optimization_algorithm
        params['gaussian__optimization_burn_in_algorithm'] = gaussian__optimization_burn_in_algorithm
        params['gaussian__optimization_burn_ins'] = gaussian__optimization_burn_ins
        self.set_params(params=params)
        if session_name == '':
            self.session_name = datetime.datetime.now().isoformat().split('.')[0].replace(':', '-') + '-hyperopt-gaussian' + '-' + self.model_type.lower()
            self.params['session_name'] = self.session_name
        else:
            self.session_name = session_name
            self.params['session_name'] = session_name