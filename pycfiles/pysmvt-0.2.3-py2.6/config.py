# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/config.py
# Compiled at: 2010-05-30 13:30:03
from os import path
import os, logging, re
from pysmvt import appimport, settings, ag, modimport
from pysmvt.logs import _create_handlers_from_settings
from werkzeug.routing import Rule, Map, Submount
from pysmvt.utils import OrderedDict, Context, tb_depth_in
from pysmvt.utils.filesystem import mkdirs
from pysmvt.exceptions import SettingsError
from pysutils import case_us2cw, multi_pop
from pysutils.config import QuickSettings

class ModulesSettings(QuickSettings):
    """
        a custom settings object for settings.modules.  The only difference
        is that when iterating over the object, only modules with
        .enabled = True are returned.
    """

    def _set_data_item(self, item, value):
        if not isinstance(value, QuickSettings):
            raise TypeError('all values set on ModuleSettings must be a QuickSettings object')
        QuickSettings._set_data_item(self, item, value)

    def __len__(self):
        return len(self.keys())

    def iteritems(self, showinactive=False):
        for (k, v) in self._data.iteritems():
            try:
                if showinactive or v.enabled == True:
                    yield (
                     k, v)
            except AttributeError, e:
                if "object has no attribute 'enabled'" not in str(e):
                    raise

    def __iter__(self):
        for v in self._data.values():
            try:
                if v.enabled == True:
                    yield v
            except AttributeError, e:
                if "object has no attribute 'enabled'" not in str(e):
                    raise

    def __contains__(self, key):
        return key in self.todict()

    def keys(self, showinactive=False):
        return [ k for (k, v) in self.iteritems(showinactive) ]

    def values(self, showinactive=False):
        return [ v for (k, v) in self.iteritems(showinactive) ]

    def todict(self, showinactive=False):
        if showinactive:
            return self._data
        d = OrderedDict()
        for (k, v) in self.iteritems():
            d[k] = v

        return d


class DefaultSettings(QuickSettings):

    def __init__(self, appname, basedir):
        QuickSettings.__init__(self)
        self.appname = appname
        self.supporting_apps = []
        self.modules = ModulesSettings()
        self.routing.routes = [
         Rule('/[pysmvt_test]', endpoint='[pysmvt_test]')]
        self.routing.prefix = ''
        self.routing.map.default_subdomain = ''
        self.routing.map.charset = 'utf-8'
        self.routing.map.strict_slashes = True
        self.routing.map.redirect_defaults = True
        self.routing.map.converters = None
        self.dirs.base = basedir
        self.dirs.writeable = path.join(basedir, 'writeable')
        self.dirs.static = path.join(basedir, 'static')
        self.dirs.templates = path.join(basedir, 'templates')
        self.dirs.data = path.join(self.dirs.writeable, 'data')
        self.dirs.logs = path.join(self.dirs.writeable, 'logs')
        self.dirs.tmp = path.join(self.dirs.writeable, 'tmp')
        self.beaker.type = 'dbm'
        self.beaker.data_dir = path.join(self.dirs.tmp, 'session_cache')
        self.beaker.lock_dir = path.join(self.dirs.tmp, 'beaker_locks')
        self.template.default = 'default.html'
        self.endpoint.sys_error = ''
        self.endpoint.sys_auth_error = ''
        self.endpoint.bad_request_error = ''
        self.exceptions.to_client = False
        self.exceptions.hide = False
        self.exceptions.email = False
        self.exceptions.log = True
        self.debugger.enabled = True
        self.debugger.interactive = False
        self.emails.from_server = ''
        self.emails.from_default = ''
        self.emails.reply_to = ''
        self.emails.cc_always = None
        self.emails.cc_defaults = None
        self.emails.bcc_always = None
        self.emails.bcc_defaults = None
        self.emails.programmers = None
        self.emails.admins = None
        self.emails.override = None
        self.email.subject_prefix = ''
        self.email.is_live = True
        self.smtp.host = 'localhost'
        self.smtp.port = 25
        self.smtp.user = ''
        self.smtp.password = ''
        self.smtp.use_tls = False
        self.default_charset = 'utf-8'
        self.default.file_mode = 416
        self.default.dir_mode = 488
        self.error_docs
        self.testing.init_callables = None
        self.logs.max_bytes = 10485760
        self.logs.backup_count = 5
        self.logs.errors.enabled = True
        self.logs.application.enabled = True
        self.logs.null_handler.enabled = False
        return


