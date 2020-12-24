# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/maldegh/Software/github_repos/deGrootLab-pmx-master/pmx/scripts/cli.py
# Compiled at: 2019-03-20 09:34:29
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import sys
from pmx import __version__

class PmxCli:

    def __init__(self):
        parser = ArgumentParser(description='\n    ------------------------\n    pmx command line scripts\n    ------------------------\n\n    Available commands are:\n        mutate       Mutate protein or DNA/RNA\n        gentop       Fill hybrid topology with B states\n        analyse      Estimate free energy from Gromacs xvg files\n\n        gmxlib       Show/set GMXLIB path', formatter_class=RawTextHelpFormatter)
        parser.add_argument('-v', '--version', action='version', version=__version__)
        parser.add_argument('command', help=SUPPRESS)
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def mutate(self):
        import mutate_v2
        mutate_v2.entry_point()

    def gentop(self):
        import generate_hybrid_topology
        generate_hybrid_topology.entry_point()

    def analyse(self):
        import analyze_dhdl
        analyze_dhdl.entry_point()

    def gmxlib(self):
        import set_gmxlib
        set_gmxlib.entry_point()


def check_unknown_cmd(unknowns):
    """Checks unknown command line arguments are raises a warning if unexpected
    commands are found.
    """
    expected = [
     'pmx', 'analyse', 'mutate', 'doublebox', 'gentop', 'gmxlib',
     'genlib', 'abfe']
    for cmd in unknowns:
        if cmd not in expected:
            print ('Unknown command found in your command line: "{}". This command will be ignored').format(cmd)


def entry_point():
    PmxCli()


if __name__ == '__main__':
    entry_point()