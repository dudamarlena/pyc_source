# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/start_custom_database.py
# Compiled at: 2018-05-03 06:13:03
import abce, dataset

class CustomLogging:

    def __init__(self, dbprotocolname, tablename):
        self.db = dataset.connect(dbprotocolname)
        self.table = self.db[tablename]

    def write_everything(self, **kveverything):
        self.table.insert(kveverything)

    def close(self):
        self.db.commit()


class MyAgent(abce.Agent):

    def write(self):
        self.custom_log('write_everything', name='joe', m=5)


def main(processes, rounds):
    sim = abce.Simulation(name='mysim', processes=processes, dbplugin=CustomLogging, dbpluginargs=['sqlite:///:memory:', 'sometable'])
    myagents = sim.build_agents(MyAgent, 'myagent', number=5)
    for i in range(rounds):
        sim.advance_round(i)
        myagents.write()

    sim.finalize()


if __name__ == '__main__':
    main(1, 5)
    main(4, 5)