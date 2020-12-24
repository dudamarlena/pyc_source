# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/core.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 4815 bytes
import warnings, os, sys, logging
logger = logging.getLogger(__name__)
from mvc.support.gui_loop import start_event_loop

def _run_user_script():
    """
        Runs the user script specified in the command-line arguments.
    """
    available, nv, cv = check_for_updates()
    if available:
        print('An update is available: current version is %s upstream version is %s - consider upgrading!' % cv, nv)
    from pyxrd.data import settings
    try:
        import imp
        user_script = imp.load_source('user_script', settings.ARGS.script)
    except BaseException as err:
        err.args = 'Error when trying to import %s: %s' % (settings.ARGS.script, err.args)
        raise

    user_script.run(settings.ARGS)


def _run_gui(project=None):
    from pkg_resources import resource_filename
    from pyxrd.application.splash import SplashScreen
    from pyxrd import __version__
    filename = resource_filename(__name__, 'application/icons/pyxrd.png')
    splash = SplashScreen(filename, __version__)
    splash.set_message('Checking for updates ...')
    update_available, nv, cv = check_for_updates()
    splash.set_message('Loading GUI ...')
    from pyxrd.data import settings
    from pyxrd.file_parsers.json_parser import JSONParser
    from pyxrd.application.models import AppModel
    from pyxrd.application.views import AppView
    from pyxrd.application.controllers import AppController
    from pyxrd.generic.gtk_tools.gtkexcepthook import plugin_gtk_exception_hook
    filename = settings.ARGS.filename
    if filename != '':
        try:
            logging.info('Opening project: %s' % filename)
            project = JSONParser.parse(filename)
        except IOError:
            logging.info('Could not load project file %s: IOError' % filename)

    os.environ['LIBOVERLAY_SCROLLBAR'] = '0'
    os.environ['UBUNTU_MENUPROXY'] = ''
    if not settings.DEBUG:
        warnings.filterwarnings(action='ignore', category=Warning)
    else:
        if splash:
            splash.close()
        gtk_exception_hook = plugin_gtk_exception_hook()
        m = AppModel(project=project)
        v = AppView()
        AppController(m, v, gtk_exception_hook=gtk_exception_hook)
        del splash
        if update_available:
            from mvc.adapters.gtk_support.dialogs.dialog_factory import DialogFactory
            DialogFactory.get_information_dialog(('An update is available (%s) - consider upgrading!' % nv),
              False,
              (v.get_toplevel()), title='Update available').run()
        else:
            print('PyXRD is up to date (current = %s)' % cv)
    start_event_loop()


def check_for_updates():
    """
        Checks for updates and returns a tuple:
            update_available, latest_version, current_version
    """
    from pyxrd.generic.outdated import check_outdated
    from pyxrd.__version import __version__
    is_outdated, latest_version = check_outdated('pyxrd', __version__)
    return (
     is_outdated, latest_version, __version__)


def run_main():
    """
        Parsers command line arguments and launches PyXRD accordingly.
    """
    mod = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if mod not in sys.path:
        sys.path.insert(1, mod)
    from pyxrd.data import settings
    settings.initialize()
    from pyxrd.logs import setup_logging
    setup_logging(basic=True)
    if settings.DEBUG:
        from pyxrd import stacktracer
        stacktracer.trace_start('trace.html',
          interval=5,
          auto=True)
    try:
        try:
            if settings.ARGS.script:
                _run_user_script()
            else:
                _run_gui()
        except:
            raise

    finally:
        for finalizer in settings.FINALIZERS:
            finalizer()

        if settings.DEBUG:
            stacktracer.trace_stop()


if __name__ == '__main__':
    run_main()