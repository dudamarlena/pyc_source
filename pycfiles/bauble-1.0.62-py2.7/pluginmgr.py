# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/pluginmgr.py
# Compiled at: 2016-10-03 09:39:22
"""
Manage plugin registry, loading, initialization and installation.  The
plugin manager should be started in the following order:

1. load the plugins: search the plugin directory for plugins,
populates the plugins dict (happens in load())

2. install the plugins if not in the registry, add properly
installed plugins in to the registry (happens in load())

3. initialize the plugins (happens in init())
"""
import logging
logger = logging.getLogger(__name__)
import types, os, re, sys, traceback, gtk
from bauble.i18n import _
from sqlalchemy import Column, Unicode, select
import sqlalchemy.orm.exc as orm_exc, bauble, bauble.db as db
from bauble.error import BaubleError
import bauble.paths as paths, bauble.utils as utils
plugins = {}
commands = {}

def register_command(handler):
    """
    Register command handlers.  If a command is a duplicate then it
    will overwrite the old command of the same name.

    :param handler:  A class which extends pluginmgr.CommandHandler
    """
    global commands
    logger.debug('registering command handler %s' % str(handler.command))
    if isinstance(handler.command, str):
        if handler.command in commands:
            logger.info('overwriting command %s' % handler.command)
        commands[handler.command] = handler
    else:
        for cmd in handler.command:
            if cmd in commands:
                logger.info('overwriting command %s' % cmd)
            commands[cmd] = handler


def _create_dependency_pairs(plugs):
    """calculate plugin dependencies, met and unmet

    plugs is an iterable of plugins.

    returned value is a pair, the first item is the dependency pairs that
    can be passed to utils.topological_sort.  The second item is a
    dictionary associating plugin names (from plugs) with the list of unmet
    dependencies.

    """
    depends = []
    unmet = {}
    for p in plugs:
        for dep in p.depends:
            try:
                depends.append((plugins[dep], p))
            except KeyError:
                logger.debug('no dependency %s for %s' % (dep, p.__name__))
                u = unmet.setdefault(p.__name__, [])
                u.append(dep)

    return (
     depends, unmet)


def load(path=None):
    """
    Search the plugin path for modules that provide a plugin. If path
    is a directory then search the directory for plugins. If path is
    None then use the default plugins path, bauble.plugins.

    This method populates the pluginmgr.plugins dict and imports the
    plugins but doesn't do any plugin initialization.

    :param path: the path where to look for the plugins
    :type path: str
    """
    if path is None:
        if bauble.main_is_frozen():
            path = os.path.join(paths.main_dir(), 'library.zip')
        else:
            path = os.path.join(paths.lib_dir(), 'plugins')
    logger.debug('pluginmgr.load(%s)' % path)
    found, errors = _find_plugins(path)
    logger.debug('found=%s, errors=%s' % (found, errors))
    if errors:
        name = (', ').join(sorted(errors.keys()))
        exc_info = errors.values()[0]
        exc_str = utils.xml_safe(exc_info[1])
        tb_str = ('').join(traceback.format_tb(exc_info[2]))
        utils.message_details_dialog('Could not load plugin: \n\n<i>%s</i>\n\n%s' % (
         name, exc_str), tb_str, type=gtk.MESSAGE_ERROR)
    if len(found) == 0:
        logger.debug('No plugins found at path: %s' % path)
    for plugin in found:
        if isinstance(plugin, (type, types.ClassType)):
            plugins[plugin.__name__] = plugin
            logger.debug('registering plugin %s: %s' % (
             plugin.__name__, plugin))
        else:
            plugins[plugin.__class__.__name__] = plugin
            logger.debug('registering plugin %s: %s' % (
             plugin.__class__.__name__, plugin))

    return


