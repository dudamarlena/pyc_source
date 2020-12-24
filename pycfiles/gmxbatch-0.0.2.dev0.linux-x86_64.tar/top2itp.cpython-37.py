# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/utilities/top2itp.py
# Compiled at: 2020-03-26 04:45:34
# Size of source mod 2**32: 4174 bytes
import argparse
from typing import Optional
from ..moleculetype import Atom
from ..topfilter import TopologyFilter

def top2itp(topfile: str, moleculetypename: str, itpfile: str, posresdefine: Optional[str]=None, posresforce: float=1000):
    """Convert a topol.top file made by pdb2gmx to an itp file containing just the first molecule definition

    :param topfile: name of the topology file (typically topol.top)
    :type topfile: str
    :param moleculetypename: name of the molecule type
    :type moleculetypename: str
    :param itpfile: output file name (.itp)
    :type itpfile: str
    :param posresdefine: if supplied, auto-generate a [ position_restraints ] section with the heavy atoms
    :type posresdefine: None or str
    :param posresforce: force for the position restraints (kJ/mol/nm)
    :type posresforce: float
    """
    fltr = TopologyFilter(topfile, handleifdefs=False, handleempty=False)
    moleculetype_sections_seen = False
    atoms = []
    with open(itpfile, 'wt') as (fout):
        for l, comment, section, filename, lineno, line in fltr.parse():
            if l.startswith('[') and l.endswith(']'):
                if section == 'moleculetype':
                    if moleculetype_sections_seen:
                        break
                    moleculetype_sections_seen = True
                elif section == 'system':
                    break
                elif not (l.startswith('[') and l.endswith(']')):
                    if section == 'moleculetype':
                        if len(l) > 0:
                            line = f"{moleculetypename}        {l.split()[1]}\n"
                            moleculetype_sections_seen = True
                    if len(l) > 0 and section == 'atoms':
                        atoms.append(Atom.fromITPLine(l))
                if section == 'position_restraints':
                    if posresdefine is not None:
                        line = ''
                if moleculetype_sections_seen:
                    fout.write(line)

        if posresdefine is not None:
            fout.write(f"#ifdef {posresdefine}\n")
            fout.write('[ position_restraints ]\n')
            fout.write(';atom type fx     fy     fz\n')
            for a in atoms:
                if not a.name.startswith('H'):
                    fout.write(f"{a.index:>5d}    1 {posresforce:>6f} {posresforce:>6f} {posresforce:>6f}\n")

            fout.write('#endif\n')


def main():
    """Entry point for top2itp

    """
    parser = argparse.ArgumentParser(description='Convert a pdb2gmx-generated topol.top to an itp file containing a single molecule definition.')
    parser.add_argument('-p', default='topol.top', help='Topology file created by gmx pdb2gmx', dest='topol', action='store',
      required=False)
    parser.add_argument('-o', default=None, help='Output file name (*.itp)', dest='itpname', action='store', required=False)
    parser.add_argument('-n', help='Molecule name', action='store', required=True, dest='molname')
    parser.add_argument('-r', help='Position restraint preprocessor macro (e.g. POSRE)', action='store', required=False, dest='posresmacro',
      default=None)
    parser.add_argument('-f', help='Position restraint force (kJ/mol/nm)', action='store', required=False, dest='posresforce',
      default=1000)
    parsed = parser.parse_args()
    top2itp((parsed.topol), (parsed.molname), (parsed.itpname if parsed.itpname is not None else parsed.molname.lower() + '.itp'),
      posresdefine=(parsed.posresmacro),
      posresforce=(float(parsed.posresforce)))