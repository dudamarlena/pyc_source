# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/test/hydro/connectors/test_hydro_cluster.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'moshebasanchig'
import unittest
from hydro.hydro_cluster import LocalHydro
from hydro.exceptions import HydroException

class LocalHydroTest(unittest.TestCase):

    def test_require_topology_instance(self):
        local_hydro = LocalHydro()
        self.assertRaises(HydroException, local_hydro.register, 'not-a-topology', None)
        return


if __name__ == '__main__':
    unittest.main()