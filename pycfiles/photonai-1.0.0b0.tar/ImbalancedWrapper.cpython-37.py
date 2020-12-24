# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/modelwrapper/ImbalancedWrapper.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 3578 bytes
from sklearn.base import BaseEstimator, TransformerMixin

class ImbalancedDataTransform(BaseEstimator, TransformerMixin):
    __doc__ = '\n    Applies the chosen strategy to the data in order to handle the imbalance in the data.\n    Instantiates the strategy filter object according to the name given as string.\n    '
    _estimator_type = 'transformer'
    IMBALANCED_DICT = {'oversampling':[
      'RandomOverSampler', 'SMOTE', 'ADASYN'], 
     'undersampling':[
      'ClusterCentroids',
      'RandomUnderSampler',
      'NearMiss',
      'InstanceHardnessThreshold',
      'CondensedNearestNeighbour',
      'EditedNearestNeighbours',
      'RepeatedEditedNearestNeighbours',
      'AllKNN',
      'NeighbourhoodCleaningRule',
      'OneSidedSelection'], 
     'combine':[
      'SMOTEENN', 'SMOTETomek']}

    def __init__(self, method_name: str='RandomUnderSampler', **kwargs):
        """
        Instantiates an object that transforms the data into balanced groups according to the given method

        Possible values for method_name:
        imbalance_type = OVERSAMPLING:
            - RandomOverSampler
            - SMOTE
            - ADASYN

        imbalance_type = UNDERSAMPLING:
            - ClusterCentroids,
            - RandomUnderSampler,
            - NearMiss,
            - InstanceHardnessThreshold,
            - CondensedNearestNeighbour,
            - EditedNearestNeighbours,
            - RepeatedEditedNearestNeighbours,
            - AllKNN,
            - NeighbourhoodCleaningRule,
            - OneSidedSelection

        imbalance_type = COMBINE:
            - SMOTEENN,
            - SMOTETomek

        :param method_name: which imbalanced strategy to use
        :type method_name: str
        :param kwargs: any parameters to pass to the imbalance strategy object
        :type kwargs:  dict
        """
        self.method_name = method_name
        self.needs_y = True
        imbalance_type = ''
        for group, possible_strategies in ImbalancedDataTransform.IMBALANCED_DICT.items():
            if method_name in possible_strategies:
                imbalance_type = group

        if imbalance_type == 'oversampling':
            home = 'over_sampling'
        else:
            if imbalance_type == 'undersampling':
                home = 'under_sampling'
            else:
                if imbalance_type == 'combine' or imbalance_type == 'combination':
                    home = 'combine'
                else:
                    raise Exception('Imbalance Type not found. Can be oversampling, undersampling or combine')
        desired_class_home = 'imblearn.' + home
        desired_class_name = method_name
        try:
            imported_module = __import__(desired_class_home, globals(), locals(), desired_class_name, 0)
            desired_class = getattr(imported_module, desired_class_name)
        except Exception as e:
            try:
                raise Exception('Imbalance Type not found. Can be oversampling, undersampling or combine')
            finally:
                e = None
                del e

        self.method = desired_class(**kwargs)
        self.x_transformed = None
        self.y_transformed = None

    def fit_sample(self, X, y):
        self.x_transformed, self.y_transformed = self.method.fit_sample(X, y)
        return (self.x_transformed, self.y_transformed)

    def fit(self, X, y, **kwargs):
        return self

    def transform(self, X, y=None, **kwargs):
        return self.fit_sample(X, y)