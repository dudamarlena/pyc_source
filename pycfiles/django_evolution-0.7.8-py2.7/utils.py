# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/utils.py
# Compiled at: 2018-06-14 23:17:51
import os
from django.db import router
from django.db.models import get_model
from django_evolution.db import EvolutionOperationsMulti

def write_sql(sql, database):
    """Output a list of SQL statements, unrolling parameters as required"""
    evolver = EvolutionOperationsMulti(database).get_evolver()
    qp = evolver.quote_sql_param
    out_sql = []
    for statement in sql:
        if isinstance(statement, tuple):
            statement = unicode(statement[0] % tuple(qp(evolver.normalize_value(s)) for s in statement[1]))
        print statement
        out_sql.append(statement)

    return out_sql


def execute_sql(cursor, sql, database):
    """
    Execute a list of SQL statements on the provided cursor, unrolling
    parameters as required
    """
    evolver = EvolutionOperationsMulti(database).get_evolver()
    statement = None
    try:
        for statement in sql:
            if isinstance(statement, tuple):
                statement = (
                 statement[0].strip(), statement[1])
                if statement[0] and not statement[0].startswith('--'):
                    cursor.execute(statement[0], tuple(evolver.normalize_value(s) for s in statement[1]))
            else:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    cursor.execute(statement)

    except Exception as e:
        e.last_sql_statement = statement
        raise

    return


def get_database_for_model_name(app_name, model_name):
    """Returns the database used for a given model.

    Given an app name and a model name, this will return the proper
    database connection name used for making changes to that model. It
    will go through any custom routers that understand that type of model.
    """
    return router.db_for_write(get_model(app_name, model_name))


def get_app_name(app):
    """Return the name of an app.

    Args:
        app (module):
            The app.

    Returns:
        bytes: The name of the app.
    """
    return ('.').join(app.__name__.split('.')[:-1])


def get_app_label(app):
    """Return the label of an app.

    Args:
        app (module):
            The app.

    Returns:
        bytes: The label of the app.
    """
    return app.__name__.split('.')[(-2)]


def get_evolutions_module(app):
    """Return the evolutions module for an app.

    Args:
        app (module):
            The app.

    Returns:
        module:
        The evolutions module for the app, or ``None`` if it could not be
        found.
    """
    app_name = get_app_name(app)
    try:
        return __import__(app_name + '.evolutions', {}, {}, [''])
    except:
        return

    return


def get_evolutions_path(app):
    """Return the evolutions path for an app.

    Args:
        app (module):
            The app.

    Returns:
        bytes:
        The path to the evolutions module for the app, or ``None`` if it
        could not be found.
    """
    module = get_evolutions_module(app)
    if module:
        return os.path.dirname(module.__file__)
    else:
        return