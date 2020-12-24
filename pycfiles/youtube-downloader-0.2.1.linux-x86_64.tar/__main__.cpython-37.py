# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blooser/anaconda3/lib/python3.7/site-packages/youtubedownloader/__main__.py
# Compiled at: 2020-05-13 11:06:53
# Size of source mod 2**32: 1927 bytes
import sys, os
from PySide2.QtQml import QQmlApplicationEngine, QQmlContext, qmlRegisterType
from PySide2.QtQuick import QQuickView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QUrl, QResource
from PySide2.QtWidgets import QApplication
from .download import DownloadManager
from .component_changer import ComponentChanger, Change
from .dialog_manager import DialogManager
from .resources import Resources
from .theme import Theme
from .paths import Paths
from .settings import Settings
from .browser import Browsers

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setApplicationName('youtube downloader')
    app.setApplicationVersion('0.1.0')
    app.setOrganizationName('blooser')
    app.setWindowIcon(QIcon(Resources.YD_LOGO))
    download_manager = DownloadManager()
    settings = Settings()
    dialog_manager = DialogManager()
    resources = Resources()
    paths = Paths()
    browsers = Browsers()
    qmlRegisterType(Change, 'yd.items', 0, 1, 'Change')
    qmlRegisterType(ComponentChanger, 'yd.items', 0, 1, 'ComponentChanger')
    qml_file = os.path.join(os.path.dirname(__file__), 'qml/main.qml')
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('Theme', Theme)
    engine.rootContext().setContextProperty('Resources', resources)
    engine.rootContext().setContextProperty('Settings', settings)
    engine.rootContext().setContextProperty('downloadManager', download_manager)
    engine.rootContext().setContextProperty('dialogManager', dialog_manager)
    engine.rootContext().setContextProperty('Paths', paths)
    engine.rootContext().setContextProperty('WebBrowsers', browsers)
    download_manager.setQMLContext(engine)
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())