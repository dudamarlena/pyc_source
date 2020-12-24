# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/configuration.py
# Compiled at: 2016-11-18 16:26:44


def init_configuration(self):
    """
    Load the application configuration from the ``SETTINGS`` environment variable.

    :returns: None

    ``SETTINGS`` must contain a filename that points to the configuration file.
    """
    self.app.config.from_envvar('SETTINGS')