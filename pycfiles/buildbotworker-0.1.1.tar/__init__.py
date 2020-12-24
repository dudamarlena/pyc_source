# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bbicon\__init__.py
# Compiled at: 2011-01-22 06:18:02
import sys, logging
from PyQt4.QtGui import QApplication, qApp, QIcon
from bbicon import Settings, BuildBotIcon

def main(argv=sys.argv):
    import bbicon_qrc
    a = QApplication(argv) if qApp.startingUp() else qApp
    a.setQuitOnLastWindowClosed(False)
    a.setWindowIcon(QIcon(':/buildboticon-success.png'))
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    settings = Settings()
    if not settings.configure(argv):
        return 1
    else:
        bbi = BuildBotIcon(settings)
        bbi.start()
        return a.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv))