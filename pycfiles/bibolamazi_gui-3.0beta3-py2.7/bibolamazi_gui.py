# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/bibolamazi_gui.py
# Compiled at: 2015-05-11 05:40:29
import sys, os, os.path, re, logging, subprocess, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import bibolamazi.init
from bibolamazi.core import blogger
from bibolamazi.core import bibolamazifile
from bibolamazi.core import main
from bibolamazi.core.butils import BibolamaziError
from bibolamazi.core.bibfilter import factory as filters_factory
from bibolamazi.core import version as bibolamaziversion
import openbibfile, helpbrowser, settingswidget
from .favorites import FavoriteCmdsList
from .qtauto.ui_mainwidget import Ui_MainWidget
logger = logging.getLogger(__name__)

class BibolamaziApplication(QApplication):

    def __init__(self):
        self.main_widget = None
        super(BibolamaziApplication, self).__init__(sys.argv)
        self.setWindowIcon(QIcon(':/pic/bibolamazi_icon.png'))
        self.setApplicationName('Bibolamazi')
        self.setApplicationVersion(bibolamaziversion.version_str)
        self.setOrganizationDomain('org.bibolamazi')
        self.setOrganizationName('Bibolamazi Project')
        setup_software_updater()
        self.main_widget = MainWidget()
        self.main_widget.show()
        self.main_widget.raise_()
        return

    def event(self, event):
        if event.type() == QEvent.FileOpen:
            logger.info('Opening file %s', event.file())
            if self.main_widget is None:
                logger.error("ERROR: CAN'T OPEN FILE: MAIN WIDGET IS NONE!")
            else:
                self.main_widget.openFile(event.file())
            return True
        return super(BibolamaziApplication, self).event(event)


def find_retina_resolution():
    try:
        output = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'])
    except Exception as e:
        logger.info("Couldn't check for retina display: %s", e)
        return

    logger.debug('Got display information:\n%s', output)
    m = re.search('Retina:\\s*(?P<answer>Yes|No)', output, flags=re.IGNORECASE)
    if not m:
        return
    else:
        if m.group('answer').lower() != 'yes':
            return
        m2 = re.search('Resolution:\\s*(?P<resX>\\d+)\\s*x\\s*(?P<resY>\\d+)', output, flags=re.IGNORECASE)
        if not m:
            logger.info("Couldn't find resolution information for retina display.")
            return
        return (int(m2.group('resX')), int(m2.group('resY')))