def appinit(settings_mod=None, profile=None, settings_cls=None):
    """
        called to setup the application's settings
        variable
    """
    if settings_cls is None:
        Settings = getattr(settings_mod, profile)
    else:
        Settings = settings_cls
    settings._push_object(Settings())
    ag._push_object(Context())
    level1map = {'critical': logging.CRITICAL, 
       'fatal': logging.FATAL, 
       'error': logging.ERROR, 
       'warning': logging.WARNING, 
       'warn': logging.WARN, 
       'info': logging.INFO, 
       'debug': logging.DEBUG}
    keywords = ('enabled', 'filter', 'date_format', 'format')
    if settings.has_key('logging') and settings.logging.get('enabled', True):
        for level1 in settings.logging.keys():
            l1_value = settings.logging[level1]
            p = re.compile('L\\d\\d?$')
            match = p.match(level1)
            if level1.lower() in level1map:
                logger_level = level1map[level1.lower()]
            elif match:
                logger_level = int(match.group().lstrip('L'))
                if logger_level < 0 or logger_level > 50:
                    SettingsError('Invalid logging key: %s' % level1)
            elif level1 in keywords:
                if level1 == 'filter':
                    default_filter = logging.Filter(settings.logging.filter)
                    continue
                elif level1 == 'format':
                    default_format = logging.Formatter(settings.logging.format)
                    continue
                elif level1 == 'date_format':
                    continue
                else:
                    continue
            else:
                raise SettingsError('Invalid logging key: %s' % level1)
            if not l1_value.get('enabled', True):
                continue
            logger = logging.getLogger()
            logger.setLevel(logger_level)
            for l2_key in l1_value.keys():
                l2_value = l1_value[l2_key]
                if l2_key in keywords:
                    continue
                handler_name = case_us2cw(l2_key) + 'Handler'
                if not hasattr(logging, handler_name):
                    raise SettingsError('Invalid handler: %s' % l2_key)
                handler_args = l2_value.todict()
                handler_kw = multi_pop(handler_args, *keywords)
                if not handler_kw.get('enabled', True):
                    continue
                handler = getattr(logging, handler_name)(**handler_args)
                filter = handler_kw.get('filter') or l1_value.get('filter') or settings.logging.get('filter')
                format = handler_kw.get('format') or l1_value.get('format') or settings.logging.get('format')
                date_format = handler_kw.get('date_format') or l1_value.get('date_format') or settings.logging.get('date_format')
                if filter:
                    handler.addFilter(logging.Filter(filter))
                if format or date_format:
                    handler.setFormatter(logging.Formatter(format, date_format))
                logger.addHandler(handler)

    mkdirs(settings.dirs.data)
    mkdirs(settings.dirs.logs)
    mkdirs(settings.dirs.tmp)
    for module in settings.modules.keys():
        try:
            Settings = modimport('%s.settings' % module, 'Settings')
            ms = Settings()
            ms.update(settings.modules[module])
            settings.modules[module] = ms
        except ImportError:
            if not tb_depth_in(3):
                raise

    settings.lock()
    _create_handlers_from_settings(settings)
    ag.route_map = Map(**settings.routing.map.todict())
    _add_routing_rules(settings.routing.routes)
    for module in settings.modules:
        if hasattr(module, 'routes'):
            _add_routing_rules(module.routes)

    return


def _add_routing_rules(rules):
    if settings.routing.prefix:
        ag.route_map.add(Submount(settings.routing.prefix, rules))
    for rule in rules or ():
        ag.route_map.add(rule)


def appslist(reverse=False):
    if reverse:
        apps = list(settings.supporting_apps)
        apps.reverse()
        apps.append(settings.appname)
        return apps
    return [
     settings.appname] + settings.supporting_apps