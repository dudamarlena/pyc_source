# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/gui/codefile.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Jan 18, 2010

@author: brianthorne
"""
from os import path
import sys, inspect, logging
from introspection import interrogate
from scipysim import Event
from scipysim.actors import Siso, Actor

class CodeFile:
    """
    This class wraps an Actor or a model for the GUI.
    It contains instructions for drawing, connecting and running a simulation.
    
    """

    def __init__(self, filepath, name=None):
        """Wrap an Actor for the GUI, parses the number of inputs etc.
        If the name is not given it will be the stripped file name.
        TODO: Add GUI support. image, position, input connectors etc...
        """
        self.filepath = filepath
        assert path.exists(filepath)
        self.name = path.split(filepath)[1].split('.')[0] if name is None else name
        self.image = None
        logging.debug('Loading a %s block from %s' % (self.name, self.filepath))
        logging.debug('Trying to load the module in Python')
        sys.path.insert(0, path.split(filepath)[0])
        module = __import__(self.name)
        logging.debug('%s module imported' % self.name)
        try:
            block_class = getattr(module, self.name.title())
        except AttributeError:
            logging.debug('Module was not called the same as the filename')
            logging.debug(interrogate(module))
            modules = [ c for c in dir(module) if not inspect.isfunction(getattr(module, c)) and inspect.isclass(getattr(module, c)) and callable(getattr(module, c)) and issubclass(getattr(module, c), Actor) ]
            logging.debug('Got a list of classes that inherit from Actor: %s' % repr(modules))
            if len(modules) > 1:
                from difflib import get_close_matches
                modules = get_close_matches(self.name, modules, 1, 0.1)
            assert len(modules) > 0
            logging.debug('Modules found that nearly match module name are: %s.' % modules)
            module_name = modules[0]
            block_class = getattr(module, module_name)

        logging.debug("Block class is '%s'" % block_class)
        if issubclass(block_class, Siso):
            logging.debug('Inherits from SISO - we know that it has one input and one output')
            self.num_inputs = 1
            self.num_outputs = 1
        elif hasattr(block_class, 'num_inputs') and hasattr(block_class, 'num_outputs'):
            self.num_inputs = block_class.num_inputs
            self.num_outputs = block_class.num_outputs
        elif issubclass(block_class, Event):
            logging.debug('Skipping Event class')
        else:
            logging.error('Non siso module, and no info on how many inputs/outputs?')
            raise NotImplementedError()
        assert hasattr(block_class, 'output_domains') and hasattr(block_class, 'input_domains')
        self.output_domains = block_class.output_domains
        self.input_domains = block_class.input_domains
        return

    def get_code(self):
        """Load an actor or model file."""
        text = ('').join(open(self.filepath, 'r').readlines())
        return text

    def __repr__(self):
        """Return the name of this code file object"""
        return self.name