# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/predictors.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 58395 bytes
"""This module provides ML algorithms to learn and predict on the
generated features.

The predictor classes defined in this module serve two
purposes. First, a predictor can be provided as ``feature_selector``
in :class:`~getml.models.MultirelModel` or
:class:`~getml.models.RelboostModel` to only select the best features
generated during the automated feature engineering and to get rid off
any redundancies. Second, by providing it as a ``predictor``, it will
be trained on the features of the supplied data set and used to
predict to unknown results. Every time a new data set is provided in
the :meth:`~getml.models.MultirelModel.predict` method of one of the
:mod:`~getml.models`, the raw relational data is interpreted in the
data model, which was provided during the construction of the model,
transformed into features using the trained feature engineering
algorithm, and, finally, its :ref:`target<annotating_roles_target>`
will be predicted using the trained predictor.

The provided algorithms can be grouped according to their finesse and
whether you want to use them for a classification or 
regression problem.

.. csv-table::

    "", "simple", "sophisticated"
    "regression", ":class:`~getml.predictors.LinearRegression`", ":class:`~getml.predictors.XGBoostRegressor`"
    "classification", ":class:`~getml.predictors.LogisticRegression`", ":class:`~getml.predictors.XGBoostClassifier`"

Note: 

    All predictors will be trained and called entirely within
    :class:`~getml.models.MultirelModel` and
    :class:`~getml.models.RelboostModel` using their
    :meth:`~getml.models.MultirelModel.fit`,
    :meth:`~getml.models.MultirelModel.score`, and
    :meth:`~getml.models.MultirelModel.predict` methods.
"""
import numpy as np, numbers
from getml.helpers.validation import _check_parameter_bounds

def _validate_linear_model_parameters(parameters):
    """Checks both the types and values of the `parameters` and raises an
    exception is something is off.

    Examples:

        .. code-block:: python

            getml.helpers.validation._validate_linear_model_parameters(
                {'learning_rate': 0.1})

    Args:
        parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.LinearRegression` and
            :class:`~getml.predictors.LogisticRegression`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        Both :class:`~getml.predictors.LinearRegression` and
        :class:`~getml.predictors.LogisticRegression` have an instance
        variable called ``type``, which is not checked in this
        function but in the corresponding
        :meth:`~getml.predictors.LinearRegression.validate` method. If
        it is supplied to this function, it won't cause harm but will
        be ignored instead of checked.
    """
    allowed_parameters = {
     'learning_rate',
     'reg_lambda',
     'type'}
    for kkey in parameters:
        if kkey not in allowed_parameters:
            raise KeyError("'unknown parameter: " + kkey)
        if kkey == 'learning_rate':
            if not isinstance(parameters['learning_rate'], numbers.Real):
                raise TypeError("'learning_rate' must be a real number")
            _check_parameter_bounds(parameters['learning_rate'], 'learning_rate', [
             np.finfo(np.float64).resolution, np.finfo(np.float64).max])
        if kkey == 'reg_lambda':
            if not isinstance(parameters['reg_lambda'], numbers.Real):
                raise TypeError("'reg_lambda' must be a real number")
            _check_parameter_bounds(parameters['reg_lambda'], 'reg_lambda', [
             0.0, np.finfo(np.float64).max])


