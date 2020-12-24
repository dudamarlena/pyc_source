# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/tests/test_fmi_util.py
# Compiled at: 2018-12-15 16:31:42
"""
Module containing the tests for the FMI interface.
"""
import nose, os, scipy.sparse.csc
from collections import OrderedDict
from pyfmi import testattr
from pyfmi.fmi import FMUModel, FMUException, FMUModelME1, FMUModelCS1, load_fmu, FMUModelCS2, FMUModelME2, PyEventInfo
import pyfmi.fmi_util as fmi_util, pyfmi.fmi as fmi

class Test_FMIUtil:

    @testattr(stddist=True)
    def test_cpr_seed(self):
        structure = OrderedDict([('der(inertia3.phi)', ['inertia3.w']),
         (
          'der(inertia3.w)', ['damper.phi_rel', 'inertia3.phi']),
         (
          'der(damper.phi_rel)', ['damper.w_rel']),
         (
          'der(damper.w_rel)',
          [
           'damper.phi_rel', 'damper.w_rel', 'inertia3.phi'])])
        states = [
         'inertia3.phi', 'inertia3.w', 'damper.phi_rel', 'damper.w_rel']
        groups = fmi_util.cpr_seed(structure, states)
        assert groups[0][5] == [1, 2, 3]
        assert groups[1][5] == [5, 7]
        assert groups[2][5] == [8, 9]
        assert groups[0][4] == [0, 1, 2]
        assert groups[1][4] == [3, 4]
        assert groups[2][4] == [5, 6]