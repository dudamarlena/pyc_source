# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_extras/flask_extras/filters/config.py
# Compiled at: 2017-01-09 16:41:25
# Size of source mod 2**32: 2037 bytes
"""Provides configuration utilities for using the filters."""
from __future__ import absolute_import
from inspect import getmembers
from inspect import isfunction
from . import filters
from . import munging
from . import random

def _get_funcs(module):
    """Extract all functions from a module.

    Args:
        module (module): A python module reference.

    Returns:
        funcs (dict): A dictionary of names and functions extracted.

    """
    return {name:func for name, func in getmembers(module) if isfunction(func) if isfunction(func)}


def _inject_filters(app, filters):
    """Inject a set of filters into a Flask app.

    Args:
        app (object): The Flask application.
        filters (dict): A dictionary of name and functions.

    Returns:
        app (object): The Flask application.
    """
    for name, func in filters.iteritems():
        app.jinja_env.filters[name] = func

    return app


def config_flask_filters(app):
    """Register a Flask app with all the available filters.

    Args:
        app (object): The Flask application instance.
        filters (list): The list of filter functions to use.

    Returns:
        app (object): The modified Flask application instance.
    """
    app = _inject_filters(app, _get_funcs(filters))
    app = _inject_filters(app, _get_funcs(random))
    app = _inject_filters(app, _get_funcs(munging))
    return app


def _inject_template_globals(app, funcs):
    """Inject a set of functions into a Flask app as template_globals.

    Args:
        app (object): The Flask application.
        funcs (dict): A dictionary of name and functions.

    Returns:
        app (object): The Flask application.
    """
    for name, func in funcs.iteritems():
        app.add_template_global(name, func)

    return app


def config_flask_globals(app):
    """Configure a Flask app to use all functions as template_globals."""
    app = _inject_template_globals(app, _get_funcs(filters))
    return app