def _validate_xgboost_parameters(parameters):
    """Checks both the types and values of the `parameters` and raises an
    exception is something is off.

    Examples:

        .. code-block:: python

            getml.helpers.validation.validate_XGBoost_parameters(
                {'learning_rate': 0.1, 'gamma': 3.2})

    Args:
        parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.XGBoostRegressor` and
            :class:`~getml.predictors.XGBoostClassifier`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        Both :class:`~getml.predictors.XGBoostRegressor` and
        :class:`~getml.predictors.XGBoostClassifier` have an instance
        variable called ``type``, which is not checked in this
        function but in the corresponding
        :meth:`~getml.predictors.XGBoostRegressor.validate` method. If
        it is supplied to this function, it won't cause harm but will
        be ignored instead of checked.
    """
    allowed_parameters = {
     'booster',
     'colsample_bylevel',
     'colsample_bytree',
     'gamma',
     'learning_rate',
     'max_delta_step',
     'max_depth',
     'min_child_weights',
     'n_estimators',
     'n_jobs',
     'normalize_type',
     'num_parallel_tree',
     'objective',
     'one_drop',
     'rate_drop',
     'reg_alpha',
     'reg_lambda',
     'sample_type',
     'silent',
     'skip_drop',
     'subsample',
     'type'}
    for kkey in parameters:
        if kkey not in allowed_parameters:
            raise KeyError("'unknown XGBoost parameter: " + kkey)
        else:
            if kkey == 'booster':
                if type(parameters['booster']) is not str:
                    raise TypeError("'booster' must be of type str")
                else:
                    if parameters['booster'] not in ('gbtree', 'gblinear', 'dart'):
                        raise ValueError("'booster' must either be 'gbtree', 'gblinear', or 'dart'")
                    else:
                        if kkey == 'colsample_bylevel':
                            if not isinstance(parameters['colsample_bylevel'], numbers.Real):
                                raise TypeError("'colsample_bylevel' must be a real number")
                            _check_parameter_bounds(parameters['colsample_bylevel'], 'colsample_bylevel', [
                             np.finfo(np.float64).resolution, 1.0])
                        elif kkey == 'colsample_bytree':
                            if not isinstance(parameters['colsample_bytree'], numbers.Real):
                                raise TypeError("'colsample_bytree' must be a real number")
                            _check_parameter_bounds(parameters['colsample_bytree'], 'colsample_bytree', [
                             np.finfo(np.float64).resolution, 1.0])
                        elif kkey == 'gamma':
                            if not isinstance(parameters['gamma'], numbers.Real):
                                raise TypeError("'gamma' must be a real number")
                            _check_parameter_bounds(parameters['gamma'], 'gamma', [
                             0.0, np.finfo(np.float64).max])
                        else:
                            if kkey == 'learning_rate':
                                if not isinstance(parameters['learning_rate'], numbers.Real):
                                    raise TypeError("'learning_rate' must be a real number")
                                _check_parameter_bounds(parameters['learning_rate'], 'learning_rate', [
                                 0.0, 1.0])
                            if kkey == 'max_delta_step':
                                if not isinstance(parameters['max_delta_step'], numbers.Real):
                                    raise TypeError("'max_delta_step' must be a real number")
                                _check_parameter_bounds(parameters['max_delta_step'], 'max_delta_step', [
                                 0.0, np.finfo(np.float64).max])
                            if kkey == 'max_depth':
                                if not isinstance(parameters['max_depth'], numbers.Real):
                                    raise TypeError("'max_depth' must be a real number")
                                _check_parameter_bounds(parameters['max_depth'], 'max_depth', [
                                 0.0, np.iinfo(np.int32).max])
                            if kkey == 'min_child_weights':
                                if not isinstance(parameters['min_child_weights'], numbers.Real):
                                    raise TypeError("'min_child_weights' must be a real number")
                                _check_parameter_bounds(parameters['min_child_weights'], 'min_child_weights', [
                                 0.0, np.finfo(np.float64).max])
                            if kkey == 'n_estimators':
                                if not isinstance(parameters['n_estimators'], numbers.Real):
                                    raise TypeError("'n_estimators' must be a real number")
                                _check_parameter_bounds(parameters['n_estimators'], 'n_estimators', [
                                 10, np.iinfo(np.int32).max])
                            if kkey == 'normalize_type':
                                if type(parameters['normalize_type']) is not str:
                                    raise TypeError("'normalize_type' must be of type str")
                                if 'booster' in parameters and parameters['booster'] == 'dart' and parameters['normalize_type'] is ['forest', 'tree']:
                                    raise ValueError("'normalize_type' must either be 'forest' or 'tree'")
                        if kkey == 'num_parallel_tree':
                            if not isinstance(parameters['num_parallel_tree'], numbers.Real):
                                raise TypeError("'num_parallel_tree' must be a real number")
                            _check_parameter_bounds(parameters['num_parallel_tree'], 'num_parallel_tree', [
                             1, np.iinfo(np.int32).max])
                        if kkey == 'n_jobs':
                            if not isinstance(parameters['n_jobs'], numbers.Real):
                                raise TypeError("'n_jobs' must be a real number")
                            _check_parameter_bounds(parameters['n_jobs'], 'n_jobs', [
                             1, np.iinfo(np.int32).max])
                        if kkey == 'objective':
                            if type(parameters['objective']) is not str:
                                raise TypeError("'objective' must be of type str")
                            if parameters['objective'] not in ('reg:squarederror',
                                                               'reg:tweedie', 'reg:linear',
                                                               'reg:logistic', 'binary:logistic',
                                                               'binary:logitraw'):
                                raise ValueError("'objective' must either be 'reg:squarederror', 'reg:tweedie', 'reg:linear', 'reg:logistic', 'binary:logistic', or 'binary:logitraw'")
                    if kkey == 'one_drop' and type(parameters['one_drop']) is not bool:
                        raise TypeError("'one_drop' must be a bool")
                if kkey == 'rate_drop':
                    if not isinstance(parameters['rate_drop'], numbers.Real):
                        raise TypeError("'rate_drop' must be a real number")
                    _check_parameter_bounds(parameters['rate_drop'], 'rate_drop', [
                     0.0, 1.0])
                if kkey == 'reg_alpha':
                    if not isinstance(parameters['reg_alpha'], numbers.Real):
                        raise TypeError("'reg_alpha' must be a real number")
                    _check_parameter_bounds(parameters['reg_alpha'], 'reg_alpha', [
                     0.0, np.finfo(np.float64).max])
                if kkey == 'reg_lambda':
                    if not isinstance(parameters['reg_lambda'], numbers.Real):
                        raise TypeError("'reg_lambda' must be a real number")
                    _check_parameter_bounds(parameters['reg_lambda'], 'reg_lambda', [
                     0.0, np.finfo(np.float64).max])
            elif kkey == 'sample_type':
                if type(parameters['sample_type']) is not str:
                    raise TypeError("'sample_type' must be of type str")
                if 'booster' in parameters and parameters['booster'] == 'dart':
                    if parameters['sample_type'] not in ('uniform', 'weighted'):
                        raise ValueError("'sample_type' must either be 'uniform' or 'weighted'")
            if kkey == 'silent' and type(parameters['silent']) is not bool:
                raise TypeError("'silent' must be of type bool")
        if kkey == 'skip_drop':
            if not isinstance(parameters['skip_drop'], numbers.Real):
                raise TypeError("'skip_drop' must be a real number")
            _check_parameter_bounds(parameters['skip_drop'], 'skip_drop', [
             0.0, 1.0])
        if kkey == 'subsample':
            if not isinstance(parameters['subsample'], numbers.Real):
                raise TypeError("'subsample' must be a real number")
            _check_parameter_bounds(parameters['subsample'], 'subsample', [
             np.finfo(np.float64).resolution, 1.0])


