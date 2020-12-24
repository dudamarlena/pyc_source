# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_population_noncoll.py
# Compiled at: 2020-01-17 14:44:58
# Size of source mod 2**32: 718 bytes
import os, pychemia
from .local_mongo import has_local_mongo

def notest_popu_noncoll():
    """
    Test (pychemia.population.NonCollinearMagMoms)              :
    """
    if not pychemia.HAS_PYMONGO:
        print('PyChemiaDB was disabled')
        return
    else:
        return has_local_mongo() or None
    source = 'tests/data/vasp_02'
    assert os.path.isfile(source + os.sep + 'INCAR')
    assert os.path.isfile(source + os.sep + 'POSCAR')
    popu = pychemia.population.NonCollinearMagMoms('test', source)
    popu.pcdb.clean()
    popu.random_population(16)
    assert len(popu) == 16
    popu.pcdb.clean()


if __name__ == '__main__':
    test_popu_noncoll()