def init(force=False):
    """
    Initialize the plugin manager.

    1. Check for and install any plugins in the plugins dict that
    aren't in the registry.
    2. Call each init() for each plugin the registry in order of dependency
    3. Register the command handlers in the plugin's commands[]

    NOTE: This is called after after Ghini has created the GUI and
    established a connection to a database with db.open()

    """
    logger.debug('bauble.pluginmgr.init()')
    registered = plugins.values()
    logger.debug('registered plugins: %s' % plugins)
    try:
        registered_names = PluginRegistry.names()
        not_installed = [ p for n, p in plugins.iteritems() if n not in registered_names
                        ]
        if len(not_installed) > 0:
            msg = _('The following plugins were not found in the plugin registry:\n\n<b>%s</b>\n\n<i>Would you like to install them now?</i>') % (', ').join([ p.__class__.__name__ for p in not_installed ])
            if force or utils.yes_no_dialog(msg):
                install([ p for p in not_installed ])
        not_registered = []
        for name in PluginRegistry.names():
            try:
                registered.append(plugins[name])
            except KeyError as e:
                logger.debug("could not find '%s' plugin. removing from database" % e)
                not_registered.append(utils.utf8(name))
                PluginRegistry.remove(name=name)

        if not_registered:
            msg = _('The following plugins are in the registry but could not be loaded:\n\n%(plugins)s') % {'plugins': utils.utf8((', ').join(sorted(not_registered)))}
            utils.message_dialog(utils.xml_safe(msg), type=gtk.MESSAGE_WARNING)
    except Exception as e:
        logger.warning('unhandled exception %s' % e)
        raise

    if not registered:
        return
    else:
        deps, unmet = _create_dependency_pairs(registered)
        ordered = utils.topological_sort(registered, deps)
        if not ordered:
            raise BaubleError(_('The plugins contain a dependency loop. This can happen if two plugins directly or indirectly rely on each other'))
        for plugin in ordered:
            logger.debug('about to invoke init on: %s' % plugin)
            try:
                plugin.init()
                logger.debug('plugin %s initialized' % plugin)
            except KeyError as e:
                ordered.remove(plugin)
                msg = _("The %(plugin_name)s plugin is listed in the registry but isn't wasn't found in the plugin directory") % dict(plugin_name=plugin.__class__.__name__)
                logger.warning(msg)
            except Exception as e:
                logger.error(e)
                ordered.remove(plugin)
                logger.error(traceback.print_exc())
                safe = utils.xml_safe
                values = dict(entry_name=plugin.__class__.__name__, exception=safe(e))
                utils.message_details_dialog(_("Error: Couldn't initialize %(entry_name)s\n\n%(exception)s.") % values, traceback.format_exc(), gtk.MESSAGE_ERROR)

        for plugin in ordered:
            if plugin.commands in (None, []):
                continue
            for cmd in plugin.commands:
                try:
                    register_command(cmd)
                except Exception as e:
                    logger.debug('exception %s while registering command %s' % (
                     e, cmd))
                    msg = 'Error: Could not register command handler.\n\n%s' % utils.xml_safe(str(e))
                    utils.message_dialog(msg, gtk.MESSAGE_ERROR)

        if bauble.gui:
            bauble.gui.build_tools_menu()
        return


def install(plugins_to_install, import_defaults=True, force=False):
    """
    :param plugins_to_install: A list of plugins to install. If the
        string "all" is passed then install all plugins listed in the
        bauble.pluginmgr.plugins dict that aren't already listed in
        the plugin registry.

    :param import_defaults: Flag passed to the plugin's install()
        method to indicate whether it should import its default data.
    :type import_defaults: bool

    :param force:  Force, don't ask questions.
    :type force: book
    """
    logger.debug('pluginmgr.install(%s)' % str(plugins_to_install))
    if plugins_to_install is 'all':
        to_install = plugins.values()
    else:
        to_install = plugins_to_install
    if len(to_install) == 0:
        return
    depends, unmet = _create_dependency_pairs(to_install)
    if unmet != {}:
        logger.debug(unmet)
        raise BaubleError('unmet dependencies')
    to_install = utils.topological_sort(to_install, depends)
    if not to_install:
        raise BaubleError(_('The plugins contain a dependency loop. This can happend if two plugins directly or indirectly rely on each other'))
    try:
        for p in to_install:
            logger.debug('install: %s' % p)
            p.install(import_defaults=import_defaults)
            if not PluginRegistry.exists(p):
                PluginRegistry.add(p)

    except Exception as e:
        logger.warning('bauble.pluginmgr.install(): %s' % utils.utf8(e))
        raise