class _Predictor(object):
    __doc__ = '\n    Base class. Should not ever be directly initialized!\n    '

    def __eq__(self, other):
        """Compares the current instance with another one.

        Raises:
            TypeError: If `other` is not a predictor function.

        Returns:
            bool: Indicating whether the current instance and `other`
                are the same.
        """
        if not isinstance(other, _Predictor):
            raise TypeError('A predictor can only compared to another predictor!')
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False
        for kkey in self.__dict__:
            if kkey not in other.__dict__:
                return False
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False
                elif self.__dict__[kkey] != other.__dict__[kkey]:
                    return False

        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = ''
        indent1 = '  '
        for kkey, vvalue in self.__dict__.items():
            result += '\n' + indent1 + kkey + ': ' + str(vvalue)

        return result

    def _getml_deserialize(self):
        encodingDict = dict()
        for kkey in self.__dict__:
            encodingDict[kkey + '_'] = self.__dict__[kkey]

        anotherEncodingDict = dict()
        if self.type == 'LinearRegression' or self.type == 'LogisticRegression':
            for kkey in encodingDict:
                if kkey == 'reg_lambda_':
                    anotherEncodingDict['lambda_'] = encodingDict[kkey]
                else:
                    anotherEncodingDict[kkey] = encodingDict[kkey]

        else:
            anotherEncodingDict = encodingDict
        return anotherEncodingDict


