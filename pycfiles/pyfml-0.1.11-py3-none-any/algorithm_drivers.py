# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/common/algorithm_drivers.py
# Compiled at: 2018-12-15 16:31:42
__doc__ = ' \nModule containing optimization, simulation and initialization algorithms.\n'
import logging, time, numpy as N
from .xmlparser import XMLException
default_int = int
int = N.int32
N.int = N.int32

class AlgorithmBase(object):
    """ 
    Abstract class which all algorithms that are to be used in
    simulating/optimization/initialization with Model classes extending
    common.core.BaseModel must implement.
    """

    def __init__(self, model, alg_args):
        pass

    def solve(self):
        pass

    def get_result(self):
        pass

    @classmethod
    def get_default_options(self):
        pass


class ResultBase(object):
    """ 
    Base class for an algorithm result. All algorithms used in any of the 
    high-level functions should return an object which extends this class.
    """

    def __init__(self, model=None, result_file_name=None, solver=None, result_data=None, options=None):
        """ 
        Create a result object containing the model used in the algorithm, the 
        name of the result file, the solver used in the algorithm, the result 
        data object and the object (dict) holding the options used in the 
        algorithm run.
                       
        Parameters::
        
            model -- 
                The Model (extending common.BaseModel) object for the model used
                in the algorithm.
                
            result_file_name --
                Name of the file containing the algorithm result created on the 
                file system.
                
            solver --
                The solver object used in the algorithm.
                
            result_data --
                The result data object created when running the algorithm. Holds 
                the whole result data matrix.
                
            options --
                The options object with the options that the algorithm was run 
                with.
        """
        self._model = model
        self._result_file_name = result_file_name
        self._solver = solver
        self._result_data = result_data
        self._options = options

    def _get_model(self):
        if self._model is not None:
            return self._model
        else:
            raise Exception('model has not been set')
            return

    def _set_model(self, model):
        self._model = model

    model = property(fget=_get_model, fset=_set_model, doc='\n    Property for accessing the model that was used in the algorithm.\n    ')

    def _get_result_file(self):
        if self._result_file_name is not None:
            return self._result_file_name
        else:
            raise Exception('result file name has not been set')
            return

    def _set_result_file(self, file_name):
        self._result_file_name = result_file_name

    result_file = property(fget=_get_result_file, fset=_set_result_file, doc='\n    Property for accessing the name of the result file created in the algorithm.\n    ')

    def _get_solver(self):
        if self._solver is not None:
            return self._solver
        else:
            raise Exception('solver has not been set')
            return

    def _set_solver(self, solver):
        self._solver = solver

    solver = property(fget=_get_solver, fset=_set_solver, doc='\n    Property for accessing the solver that was used in the algorithm.\n    ')

    def _get_result_data(self):
        if self._result_data is not None:
            return self._result_data
        else:
            raise Exception('result data has not been set')
            return

    def _set_result_data(self, result_data):
        self._result_data = result_data

    result_data = property(fget=_get_result_data, fset=_set_result_data, doc='\n    Property for accessing the result data matrix that was created in the \n    algorithm.\n    ')

    def _get_options(self):
        if self._options is not None:
            return self._options
        else:
            raise Exception('options has not been set')
            return

    def _set_options(self, options):
        self._options = options

    options = property(fget=_get_options, fset=_set_options, doc='\n    Property for accessing he options object holding the options used in the \n    algorithm.\n    ')


class JMResultBase(ResultBase):

    def keys(self):
        """
        Returns the variable names in the result file.
        """
        return self.result_data.name

    def __getitem__(self, key):
        """
        Returns vector with result trajectory for a variable, parameter 
        or constant that has the same length as the time vector.
        
        Parameters::
        
            key --
                Name of the variable/parameter/constant.
        """
        val_x = self.result_data.get_variable_data(key).x
        if self.result_data.is_variable(key):
            return val_x
        time = self.result_data.get_variable_data('time')
        return val_x[0].repeat(len(time.t))

    def final(self, key):
        """
        Returns the final value of a variable result trajectory.

        Parameters::
        
            key --
                Name of the variable/parameter/constant.
        """
        val_x = self.result_data.get_variable_data(key).x
        return val_x[(-1)]

    def initial(self, key):
        """
        Returns the initial value of a variable result trajectory.

        Parameters::
        
            key --
                Name of the variable/parameter/constant.
        """
        val_x = self.result_data.get_variable_data(key).x
        return val_x[0]

    def is_variable(self, name):
        """
        Returns True if the given name corresponds to a time-varying variable.
        
        Parameters::
        
            name --
                Name of the variable/parameter/constant.
                
        Returns::
        
            True if the variable is time-varying.
        """
        return self.result_data.is_variable(name)

    def is_negated(self, name):
        return self.result_data.is_negated(name)

    def _get_data_matrix(self):
        return self.result_data.get_data_matrix()

    data_matrix = property(fget=_get_data_matrix, doc='\n    Property for accessing the result matrix.\n    ')

    def get_column(self, name):
        """
        Returns the column number in the data matrix where the values of the 
        variable are stored.
        
        Parameters::
        
            name --
                Name of the variable/parameter/constant.
            
        Returns::
        
            The column number.
        """
        return self.result_data.get_column(name)


