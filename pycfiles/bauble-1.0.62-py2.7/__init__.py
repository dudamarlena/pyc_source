# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/__init__.py
# Compiled at: 2016-09-10 10:29:08
"""
The top level module for Ghini.
"""
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleLevel = logging.INFO
import imp, os, sys, bauble.paths as paths
from bauble.version import version
version_tuple = tuple(version.split('.'))
from bauble.i18n import _

def pb_set_fraction(fraction):
    """set progressbar fraction safely

    provides a safe way to handle the progress bar if the gui isn't started,
    we use this in the tests where there is no gui
    """
    global gui
    if gui is not None and gui.progressbar is not None:
        gui.progressbar.set_fraction(fraction)
    return


def main_is_frozen():
    """
    Return True if we are running in a py2exe environment, else
    return False
    """
    return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')


if main_is_frozen():
    zipfile = sys.path[(-1)]
    sys.path.insert(0, zipfile)
    os.environ['PATH'] = '%s%s%s%s%s%s' % (
     os.pathsep, os.path.join(paths.main_dir(), 'gtk', 'bin'),
     os.pathsep, os.path.join(paths.main_dir(), 'gtk', 'lib'),
     os.pathsep, os.environ['PATH'])
sys.path.append(paths.lib_dir())
import logging
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
gui = None
default_icon = None
conn_name = None
import traceback, bauble.error as err

def save_state():
    """
    Save the gui state and preferences.
    """
    from bauble.prefs import prefs
    if gui is not None:
        gui.save_state()
    prefs.save()
    return


def quit():
    """
    Stop all tasks and quit Ghini.
    """
    import gtk, bauble.utils as utils
    try:
        import bauble.task as task
    except Exception as e:
        logger.error('bauble.quit(): %s' % utils.utf8(e))
    else:
        task.kill()

    try:
        save_state()
        gtk.main_quit()
    except RuntimeError as e:
        sys.exit(1)


last_handler = None

def command_handler(cmd, arg):
    """
    Call a command handler.

    :param cmd: The name of the command to call
    :type cmd: str

    :param arg: The arg to pass to the command handler
    :type arg: list
    """
    global last_handler
    logger.debug('entering ui.command_handler %s %s' % (cmd, arg))
    import gtk, bauble.utils as utils, bauble.pluginmgr as pluginmgr
    handler_cls = None
    try:
        handler_cls = pluginmgr.commands[cmd]
    except KeyError as e:
        if cmd is None:
            utils.message_dialog(_('No default handler registered'))
        else:
            utils.message_dialog(_('No command handler for %s') % cmd)
            return

    if not isinstance(last_handler, handler_cls):
        last_handler = handler_cls()
    handler_view = last_handler.get_view()
    old_view = gui.get_view()
    if type(old_view) != type(handler_view) and handler_view:
        if hasattr(old_view, 'accel_group'):
            gui.window.remove_accel_group(old_view.accel_group)
        gui.set_view(handler_view)
        if hasattr(handler_view, 'accel_group'):
            gui.window.add_accel_group(handler_view.accel_group)
    try:
        last_handler(cmd, arg)
    except Exception as e:
        msg = utils.xml_safe(e)
        logger.error('bauble.command_handler(): %s' % msg)
        utils.message_details_dialog(msg, traceback.format_exc(), gtk.MESSAGE_ERROR)

    return


conn_default_pref = 'conn.default'
conn_list_pref = 'conn.list'