class LinearRegression(_Predictor):
    __doc__ = 'Simple predictor for regression problems.\n    \n    Learns a simple linear relationship using ordinary least squares (OLS)\n    regression:\n\n    .. math::\n\n        \\hat{y} = w_0 + w_1 * feature_1 + w_2 * feature_2 + ... \n\n    The weights are optimized by minimizing the squared loss of the\n    predictions :math:`\\hat{y}` w.r.t. the :ref:`targets\n    <annotating_roles_target>` :math:`y`.\n\n    .. math::\n\n        L(y,\\hat{y}) = \\frac{1}{n} \\sum_{i=1}^{n} (y_i -\\hat{y}_i)^2\n    \n    Linear regressions can be trained arithmetically or numerically.\n    Training arithmetically is more accurate, but suffers worse\n    scalability.\n\n    If you decide to pass :ref:`categorical\n    features<annotating_roles_categorical>` to the\n    :class:`~getml.predictors.LinearRegression`, it will be trained\n    numerically. Otherwise, it will be trained arithmetically.\n\n    Args:\n\n        learning_rate (float, optional):\n\n            The learning rate used for training numerically (only\n            relevant when categorical features are included). Range:\n            (0, :math:`\\infty`]\n\n        reg_lambda (float, optional):\n\n            L2 regularization parameter. Range: [0, :math:`\\infty`]\n\n    Raises:\n        TypeError: If any of the input arguments does not match its \n            expected type.\n\n    Note:\n\n        This class will be trained using the\n        :meth:`~getml.models.MultirelModel.fit` method and used for\n        prediction using the\n        :meth:`~getml.models.MultirelModel.predict` method of either\n        :class:`~getml.models.MultirelModel` or\n        :class:`~getml.models.RelboostModel`.\n\n    '

    def __init__(self, learning_rate=0.9, reg_lambda=1e-10):
        self.type = 'LinearRegression'
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate
        self.validate()

    def __str__(self):
        result = 'LinearRegression:' + super(LinearRegression, self).__str__()
        return result

    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:
            
            .. code-block:: python

                l = getml.predictors.LinearRegression()
                l.learning_rate = 8.1
                l.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """
        _validate_linear_model_parameters(self.__dict__)


class LogisticRegression(_Predictor):
    __doc__ = 'Simple predictor for classification problems.\n\n    Learns a simple linear relationship using the sigmoid function:\n\n    .. math::\n\n        \\hat{y} = \\sigma(w_0 + w_1 * feature_1 + w_2 * feature_2 + ...)\n\n    :math:`\\sigma` denotes the sigmoid function:  \n\n    .. math::\n\n        \\sigma(z) = \\frac{1}{1 + exp(-z)}\n    \n    The weights are optimized by minimizing the cross entropy loss of\n    the predictions :math:`\\hat{y}` w.r.t. the :ref:`targets\n    <annotating_roles_target>` :math:`y`.\n\n    .. math::\n\n        L(\\hat{y},y) = - y*\\log \\hat{y} - (1 - y)*\\log(1 - \\hat{y})\n    \n    Logistic regressions are always trained numerically. \n\n    If you decide to pass :ref:`categorical\n    features<annotating_roles_categorical>` to the\n    :class:`~getml.predictors.LogisticRegression`, it will be trained\n    using the Broyden-Fletcher-Goldfarb-Shannon (BFGS) algorithm.\n    Otherwise, it will be trained using adaptive moments (Adam). BFGS\n    is more accurate, but less scalable than Adam.\n\n    Args:\n\n        learning_rate (float, optional):\n\n            The learning rate used for the Adaptive Moments algorithm\n            (only relevant when categorical features are\n            included). Range: (0, :math:`\\infty`]\n\n        reg_lambda (float, optional):\n\n            L2 regularization parameter. Range: [0, :math:`\\infty`]\n\n    Raises:\n        TypeError: If any of the input arguments does not match its \n            expected type.\n\n    Note:\n\n        This class will be trained using the\n        :meth:`~getml.models.MultirelModel.fit` method and used for\n        prediction using the\n        :meth:`~getml.models.MultirelModel.predict` method of either\n        :class:`~getml.models.MultirelModel` or\n        :class:`~getml.models.RelboostModel`.\n    '

    def __init__(self, learning_rate=0.9, reg_lambda=1e-10):
        self.type = 'LogisticRegression'
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate
        self.validate()

    def __str__(self):
        result = 'LogisticRegression:' + super(LogisticRegression, self).__str__()
        return result

    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:
            
            .. code-block:: python

                l = getml.predictors.LogisticRegression()
                l.learning_rate = 20
                l.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """
        _validate_linear_model_parameters(self.__dict__)
        if self.type != 'LogisticRegression':
            raise ValueError("'type' must be 'LogisticRegression'")


