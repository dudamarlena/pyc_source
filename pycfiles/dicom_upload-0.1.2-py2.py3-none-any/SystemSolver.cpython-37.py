# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/parametertree/SystemSolver.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 16215 bytes
from collections import OrderedDict
import numpy as np

class SystemSolver(object):
    """SystemSolver"""
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
        elif constraint == 'fixed':
            if 'f' not in var[3]:
                raise TypeError("Fixed constraints not allowed for '%s'" % name)
            var[2] = constraint
        elif isinstance(constraint, tuple):
            if 'r' not in var[3]:
                raise TypeError("Range constraints not allowed for '%s'" % name)
            assert len(constraint) == 2
            var[2] = constraint
        elif constraint is not True:
            raise TypeError("constraint must be None, True, 'fixed', or tuple. (got %s)" % constraint)
        if var[1] is np.ndarray:
            value = np.array(value, dtype=float)
        elif var[1] in (int, float, tuple):
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
               40  CALL_FUNCTION_2       2  ''
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
        """Camera"""
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