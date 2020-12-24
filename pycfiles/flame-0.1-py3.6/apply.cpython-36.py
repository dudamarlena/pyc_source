# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/apply.py
# Compiled at: 2018-06-26 03:51:36
# Size of source mod 2**32: 7505 bytes
import numpy as np, pickle, os
from flame.util import utils
from sklearn.metrics import mean_squared_error, matthews_corrcoef as mcc
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.metrics import confusion_matrix

class Apply:

    def __init__(self, parameters, results):
        self.parameters = parameters
        self.results = results
        self.results['origin'] = 'apply'

    def external_validation(self):
        """ when experimental values are available for the predicted compounds, apply external validation """
        if 'ymatrix' not in self.results:
            return
        else:
            ext_val_results = []
            if not self.parameters['quantitative']:
                Ye = np.asarray(self.results['ymatrix'])
                Yp = np.asarray(self.results['values'])
                if Ye.size == 0:
                    raise ValueError('Experimental activity vector is empty')
                if Yp.size == 0:
                    raise ValueError('Predicted activity vector is empty')
                TN, FP, FN, TP = confusion_matrix(Ye, Yp, labels=[0, 1]).ravel()
                MCC = mcc(Ye, Yp)
                if TP + FN > 0:
                    sensitivity = TP / (TP + FN)
                else:
                    sensitivity = 0.0
                if TN + FP > 0:
                    specificity = TN / (TN + FP)
                else:
                    specificity = 0.0
                ext_val_results.append(('TP', 'True positives in external-validation', float(TP)))
                ext_val_results.append(('TN', 'True negatives in external-validation', float(TN)))
                ext_val_results.append(('FP', 'False positives in external-validation', float(FP)))
                ext_val_results.append(('FN', 'False negatives in external-validation', float(FN)))
                ext_val_results.append(('Sensitivity', 'Sensitivity in external-validation', float(sensitivity)))
                ext_val_results.append(('Specificity', 'Specificity in external-validation', float(specificity)))
                ext_val_results.append(('MCC', 'Mattews Correlation Coefficient in external-validation', float(MCC)))
            else:
                Ye = np.asarray(self.results['ymatrix'])
                Yp = np.asarray(self.results['values'])
                Ym = np.mean(Ye)
                nobj = len(Yp)
                SSY0_out = np.sum(np.square(Ym - Ye))
                SSY_out = np.sum(np.square(Ye - Yp))
                scoringP = mean_squared_error(Ye, Yp)
                SDEP = np.sqrt(SSY_out / nobj)
                Q2 = 1.0 - SSY_out / SSY0_out
                ext_val_results.append(('scoringP', 'Scoring P', scoringP))
                ext_val_results.append(('Q2', 'Determination coefficient in cross-validation', Q2))
                ext_val_results.append(('SDEP', 'Standard Deviation Error of the Predictions', SDEP))
        utils.add_result(self.results, ext_val_results, 'external-validation', 'external validation', 'method', 'single', 'External validation results')

    def run_internal(self):
        """ 

        Runs prediction tasks using internally defined methods

        Most of these methods can be found at the stats folder

        """
        X = self.results['xmatrix']
        try:
            nobj, nvarx = np.shape(X)
        except:
            self.results['error'] = 'Failed to generate MD'
            return
        else:
            if nobj == 0 or nvarx == 0:
                self.results['error'] = 'Failed to extract activity or to generate MD'
                return
            try:
                model_file = os.path.join(self.parameters['model_path'], 'model.pkl')
                with open(model_file, 'rb') as (input_file):
                    estimator = pickle.load(input_file)
            except:
                self.results['error'] = 'No valid model estimator found'
                return
            else:
                estimator.project(X, self.results)
        if not self.parameters['conformal']:
            self.external_validation()

    def run_R(self):
        """ Runs prediction tasks using an importer KNIME workflow """
        self.results['error'] = 'R toolkit is not supported in this version'

    def run_KNIME(self):
        """ Runs prediction tasks using R code """
        self.results['error'] = 'KNIME toolkit is not supported in this version'

    def run_custom(self):
        """ Template to be overriden in apply_child.py

            Input: must be already present in self.results
            Output: add prediction results to self.results using the utils.add_result() method 

        """
        self.results['error'] = 'custom prediction must be defined in the model apply_chlid class'

    def run(self):
        """ 

        Runs prediction tasks using the information present in self.results. 

        Depending on the modelingToolkit defined in self.parameters this task will use internal methods
        or make use if imported code in R/KNIME

        The custom option allows advanced uses to write their own function 'run_custom' method in 
        the model apply_child.py

        """
        if self.parameters['modelingToolkit'] == 'internal':
            self.run_internal()
        else:
            if self.parameters['modelingToolkit'] == 'R':
                self.run_R()
            else:
                if self.parameters['modelingToolkit'] == 'KNIME':
                    self.run_KNIME()
                else:
                    if self.parameters['modelingToolkit'] == 'custom':
                        self.run_custom()
                    else:
                        self.results['error'] = (
                         'Unknown prediction toolkit to run ', self.parameters['modelingToolkit'])
        return self.results