class XGBoostClassifier(_Predictor):
    __doc__ = "Gradient boosting classifier based on \n    `xgboost <https://xgboost.readthedocs.io/en/latest/>`_.\n    \n    XGBoost is an implementation of the gradient tree boosting algorithm that\n    is widely recognized for its efficiency and predictive accuracy.\n\n    Gradient tree boosting trains an ensemble of decision trees by training \n    each tree to predict the *prediction error of all previous trees* in the \n    ensemble:\n    \n    .. math::\n\n        \\min_{\\nabla f_{t,i}} \\sum_i L(f_{t-1,i} + \\nabla f_{t,i}; y_i),     \n\n    where :math:`\\nabla f_{t,i}` is the prediction generated by the\n    newest decision tree for sample :math:`i` and :math:`f_{t-1,i}` is\n    the prediction generated by all previous trees, :math:`L(...)` is\n    the loss function used and :math:`y_i` is the :ref:`target\n    <annotating_roles_target>` we are trying to predict.\n    \n    XGBoost implements this general approach by adding two specific components:\n\n    1. The loss function :math:`L(...)` is approximated using a Taylor series. \n\n    2. The leaves of the decision tree :math:`\\nabla f_{t,i}` contain weights \n       that can be regularized. \n\n    These weights are calculated as follows:\n\n    .. math::\n    \n        w_l = -\\frac{\\sum_{i \\in l} g_i}{ \\sum_{i \\in l} h_i + \\lambda},\n    \n    where :math:`g_i` and :math:`h_i` are the first and second order derivative\n    of :math:`L(...)` w.r.t. :math:`f_{t-1,i}`, :math:`w_l` denotes the weight \n    on leaf :math:`l` and :math:`i \\in l` denotes all samples on that leaf.\n\n    :math:`\\lambda` is the regularization parameter `reg_lambda`. \n    This hyperparameter can be set by the users or the hyperparameter\n    optimization algorithm to avoid overfitting.\n     \n    Args:\n        booster (string, optional):\n\n            Which base classifier to use. \n\n            Possible values: \n\n            * 'gbtree': normal gradient boosted decision trees\n            * 'gblinear': uses a linear model instead of decision trees\n            * 'dart': adds dropout to the standard gradient boosting algorithm.\n              Please also refer to the remarks on *rate_drop* for further \n              explanation on 'dart'.\n\n        colsample_bylevel (float, optional):\n\n            Subsample ratio for the columns used, for each level\n            inside a tree. \n            \n            Note that XGBoost grows its trees level-by-level, not \n            node-by-node.\n            At each level, a subselection of the features will be randomly \n            picked and the best \n            feature for each split will be chosen. This hyperparameter \n            determines the share of features randomly picked at each level. \n            When set to 1, then now such sampling takes place.\n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n\n        colsample_bytree (float, optional):\n\n            Subsample ratio for the columns used, for each tree. \n            This means that for each tree, a subselection\n            of the features will be randomly chosen. This hyperparameter \n            determines the share of features randomly picked for each tree.\n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n        \n        gamma (float, optional):\n\n            Minimum loss reduction required for any update \n            to the tree. This means that every potential update \n            will first be evaluated for its improvement to the loss \n            function. If the improvement exceeds gamma,\n            the update will be accepted.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        learning_rate (float, optional):\n\n            Learning rate for the gradient boosting algorithm.\n            When a new tree :math:`\\nabla f_{t,i}` is trained,\n            it will be added to the existing trees  \n            :math:`f_{t-1,i}`. Before doing so, it will be \n            multiplied by the *learning_rate*.  \n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, 1]\n\n        max_delta_step (float, optional):\n\n            The maximum delta step allowed for the weight estimation\n            of each tree. \n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`)\n\n        max_depth (int, optional):\n        \n            Maximum allowed depth of the trees. \n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        min_child_weights (float, optional):\n\n            Minimum sum of weights needed in each child node for a\n            split. The idea here is that any leaf should have \n            a minimum number of samples in order to avoid overfitting.\n            This very common form of regularizing decision trees is \n            slightly\n            modified to refer to weights instead of number of samples,\n            but the basic idea is the same.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        n_estimators (int, optional):\n\n            Number of estimators (trees).\n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [10, :math:`\\infty`]\n\n        normalize_type (string, optional):\n\n            This determines how to normalize trees during 'dart'.\n\n            Possible values:\n\n            * 'tree': a new tree has the same weight as a single\n              dropped tree.\n\n            * 'forest': a new tree has the same weight as a the sum of\n              all dropped trees.\n\n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n        n_jobs (int, optional):\n\n            Number of parallel threads. \n            \n            Range: [1, :math:`\\infty`]\n\n        objective (string, optional):\n\n            Specify the learning task and the corresponding\n            learning objective.\n\n            Possible values:\n\n            * 'reg:logistic'\n            * 'binary:logistic'\n            * 'binary:logitraw'\n\n        one_drop (bool, optional):\n\n            If set to True, then at least one tree will always be\n            dropped out. Setting this hyperparameter to *true* reduces \n            the likelihood of overfitting. \n            \n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n\n            Will be ignored if `booster` is not set to 'dart'.\n\n        rate_drop (float, optional):\n\n            Dropout rate for trees - determines the probability\n            that a tree will be dropped out. Dropout is an \n            algorithm that enjoys considerable popularity in\n            the deep learning community. It means that every node can \n            be randomly removed during training. \n            \n            This approach\n            can also be applied to gradient boosting, where it \n            means that every tree can be randomly removed with \n            a certain probability. Said probability is determined\n            by *rate_drop*. Dropout for gradient boosting is \n            referred to as the 'dart' algorithm.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n        reg_alpha(float, optional):\n\n            L1 regularization on the weights.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        reg_lambda (float, optional):\n\n            L2 regularization on the weights. Please refer to \n            the introductory remarks to understand how this\n            hyperparameter influences your weights.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        sample_type (string, optional):\n\n            Possible values:\n\n            * 'uniform': every tree is equally likely to be dropped\n              out\n\n            * 'weighted': the dropout probability will be proportional\n              to a tree's weight\n            \n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n\n            Will be ignored if `booster` is not set to 'dart'.\n\n        silent (bool, optional):\n\n            In silent mode, XGBoost will not print out information on\n            the training progress.\n\n        skip_drop (float, optional):\n\n            Probability of skipping the dropout during a given\n            iteration. Please also refer to the remarks on \n            *rate_drop* for further explanation.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n            Range: [0, 1]\n        \n        subsample (float, optional):\n\n            Subsample ratio from the training set. This means\n            that for every tree a subselection of *samples*\n            from the training set will be included into training.\n            Please note that this samples *without* replacement -\n            the common approach for random forests is to sample \n            *with* replace.\n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n\n    Raises:\n        TypeError: If any of the input arguments does not match its \n            expected type.\n\n    Note:\n\n        This class will be trained using the\n        :meth:`~getml.models.MultirelModel.fit` method and used for\n        prediction using the\n        :meth:`~getml.models.MultirelModel.predict` method of either\n        :class:`~getml.models.MultirelModel` or\n        :class:`~getml.models.RelboostModel`.\n\n    "

    def __init__(self, booster='gbtree', colsample_bylevel=1.0, colsample_bytree=1.0, gamma=0.0, learning_rate=0.1, max_delta_step=0.0, max_depth=3, min_child_weights=1.0, n_estimators=100, normalize_type='tree', num_parallel_tree=1, n_jobs=1, objective='binary:logistic', one_drop=False, rate_drop=0.0, reg_alpha=0.0, reg_lambda=1.0, sample_type='uniform', silent=True, skip_drop=0.0, subsample=1.0):
        self.type = 'XGBoostClassifier'
        self.booster = booster
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bytree = colsample_bytree
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.max_delta_step = max_delta_step
        self.max_depth = max_depth
        self.min_child_weights = min_child_weights
        self.n_estimators = n_estimators
        self.normalize_type = normalize_type
        self.num_parallel_tree = num_parallel_tree
        self.n_jobs = n_jobs
        self.objective = objective
        self.one_drop = one_drop
        self.rate_drop = rate_drop
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.sample_type = sample_type
        self.silent = silent
        self.skip_drop = skip_drop
        self.subsample = subsample
        self.validate()

    def __str__(self):
        result = 'XGBoostClassifier:' + super(XGBoostClassifier, self).__str__()
        return result

    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:
            
            .. code-block:: python

                x = getml.predictors.XGBoostClassifier()
                x.gamma = 200
                x.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """
        _validate_xgboost_parameters(self.__dict__)
        if self.type != 'XGBoostClassifier':
            raise ValueError("'type' must be 'XGBoostClassifier'")
        if self.objective not in ('reg:logistic', 'binary:logistic', 'binary:logitraw'):
            raise ValueError("'objective' supported in XGBoostClassifier are 'reg:logistic', 'binary:logistic', and 'binary:logitraw'")


class XGBoostRegressor(_Predictor):
    __doc__ = "Gradient boosting regressor based on `xgboost <https://xgboost.readthedocs.io/en/latest/>`_.\n\n    XGBoost is an implementation of the gradient tree boosting algorithm that\n    is widely recognized for its efficiency and predictive accuracy.\n\n    Gradient tree boosting trains an ensemble of decision trees by training \n    each tree to predict the *prediction error of all previous trees* in the \n    ensemble:\n    \n    .. math::\n\n        \\min_{\\nabla f_{t,i}} \\sum_i L(f_{t-1,i} + \\nabla f_{t,i}; y_i),     \n\n    where :math:`\\nabla f_{t,i}` is the prediction generated by the\n    newest decision tree for sample :math:`i` and :math:`f_{t-1,i}` is\n    the prediction generated by all previous trees, :math:`L(...)` is\n    the loss function used and :math:`y_i` is the :ref:`target\n    <annotating_roles_target>` we are trying to predict.\n    \n    XGBoost implements this general approach by adding two specific components:\n\n    1. The loss function :math:`L(...)` is approximated using a Taylor series. \n\n    2. The leaves of the decision tree :math:`\\nabla f_{t,i}` contain weights \n       that can be regularized. \n\n    These weights are calculated as follows:\n\n    .. math::\n    \n        w_l = -\\frac{\\sum_{i \\in l} g_i}{ \\sum_{i \\in l} h_i + \\lambda},\n    \n    where :math:`g_i` and :math:`h_i` are the first and second order derivative\n    of :math:`L(...)` w.r.t. :math:`f_{t-1,i}`, :math:`w_l` denotes the weight \n    on leaf :math:`l` and :math:`i \\in l` denotes all samples on that leaf.\n\n    :math:`\\lambda` is the regularization parameter `reg_lambda`. \n    This hyperparameter can be set by the users or the hyperparameter\n    optimization algorithm to avoid overfitting.\n     \n    Args:\n        booster (string, optional):\n\n            Which base classifier to use. \n\n            Possible values: \n\n            * 'gbtree': normal gradient boosted decision trees\n            * 'gblinear': uses a linear model instead of decision trees\n            * 'dart': adds dropout to the standard gradient boosting algorithm.\n              Please also refer to the remarks on *rate_drop* for further \n              explanation on 'dart'.\n\n        colsample_bylevel (float, optional):\n\n            Subsample ratio for the columns used, for each level\n            inside a tree. \n            \n            Note that XGBoost grows its trees level-by-level, not \n            node-by-node.\n            At each level, a subselection of the features will be randomly \n            picked and the best \n            feature for each split will be chosen. This hyperparameter \n            determines the share of features randomly picked at each level. \n            When set to 1, then now such sampling takes place.\n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n\n        colsample_bytree (float, optional):\n\n            Subsample ratio for the columns used, for each tree. \n            This means that for each tree, a subselection\n            of the features will be randomly chosen. This hyperparameter \n            determines the share of features randomly picked for each tree.\n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n        \n        gamma (float, optional):\n\n            Minimum loss reduction required for any update \n            to the tree. This means that every potential update \n            will first be evaluated for its improvement to the loss \n            function. If the improvement exceeds gamma,\n            the update will be accepted.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        learning_rate (float, optional):\n\n            Learning rate for the gradient boosting algorithm.\n            When a new tree :math:`\\nabla f_{t,i}` is trained,\n            it will be added to the existing trees  \n            :math:`f_{t-1,i}`. Before doing so, it will be \n            multiplied by the *learning_rate*.  \n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, 1]\n\n        max_delta_step (float, optional):\n\n            The maximum delta step allowed for the weight estimation\n            of each tree. \n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`)\n\n        max_depth (int, optional):\n        \n            Maximum allowed depth of the trees. \n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        min_child_weights (float, optional):\n\n            Minimum sum of weights needed in each child node for a\n            split. The idea here is that any leaf should have \n            a minimum number of samples in order to avoid overfitting.\n            This very common form of regularizing decision trees is \n            slightly\n            modified to refer to weights instead of number of samples,\n            but the basic idea is the same.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        n_estimators (int, optional):\n\n            Number of estimators (trees).\n\n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [10, :math:`\\infty`]\n\n        normalize_type (string, optional):\n\n            This determines how to normalize trees during 'dart'.\n\n            Possible values:\n\n            * 'tree': a new tree has the same weight as a single\n              dropped tree.\n\n            * 'forest': a new tree has the same weight as a the sum of\n              all dropped trees.\n\n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n        n_jobs (int, optional):\n\n            Number of parallel threads. \n            \n            Range: [1, :math:`\\infty`]\n\n        objective (string, optional):\n\n            Specify the learning task and the corresponding\n            learning objective.\n\n            Possible values:\n\n            * 'reg:squarederror'\n            * 'reg:tweedie'\n\n        one_drop (bool, optional):\n\n            If set to True, then at least one tree will always be\n            dropped out. Setting this hyperparameter to *true* reduces \n            the likelihood of overfitting. \n            \n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n\n            Will be ignored if `booster` is not set to 'dart'.\n\n        rate_drop (float, optional):\n\n            Dropout rate for trees - determines the probability\n            that a tree will be dropped out. Dropout is an \n            algorithm that enjoys considerable popularity in\n            the deep learning community. It means that every node can \n            be randomly removed during training. \n            \n            This approach\n            can also be applied to gradient boosting, where it \n            means that every tree can be randomly removed with \n            a certain probability. Said probability is determined\n            by *rate_drop*. Dropout for gradient boosting is \n            referred to as the 'dart' algorithm.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n        reg_alpha(float, optional):\n\n            L1 regularization on the weights.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        reg_lambda (float, optional):\n\n            L2 regularization on the weights. Please refer to \n            the introductory remarks to understand how this\n            hyperparameter influences your weights.\n\n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: [0, :math:`\\infty`]\n\n        sample_type (string, optional):\n\n            Possible values:\n\n            * 'uniform': every tree is equally likely to be dropped\n              out\n\n            * 'weighted': the dropout probability will be proportional\n              to a tree's weight\n            \n            Please also refer to the remarks on \n            *rate_drop* for further explanation.\n\n            Will be ignored if `booster` is not set to 'dart'.\n\n        silent (bool, optional):\n\n            In silent mode, XGBoost will not print out information on\n            the training progress.\n\n        skip_drop (float, optional):\n\n            Probability of skipping the dropout during a given\n            iteration. Please also refer to the remarks on \n            *rate_drop* for further explanation.\n            \n            *Increasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Will be ignored if `booster` is not set to 'dart'.\n\n            Range: [0, 1]\n        \n        subsample (float, optional):\n\n            Subsample ratio from the training set. This means\n            that for every tree a subselection of *samples*\n            from the training set will be included into training.\n            Please note that this samples *without* replacement -\n            the common approach for random forests is to sample \n            *with* replace.\n            \n            *Decreasing* this hyperparameter reduces the \n            likelihood of overfitting. \n            \n            Range: (0, 1]\n\n    Raises:\n        TypeError: If any of the input arguments does not match its \n            expected type.\n\n    Note:\n\n        This class will be trained using the\n        :meth:`~getml.models.MultirelModel.fit` method and used for\n        prediction using the\n        :meth:`~getml.models.MultirelModel.predict` method of either\n        :class:`~getml.models.MultirelModel` or\n        :class:`~getml.models.RelboostModel`.\n\n    "

    def __init__(self, booster='gbtree', colsample_bylevel=1.0, colsample_bytree=1.0, gamma=0.0, learning_rate=0.1, max_delta_step=0.0, max_depth=3, min_child_weights=1.0, n_estimators=100, normalize_type='tree', num_parallel_tree=1, n_jobs=1, objective='reg:squarederror', one_drop=False, rate_drop=0.0, reg_alpha=0.0, reg_lambda=1.0, silent=True, sample_type='uniform', skip_drop=0.0, subsample=1.0):
        self.type = 'XGBoostRegressor'
        self.booster = booster
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bytree = colsample_bytree
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.max_delta_step = max_delta_step
        self.max_depth = max_depth
        self.min_child_weights = min_child_weights
        self.n_estimators = n_estimators
        self.normalize_type = normalize_type
        self.num_parallel_tree = num_parallel_tree
        self.n_jobs = n_jobs
        self.objective = objective
        self.one_drop = one_drop
        self.rate_drop = rate_drop
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.sample_type = sample_type
        self.silent = silent
        self.skip_drop = skip_drop
        self.subsample = subsample
        self.validate()

    def __str__(self):
        result = 'XGBoostRegressor:' + super(XGBoostRegressor, self).__str__()
        return result

    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:
            
            .. code-block:: python

                x = getml.predictors.XGBoostRegressor()
                x.gamma = 200
                x.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """
        _validate_xgboost_parameters(self.__dict__)
        if self.type != 'XGBoostRegressor':
            raise ValueError("'type' must be 'XGBoostRegressor'")
        if self.objective not in ('reg:squarederror', 'reg:tweedie', 'reg:linear'):
            raise ValueError("'objective' supported in XGBoostRegressor are 'reg:squarederror', 'reg:tweedie', and 'reg:linear'")