class MainWidget(QWidget):

    def __init__(self):
        global swu_interface
        super(MainWidget, self).__init__()
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        if sys.platform.startswith('darwin') and QT_VERSION_STR.startswith('4.8.'):
            retinaresolution = find_retina_resolution()
            if retinaresolution is not None:
                mydesktop = QApplication.desktop()
                myratio = 2
                print 'myratio=', myratio
                self.mypict = QPicture()
                mypaint = QPainter(self.mypict)
                self.myicon = QIcon(':pic/bibolamazi.svg')
                mysize = QSize(375, 150)
                mypaint.drawPixmap(QRect(QPoint(0, 0), mysize), self.myicon.pixmap(myratio * mysize))
                self.ui.lblMain.setPicture(self.mypict)
        self.openbibfiles = []
        self.helpbrowser = None
        self.settingswidget = None
        self.favoriteCmdsList = FavoriteCmdsList(parent=self)
        self.favoriteCmdsList.loadFromSettings(QSettings())
        self.menubar = None
        self.shortcuts = []
        self.upd_checkenabled_action = None
        self.upd_checknow_action = None
        if swu_interface is not None:
            self.upd_checkenabled_action = QAction('Regularly Check for Updates', self)
            self.upd_checkenabled_action.setCheckable(True)
            self.upd_checkenabled_action.setChecked(swu_interface.checkForUpdatesEnabled())
            self.upd_checkenabled_action.toggled.connect(swu_interface.setCheckForUpdatesEnabled)
            swu_interface.checkForUpdatesEnabledChanged.connect(self.upd_checkenabled_action.setChecked)
            self.upd_checknow_action = QAction('Check for Updates Now', self)
            self.upd_checknow_action.triggered.connect(self.doCheckForUpdates)
        if sys.platform.startswith('darwin'):
            self.menubar = QMenuBar(None)
            filemenu = self.menubar.addMenu('File')
            filemenu.addAction('New', self, SLOT('on_btnNewFile_clicked()'), QKeySequence('Ctrl+N'))
            filemenu.addAction('Open', self, SLOT('on_btnOpenFile_clicked()'), QKeySequence('Ctrl+O'))
            filemenu.addAction('Settings', self, SLOT('on_btnSettings_clicked()'))
            if self.upd_checkenabled_action:
                filemenu.addSeparator()
                filemenu.addAction(self.upd_checkenabled_action)
            if self.upd_checknow_action:
                filemenu.addAction(self.upd_checknow_action)
            helpmenu = self.menubar.addMenu('Help')
            helpmenu.addAction('Open Help && Reference Browser', self, SLOT('on_btnHelp_clicked()'), QKeySequence('Ctrl+R'))
        else:
            self.shortcuts += [
             (
              QAction('New', self), 'Ctrl+N', self.on_btnNewFile_clicked),
             (
              QAction('Open', self), 'Ctrl+O', self.on_btnOpenFile_clicked),
             (
              QAction('Help', self), 'Ctrl+R', self.on_btnHelp_clicked),
             (
              QAction('Quit', self), 'Ctrl+Q', self.on_btnQuit_clicked),
             (
              QAction('Settings', self), 'Ctrl+P', self.on_btnSettings_clicked)]
            if self.upd_checkenabled_action:
                self.shortcuts += []
            if self.upd_checknow_action:
                self.shortcuts += [
                 (
                  self.upd_checknow_action, 'Ctrl+U', None)]
            for a, key, slot in self.shortcuts:
                a.setShortcut(QKeySequence(key))
                if slot is not None:
                    a.triggered.connect(slot)
                a.setShortcutContext(Qt.ApplicationShortcut)
                self.addAction(a)

        self.setWindowIcon(QIcon(':/pic/bibolamazi_icon.png'))
        return

    def doCheckForUpdates(self):
        if swu_interface is not None:
            ret = swu_interface.do_check_for_updates()
            if ret is None:
                pass
            elif ret is False:
                QMessageBox.information(self, 'Software Update Check', 'There are no new updates.')
            elif isinstance(ret, tuple):
                if len(ret) == 3:
                    QMessageBox.critical(self, 'Error: Software Update Check', ret[2])
                    return
                return
        return

    def openFile(self, fname):
        w = openbibfile.OpenBibFile()
        w.setFavoriteCmdsList(self.favoriteCmdsList)
        w.setOpenFile(fname)
        w.show()
        w.raise_()
        w.fileClosed.connect(self.bibFileClosed)
        self.openbibfiles.append(w)
        w.requestHelpTopic.connect(self.openHelpTopic)

    @pyqtSlot(QString)
    def openHelpTopic(self, path):
        self.on_btnHelp_clicked()
        self.helpbrowser.openHelpTopic(path)

    @pyqtSlot()
    def on_btnOpenFile_clicked(self):
        fname = str(QFileDialog.getOpenFileName(self, 'Open Bibolamazi File', QString(), 'Bibolamazi Files (*.bibolamazi.bib);;All Files (*)'))
        if fname:
            self.openFile(fname)

    @pyqtSlot()
    def on_btnNewFile_clicked(self):
        saveFileDialog = QFileDialog(self, 'Create Bibolamazi File', QString(), 'Bibolamazi Files (*.bibolamazi.bib);;All Files (*)')
        if sys.platform.startswith('darwin'):
            saveFileDialog.setOptions(QFileDialog.DontUseNativeDialog)
        saveFileDialog.setDefaultSuffix('bibolamazi.bib')
        saveFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        saveFileDialog.setFileMode(QFileDialog.AnyFile)
        if not saveFileDialog.exec_():
            return
        newfilename = [ unicode(x) for x in saveFileDialog.selectedFiles() ][0]
        if not newfilename:
            return
        if os.path.exists(newfilename):
            QMessageBox.critical(self, 'File Exists', "Cowardly refusing to overwrite existing file `%s'. Please remove it first." % newfilename)
            return
        try:
            bfile = bibolamazifile.BibolamaziFile(newfilename, create=True)
            bfile.saveToFile()
        except Exception as e:
            QMessageBox.critical(self, 'Error', "Error: Can't create file: %s" % e)
            return

        self.openFile(newfilename)

    @pyqtSlot()
    def on_btnHelp_clicked(self):
        if self.helpbrowser is None:
            self.helpbrowser = helpbrowser.HelpBrowser()
        self.helpbrowser.show()
        self.helpbrowser.raise_()
        return

    @pyqtSlot()
    def on_btnQuit_clicked(self):
        self.close()

    @pyqtSlot()
    def on_btnSettings_clicked(self):
        global swu_sourcefilter_devel
        if self.settingswidget is None:
            self.settingswidget = settingswidget.SettingsWidget(swu_interface=swu_interface, swu_sourcefilter_devel=swu_sourcefilter_devel, mainwin=self)
        self.settingswidget.show()
        self.settingswidget.raise_()
        return

    @pyqtSlot()
    def bibFileClosed(self):
        sender = self.sender()
        if sender not in self.openbibfiles:
            logger.warning('Widget sender of fileClosed() not in our openbibfiles list!!')
            return
        logger.debug('file is closed.')
        self.openbibfiles.remove(sender)

    def closeEvent(self, event):
        logger.debug('Close!!')
        for w in self.openbibfiles:
            ans = w.close()
            if not ans:
                event.ignore()
                return

        if self.helpbrowser:
            self.helpbrowser.close()
        self.favoriteCmdsList.saveToSettings(QSettings())
        super(MainWidget, self).closeEvent(event)


