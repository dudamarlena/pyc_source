# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/tests/test_fmi_util.py
# Compiled at: 2018-12-15 16:31:42
__doc__ = '\nModule containing the tests for the FMI interface.\n'
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