# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/loader.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 3555 bytes
import configparser, importlib, importlib.util, os
from pathlib import Path
import types
from loguru import logger
from asyncpg_migrate import exceptions
from asyncpg_migrate import model

def load_configuration(filename: Path) -> model.Config:
    logger.debug('Loading configuration from {filename}',
      filename=filename)
    parser = configparser.ConfigParser(defaults=(os.environ),
      default_section='migrations',
      strict=False,
      interpolation=(configparser.ExtendedInterpolation()))
    parser.read(filename)
    user = parser.get('migrations', 'db_user')
    password = parser.get('migrations', 'db_password')
    host = parser.get('migrations', 'db_host')
    port = parser.getint('migrations', 'db_port')
    database_name = parser.get('migrations', 'db_name')
    script_location = Path(parser.get('migrations', 'script_location'))
    if not script_location.is_absolute():
        script_location = Path.cwd() / script_location
    return model.Config(script_location=script_location,
      database_dsn=f"postgres://{user}:{password}@{host}:{port}/{database_name}",
      database_name=database_name)


def load_migrations(config: model.Config) -> model.Migrations:
    logger.debug('Loading migrations via {config}', config=config)
    all_migrations = model.Migrations()
    for f in config.script_location.iterdir():
        if not f.is_file():
            continue
        module = load_python_module(f)
        revision = getattr(module, 'revision', None)
        upgrade_callable = getattr(module, 'upgrade', None)
        downgrade_callable = getattr(module, 'downgrade', None)
        try:
            revision = model.Revision.decode(revision, all_migrations.revisions())
        except (TypeError, ValueError) as ex:
            try:
                raise exceptions.MigrationLoadError(f"Value ({revision}, {type(revision)}) cannot be parsed as valid revision") from ex
            finally:
                ex = None
                del ex

        else:
            if revision in all_migrations:
                duplicated_migration = all_migrations[revision]
                raise exceptions.MigrationLoadError(f"{revision} has been already loaded, there is duplicate in {duplicated_migration.path}")
            if not upgrade_callable:
                raise exceptions.MigrationLoadError(f"{module} does not define upgrade function")
            if not downgrade_callable:
                raise exceptions.MigrationLoadError(f"{module} does not define downgrade function")
            migration = model.Migration(revision=revision,
              label=(f.name),
              path=f,
              upgrade=upgrade_callable,
              downgrade=downgrade_callable)
            all_migrations[migration.revision] = migration

    return all_migrations


def load_python_module(path: Path) -> types.ModuleType:
    module_id = path.name.replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_id, str(path))
    module = importlib.util.module_from_spec(spec)
    if spec.loader:
        exec_module = getattr(spec.loader, 'exec_module', None)
        if exec_module:
            exec_module(module)
            return module
    raise ValueError(f"Failed to read {path} as python file")