# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\startup.py
# Compiled at: 2013-12-18 14:05:11
import argparse, os, tempfile, sys, struct
from .struct import listwrap
from .cnv import CNV
from .logs import Log
from .files import File

def _argparse(defs):
    parser = argparse.ArgumentParser()
    for d in listwrap(defs):
        args = d.copy()
        name = args.name
        args.name = None
        parser.add_argument(*listwrap(name).list, **args.dict)

    namespace = parser.parse_args()
    output = {k:getattr(namespace, k) for k in vars(namespace)}
    return struct.wrap(output)


def read_settings(filename=None, defs=None):
    if filename:
        settings_file = File(filename)
        if not settings_file.exists:
            Log.error('Can not file settings file {{filename}}', {'filename': settings_file.abspath})
        json = settings_file.read()
        settings = CNV.JSON2object(json, flexible=True)
        if defs:
            settings.args = _argparse(defs)
        return settings
    defs = listwrap(defs)
    defs.append({'name': [
              '--settings', '--settings-file', '--settings_file'], 
       'help': 'path to JSON file with settings', 
       'type': str, 
       'dest': 'filename', 
       'default': './settings.json', 
       'required': False})
    args = _argparse(defs)
    settings_file = File(args.filename)
    if not settings_file.exists:
        Log.error('Can not file settings file {{filename}}', {'filename': settings_file.abspath})
    json = settings_file.read()
    settings = CNV.JSON2object(json, flexible=True)
    settings.args = args
    return settings


class SingleInstance:
    """
    ONLY ONE INSTANCE OF PROGRAM ALLOWED
    If you want to prevent your script from running in parallel just instantiate SingleInstance() class.
    If is there another instance already running it will exist the application with the message
    "Another instance is already running, quitting.", returning -1 error code.

    me = SingleInstance()

    This option is very useful if you have scripts executed by crontab at small amounts of time.

    Remember that this works by creating a lock file with a filename based on the full path to the script file.
    """

    def __init__(self, flavor_id=''):
        import sys
        self.initialized = False
        basename = os.path.splitext(os.path.abspath(sys.argv[0]))[0].replace('/', '-').replace(':', '').replace('\\', '-') + '-%s' % flavor_id + '.lock'
        self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + basename)

    def __enter__(self):
        Log.debug('SingleInstance lockfile: ' + self.lockfile)
        if sys.platform == 'win32':
            try:
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except Exception as e:
                Log.warning('Another instance is already running, quitting.', e)
                sys.exit(-1)

        else:
            import fcntl
            self.fp = open(self.lockfile, 'w')
            try:
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                Log.warning('Another instance is already running, quitting.')
                sys.exit(-1)

        self.initialized = True

    def __exit__(self, type, value, traceback):
        self.__del__()

    def __del__(self):
        import sys, os
        temp, self.initialized = self.initialized, False
        if not temp:
            return
        try:
            if sys.platform == 'win32':
                if hasattr(self, 'fd'):
                    os.close(self.fd)
                    os.unlink(self.lockfile)
            else:
                import fcntl
                fcntl.lockf(self.fp, fcntl.LOCK_UN)
                if os.path.isfile(self.lockfile):
                    os.unlink(self.lockfile)
        except Exception as e:
            Log.warning('Problem with SingleInstance __del__()', e)
            sys.exit(-1)