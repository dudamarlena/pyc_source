# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: graphdash/defaults.py
# Compiled at: 2019-04-25 09:26:58
import argparse
from .struct.semifrozendict import SemiFrozenDict
SINK = 'Default'
DEFAULT_FAMILY = ()

def default_graph_data():
    """Default graph data.
    """
    return SemiFrozenDict({'name': None, 
       'title': 'No *title* provided', 
       'index': set(), 
       'pretext': '', 
       'text': '', 
       'file': None, 
       'export': None, 
       'rank': None, 
       'showtitle': False, 
       'labels': set(), 
       'other': None, 
       'id': None})


def default_family_data():
    """Default family data.
    """
    return SemiFrozenDict({'text': '', 
       'rank': None, 
       'alias': None, 
       'labels': set(), 
       'graphs': []})


class HashableSemiFrozenDict(SemiFrozenDict):
    """Ad hoc label structure, to allow set of dicts."""

    def __hash__(self):
        return hash(frozenset(self.items()))


def default_label_data():
    """Default label data.
    """
    return HashableSemiFrozenDict({'name': 'no_name_provided', 
       'text': 'No text provided', 
       'color': '#268bd2', 
       'text_color': 'white', 
       'tooltip': None})


def default_conf():
    """Default configuration.
    """
    return SemiFrozenDict({'root': 'default_graph_dir', 
       'families': None, 
       'title': 'Default title', 
       'subtitle': 'Default subtitle', 
       'placeholder': 'Free text and #keywords', 
       'header': '', 
       'footer': '', 
       'showfamilynumbers': True, 
       'showgraphnumbers': True, 
       'theme': 'dark', 
       'keep': 0.2, 
       'logfile': 'webapp.log', 
       'raw': False, 
       'verbose': False, 
       'debug': False, 
       'headless': False, 
       'port': 5555, 
       'export_conf': None, 
       'export_families': None})


DEFAULT_FAMILIES_GLOB = '.FAMILIES.*'

def add_boolean(parser, short_opt_on, long_opt_on, **kwargs):
    """Automatically add --stuff, --no-stuff and default for boolean option.
    """
    dest = long_opt_on.lstrip('-')
    long_opt_off = '--no-' + dest
    parser.add_argument(long_opt_on, short_opt_on, dest=dest, action='store_true', help=kwargs.get('help', ''))
    parser.add_argument(long_opt_off, dest=dest, action='store_false')
    parser.set_defaults(dest=kwargs.get('default', None))
    return


def get_parser():
    """Argument parser.
    """
    parser = argparse.ArgumentParser(description='GraphDash, a dashboard for graphs.')
    parser.add_argument('-c', '--conf', help='\n    Path to configuration file.\n    ')
    parser.add_argument('-r', '--root', help='\n    Root directory of the graphs.\n    ')
    parser.add_argument('-t', '--theme', help='\n    Change css theme.\n    ')
    parser.add_argument('-k', '--keep', type=float, help='\n    Proportion of common words kept for autocompletion.\n    ')
    parser.add_argument('-l', '--logfile', help='\n    Change default log file of the webapp.\n    ')
    parser.add_argument('-f', '--families', help='\n    Path to families file.\n    ')
    parser.add_argument('-F', '--export-families', help='\n    Export families file from loaded data, eventually\n    to be filled later by user.\n    ')
    parser.add_argument('-C', '--export-conf', help='\n    Export configuration file from defaults, eventually\n    to be filled later by user.\n    ')
    add_boolean(parser, '-a', '--raw', help='\n    Toggle raw mode: when loading, look for all graphs and ignore metadata.\n    ')
    add_boolean(parser, '-v', '--verbose', help='\n    Toggle verbosity when loading application.\n    ')
    add_boolean(parser, '-d', '--debug', help='\n    Toggle debug mode: enable Grunt livereload, enable Flask debug mode.\n    ')
    add_boolean(parser, '-H', '--headless', help='\n    Toggle headless mode: do not render pages, just search results.\n    This may be useful on large data sets.\n    ')
    parser.add_argument('-p', '--port', type=int, help='\n    When launched with Flask development server, port.\n    ')
    return parser