def _decode_predictor(rawDict):
    """A custom decoder function for :mod:`~getml.predictors`.

    Args:
        rawDict (dict): dict naively deserialized from JSON msg.

    Raises:
        KeyError: If the ``type`` key in `rawDict` is either not present
            or of unknown type.
        ValueError: If not all keys in `rawDict` have a trailing
            underscore.
        TypeError: If `rawDict` is not of type :py:class:`dict`.

    Returns: Either :class:`~getml.predictors.LinearRegression`,
        :class:`~getml.predictors.LogisticRegression`,
        :class:`~getml.predictors.XGBoostRegressor`, or
        :class:`~getml.predictors.XGBoostClassifier`.

    Examples:

        Create a :class:`~getml.predictors.LinearRegression`,
        serialize it, and deserialize it again.

        .. code-block:: python

            p = getml.predictors.LinearRegression()
            p_serialized = json.dumps(p, cls = getml.communication._GetmlEncoder)
            p2 = json.loads(p_serialized, object_hook = getml.helpers.predictors._decode_predictor)
            p == p2

    """
    if type(rawDict) is not dict:
        raise TypeError('_decode_predictor is expecting a dict as input')
    else:
        decodingDict = dict()
        for kkey in rawDict:
            if kkey[(len(kkey) - 1)] != '_':
                ValueError('All keys in the JSON must have a trailing underscore.')
            decodingDict[kkey[:len(kkey) - 1]] = rawDict[kkey]

        if 'type' in decodingDict:
            if decodingDict['type'] == 'LinearRegression':
                del decodingDict['type']
                anotherDecodingDict = dict()
                for kkey in decodingDict:
                    if kkey == 'lambda':
                        anotherDecodingDict['reg_lambda'] = decodingDict[kkey]
                    else:
                        anotherDecodingDict[kkey] = decodingDict[kkey]

                return LinearRegression(**anotherDecodingDict)
            if decodingDict['type'] == 'LogisticRegression':
                del decodingDict['type']
                anotherDecodingDict = dict()
                for kkey in decodingDict:
                    if kkey == 'lambda':
                        anotherDecodingDict['reg_lambda'] = decodingDict[kkey]
                    else:
                        anotherDecodingDict[kkey] = decodingDict[kkey]

                return LogisticRegression(**anotherDecodingDict)
            if decodingDict['type'] == 'XGBoostRegressor':
                del decodingDict['type']
                del decodingDict['objective']
                return XGBoostRegressor(**decodingDict)
            if decodingDict['type'] == 'XGBoostClassifier':
                del decodingDict['type']
                return XGBoostClassifier(**decodingDict)
            KeyError("Unable to deserialize predictor: unknown 'type_': [" + decodingDict['type'] + ']')
        else:
            KeyError("Unable to deserialize predictor: no 'type_'")