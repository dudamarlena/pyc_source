# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_testing.py
# Compiled at: 2011-06-28 10:17:42
"""
Nose plugin to run Django applications in a WSGI environment.

This module has no automated tests on purpose. Functional tests would be very
useful.

"""
from nose.plugins import Plugin
from paste.deploy import loadapp
__all__ = ('DjangoWsgifiedPlugin', )

class DjangoWsgifiedPlugin(Plugin):
    """
    Loads the Django application described by the PasteDeploy configuration URL
    in a WSGI environment suitable for testing.
    
    """
    enabled = False
    name = 'django-wsgified'
    enableOpt = 'paste_config_uri'

    def options(self, parser, env):
        help = 'Load the Django application described by the PasteDeploy configuration URI in a WSGI environment suitable for testing.'
        parser.add_option('--with-%s' % self.name, type='string', default='', dest=self.enableOpt, help=help)
        parser.add_option('--no-db', action='store_true', default=False, dest='no_db', help='Do not set up a Django test database')

    def configure(self, options, conf):
        """Store the URI to the PasteDeploy configuration."""
        super(DjangoWsgifiedPlugin, self).configure(options, conf)
        self.paste_config_uri = getattr(options, self.enableOpt)
        self.enabled = bool(self.paste_config_uri)
        self.verbosity = options.verbosity
        self.create_db = not options.no_db

    def begin(self):
        loadapp(self.paste_config_uri)
        from django.test.utils import setup_test_environment
        setup_test_environment()
        if self.create_db:
            from django.conf import settings
            from django.db import connection
            self.db_name = settings.DATABASE_NAME
            connection.creation.create_test_db(self.verbosity, autoclobber=True)

    def finalize(self, result=None):
        from django.test.utils import teardown_test_environment
        teardown_test_environment()
        if self.create_db:
            from django.db import connection
            connection.creation.destroy_test_db(self.db_name, self.verbosity)