class PluginRegistry(db.Base):
    """
    The PluginRegistry contains a list of plugins that have been installed
    in a particular instance of a Ghini database.  At the moment it only
    includes the name and version of the plugin but this is likely to change
    in future versions.
    """
    __tablename__ = 'plugin'
    name = Column(Unicode(64), unique=True)
    version = Column(Unicode(12))

    @staticmethod
    def add(plugin):
        """
        Add a plugin to the registry.

        Warning: Adding a plugin to the registry does not install it.  It
        should be installed before adding.
        """
        p = PluginRegistry(name=utils.utf8(plugin.__class__.__name__), version=utils.utf8(plugin.version))
        session = db.Session()
        session.add(p)
        session.commit()
        session.close()

    @staticmethod
    def remove(plugin=None, name=None):
        """
        Remove a plugin from the registry by name.
        """
        if name is None:
            name = plugin.__class__.__name__
        session = db.Session()
        p = session.query(PluginRegistry).filter_by(name=utils.utf8(name)).one()
        session.delete(p)
        session.commit()
        session.close()
        return

    @staticmethod
    def all(session):
        close_session = False
        if not session:
            close_session = True
            session = db.Session()
        q = session.query(PluginRegistry)
        results = list(q)
        if close_session:
            session.close()
        return results

    @staticmethod
    def names(bind=None):
        t = PluginRegistry.__table__
        results = select([t.c.name], bind=bind).execute(bind=bind)
        names = [ n[0] for n in results ]
        results.close()
        return names

    @staticmethod
    def exists(plugin):
        """
        Check if plugin exists in the plugin registry.
        """
        if isinstance(plugin, basestring):
            name = plugin
            version = None
        else:
            name = plugin.__class__.__name__
            version = plugin.version
        session = db.Session()
        try:
            try:
                logger.debug('not using value of version (%s).' % version)
                session.query(PluginRegistry).filter_by(name=utils.utf8(name)).one()
                return True
            except orm_exc.NoResultFound as e:
                logger.debug(e)
                return False

        finally:
            session.close()

        return


class Plugin(object):
    """
    tools:
      a list of BaubleTool classes that this plugin provides, the
      tools' category and label will be used in Ghini's "Tool" menu
    depends:
      a list of names classes that inherit from BaublePlugin that this
      plugin depends on
    cmds:
      a map of commands this plugin handled with callbacks,
      e.g dict('cmd', lambda x: handler)
    description:
      a short description of the plugin
    """
    commands = []
    tools = []
    depends = []
    description = ''
    version = '0.0'

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def init(cls):
        """
        init() is run when Ghini is first started
        """
        pass

    @classmethod
    def install(cls, import_defaults=True):
        """
        install() is run when a new plugin is installed, it is usually
        only run once for the lifetime of the plugin
        """
        pass


class EditorPlugin(Plugin):
    """
    a plugin that provides one or more editors, the editors should
    implement the Editor interface
    """
    editors = []


class Tool(object):
    category = None
    label = None
    enabled = True

    @classmethod
    def start(cls):
        pass


