# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/start_combinable_actions.py
# Compiled at: 2018-03-09 13:33:07
import abce

class Agent(abce.Agent):

    def actionA(self):
        print (
         self.name, 'actionA')

    def actionB(self):
        print (
         self.name, 'actionB')


def main(processes, rounds):
    sim = abce.Simulation(processes=processes)
    aagents = sim.build_agents(Agent, 'aagent', number=5)
    bagents = sim.build_agents(Agent, 'bagent', number=5)
    actionA = aagents.actionA
    actionB = bagents.actionB
    for r in range(rounds):
        sim.advance_round(r)
        (aagents.actionA + aagents.actionB)()
        (aagents.actionA + bagents.actionB)()
        (aagents.actionB + bagents.actionB)()
        aagents.actionA()
        bagents.actionB()
        (actionA + actionB)()

    sim.finalize()


if __name__ == '__main__':
    main(1, 1)
    main(4, 1)