class AssimuloSimResult(JMResultBase):
    pass


class OptionBase(dict):
    """ 
    Base class for an algorithm option class. 
    
    All algorithm option classes should extend this class. 
    
    This class extends the dict class overriding __init__, __setitem__, update 
    and setdefault methods with the purpose of offering a key check for the 
    extending classes.
    
    The extending class can define a set of keys and default values by 
    overriding __init__ or when instantiating the extended class and thereby not 
    allow any other keys to be added to the dict.
    
    Example overriding __init__::
    
        class MyOptionsClass(OptionBase):
            def __init__(self, *args, **kw):
                mydefaults = {'def1':1, 'def2':2}
                super(MyOptionsClass,self).__init__(mydefaults)
            
                self.update(*args, **kw)
                
        >> opts = MyOptionsClass()
        >> opts['def1'] = 3   // ok
        >> opts.update({'def2':4})   // ok
        >> opts['def3']= 5   // not ok
        
                
         * Example setting defaults in constructor:
         
         class MyOptionsClass(OptionBase):pass
         
        >> opts = MyOptionsClass(def1=1, def2=2)
        >> opts['def1'] = 3   // ok
        >> opts.update({'def2':4})   // ok
        >> opts['def3']= 5   // not ok
        
        >> opts2 = MyOptionsClass()   // this class has no restrictions on keys
        >> opts2['def5'] = 'hello'   //ok
    """

    def __init__(self, *args, **kw):
        super(OptionBase, self).__init__(*args, **kw)
        self._keys = super(OptionBase, self).keys()

    def __setitem__(self, key, value):
        if self._keys:
            if key not in self._keys:
                raise UnrecognizedOptionError('The key: %s, is not a valid option' % str(key))
        super(OptionBase, self).__setitem__(key, value)

    def update(self, *args, **kw):
        if args:
            if len(args) > 1:
                raise TypeError('update expected at most 1 arguments, got %d' % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]

        for key in kw:
            self[key] = kw[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

    def _update_keep_dict_defaults(self, *args, **kw):
        """ 
        Go through args/kw and for each value in a key-value-set that is a dict 
        - update the current dict with the new dict (don't overwrite).
        """
        if args:
            if len(args) > 1:
                raise TypeError('update expected at most 1 arguments, got %d' % len(args))
            other = dict(args[0])
            for key in other:
                if key not in self._keys:
                    raise UnrecognizedOptionError('The key: %s, is not a valid option' % str(key))
                if isinstance(self[key], dict):
                    self[key].update(other[key])
                else:
                    self[key] = other[key]

        for key in kw:
            if key not in self._keys:
                raise UnrecognizedOptionError('The key: %s, is not a valid option' % str(key))
            if isinstance(self[key], dict):
                self[key].update(kw[key])
            else:
                self[key] = kw[key]


class InvalidAlgorithmOptionException(Exception):
    """ 
    Exception raised when an algorithm options argument is encountered that is 
    not valid.
    """

    def __init__(self, arg):
        self.msg = 'Invalid algorithm options object: ' + str(arg)

    def __str__(self):
        return repr(self.msg)


class InvalidSolverArgumentException(Exception):
    """ 
    Exception raised when a solver argument is encountered that does not exist.
    """

    def __init__(self, arg):
        self.msg = 'Invalid solver argument: ' + str(arg)

    def __str__(self):
        return repr(self.msg)


class UnrecognizedOptionError(Exception):
    pass