class View(gtk.VBox):

    def __init__(self, *args, **kwargs):
        """
        If a class extends this View and provides its own __init__ it *must*
        call its parent (this) __init__
        """
        filename = kwargs.get('filename')
        if filename is not None:
            del kwargs['filename']
            root_widget_name = kwargs.get('root_widget_name')
            del kwargs['root_widget_name']
        super(View, self).__init__(*args, **kwargs)
        if filename is not None:
            from bauble import utils, editor
            self.widgets = utils.load_widgets(filename)
            self.view = editor.GenericEditorView(filename, root_widget_name=root_widget_name)
            root_widget = getattr(self.view.widgets, root_widget_name)
            widget = root_widget.get_children()[0]
            self.view.widgets.remove_parent(widget)
            self.add(widget)
        self.running_threads = []
        return

    def cancel_threads(self):
        for k in self.running_threads:
            k.cancel()

        for k in self.running_threads:
            k.join()

        self.running_threads = []

    def start_thread(self, thread):
        self.running_threads.append(thread)
        thread.start()
        return thread

    def update(self):
        pass


class CommandHandler(object):
    command = None

    def get_view(self):
        """
        return the  view for this command handler
        """
        return

    def __call__(self, cmd, arg):
        """
        do what this command handler does

        :param arg:
        """
        raise NotImplementedError


def _find_module_names(path):
    """
    :param path: where to look for modules
    """
    modules = []
    if path.find('library.zip') != -1:
        from zipfile import ZipFile
        z = ZipFile(path)
        filenames = z.namelist()
        rx = re.compile('(.+)\\__init__.py[oc]')
        for f in filenames:
            m = rx.match(f)
            if m is not None:
                modules.append(m.group(1).replace('/', '.')[:-1])

        z.close()
    else:
        for dir, subdir, files in os.walk(path):
            if dir != path and '__init__.py' in files:
                modules.append(dir[len(path) + 1:].replace(os.sep, '.'))

    return modules


def _find_plugins(path):
    """
    Return the plugins at path.
    """
    plugins = []
    import bauble.plugins
    plugin_module = bauble.plugins
    errors = {}
    if path.find('library.zip') != -1:
        plugin_names = [ m for m in _find_module_names(path) if m.startswith('bauble.plugins') ]
    else:
        plugin_names = [ 'bauble.plugins.%s' % m for m in _find_module_names(path)
                       ]
    for name in plugin_names:
        mod = None
        if name in sys.modules:
            mod = sys.modules[name]
        else:
            try:
                mod = __import__(name, globals(), locals(), [name], -1)
            except Exception as e:
                msg = _('Could not import the %(module)s module.\n\n%(error)s') % {'module': name, 'error': e}
                logger.debug(msg)
                errors[name] = sys.exc_info()

            if not hasattr(mod, 'plugin'):
                continue
            try:
                mod_plugin = mod.plugin()
                logger.debug('module %s contains callable plugin: %s' % (
                 mod, mod_plugin))
            except:
                mod_plugin = mod.plugin
                logger.debug('module %s contains non callable plugin: %s' % (
                 mod, mod_plugin))

        is_plugin_class = lambda p: isinstance(p, (type, types.ClassType)) and issubclass(p, Plugin)
        is_plugin_instance = lambda p: isinstance(p, Plugin)
        if isinstance(mod_plugin, (list, tuple)):
            for p in mod_plugin:
                if is_plugin_class(p):
                    logger.debug('append plugin class %s:%s' % (name, p))
                    plugins.append(p())
                elif is_plugin_instance(p):
                    logger.debug('append plugin instance %s:%s' % (name, p))
                    plugins.append(p)

        elif is_plugin_class(mod_plugin):
            logger.debug('append plugin class %s:%s' % (name, mod_plugin))
            plugins.append(mod_plugin())
        elif is_plugin_instance(mod_plugin):
            logger.debug('append plugin instance %s:%s' % (name, mod_plugin))
            plugins.append(mod_plugin)
        else:
            logger.warning(_('%s.plugin is not an instance of pluginmgr.Plugin') % mod.__name__)

    return (
     plugins, errors)