# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2018/pinetree/tests/params/single_gene.py
# Compiled at: 2018-02-08 20:30:48
import pinetree as pt

def execute(output):
    sim = pt.Simulation(cell_volume=8e-16)
    sim.seed(34)
    sim.add_polymerase(name='rnapol', copy_number=1, speed=40, footprint=10)
    sim.add_polymerase(name='ribosome', copy_number=1, speed=30, footprint=10)
    plasmid = pt.Genome(name='T7', length=605)
    plasmid.add_promoter(name='phi1', start=1, stop=10, interactions={'rnapol': 200000000.0})
    plasmid.add_terminator(name='t1', start=604, stop=605, efficiency={'rnapol': 1.0})
    plasmid.add_gene(name='rnapol', start=26, stop=225, rbs_start=11, rbs_stop=26, rbs_strength=10000000.0)
    plasmid.add_gene(name='proteinX', start=241, stop=280, rbs_start=226, rbs_stop=241, rbs_strength=10000000.0)
    plasmid.add_gene(name='proteinY', start=296, stop=595, rbs_start=281, rbs_stop=296, rbs_strength=10000000.0)
    sim.register_genome(plasmid)
    sim.run(stop_time=40, time_step=1, output_prefix=output)


if __name__ == '__main__':
    execute('')