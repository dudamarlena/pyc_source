# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/predict.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 2967 bytes
import os, importlib
from flame.util import utils
from flame.control import Control

class Predict:

    def __init__(self, model, version, output_format=None):
        self.model = model
        self.version = version
        self.control = Control(model, version)
        self.parameters = self.control.get_parameters()
        if output_format != None:
            self.parameters['output_format'] = output_format

    def get_model_set(self):
        """ Returns a Boolean indicating if the model uses external input sources and a list with these sources """
        return self.control.get_model_set()

    def set_single_CPU(self):
        """ Forces the use of a single CPU """
        self.parameters['numCPUs'] = 1

    def run(self, input_source):
        """ Executes a default predicton workflow """
        results = {}
        epd = utils.model_path(self.model, self.version)
        if not os.path.isdir(epd):
            results['error'] = 'unable to find model: ' + self.model + ' version: ' + str(self.version)
        if 'error' not in results:
            modpath = utils.module_path(self.model, self.version)
            idata_child = importlib.import_module(modpath + '.idata_child')
            apply_child = importlib.import_module(modpath + '.apply_child')
            odata_child = importlib.import_module(modpath + '.odata_child')
            idata = idata_child.IdataChild(self.parameters, input_source)
            results = idata.run()
        if 'error' not in results:
            apply = apply_child.ApplyChild(self.parameters, results)
            results = apply.run()
        odata = odata_child.OdataChild(self.parameters, results)
        return odata.run()