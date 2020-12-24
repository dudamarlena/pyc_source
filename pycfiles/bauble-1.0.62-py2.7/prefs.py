# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/prefs.py
# Compiled at: 2016-10-03 09:39:22
import os, gtk, logging
logger = logging.getLogger(__name__)
import bauble
from bauble.i18n import _
import bauble.db as db, bauble.paths as paths, bauble.pluginmgr as pluginmgr
testing = False
default_filename = 'config'
default_prefs_file = os.path.join(paths.appdata_dir(), default_filename)
config_version_pref = 'bauble.config.version'
config_version = (
 bauble.version_tuple[0], bauble.version_tuple[1])
date_format_pref = 'bauble.default_date_format'
picture_root_pref = 'bauble.picture_root'
parse_dayfirst_pref = 'bauble.parse_dayfirst'
parse_yearfirst_pref = 'bauble.parse_yearfirst'
units_pref = 'bauble.units'
use_sentry_client_pref = 'bauble.use_sentry_client'
from ConfigParser import RawConfigParser

class _prefs(dict):

    def __init__(self, filename=default_prefs_file):
        self._filename = filename

    def init(self):
        """
        initialize the preferences, should only be called from app.main
        """
        head, tail = os.path.split(self._filename)
        if not os.path.exists(head):
            os.makedirs(head)
        self.config = RawConfigParser()
        if not os.path.exists(self._filename):
            self[config_version_pref] = config_version
        else:
            self.config.read(self._filename)
        version = self[config_version_pref]
        if version is None:
            logger.warning('%s has no config version pref' % self._filename)
            logger.warning('setting the config version to %s.%s' % config_version)
            self[config_version_pref] = config_version
        if use_sentry_client_pref not in self:
            self[use_sentry_client_pref] = False
        if picture_root_pref not in self:
            self[picture_root_pref] = ''
        if date_format_pref not in self:
            self[date_format_pref] = '%d-%m-%Y'
        if parse_dayfirst_pref not in self:
            format = self[date_format_pref]
            if format.find('%d') < format.find('%m'):
                self[parse_dayfirst_pref] = True
            else:
                self[parse_dayfirst_pref] = False
        if parse_yearfirst_pref not in self:
            format = self[date_format_pref]
            if format.find('%Y') == 0 or format.find('%y') == 0:
                self[parse_yearfirst_pref] = True
            else:
                self[parse_yearfirst_pref] = False
        if units_pref not in self:
            self[units_pref] = 'metric'
        return

    @staticmethod
    def _parse_key(name):
        index = name.rfind('.')
        return (name[:index], name[index + 1:])

    def get(self, key, default):
        """
        get value for key else return default
        """
        value = self[key]
        if value is None:
            return default
        else:
            return value

    def __getitem__(self, key):
        section, option = _prefs._parse_key(key)
        if not self.config.has_section(section) or not self.config.has_option(section, option):
            return
        i = self.config.get(section, option)
        eval_chars = '{[('
        if i == '':
            return i
        else:
            if i[0] in eval_chars:
                return eval(i)
            else:
                if i == 'True' or i == 'False':
                    return eval(i)
                return i

            return

    def iteritems(self):
        global prefs
        return [ ('%s.%s' % (section, name), value) for section in sorted(prefs.config.sections()) for name, value in prefs.config.items(section) ]

    def __setitem__(self, key, value):
        section, option = _prefs._parse_key(key)
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def __contains__(self, key):
        section, option = _prefs._parse_key(key)
        if self.config.has_section(section) and self.config.has_option(section, option):
            return True
        return False

    def save(self, force=False):
        if testing and not force:
            return
        else:
            try:
                f = open(self._filename, 'w+')
                self.config.write(f)
                f.close()
            except Exception:
                msg = _("Ghini can't save your user preferences. \n\nPlease check the file permissions of your config file:\n %s") % self._filename
                if bauble.gui is not None and bauble.gui.window is not None:
                    import bauble.utils as utils
                    utils.message_dialog(msg, type=gtk.MESSAGE_ERROR, parent=bauble.gui.window)
                else:
                    logger.error(msg)

            return


class PrefsView(pluginmgr.View):
    """
    The PrefsView displays the values of in the preferences and the registry.
    """
    pane_size_pref = 'bauble.prefs.pane_position'

    def __init__(self):
        logger.debug('PrefsView::__init__')
        super(PrefsView, self).__init__(filename=os.path.join(paths.lib_dir(), 'bauble.glade'), root_widget_name='prefs_window')
        self.view.connect_signals(self)
        self.prefs_ls = self.view.widgets.prefs_prefs_ls
        self.plugins_ls = self.view.widgets.prefs_plugins_ls
        self.update()

    def on_prefs_prefs_tv_row_activated(self, tv, path, column):
        modified = False
        key, repr_str, type_str = self.prefs_ls[path]
        if type_str == 'bool':
            self.prefs_ls[path][1] = prefs[key] = not prefs[key]
            modified = True
        if modified:
            prefs.save()

    def update(self):
        self.widgets.prefs_prefs_ls.clear()
        for key, value in sorted(prefs.iteritems()):
            self.widgets.prefs_prefs_ls.append((
             key, value, prefs[key].__class__.__name__))

        self.widgets.prefs_plugins_ls.clear()
        from bauble.pluginmgr import PluginRegistry
        session = db.Session()
        plugins = session.query(PluginRegistry.name, PluginRegistry.version)
        for item in plugins:
            self.widgets.prefs_plugins_ls.append(item)

        session.close()


class PrefsCommandHandler(pluginmgr.CommandHandler):
    command = ('prefs', 'config')
    view = None

    def __call__(self, cmd, arg):
        pass

    def get_view(self):
        if self.view is None:
            self.__class__.view = PrefsView()
        return self.view


pluginmgr.register_command(PrefsCommandHandler)
prefs = _prefs()