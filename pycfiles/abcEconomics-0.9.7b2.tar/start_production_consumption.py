# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/start_production_consumption.py
# Compiled at: 2018-03-08 03:37:49
import abce
from production_multifirm import ProductionMultifirm
from utility_household import UtilityHousehold

def main(processes, rounds=5):
    s = abce.Simulation(processes=processes, name='production_consumption_test')
    print 'build ProductionMultifirm'
    productionmultifirm = s.build_agents(ProductionMultifirm, 'productionmultifirm', 1, rounds=rounds)
    print 'build UtilityHousehold'
    utilityhousehold = s.build_agents(UtilityHousehold, 'utilityhousehold', 5, rounds=rounds)
    all_agents = utilityhousehold + productionmultifirm
    for r in range(rounds):
        s.advance_round(r)
        productionmultifirm.production()
        utilityhousehold.consumption()
        all_agents.all_tests_completed()

    s.finalize()


if __name__ == '__main__':
    main(processes=1, rounds=5)
    print 'Iteration with 1 core finished'
    main(processes=4, rounds=5)
    print 'Iteration with multiple processes finished'