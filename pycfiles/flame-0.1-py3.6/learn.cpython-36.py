# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/learn.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 4026 bytes
import os, pickle, numpy as np
from flame.stats.RF import RF
from flame.stats.SVM import SVM
from flame.stats.GNB import GNB
from flame.stats.PLSR import PLSR
from flame.stats.PLSDA import PLSDA

class Learn:

    def __init__(self, parameters, results):
        self.parameters = parameters
        self.X = results['xmatrix']
        self.Y = results['ymatrix']
        self.results = results
        self.results['origin'] = 'learn'

    def run_custom(self):
        """
        Build a model using custom code to be defined in the learn child
        classes.
        """
        self.results['error'] = 'not implemented'

    def run_internal(self):
        """
        Builds a model using the internally defined machine learning tools.

        All input parameters are extracted from self.parameters.

        The main output is an instance of basemodel saved in
        the model folder as a pickle (model.pkl) and used for prediction.

        The results of building and validation are added to results,
        but also saved to the model folder as a pickle (info.pkl)
        for being displayed in manage tools.
        """
        registered_methods = [
         (
          'RF', RF),
         (
          'SVM', SVM),
         (
          'GNB', GNB),
         (
          'PLSR', PLSR),
         (
          'PLSDA', PLSDA)]
        model = None
        for imethod in registered_methods:
            if imethod[0] == self.parameters['model']:
                model = imethod[1](self.X, self.Y, self.parameters)
                break

        if not model:
            self.results['error'] = 'modeling method not recognised'
            return
        success, results = model.build()
        if not results:
            self.results['error'] = results
            return
        self.results['model_build'] = results
        success, results = model.validate()
        if not success:
            self.results['error'] = results
            return
        self.results['model_validate'] = results
        with open(os.path.join(self.parameters['model_path'], 'model.pkl'), 'wb') as (handle):
            pickle.dump(model, handle, protocol=(pickle.HIGHEST_PROTOCOL))
        with open(os.path.join(self.parameters['model_path'], 'info.pkl'), 'wb') as (handle):
            pickle.dump(self.results['model_build'], handle)
            pickle.dump(self.results['model_validate'], handle)

    def run(self):
        """
        Builds the model using the appropriate toolkit (internal or custom).
        """
        toolkit = self.parameters['modelingToolkit']
        if toolkit == 'internal':
            self.run_internal()
        else:
            if toolkit == 'custom':
                self.run_custom()
            else:
                self.results['error'] = 'modeling Toolkit ' + toolkit + ' is not supported yet'
        return self.results