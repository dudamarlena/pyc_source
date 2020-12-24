# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/canvas_launcher/launcher.py
# Compiled at: 2020-01-08 09:31:39
# Size of source mod 2**32: 3024 bytes
from silx.gui import qt
from Orange.canvas import config, __main__ as main
from .splash import splash_screen, getIcon
import tomwer.version, os, sys
from Orange.misc import environ

def version():
    return tomwer.version.version


class TomwerConfig(config.Config):
    ApplicationName = 'tomwer'
    ApplicationVersion = version()

    @staticmethod
    def splash_screen():
        return splash_screen()

    @staticmethod
    def core_packages():
        return super(TomwerConfig, TomwerConfig).core_packages() + [
         'tomwer-add-on']

    @staticmethod
    def application_icon():
        return getIcon()


class TomwerSplashScreen(qt.QSplashScreen):
    __doc__ = 'SplashScreen to overwrite the one of Orange'

    def __init__(self, parent=None, pixmap=None, textRect=None, textFormat=qt.Qt.PlainText, **kwargs):
        (qt.QSplashScreen.__init__)(self, parent, pixmap=pixmap, **kwargs)

    def showMessage(self, message, alignment=qt.Qt.AlignLeft, color=qt.Qt.black):
        version = 'version ' + str(tomwer.version.version)
        super().showMessage(version, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.black)


class Launcher:
    __doc__ = 'Proxy to orange-canvas'

    def launch(self, argv):
        config.Config = TomwerConfig
        self.fix_application_dirs()
        self.replace_splash_screen()
        self.main(argv)

    def fix_application_dirs(self):

        def data_dir(versioned=True):
            """
            Return the platform dependent Orange data directory.

            This is ``data_dir_base()``/Orange/__VERSION__/ directory if versioned is
            `True` and ``data_dir_base()``/Orange/ otherwise.
            """
            base = environ.data_dir_base()
            if versioned:
                return os.path.join(base, 'tomwer', version())
            return os.path.join(base, 'tomwer')

        environ.data_dir = data_dir

        def cache_dir(*args):
            """
            Return the platform dependent Orange cache directory.
            """
            if sys.platform == 'darwin':
                base = os.path.expanduser('~/Library/Caches')
            else:
                if sys.platform == 'win32':
                    base = os.getenv('APPDATA', os.path.expanduser('~/AppData/Local'))
                else:
                    if os.name == 'posix':
                        base = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
                    else:
                        base = os.path.expanduser('~/.cache')
            base = os.path.join(base, 'tomwer', version())
            if sys.platform == 'win32':
                return os.path.join(base, 'Cache')
            return base

        environ.cache_dir = cache_dir

    def replace_splash_screen(self):
        main.SplashScreen = TomwerSplashScreen

    def main(self, argv):
        from Orange.canvas.__main__ import main
        main(argv)