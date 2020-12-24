# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2018/pinetree/tests/params/single_gene_x.py
# Compiled at: 2018-02-12 19:43:29
import pinetree as pt

def execute(output):
    sim = pt.Simulation(cell_volume=8e-16)
    sim.seed(34)
    sim.add_polymerase(name='rnapol', copy_number=10, speed=40, footprint=10)
    sim.add_polymerase(name='ribosome', copy_number=100, speed=30, footprint=10)
    plasmid = pt.Genome(name='T7', length=605)
    plasmid.add_promoter(name='phi1', start=1, stop=10, interactions={'rnapol': 200000000.0})
    plasmid.add_terminator(name='t1', start=604, stop=605, efficiency={'rnapol': 1.0})
    plasmid.add_gene(name='proteinX', start=26, stop=225, rbs_start=11, rbs_stop=26, rbs_strength=10000000.0)
    sim.register_genome(plasmid)
    sim.run(stop_time=60, time_step=1, output_prefix=output)


if __name__ == '__main__':
    execute('')