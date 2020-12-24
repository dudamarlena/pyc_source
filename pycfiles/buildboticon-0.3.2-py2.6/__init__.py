# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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