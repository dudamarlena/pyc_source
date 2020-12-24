# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/init.py
# Compiled at: 2014-06-16 16:12:17
import os, pkg_resources
from kolekto.printer import printer
from kolekto.commands import Command
from kolekto.exceptions import KolektoRuntimeError
DEFAULT_CONFIG = '\nprofile = \'{profile}\'\n\nview \'Titles\' {{\n    pattern = \'{{title}}.{{ext}}\'\n}}\n\n# By default, the tree will use the tmdb_proxy datasource which will allow\n# you to get data from TMDB without requiring an API key:\ndatasource \'tmdb_proxy\' {{\n    base_url = \'http://api.kolekto-project.org/\'\n    max_results = 2\n}}\n\n# Uncomment and enter your API key to enable the TMDB datasource:\n#datasource \'tmdb\' {{\n#    api_key = \'<enter your tmdb api key>\'\n#    max_results = 2\n#}}\n\n# Get informations from files (quality, runtime...):\ndatasource \'mediainfos\' {{}}\n\n# Uncomment these lines to enable fields rewriting datasource:\n#datasource \'rewrite\' {{\n#    rewrite \'title_upper\' {{\n#        value = \'movie["title"].upper()\'\n#    }}\n#}}\n'

def get_profiles_name():
    return set(x.name for x in pkg_resources.iter_entry_points(group='kolekto.profiles'))


class Init(Command):
    """ Create links in the kolekto tree.
    """
    help = 'initialize a new Kolekto tree'

    def prepare(self):
        self.add_arg('--profile', '-p', default='movies', choices=get_profiles_name(), help='Select the profile to use')

    def run(self, args, config):
        if config is not None:
            raise KolektoRuntimeError('Already a Kolekto tree')
        movies_directory = os.path.join(args.tree, '.kolekto', 'movies')
        if not os.path.isdir(movies_directory):
            os.makedirs(movies_directory)
        with open(os.path.join(args.tree, '.kolekto', 'config'), 'w') as (fconfig):
            fconfig.write(DEFAULT_CONFIG.format(profile=args.profile))
        printer.p('Initialized empty Kolekto tree in {where}.', where=os.path.abspath(args.tree))
        self.get_metadata_db(args.tree)
        return