swu_updater = None
swu_interface = None
swu_source = None
swu_sourcefilter_devel = None

def setup_software_updater():
    global swu_interface
    global swu_source
    global swu_sourcefilter_devel
    global swu_updater
    if not hasattr(sys, '_MEIPASS'):
        return
    import logging
    from updater4pyi import upd_core, upd_source, upd_iface, upd_log
    from updater4pyi.upd_source import relpattern, RELTYPE_BUNDLE_ARCHIVE, RELTYPE_EXE
    from updater4pyi.upd_iface_pyqt4 import UpdatePyQt4Interface
    swu_source = upd_source.UpdateGithubReleasesSource('phfaist/bibolamazi')
    swu_sourcefilter_devel = upd_source.UpdateSourceDevelopmentReleasesFilter(False)
    swu_source.add_release_filter(swu_sourcefilter_devel)
    swu_updater = upd_core.Updater(current_version=bibolamaziversion.version_str, update_source=swu_source)
    swu_interface = UpdatePyQt4Interface(swu_updater, progname='Bibolamazi', ask_before_checking=True, parent=QApplication.instance())
    swu_interface.start()


def run_main():
    blogger.setup_simple_console_logging()
    logging.getLogger().setLevel(logging.DEBUG)
    try:
        import bibolamazi_compiled_filter_list as pc
        filters_factory.load_precompiled_filters('bibolamazi.filters', dict([ (fname, pc.__dict__[fname]) for fname in pc.filter_list ]))
    except ImportError:
        pass

    logger.debug('starting application')
    app = BibolamaziApplication()
    try:
        main.setup_filterpackages_from_env()
        settingswidget.setup_filterpackages_from_settings(QSettings())
    except (filters_factory.NoSuchFilter, filters_factory.NoSuchFilterPackage, BibolamaziError):
        QMessageBox.warning(None, 'Filter packages error', 'An error was detected in the filter packages configuration. Please edit your settings.')

    args = app.arguments()
    _rxscript = re.compile('\\.(py[co]?|exe)$', flags=re.IGNORECASE)
    for k in xrange(1, len(args)):
        fn = str(args[k])
        if _rxscript.search(fn):
            logger.debug('skipping own arg: %s', fn)
            continue
        logger.debug('opening arg: %s', fn)
        app.main_widget.openFile(fn)

    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    run_main()