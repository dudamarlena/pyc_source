# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/parametertree/SystemSolver.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 16215 bytes
from collections import OrderedDict
import numpy as np

class SystemSolver(object):
    __doc__ = '\n    This abstract class is used to formalize and manage user interaction with a \n    complex system of equations (related to "constraint satisfaction problems").\n    It is often the case that devices must be controlled\n    through a large number of free variables, and interactions between these \n    variables make the system difficult to manage and conceptualize as a user\n    interface. This class does _not_ attempt to numerically solve the system\n    of equations. Rather, it provides a framework for subdividing the system\n    into manageable pieces and specifying closed-form solutions to these small \n    pieces.\n    \n    For an example, see the simple Camera class below.\n    \n    Theory of operation: Conceptualize the system as 1) a set of variables\n    whose values may be either user-specified or automatically generated, and \n    2) a set of functions that define *how* each variable should be generated. \n    When a variable is accessed (as an instance attribute), the solver first\n    checks to see if it already has a value (either user-supplied, or cached\n    from a previous calculation). If it does not, then the solver calls a \n    method on itself (the method must be named `_variableName`) that will\n    either return the calculated value (which usually involves acccessing\n    other variables in the system), or raise RuntimeError if it is unable to\n    calculate the value (usually because the user has not provided sufficient\n    input to fully constrain the system). \n    \n    Each method that calculates a variable value may include multiple \n    try/except blocks, so that if one method generates a RuntimeError, it may \n    fall back on others. \n    In this way, the system may be solved by recursively searching the tree of \n    possible relationships between variables. This allows the user flexibility\n    in deciding which variables are the most important to specify, while \n    avoiding the apparent combinatorial explosion of calculation pathways\n    that must be considered by the developer.\n    \n    Solved values are cached for efficiency, and automatically cleared when \n    a state change invalidates the cache. The rules for this are simple: any\n    time a value is set, it invalidates the cache *unless* the previous value\n    was None (which indicates that no other variable has yet requested that \n    value). More complex cache management may be defined in subclasses.\n    \n    \n    Subclasses must define:\n    \n    1) The *defaultState* class attribute: This is a dict containing a \n       description of the variables in the system--their default values,\n       data types, and the ways they can be constrained. The format is::\n       \n           { name: [value, type, constraint, allowed_constraints], ...}\n       \n       * *value* is the default value. May be None if it has not been specified\n         yet.\n       * *type* may be float, int, bool, np.ndarray, ...\n       * *constraint* may be None, single value, or (min, max)\n            * None indicates that the value is not constrained--it may be \n              automatically generated if the value is requested.\n       * *allowed_constraints* is a string composed of (n)one, (f)ixed, and (r)ange. \n       \n       Note: do not put mutable objects inside defaultState!\n       \n    2) For each variable that may be automatically determined, a method must \n       be defined with the name `_variableName`. This method may either return\n       the \n    '
    defaultState = OrderedDict()

    def __init__(self):
        self.__dict__['_vars'] = OrderedDict()
        self.__dict__['_currentGets'] = set()
        self.reset()

    def reset(self):
        """
        Reset all variables in the solver to their default state.
        """
        self._currentGets.clear()
        for k in self.defaultState:
            self._vars[k] = self.defaultState[k][:]

    def __getattr__(self, name):
        if name in self._vars:
            return self.get(name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """
        Set the value of a state variable. 
        If None is given for the value, then the constraint will also be set to None.
        If a tuple is given for a scalar variable, then the tuple is used as a range constraint instead of a value.
        Otherwise, the constraint is set to 'fixed'.
        
        """
        if name in self._vars:
            if value is None:
                self.set(name, value, None)
            elif isinstance(value, tuple) and self._vars[name][1] is not np.ndarray:
                self.set(name, None, value)
            else:
                self.set(name, value, 'fixed')
        elif hasattr(self, name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(name)

    def get(self, name):
        """
        Return the value for parameter *name*. 
        
        If the value has not been specified, then attempt to compute it from
        other interacting parameters.
        
        If no value can be determined, then raise RuntimeError.
        """
        if name in self._currentGets:
            raise RuntimeError("Cyclic dependency while calculating '%s'." % name)
        self._currentGets.add(name)
        try:
            v = self._vars[name][0]
            if v is None:
                cfunc = getattr(self, '_' + name, None)
                if cfunc is None:
                    v = None
                else:
                    v = cfunc()
                if v is None:
                    raise RuntimeError("Parameter '%s' is not specified." % name)
                v = self.set(name, v)
        finally:
            self._currentGets.remove(name)

        return v

    def set(self, name, value=None, constraint=True):
        """
        Set a variable *name* to *value*. The actual set value is returned (in
        some cases, the value may be cast into another type).
        
        If *value* is None, then the value is left to be determined in the 
        future. At any time, the value may be re-assigned arbitrarily unless
        a constraint is given.
        
        If *constraint* is True (the default), then supplying a value that 
        violates a previously specified constraint will raise an exception.
        
        If *constraint* is 'fixed', then the value is set (if provided) and
        the variable will not be updated automatically in the future.

        If *constraint* is a tuple, then the value is constrained to be within the 
        given (min, max). Either constraint may be None to disable 
        it. In some cases, a constraint cannot be satisfied automatically,
        and the user will be forced to resolve the constraint manually.
        
        If *constraint* is None, then any constraints are removed for the variable.
        """
        var = self._vars[name]
        if constraint is None:
            if 'n' not in var[3]:
                raise TypeError("Empty constraints not allowed for '%s'" % name)
            var[2] = constraint
        else:
            if constraint == 'fixed':
                if 'f' not in var[3]:
                    raise TypeError("Fixed constraints not allowed for '%s'" % name)
                var[2] = constraint
            else:
                if isinstance(constraint, tuple):
                    if 'r' not in var[3]:
                        raise TypeError("Range constraints not allowed for '%s'" % name)
                    assert len(constraint) == 2
                    var[2] = constraint
                else:
                    if constraint is not True:
                        raise TypeError("constraint must be None, True, 'fixed', or tuple. (got %s)" % constraint)
                    elif var[1] is np.ndarray:
                        value = np.array(value, dtype=float)
                    else:
                        if var[1] in (int, float, tuple):
                            if value is not None:
                                value = var[1](value)
                    if constraint is True and not self.check_constraint(name, value):
                        raise ValueError('Setting %s = %s violates constraint %s' % (name, value, var[2]))
                    if var[0] is not None:
                        self.resetUnfixed()
                    var[0] = value
                    return value

    def check_constraint--- This code section failed: ---

 L. 201         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _vars
                4  LOAD_FAST                'name'
                6  BINARY_SUBSCR    
                8  LOAD_CONST               2
               10  BINARY_SUBSCR    
               12  STORE_FAST               'c'

 L. 202        14  LOAD_FAST                'c'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'value'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    34  'to 34'
             30_0  COME_FROM            20  '20'

 L. 203        30  LOAD_CONST               True
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L. 204        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'c'
               38  LOAD_GLOBAL              tuple
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  POP_JUMP_IF_FALSE    92  'to 92'

 L. 205        44  LOAD_FAST                'c'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_CONST               None
               52  COMPARE_OP               is
               54  POP_JUMP_IF_TRUE     68  'to 68'
               56  LOAD_FAST                'c'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'value'
               64  COMPARE_OP               <=
               66  JUMP_IF_FALSE_OR_POP    90  'to 90'
             68_0  COME_FROM            54  '54'

 L. 206        68  LOAD_FAST                'c'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  JUMP_IF_TRUE_OR_POP    90  'to 90'
               80  LOAD_FAST                'c'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'value'
               88  COMPARE_OP               >=
             90_0  COME_FROM            78  '78'
             90_1  COME_FROM            66  '66'
               90  RETURN_VALUE     
             92_0  COME_FROM            42  '42'

 L. 208        92  LOAD_FAST                'value'
               94  LOAD_FAST                'c'
               96  COMPARE_OP               ==
               98  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 90

    def saveState(self):
        """
        Return a serializable description of the solver's current state.
        """
        state = OrderedDict()
        for name, var in self._vars.items():
            state[name] = (
             var[0], var[2])

        return state

    def restoreState(self, state):
        """
        Restore the state of all values and constraints in the solver.
        """
        self.reset()
        for name, var in state.items():
            self.set(name, var[0], var[1])

    def resetUnfixed(self):
        """
        For any variable that does not have a fixed value, reset
        its value to None.
        """
        for var in self._vars.values():
            if var[2] != 'fixed':
                var[0] = None

    def solve(self):
        for k in self._vars:
            getattr(self, k)

    def __repr__(self):
        state = OrderedDict()
        for name, var in self._vars.items():
            if var[2] == 'fixed':
                state[name] = var[0]

        state = ', '.join(['%s=%s' % (n, v) for n, v in state.items()])
        return '<%s %s>' % (self.__class__.__name__, state)


if __name__ == '__main__':

    class Camera(SystemSolver):
        __doc__ = '\n        Consider a simple SLR camera. The variables we will consider that \n        affect the camera\'s behavior while acquiring a photo are aperture, shutter speed,\n        ISO, and flash (of course there are many more, but let\'s keep the example simple).\n\n        In rare cases, the user wants to manually specify each of these variables and\n        no more work needs to be done to take the photo. More often, the user wants to\n        specify more interesting constraints like depth of field, overall exposure, \n        or maximum allowed ISO value.\n\n        If we add a simple light meter measurement into this system and an \'exposure\'\n        variable that indicates the desired exposure (0 is "perfect", -1 is one stop \n        darker, etc), then the system of equations governing the camera behavior would\n        have the following variables:\n\n            aperture, shutter, iso, flash, exposure, light meter\n\n        The first four variables are the "outputs" of the system (they directly drive \n        the camera), the last is a constant (the camera itself cannot affect the \n        reading on the light meter), and \'exposure\' specifies a desired relationship \n        between other variables in the system.\n\n        So the question is: how can I formalize a system like this as a user interface?\n        Typical cameras have a fairly limited approach: provide the user with a list\n        of modes, each of which defines a particular set of constraints. For example:\n\n            manual: user provides aperture, shutter, iso, and flash\n            aperture priority: user provides aperture and exposure, camera selects\n                            iso, shutter, and flash automatically\n            shutter priority: user provides shutter and exposure, camera selects\n                            iso, aperture, and flash\n            program: user specifies exposure, camera selects all other variables\n                    automatically\n            action: camera selects all variables while attempting to maximize \n                    shutter speed\n            portrait: camera selects all variables while attempting to minimize \n                    aperture\n\n        A more general approach might allow the user to provide more explicit \n        constraints on each variable (for example: I want a shutter speed of 1/30 or \n        slower, an ISO no greater than 400, an exposure between -1 and 1, and the \n        smallest aperture possible given all other constraints) and have the camera \n        solve the system of equations, with a warning if no solution is found. This\n        is exactly what we will implement in this example class.\n        '
        defaultState = OrderedDict([
         (
          'aperture', [None, float, None, 'nf']),
         (
          'shutter', [None, float, None, 'nf']),
         (
          'iso', [None, int, None, 'nf']),
         (
          'flash', [None, float, None, 'nf']),
         (
          'exposure', [None, float, None, 'f']),
         (
          'lightMeter', [None, float, None, 'f']),
         (
          'balance', [None, float, None, 'n'])])

        def _aperture(self):
            """
            Determine aperture automatically under a variety of conditions.
            """
            iso = self.iso
            exp = self.exposure
            light = self.lightMeter
            try:
                sh = self.shutter
                ap = 4.0 * (sh / 0.016666666666666666) * (iso / 100.0) * 2 ** exp * 2 ** light
                ap = np.clip(ap, 2.0, 16.0)
            except RuntimeError:
                sh = 0.016666666666666666
                raise

            return ap

        def _balance(self):
            iso = self.iso
            light = self.lightMeter
            sh = self.shutter
            ap = self.aperture
            fl = self.flash
            bal = 4.0 / ap * (sh / 0.016666666666666666) * (iso / 100.0) * 2 ** light
            return np.log2(bal)


    camera = Camera()
    camera.iso = 100
    camera.exposure = 0
    camera.lightMeter = 2
    camera.shutter = 0.016666666666666666
    camera.flash = 0
    camera.solve()
    print(camera.saveState())