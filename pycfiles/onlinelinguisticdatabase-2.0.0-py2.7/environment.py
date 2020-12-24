# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/config/environment.py
# Compiled at: 2016-09-19 13:27:02
"""Pylons environment configuration.

.. module:: environment
   :synopsis: Pylons environment configuration.

"""
import os, re
from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config
import onlinelinguisticdatabase.lib.app_globals as app_globals, onlinelinguisticdatabase.lib.helpers
from onlinelinguisticdatabase.lib.foma_worker import start_foma_worker
from onlinelinguisticdatabase.config.routing import make_map
from onlinelinguisticdatabase.model import init_model
import logging
log = logging.getLogger(__name__)

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config`` object.
    
    .. note::
    
        This is where the ``regexp`` operator for SQLite is defined and where
        the ``PRAGMA`` command is issued to make SQLite LIKE queries
        case-sensitive.

    """
    config = PylonsConfig()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='onlinelinguisticdatabase', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = onlinelinguisticdatabase.lib.helpers
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', default_filters=['escape'], imports=[
     'from webhelpers.html import escape'])
    engine = engine_from_config(config, 'sqlalchemy.')
    RDBMSName = config['sqlalchemy.url'].split(':')[0]
    app_globals.RDBMSName = RDBMSName
    if RDBMSName == 'sqlite':
        try:
            from sqlalchemy import event
            from sqlalchemy.engine import Engine

            @event.listens_for(Engine, 'connect')
            def sqlite_patches(dbapi_connection, connection_record):

                def regexp(expr, item):
                    """This is the Python re-based regexp function that we provide
                    for SQLite.  Note that searches will be case-sensitive by
                    default.  Such behaviour is assured in MySQL by inserting
                    COLLATE expressions into the query (cf. in SQLAQueryBuilder.py).
                    """
                    patt = re.compile(expr)
                    try:
                        return item and patt.search(item) is not None
                    except TypeError:
                        return item and patt.search(str(item)) is not None

                    return

                dbapi_connection.create_function('regexp', 2, regexp)
                cursor = dbapi_connection.cursor()
                cursor.execute('PRAGMA case_sensitive_like=ON')
                cursor.close()

        except ImportError:
            from sqlalchemy.interfaces import PoolListener

            class SQLiteSetup(PoolListener):
                """A PoolListener used to provide the SQLite dbapi with a regexp function.
                """

                def connect(self, conn, conn_record):
                    conn.create_function('regexp', 2, self.regexp)

                def regexp(self, expr, item):
                    """This is the Python re-based regexp function that we provide for SQLite.
                    Note that searches will be case-sensitive by default, which may not be
                    the default for the MySQL regexp, depending on the collation."""
                    patt = re.compile(expr)
                    try:
                        return item and patt.search(item) is not None
                    except TypeError:
                        return item and patt.search(str(item)) is not None

                    return

            engine = engine_from_config(config, 'sqlalchemy.', listeners=[SQLiteSetup()])
            engine.execute('PRAGMA case_sensitive_like=ON')

    init_model(engine)
    foma_worker = start_foma_worker()
    return config