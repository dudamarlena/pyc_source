# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/control.py
# Compiled at: 2018-06-21 09:57:14
# Size of source mod 2**32: 3112 bytes
from flame.util import utils
import os, yaml

class Control:

    def __init__(self, model, version):
        self.yaml_file = utils.model_path(model, version) + '/parameters.yaml'
        success, parameters = self.load_parameters(model)
        if not success:
            print('CRITICAL ERROR: unable to load parameter file.Running with fallback defaults')
            parameters = self.get_defaults()
        self.parameters = parameters
        self.parameters['endpoint'] = model
        self.parameters['version'] = version
        self.parameters['model_path'] = utils.model_path(model, version)
        self.parameters['md5'] = utils.md5sum(self.yaml_file)

    def load_parameters(self, model):
        """
        Loads parameters from a yaml file
        """
        if not os.path.isfile(self.yaml_file):
            return (False, None)
        else:
            try:
                with open(self.yaml_file, 'r') as (pfile):
                    parameters = yaml.load(pfile)
            except:
                return (False, None)

            return (True, parameters)

    def get_parameters(self):
        """
        Commodity function to access stored parameters
        """
        return self.parameters

    def get_model_set(self):
        """
        Returns a Boolean indicating if the model uses external input
        sources and a list with these sources.
        """
        ext_input = False
        model_set = None
        if 'ext_input' in self.parameters:
            if self.parameters['ext_input']:
                if 'model_set' in self.parameters:
                    if len(self.parameters['model_set']) > 1:
                        model_set = self.parameters['model_set']
                        ext_input = True
        return (
         ext_input, model_set)

    def get_defaults(self):
        """
        Fallback for setting parameters even when
        no "config.yaml" file is found
        """
        self.yaml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'children', 'parameters.yaml')
        with open(self.yaml_file, 'r') as (pfile):
            parameters = yaml.load(pfile)
        return parameters