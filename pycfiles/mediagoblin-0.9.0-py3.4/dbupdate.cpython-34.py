# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/dbupdate.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 7925 bytes
import logging, six
from alembic import command
from sqlalchemy.orm import sessionmaker
from mediagoblin.db.open import setup_connection_and_db_from_config
from mediagoblin.db.migration_tools import MigrationManager, build_alembic_config, populate_table_foundations
from mediagoblin.init import setup_global_and_app_config
from mediagoblin.tools.common import import_component
_log = logging.getLogger(__name__)
logging.basicConfig()

def dbupdate_parse_setup(subparser):
    pass


class DatabaseData(object):

    def __init__(self, name, models, migrations):
        self.name = name
        self.models = models
        self.migrations = migrations

    def make_migration_manager(self, session):
        return MigrationManager(self.name, self.models, self.migrations, session)


def gather_database_data(plugins):
    """
    Gather all database data relevant to the extensions installed.

    Gather all database data relevant to the extensions we have
    installed so we can do migrations and table initialization.

    Returns a list of DatabaseData objects.
    """
    managed_dbdata = []
    from mediagoblin.db.models import MODELS as MAIN_MODELS
    from mediagoblin.db.migrations import MIGRATIONS as MAIN_MIGRATIONS
    managed_dbdata.append(DatabaseData('__main__', MAIN_MODELS, MAIN_MIGRATIONS))
    for plugin in plugins:
        try:
            models = import_component('{0}.models:MODELS'.format(plugin))
        except ImportError as exc:
            _log.debug('No models found for {0}: {1}'.format(plugin, exc))
            models = []
        except AttributeError as exc:
            _log.warning('Could not find MODELS in {0}.models, have you forgotten to add it? ({1})'.format(plugin, exc))
            models = []

        try:
            migrations = import_component('{0}.migrations:MIGRATIONS'.format(plugin))
        except ImportError as exc:
            _log.debug('No migrations found for {0}: {1}'.format(plugin, exc))
            migrations = {}
        except AttributeError as exc:
            _log.debug('Could not find MIGRATIONS in {0}.migrations, have youforgotten to add it? ({1})'.format(plugin, exc))
            migrations = {}

        if models:
            managed_dbdata.append(DatabaseData(plugin, models, migrations))
            continue

    return managed_dbdata


def run_foundations(db, global_config):
    """
    Gather foundations data and run it.
    """
    from mediagoblin.db.models import FOUNDATIONS as MAIN_FOUNDATIONS
    all_foundations = [
     (
      '__main__', MAIN_FOUNDATIONS)]
    Session = sessionmaker(bind=db.engine)
    session = Session()
    plugins = global_config.get('plugins', {})
    for plugin in plugins:
        try:
            foundations = import_component('{0}.models:FOUNDATIONS'.format(plugin))
            all_foundations.append((plugin, foundations))
        except ImportError as exc:
            continue
        except AttributeError as exc:
            continue

    for name, foundations in all_foundations:
        populate_table_foundations(session, foundations, name)


def run_alembic_migrations(db, app_config, global_config):
    """Initialize a database and runs all Alembic migrations."""
    Session = sessionmaker(bind=db.engine)
    session = Session()
    cfg = build_alembic_config(global_config, None, session)
    return command.upgrade(cfg, 'heads')


def run_dbupdate(app_config, global_config):
    """
    Initialize or migrate the database as specified by the config file.

    Will also initialize or migrate all extensions (media types, and
    in the future, plugins)
    """
    db = setup_connection_and_db_from_config(app_config, migrations=True)
    should_run_sqam_migrations = db.engine.has_table('core__migrations') and sqam_migrations_to_run(db, app_config, global_config)
    fresh_database = not db.engine.has_table('core__migrations') and not db.engine.has_table('alembic_version')
    if should_run_sqam_migrations:
        run_all_migrations(db, app_config, global_config)
    run_alembic_migrations(db, app_config, global_config)
    if fresh_database:
        run_foundations(db, global_config)


def run_all_migrations(db, app_config, global_config):
    """Initialize or migrates a database.

    Initializes or migrates a database that already has a
    connection setup and also initializes or migrates all
    extensions based on the config files.

    It can be used to initialize an in-memory database for
    testing.
    """
    dbdatas = gather_database_data(list(global_config.get('plugins', {}).keys()))
    Session = sessionmaker(bind=db.engine)
    for dbdata in dbdatas:
        migration_manager = dbdata.make_migration_manager(Session())
        migration_manager.init_or_migrate()


def sqam_migrations_to_run(db, app_config, global_config):
    """
    Check whether any plugins have sqlalchemy-migrate migrations left to run.

    This is a kludge so we can transition away from sqlalchemy-migrate
    except where necessary.
    """
    dbdatas = gather_database_data(list(global_config.get('plugins', {}).keys()))
    Session = sessionmaker(bind=db.engine)
    from mediagoblin.db.models import MigrationData
    if Session().query(MigrationData).filter_by(name='__main__').first() is None:
        return False
    for dbdata in dbdatas:
        migration_manager = dbdata.make_migration_manager(Session())
        if migration_manager.migrations_to_run():
            return True

    return False


def dbupdate(args):
    global_config, app_config = setup_global_and_app_config(args.conf_file)
    run_dbupdate(app_config, global_config)