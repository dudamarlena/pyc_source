# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/alembic_commands.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2972 bytes
import argparse
from alembic import config
from sqlalchemy.orm import sessionmaker
from mediagoblin.db.open import setup_connection_and_db_from_config
from mediagoblin.init import setup_global_and_app_config
from mediagoblin.db.migration_tools import build_alembic_config
from mediagoblin.tools.common import import_component

class FudgedCommandLine(config.CommandLine):

    def main(self, args, db, global_config):
        options = self.parser.parse_args(args.args_for_alembic)
        if args.with_plugins:
            plugins = global_config.get('plugins', {}).keys()
            for plugin in plugins:
                try:
                    import_component('{0}.models:MODELS'.format(plugin))
                except ImportError:
                    pass

        if not hasattr(options, 'cmd'):
            print("* Only use this command if you know what you are doing! *\nIf not, use the 'gmg dbupdate' command instead.\n\n(You can also pass --with-plugins here.)Alembic help:\n")
            self.parser.print_help()
            return
        Session = sessionmaker(bind=db.engine)
        session = Session()
        cfg = build_alembic_config(global_config, options, session)
        self.run_cmd(cfg, options)


def parser_setup(subparser):
    subparser.add_argument('--with-plugins', action='store_true', help="Import all plugins' models before running alembic commands.")
    subparser.add_argument('args_for_alembic', nargs=argparse.REMAINDER)


def raw_alembic_cli(args):
    global_config, app_config = setup_global_and_app_config(args.conf_file)
    db = setup_connection_and_db_from_config(app_config, migrations=False)
    FudgedCommandLine().main(args, db, global_config)