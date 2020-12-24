# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abcEconomics/unittest/start_core_engine.py
# Compiled at: 2018-05-10 08:11:36
from buy import Buy
from sell import Sell
from give import Give
from logger_test import LoggerTest
from endowment import Endowment
from buyexpiringcapital import BuyExpiringCapital
from abcEconomics import Simulation
from messagea import MessageA
from messageb import MessageB

def main(processes, rounds):
    s = Simulation(processes=processes, name='unittest')
    s.declare_round_endowment(resource='labor_endowment', units=5, product='labor')
    s.declare_round_endowment(resource='cow', units=10, product='milk')
    s.declare_perishable(good='labor')
    print 'build Buy'
    buy = s.build_agents(Buy, 'buy', 1000, rounds=rounds)
    print 'build Sell'
    sell = s.build_agents(Sell, 'sell', 1000, rounds=rounds)
    print 'build Give'
    give = s.build_agents(Give, 'give', 2, rounds=rounds)
    print 'build Endowment'
    endowment = s.build_agents(Endowment, 'endowment', 2, rounds=rounds, creation=0)
    print 'build LoggerTest'
    loggertest = s.build_agents(LoggerTest, 'loggertest', 1, rounds=rounds)
    print 'build BuyExpiringCapital'
    _ = s.build_agents(BuyExpiringCapital, 'buyexpiringcapital', 2, rounds=rounds)
    print 'build MessageA'
    messagea = s.build_agents(MessageA, 'messagea', 20)
    print 'build MessageB'
    messageb = s.build_agents(MessageB, 'messageb', 20)
    some = buy + sell + give + loggertest
    for r in range(rounds):
        s.advance_round(r)
        for _ in range(5):
            buy.one()
            buy.two()
            buy.three()
            buy.clean_up()

        buy.panel_log(variables=['price'])
        for _ in range(5):
            sell.one()
            sell.two()
            sell.three()
            sell.clean_up()

        for _ in range(5):
            give.one()
            give.two()
            give.three()
            give.clean_up()

        for _ in range(5):
            loggertest.one()
            loggertest.two()
            loggertest.three()
            loggertest.clean_up()

        (messagea + messageb).sendmsg()
        (messageb + messagea).recvmsg()
        endowment.Iconsume()
        some.all_tests_completed()

    s.finalize()


if __name__ == '__main__':
    main(processes=1, rounds=5)
    print 'Iteration with 1 core finished'
    main(processes=4, rounds=5)
    print 'Iteration with multiple processes finished'