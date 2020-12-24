# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/management/commands/runserver.py
# Compiled at: 2016-05-20 23:42:06
import platform, sys, django, wenlincms
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.staticfiles.management.commands import runserver
from django.core.management.color import supports_color
from django.db import connection
from django.http import Http404
from django.utils.termcolors import colorize
from django.views.static import serve

class MezzStaticFilesHandler(StaticFilesHandler):

    def _should_handle(self, path):
        return path.startswith((settings.STATIC_URL, settings.MEDIA_URL))

    def get_response(self, request):
        response = super(MezzStaticFilesHandler, self).get_response(request)
        if response.status_code == 404:
            locations = ((settings.STATIC_URL, settings.STATIC_ROOT),
             (
              settings.MEDIA_URL, settings.MEDIA_ROOT))
            for url, root in locations:
                if request.path.startswith(url):
                    path = request.path.replace(url, '', 1)
                    try:
                        return serve(request, path, document_root=root)
                    except Http404:
                        pass

        return response


def banner():
    conn = connection
    db_name = {'microsoft': 'sql server'}.get(conn.vendor, conn.vendor)
    db_name = '%s%s' % (db_name[:1].upper(),
     db_name.replace('sql', 'SQL').replace('db', 'DB')[1:])
    db_version_func = {'postgresql': lambda : (
                    conn.pg_version / 10000,
                    conn.pg_version % 10000 / 100,
                    conn.pg_version % 10000 % 100), 
       'mysql': lambda : conn.mysql_version, 
       'sqlite': lambda : conn.Database.sqlite_version_info, 
       'oracle': lambda : [
                conn.oracle_version], 
       'microsoft': lambda : [
                   conn._DatabaseWrapper__get_dbms_version()], 
       'firebird': lambda : conn.server_version.split(' ')[(-1)].split('.')}.get(conn.vendor, lambda : [])
    db_version = ('.').join(map(str, db_version_func()))
    lines = ("\n\n              .....\n          _d^^^^^^^^^b_\n       .d''           ``b.\n     .p'                `q.\n    .d'                   `b.\n   .d'                     `b.   * wenlincms %(wenlincms_version)s\n   ::                       ::   * Django %(django_version)s\n  ::    WENLINCMS    ::  * Python %(python_version)s\n   ::                       ::   * %(db_name)s %(db_version)s\n   `p.                     .q'   * %(os_name)s %(os_version)s\n    `p.                   .q'\n     `b.                 .d'\n       `q..          ..p'\n          ^q........p^\n              ''''\n\n\n" % {'wenlincms_version': wenlincms.__version__, 
       'django_version': django.get_version(), 
       'python_version': sys.version.split(' ', 1)[0], 
       'db_name': db_name, 
       'db_version': db_version, 
       'os_name': platform.system(), 
       'os_version': platform.release()}).splitlines()
    if django.VERSION >= (1, 7):
        lines = lines[2:]
    if not supports_color():
        return ('\n').join(lines)
    color_states = [
     (
      lambda c: c != ' ', {}),
     (
      lambda c: c == ' ', {'fg': 'red'}),
     (
      lambda c: c != ' ' and not c.isupper(), {'fg': 'white', 'bg': 'red', 'opts': ['bold']}),
     (
      lambda c: c == ' ', {'fg': 'red'}),
     (
      lambda c: c == '*', {}),
     (
      lambda c: c != '*', {'fg': 'red'}),
     (
      lambda c: False, {})]
    for i, line in enumerate(lines):
        chars = []
        color_state = 0
        for char in line:
            color_state += color_states[color_state][0](char)
            chars.append(colorize(char, **color_states[color_state][1]))

        lines[i] = ('').join(chars)

    return ('\n').join(lines)


class Command(runserver.Command):
    """
    Overrides runserver so that we can serve uploaded files
    during development, and not require every single developer on
    every single one of their projects to have to set up multiple
    web server aliases for serving static content.
    See https://code.djangoproject.com/ticket/15199

    For ease, we also serve any static files that have been stored
    under the project's ``STATIC_ROOT``.
    """

    def inner_run(self, *args, **kwargs):
        try:
            self.stdout.write(banner())
        except:
            pass

        super(Command, self).inner_run(*args, **kwargs)

    def get_handler(self, *args, **options):
        handler = super(Command, self).get_handler(*args, **options)
        if settings.DEBUG or options['insecure_serving']:
            handler = MezzStaticFilesHandler(handler)
        return handler