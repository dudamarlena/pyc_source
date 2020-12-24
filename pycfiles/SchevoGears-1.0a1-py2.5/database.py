# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevogears/database.py
# Compiled at: 2008-01-19 12:10:14
"""Schevo-specific addins for TurboGears.

XXX: The locking mechanisms employed here are not thoroughly tested in
the face of failure.  Use carefully for now!

For copyright, license, and warranty, see bottom of file.
"""
import pkg_resources
pkg_resources.require('TurboGears')
import schevo.database, schevo.mt, turbogears
open_schevo_databases = {}

def package_database(package_name=None):
    """A Schevo database wrapper that looks for the filename based on a
    package name, or is None if no filename was found."""
    global open_schevo_databases
    if package_name in open_schevo_databases:
        return open_schevo_databases[package_name]
    filename = None
    if package_name:
        filename = turbogears.config.get('%s.schevo.dbfile' % package_name, None)
    if not filename:
        filename = turbogears.config.get('schevo.dbfile', None)
    if filename:
        db = schevo.database.open(filename)
        schevo.mt.install(db)
        open_schevo_databases[package_name] = db
        return db
    return


from cherrypy.lib import autoreload
_restart_with_reloader = autoreload.restart_with_reloader

def restart_with_reloader():
    global open_schevo_databases
    for db in open_schevo_databases.values():
        db.close()

    open_schevo_databases = {}
    return _restart_with_reloader()


autoreload.restart_with_reloader = restart_with_reloader