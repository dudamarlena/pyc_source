# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/cli/nas.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 1301 bytes
import argparse, os, sys, signal
from deephyper.search.util import load_attr_from
HPS_SEARCHES = {'ambs':'deephyper.search.nas.ambs.AMBNeuralArchitectureSearch', 
 'random':'deephyper.search.nas.full_random.Random', 
 'regevo':'deephyper.search.nas.regevo.RegularizedEvolution', 
 'ppo':'deephyper.search.nas.ppo.Ppo'}

def add_subparser(parsers):
    parser_name = 'nas'
    parser = parsers.add_parser(parser_name,
      help='Command line to run neural architecture search.')
    subparsers = parser.add_subparsers()
    for name, module_attr in HPS_SEARCHES.items():
        search_cls = load_attr_from(module_attr)
        subparser = subparsers.add_parser(name=name, conflict_handler='resolve')
        subparser = search_cls.get_parser(subparser)
        subparser.set_defaults(func=main)


def main(**kwargs):
    search_name = sys.argv[2]
    search_cls = load_attr_from(HPS_SEARCHES[search_name])
    search_obj = search_cls(**kwargs)
    try:
        on_exit = load_attr_from(f"{search_obj.__module__}.on_exit")
        signal.signal(signal.SIGINT, on_exit)
        signal.signal(signal.SIGTERM, on_exit)
    except AttributeError:
        print("This search doesn't have an exiting procedure...")

    search_obj.main()