def main(uri=None):
    """
    Run the main Ghini application.

    :param uri:  the URI of the database to connect to.  For more information
                 about database URIs see `<http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments>`_

    :type uri: str
    """
    global conn_name
    global default_icon
    global gui
    try:
        import gtk, gobject
    except ImportError as e:
        print _('** Error: could not import gtk and/or gobject')
        print e
        if sys.platform == 'win32':
            print _('Please make sure that GTK_ROOT\\bin is in your PATH.')
        sys.exit(1)

    if not os.path.exists(paths.appdata_dir()):
        os.makedirs(paths.appdata_dir())
    filename = os.path.join(paths.appdata_dir(), 'bauble.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(filename, 'w+')
    logging.getLogger().addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    logging.getLogger().addHandler(consoleHandler)
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    consoleHandler.setLevel(consoleLevel)
    from bauble.prefs import prefs, use_sentry_client_pref
    prefs.init()
    try:
        from raven import Client
        from raven.handlers.logging import SentryHandler
        if prefs[use_sentry_client_pref]:
            logger.debug('registering sentry client')
            sentry_client = Client('https://59105d22a4ad49158796088c26bf8e4c:00268114ed47460b94ce2b1b0b2a4a20@app.getsentry.com/45704')
            handler = SentryHandler(sentry_client)
            logging.getLogger().addHandler(handler)
            handler.setLevel(logging.WARNING)
        else:
            logger.debug('not registering sentry client')
    except Exception as e:
        logger.warning("can't configure sentry client")
        logger.debug('%s - %s' % (type(e), e))

    import gtk.gdk, pygtk
    if not main_is_frozen():
        pygtk.require('2.0')
    display = gtk.gdk.display_get_default()
    if display is None:
        print _('**Error: Ghini must be run in a windowed environment.')
        sys.exit(1)
    import bauble.pluginmgr as pluginmgr, bauble.utils as utils
    gobject.threads_init()
    try:
        import bauble.db as db
    except Exception as e:
        utils.message_dialog(utils.xml_safe(e), gtk.MESSAGE_ERROR)
        sys.exit(1)

    default_icon = os.path.join(paths.lib_dir(), 'images', 'icon.png')
    open_exc = None
    if uri is None:
        from bauble.connmgr import start_connection_manager
        while True:
            if not uri or not conn_name:
                conn_name, uri = start_connection_manager()
                if conn_name is None:
                    quit()
            try:
                if db.open(uri, True, True):
                    prefs[conn_default_pref] = conn_name
                    break
                else:
                    uri = conn_name = None
            except err.VersionError as e:
                logger.warning('%s(%s)' % (type(e), e))
                db.open(uri, False)
                break
            except (err.EmptyDatabaseError, err.MetaTableError, err.VersionError, err.TimestampError,
             err.RegistryError) as e:
                logger.info('%s(%s)' % (type(e), e))
                open_exc = e
                db.open(uri, False)
                break
            except err.DatabaseError as e:
                logger.debug('%s(%s)' % (type(e), e))
                open_exc = e
            except Exception as e:
                msg = _('Could not open connection.\n\n%s') % utils.xml_safe(repr(e))
                utils.message_details_dialog(msg, traceback.format_exc(), gtk.MESSAGE_ERROR)
                uri = None

    else:
        db.open(uri, True, True)
    pluginmgr.load()
    prefs.save()
    from bauble.view import DefaultCommandHandler
    pluginmgr.register_command(DefaultCommandHandler)
    import bauble.ui as ui
    gui = ui.GUI()

    def _post_loop():
        gtk.gdk.threads_enter()
        try:
            if isinstance(open_exc, err.DatabaseError):
                msg = _('Would you like to create a new Ghini database at the current connection?\n\n<i>Warning: If there is already a database at this connection any existing data will be destroyed!</i>')
                if utils.yes_no_dialog(msg, yes_delay=2):
                    try:
                        db.create()
                        pluginmgr.init()
                        prefs[conn_default_pref] = conn_name
                    except Exception as e:
                        utils.message_details_dialog(utils.xml_safe(e), traceback.format_exc(), gtk.MESSAGE_ERROR)
                        logger.error('%s(%s)' % (type(e), e))

            else:
                pluginmgr.init()
        except Exception as e:
            logger.warning('%s\n%s(%s)' % (
             traceback.format_exc(), type(e), e))
            utils.message_dialog(utils.utf8(e), gtk.MESSAGE_WARNING)

        gui.get_view().update()
        gtk.gdk.threads_leave()

    gobject.idle_add(_post_loop)
    gui.show()
    gtk.threads_enter()
    gtk.main()
    active_view = gui.get_view()
    if active_view:
        active_view.cancel_threads()
    gtk.threads_leave()
    return