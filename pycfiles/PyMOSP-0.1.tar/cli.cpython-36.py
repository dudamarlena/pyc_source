# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/cli.py
# Compiled at: 2019-09-10 09:59:08
# Size of source mod 2**32: 2434 bytes
__doc__ = '\npymoso\n\nUsage:\n  pymoso listitems\n  pymoso solve [--budget=B] [--odir=D] [--crn] [--simpar=P]\n    [(--seed <s> <s> <s> <s> <s> <s>)] [(--param <param> <val>)]...\n    <problem> <solver> <x>...\n  pymoso testsolve [--budget=B] [--odir=D] [--crn] [--isp=T] [--proc=Q]\n    [--metric] [(--seed <s> <s> <s> <s> <s> <s>)] [(--param <param> <val>)]...\n    <tester> <solver> [<x>...]\n  pymoso -h | --help\n  pymoso -v | --version\n\nOptions:\n  --budget=B                Set the simulation budget [default: 200]\n  --odir=D                  Set the output file directory name. [default: testrun]\n  --crn                     Set if common random numbers are desired.\n  --simpar=P                Set number of parallel processes for simulation replications. [default: 1]\n  --isp=T                   Set number of algorithm instances to solve. [default: 1]\n  --proc=Q                  Set number of parallel processes for the algorithm instances. [default: 1]\n  --metric                  Set if metric computation is desired.\n  --seed                    Set the random number seed with 6 spaced integers.\n  --param                   Specify a solver-specific parameter <param> <val>.\n  -h --help                 Show this screen.\n  -v --version              Show version.\n\nExamples:\n  pymoso listitems\n  pymoso solve ProbTPA RPERLE 4 14\n  pymoso solve --budget=100000 --odir=test1  ProbTPB RMINRLE 3 12\n  pymoso solve --seed 12345 32123 5322 2 9543 666666666 ProbTPC RPERLE 31 21 11\n  pymoso solve --simpar=4 --param betaeps 0.4 ProbTPA RPERLE 30 30\n  pymoso solve --param radius 3 ProbTPA RPERLE 45 45\n  pymoso testsolve --isp=16 --proc=4 TPATester RPERLE\n  pymoso testsolve --isp=20 --proc=10 --metric --crn TPBTester RMINRLE 9 9\n\nHelp:\n  Use the listitems command to view a list of available solvers, problems, and\n  test problems.\n'
from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    """
    Main CLI entrypoint.
    """
    from . import commands
    options = docopt(__doc__, version=VERSION)
    for k, v in options.items():
        if hasattr(commands, k) and v:
            commod = getattr(commands, k)
            comclasses = getmembers(commod, isclass)
            comclass = [cmcls[1] for cmcls in comclasses if cmcls[0] != 'BaseComm' if issubclass(cmcls[1], commands.basecomm.BaseComm)][0]
            cominst = comclass(options)
            cominst.run()