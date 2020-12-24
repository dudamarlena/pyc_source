# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\main.py
# Compiled at: 2019-04-14 13:47:00
# Size of source mod 2**32: 5061 bytes
"""
main .
"""
import io, sys
sys.path.append('./Styles/CustomTitlebar')
import traceback, faulthandler
from Tools.main_setting import SettingInfo
from Styles.CommonHelper import CommonHelper
from Tools.FuncMixin import FuncMixin
from Tools.LogError import logger
from UUI.Components.C_SplashScreen import C_QSplashScreen
from UUI.Components.C_Application import C_QSingleApplication
from main_preinit_ui import Ui_initUI, QStyleFactory, QApplication, QMessageBox, Qt, QPushButton

class MainWindow(Ui_initUI, FuncMixin, SettingInfo):
    __doc__ = '\n    Class documentation goes here.\n    '

    def __init__(self, parent=None):
        from Tools import BasePara
        BasePara.mw = self
        BasePara.settings = self.settings
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._initUI()
        self.restoreSettings()


def main(style=1):
    global ui
    app.setStyle(QStyleFactory.create('Fusion'))
    ui = MainWindow()
    if style == 1:
        ui.show()
    else:
        if style == 3:
            framelessWindow = CommonHelper.FrameCustomerTitle(ui, title='Wow',
              icon=':/button_Ima/git.ico')
            framelessWindow.show()
        elif style == 2:
            pass


def pageMain(style=1):
    main(style)


if __name__ == '__main__':

    def excepthook(excType, excValue, tracebackobj):
        """ globals catch error / tb = traceback"""
        try:
            errmsg = '{0}: \n{1}'.format(str(excType), str(excValue))
            tbinfofile = io.StringIO()
            traceback.print_tb(tracebackobj, None, tbinfofile)
            tbinfofile.seek(0)
            tbinfo = tbinfofile.read()
            logger.warning(errmsg + tbinfo)
            faulthandler.enable(file=(sys.stderr))
        except:
            pass

        sys.__excepthook__(excType, excValue, tracebackobj)


    sys.excepthook = excepthook

    def showSplashScreen(mainfun, needSignal=False, needShowSplash=False, style=1):
        """
        start 启动界面"

        :param mainfun: main()
        :param needSignal: only one app
        :param needShowSplash:
        :param style: 1:default ; 2:qdarkstyle; 3.unlesswindow
        :return:
        """
        global app
        app = QApplication(sys.argv) if needSignal is False else C_QSingleApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        if needSignal is True:
            if app.isRunning():
                app.sendMessage('app is running')
                QMessageBox.warning(None, '警告', '已启动软件, 请结束上一次启动的软件后再运行！')
                sys.exit(0)
        else:
            if needShowSplash is True:
                splash = C_QSplashScreen()
                splash.effect()
                app.processEvents()
                mainfun(style)
                splash.finish(ui)
            else:
                mainfun(style)
        app.setActivationWindow(ui) if needSignal is True else None


    showSplashScreen(pageMain, needSignal=False,
      needShowSplash=False,
      style=3)
    sys.exit(app.exec_())