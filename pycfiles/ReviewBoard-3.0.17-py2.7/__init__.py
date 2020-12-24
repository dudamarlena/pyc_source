# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/__init__.py
# Compiled at: 2020-02-11 04:03:56
"""Review Board version and package information.

These variables and functions can be used to identify the version of
Review Board. They're largely used for packaging purposes.
"""
from __future__ import unicode_literals
VERSION = (
 3, 0, 17, 0, b'final', 0, True)

def get_version_string():
    """Return the Review Board version as a human-readable string."""
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] or VERSION[3]:
        version += b'.%s' % VERSION[2]
    if VERSION[3]:
        version += b'.%s' % VERSION[3]
    if VERSION[4] != b'final':
        if VERSION[4] == b'rc':
            version += b' RC%s' % VERSION[5]
        else:
            version += b' %s %s' % (VERSION[4], VERSION[5])
    if not is_release():
        version += b' (dev)'
    return version


def get_package_version():
    """Return the Review Board version as a Python package version string."""
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] or VERSION[3]:
        version += b'.%s' % VERSION[2]
    if VERSION[3]:
        version += b'.%s' % VERSION[3]
    if VERSION[4] != b'final':
        version += b'%s%s' % (VERSION[4], VERSION[5])
    return version


def is_release():
    """Return whether this is a released version of Review Board."""
    return VERSION[6]


def get_manual_url():
    """Return the URL to the Review Board manual for this version."""
    if VERSION[2] == 0 and VERSION[4] != b'final':
        manual_ver = b'dev'
    else:
        manual_ver = b'%s.%s' % (VERSION[0], VERSION[1])
    return b'https://www.reviewboard.org/docs/manual/%s/' % manual_ver


def initialize():
    """Begin initialization of Review Board.

    This sets up the logging, generates cache serial numbers, loads extensions,
    and sets up other aspects of Review Board. Once it has finished, it will
    fire the :py:data:`reviewboard.signals.initializing` signal.

    This must be called at some point before most features will work, but it
    will be called automatically in a standard install. If you are writing
    an extension or management command, you do not need to call this yourself.
    """
    import importlib, logging, os, settings_local
    os.environ[b'RBSITE_PYTHONPATH'] = os.path.dirname(settings_local.__file__)
    from django.conf import settings
    from django.db import DatabaseError
    from djblets import log
    from djblets.cache.serials import generate_ajax_serial
    from djblets.siteconfig.models import SiteConfiguration
    from reviewboard import signals
    from reviewboard.admin.siteconfig import load_site_config
    from reviewboard.extensions.base import get_extension_manager
    importlib.import_module(b'reviewboard.site.templatetags')
    is_running_test = getattr(settings, b'RUNNING_TEST', False)
    if not is_running_test:
        log.init_logging()
    load_site_config()
    if not is_running_test:
        if settings.DEBUG:
            logging.debug(b'Log file for Review Board v%s (PID %s)' % (
             get_version_string(), os.getpid()))
        generate_ajax_serial()
        if not getattr(settings, b'TEMPLATE_SERIAL', None):
            settings.TEMPLATE_SERIAL = settings.AJAX_SERIAL
    try:
        from django import setup
        setup()
    except ImportError:
        pass

    siteconfig = SiteConfiguration.objects.get_current()
    if not is_running_test and siteconfig.version == get_version_string():
        try:
            get_extension_manager().load()
        except DatabaseError:
            pass

    signals.initializing.send(sender=None)
    return


__version_info__ = VERSION[:-1]
__version__ = get_package_version()