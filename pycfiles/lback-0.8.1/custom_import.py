# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/custom_import.py
# Compiled at: 2013-10-14 11:16:25
import __builtin__, os, sys, threading, traceback
from gluon import current
NATIVE_IMPORTER = __builtin__.__import__
INVALID_MODULES = set(('', 'gluon', 'applications', 'custom_import'))

def custom_import_install():
    if __builtin__.__import__ == NATIVE_IMPORTER:
        INVALID_MODULES.update(sys.modules.keys())
        __builtin__.__import__ = custom_importer


def track_changes(track=True):
    assert track in (True, False), 'must be True or False'
    current.request._custom_import_track_changes = track


def is_tracking_changes():
    return current.request._custom_import_track_changes


class CustomImportException(ImportError):
    pass


def custom_importer(name, globals=None, locals=None, fromlist=None, level=-1):
    """
    The web2py custom importer. Like the standard Python importer but it
    tries to transform import statements as something like
    "import applications.app_name.modules.x".
    If the import failed, fall back on naive_importer
    """
    globals = globals or {}
    locals = locals or {}
    fromlist = fromlist or []
    try:
        if current.request._custom_import_track_changes:
            base_importer = TRACK_IMPORTER
        else:
            base_importer = NATIVE_IMPORTER
    except:
        base_importer = NATIVE_IMPORTER

    if hasattr(current, 'request') and level <= 0 and name.partition('.')[0] not in INVALID_MODULES and isinstance(globals, dict):
        import_tb = None
        try:
            try:
                try:
                    oname = name if not name.startswith('.') else '.' + name
                    return NATIVE_IMPORTER(oname, globals, locals, fromlist, level)
                except ImportError:
                    items = current.request.folder.split(os.path.sep)
                    if not items[(-1)]:
                        items = items[:-1]
                    modules_prefix = ('.').join(items[-2:]) + '.modules'
                    if not fromlist:
                        result = None
                        for itemname in name.split('.'):
                            new_mod = base_importer(modules_prefix, globals, locals, [itemname], level)
                            try:
                                result = result or new_mod.__dict__[itemname]
                            except KeyError as e:
                                raise ImportError, 'Cannot import module %s' % str(e)

                            modules_prefix += '.' + itemname

                        return result
                    pname = modules_prefix + '.' + name
                    return base_importer(pname, globals, locals, fromlist, level)

            except ImportError as e1:
                import_tb = sys.exc_info()[2]
                try:
                    return NATIVE_IMPORTER(name, globals, locals, fromlist, level)
                except ImportError as e3:
                    raise ImportError, e1, import_tb

            except Exception as e2:
                raise e2

        finally:
            if import_tb:
                import_tb = None

    return NATIVE_IMPORTER(name, globals, locals, fromlist, level)


class TrackImporter(object):
    """
    An importer tracking the date of the module files and reloading them when
    they have changed.
    """
    THREAD_LOCAL = threading.local()
    PACKAGE_PATH_SUFFIX = os.path.sep + '__init__.py'

    def __init__(self):
        self._import_dates = {}

    def __call__(self, name, globals=None, locals=None, fromlist=None, level=-1):
        """
        The import method itself.
        """
        globals = globals or {}
        locals = locals or {}
        fromlist = fromlist or []
        try:
            self._update_dates(name, globals, locals, fromlist, level)
            result = NATIVE_IMPORTER(name, globals, locals, fromlist, level)
            self._update_dates(name, globals, locals, fromlist, level)
            return result
        except Exception as e:
            raise

    def _update_dates(self, name, globals, locals, fromlist, level):
        """
        Update all the dates associated to the statement import. A single
        import statement may import many modules.
        """
        self._reload_check(name, globals, locals, level)
        for fromlist_name in fromlist or []:
            pname = '%s.%s' % (name, fromlist_name)
            self._reload_check(pname, globals, locals, level)

    def _reload_check(self, name, globals, locals, level):
        """
        Update the date associated to the module and reload the module if
        the file has changed.
        """
        module = sys.modules.get(name)
        file = self._get_module_file(module)
        if file:
            date = self._import_dates.get(file)
            new_date = None
            reload_mod = False
            mod_to_pack = False
            try:
                new_date = os.path.getmtime(file)
            except:
                self._import_dates.pop(file, None)
                if file.endswith('.py'):
                    file = os.path.splitext(file)[0]
                    reload_mod = os.path.isdir(file) and os.path.isfile(file + self.PACKAGE_PATH_SUFFIX)
                    mod_to_pack = reload_mod
                else:
                    file += '.py'
                    reload_mod = os.path.isfile(file)
                if reload_mod:
                    new_date = os.path.getmtime(file)

            if reload_mod or not date or new_date > date:
                self._import_dates[file] = new_date
            if reload_mod or date and new_date > date:
                if mod_to_pack:
                    mod_name = module.__name__
                    del sys.modules[mod_name]
                    NATIVE_IMPORTER(mod_name, globals, locals, [], level)
                else:
                    reload(module)
        return

    def _get_module_file(self, module):
        """
        Get the absolute path file associated to the module or None.
        """
        file = getattr(module, '__file__', None)
        if file:
            file = os.path.splitext(file)[0] + '.py'
            if file.endswith(self.PACKAGE_PATH_SUFFIX):
                file = os.path.dirname(file)
        return file


TRACK_IMPORTER = TrackImporter()