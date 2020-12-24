# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gonullugui/coreui.py
# Compiled at: 2017-07-23 05:53:59
# Size of source mod 2**32: 18126 bytes
from PyQt5.QtCore import QDir, QFile, QIODevice, QProcess, QT_VERSION_STR
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDesktopWidget, QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QTextEdit, QToolTip
from pkg_resources import parse_version
from .version import __version__
launching = QProcess()

class launchingWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle(self.tr('Launching Gonullu'))
        self.setFixedSize(304, 169)
        launchingWindowLeft = (QDesktopWidget().width() - self.width()) // 2
        launchingWindowTop = (QDesktopWidget().height() - self.height()) // 2
        self.move(launchingWindowLeft, launchingWindowTop)
        memoryLabel = QLabel(self.tr('Memory Percent:'))
        memoryLabel.setToolTip(self.tr('Reserve memory as percent of full memory for Gonullu'))
        cpuLabel = QLabel(self.tr('Number of CPUs:'))
        cpuLabel.setToolTip(self.tr('Reserve number of CPUs for Gonullu'))
        emailLabel = QLabel(self.tr('E-Mail Address:'))
        emailLabel.setToolTip(self.tr('Enter e-mail adress for Gonullu. The address must be authorized.'))
        self.memoryEdit = QLineEdit()
        self.memoryEdit.setToolTip(self.tr('Reserve memory as percent of full memory for Gonullu'))
        self.cpuEdit = QLineEdit()
        self.cpuEdit.setToolTip(self.tr('Reserve number of CPUs for Gonullu'))
        self.emailEdit = QLineEdit()
        self.emailEdit.setToolTip(self.tr('Enter e-mail adress for Gonullu. The address must be authorized.'))
        launchButton = QPushButton(self.tr('Launch'))
        launchButton.setToolTip(self.tr('Launch Gonullu with main window'))
        aboutButton = QPushButton(self.tr('About'))
        aboutButton.setToolTip(self.tr('About Gonullu GUI'))
        aboutQtButton = QPushButton(self.tr('About Qt'))
        aboutQtButton.setToolTip(self.tr('About Qt'))
        launchingWindowLayout = QGridLayout()
        launchingWindowLayout.setSpacing(10)
        launchingWindowLayout.addWidget(memoryLabel, 0, 0)
        launchingWindowLayout.addWidget(self.memoryEdit, 0, 1, 1, 2)
        launchingWindowLayout.addWidget(cpuLabel, 1, 0)
        launchingWindowLayout.addWidget(self.cpuEdit, 1, 1, 1, 2)
        launchingWindowLayout.addWidget(emailLabel, 2, 0)
        launchingWindowLayout.addWidget(self.emailEdit, 2, 1, 1, 2)
        launchingWindowLayout.addWidget(launchButton, 3, 0)
        launchingWindowLayout.addWidget(aboutButton, 3, 1)
        launchingWindowLayout.addWidget(aboutQtButton, 3, 2)
        self.setLayout(launchingWindowLayout)
        launchButton.clicked.connect(self.launchSlot)
        aboutButton.clicked.connect(self.aboutSlot)
        aboutQtButton.clicked.connect(self.aboutQtSlot)

    def launchSlot(self):
        if self.memoryEdit.text() == '' or self.cpuEdit.text() == '':
            QMessageBox().critical(self, self.tr('Gonullu Graphical User Interface'), self.tr("'Memory Percent' and 'Number of CPUs' entering areas can not be empty."), QMessageBox.Ok)
            return
        self.mainWindow = mainWindow()
        self.mainWindow.show()
        self.close()
        launchCommand = 'gonullu'
        launchCommand += ' -m ' + self.memoryEdit.text() + ' -c ' + self.cpuEdit.text()
        if self.emailEdit.text() != '':
            launchCommand += ' -e ' + self.emailEdit.text()
        launching.start(launchCommand, mode=QIODevice.ReadOnly)
        launching.started.connect(self.mainWindow.launchOk)
        if parse_version(QT_VERSION_STR) >= parse_version('5.6'):
            launching.errorOccurred.connect(self.mainWindow.launchError)

    def aboutSlot(self):
        QMessageBox.about(self, self.tr('About'), self.tr('Gonullu Graphical User Interface\n\nVersion ') + __version__)

    def aboutQtSlot(self):
        QMessageBox.aboutQt(self, self.tr('About'))


class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle(self.tr('Gonullu GUI Main Window'))
        self.resize(640, 480)
        mainWindowLeft = (QDesktopWidget().width() - self.width()) // 2
        mainWindowTop = (QDesktopWidget().height() - self.height()) // 2
        self.move(mainWindowLeft, mainWindowTop)
        self.stdoutArea = QTextEdit()
        self.stdoutArea.setReadOnly(True)
        self.stdoutArea.setToolTip(self.tr('Standart output is directed here and /var/log/stdout file, standart error output is directed to /var/log/stderr file. Success messages are green, warning messages are orange, error messages are red.'))
        self.setCentralWidget(self.stdoutArea)
        self.themeTextEditColor = self.stdoutArea.textColor()
        logsDir = QDir('/var/log/')
        createDir = logsDir.mkdir('gonullu-gui')
        self.stdoutFile = QFile('/var/log/gonullu-gui/stdout')
        stdoutFileOpen = self.stdoutFile.open(QIODevice.WriteOnly | QIODevice.Text)
        if not stdoutFileOpen:
            QMessageBox().information(None, self.tr('Gonullu Graphical User Interface'), self.tr('Failed to open standart output log file.'), QMessageBox.Ok)
        self.stderrFile = QFile('/var/log/gonullu-gui/stderr')
        stderrFileOpen = self.stderrFile.open(QIODevice.WriteOnly | QIODevice.Text)
        if not stderrFileOpen:
            QMessageBox().information(None, self.tr('Gonullu Graphical User Interface'), self.tr('Failed to open standart error log file.'), QMessageBox.Ok)

    def launchOk(self):
        self.statusBar().showMessage(self.tr('Gonullu is running...'))
        launching.readyReadStandardOutput.connect(self.readFromStdout)
        launching.readyReadStandardError.connect(self.readFromStderr)

    def launchError(self):
        QMessageBox().critical(self, self.tr('Gonullu Graphical User Interface'), self.tr('Gonullu failed to start.'), QMessageBox.Ok)

    def readFromStdout(self):
        data = launching.readAllStandardOutput()
        strdata = str(bytes(data), encoding='utf-8')
        if strdata.endswith(('\r', '\n')):
            strdata = strdata[:-1]
        if strdata.startswith(('\r', '\n')):
            strdata = strdata[1:]
        strdatasplitted = strdata.split()
        if strdata[:12] == '  [x] Hata: ':
            self.stdoutArea.setTextColor(QColor('#FF0000'))
        else:
            if strdata[:13] == '  [!] Uyarı: ':
                self.stdoutArea.setTextColor(QColor('#FFA500'))
            else:
                if strdata[:16] == '  [+] Başarılı: ':
                    self.stdoutArea.setTextColor(QColor('#008000'))
                if strdata[-22:] == 'yeni paket bekleniyor.':
                    self.stdoutArea.append(self.tr('Waiting for new package for {0} seconds...').format(strdatasplitted[2]))
                else:
                    if strdata[-15:] == 'saniyede bitti.':
                        self.stdoutArea.append(self.tr('Finished building {0} package in {1} seconds.').format(strdatasplitted[4], strdatasplitted[7]))
                    else:
                        if strdata[-25:] == 'paketi için devam ediyor.':
                            self.stdoutArea.append(self.tr('Building {0} package for {1} seconds...').format(strdatasplitted[7], strdatasplitted[2]))
                        else:
                            if strdata[-30:] == 'docker servisini çalıştırınız!':
                                self.stdoutArea.append(self.tr('Please start docker service before.'))
                            else:
                                if strdata[:31] == '  [x] Hata: Bilinmeyen bir hata':
                                    self.stdoutArea.append(self.tr('Unknown error: ') + strdata[49:-35])
                                    self.stdoutArea.append(self.tr('Exiting Gonullu...'))
                                else:
                                    if strdata[-21:] == 'Programdan çıkılıyor.':
                                        self.stdoutArea.append(self.tr('Exiting Gonullu...'))
                                    else:
                                        if strdata[-19:] == 'imajı güncelleniyor':
                                            self.stdoutArea.append(self.tr('Updating {0} image...').format(strdatasplitted[2]))
                                        else:
                                            if strdata[-28:] == 'İmaj son sürüme güncellendi':
                                                self.stdoutArea.append(self.tr('The image has been updated to last version.'))
                                            else:
                                                if strdata[-28:] == 'tekrar bağlanmaya çalışıyor!':
                                                    self.stdoutArea.append(self.tr("Couldn't access the server for {0} seconds, reconnecting...").format(strdatasplitted[3]))
                                                else:
                                                    if strdata[-32:] == 'tekrar gönderilmeye çalışılacak.':
                                                        self.stdoutArea.append(self.tr('{0} file will be resent.').format(strdatasplitted[2]))
                                                    else:
                                                        if strdata[-21:] == 'dosyası gönderiliyor.':
                                                            self.stdoutArea.append(self.tr('{0} file is being sent...').format(strdatasplitted[2]))
                                                        else:
                                                            if strdata[-30:] == 'dosyası başarı ile gönderildi.':
                                                                self.stdoutArea.append(self.tr('{0} file has been sent successfully.').format(strdatasplitted[2]))
                                                            else:
                                                                if strdata[-22:] == 'dosyası gönderilemedi!':
                                                                    self.stdoutArea.append(self.tr("{0} file couldn't be sent.").format(strdatasplitted[2]))
                                                                else:
                                                                    if strdata[:31] == '  [*] Bilgi: Yeni paket bulundu':
                                                                        self.stdoutArea.append(self.tr('New package found: {0}').format(strdatasplitted[7]))
                                                                    else:
                                                                        if strdata[-24:] == 'adresiniz yetkili değil!':
                                                                            self.stdoutArea.append(self.tr("Entered e-mail address isn't authorized."))
                                                                        else:
                                                                            if strdata[-24:] == 'Docker imajı bulunamadı!':
                                                                                self.stdoutArea.append(self.tr("The Docker image couldn't be found."))
                                                                            else:
                                                                                if strdata[-32:] == 'Tanımlı olmayan bir hata oluştu!':
                                                                                    self.stdoutArea.append(self.tr('A nondefined error has occured.'))
                                                                                else:
                                                                                    if strdata[-18:] == 'dosyası işlenemedi':
                                                                                        self.stdoutArea.append(self.tr("{0} file couldn't be handled.").format(strdatasplitted[2]))
                                                                                    else:
                                                                                        if strdata[:9] == 'Namespace':
                                                                                            strdatasplitted = strdata.split(', ')
                                                                                            self.stdoutArea.append(self.tr('Namespace:\n    cpu_set={0}\n    email={1}\n    job={2}\n    memory_limit={3}\n    usage={4}').format(strdatasplitted[0].split('=')[1], strdatasplitted[1].split('=')[1], strdatasplitted[2].split('=')[1], strdatasplitted[3].split('=')[1], strdatasplitted[4].split('=')[1][:-1]))
                                                                                        else:
                                                                                            if strdata == '':
                                                                                                pass
                                                                                            else:
                                                                                                self.stdoutArea.append(str(data, encoding='utf-8'))
        self.stdoutArea.setTextColor(self.themeTextEditColor)
        writingToStdoutBuffer = self.stdoutFile.write(data)
        if writingToStdoutBuffer == -1:
            self.statusBar().showMessage(self.tr('Failed to write standard output log to buffer.'))
        flushingToStdoutFile = self.stdoutFile.flush()
        if not flushingToStdoutFile:
            self.statusBar().showMessage(self.tr('Failed to flush standard output log to file.'))

    def readFromStderr(self):
        data = launching.readAllStandardError()
        writingToStderrBuffer = self.stderrFile.write(data)
        if writingToStderrBuffer == -1:
            self.statusBar().showMessage(self.tr('Failed to write standard error log to buffer.'))
        flushingToStderrFile = self.stderrFile.flush()
        if not flushingToStderrFile:
            self.statusBar().showMessage(self.tr('Failed to flush standard error log to file.'))

    def closeEvent(self, event):
        writingLastLineToStdoutBuffer = self.stdoutFile.write(b'\n')
        if writingLastLineToStdoutBuffer == -1:
            self.statusBar().showMessage(self.tr('Failed to write standard output log to buffer.'))
        flushingLastLineToStdoutFile = self.stdoutFile.flush()
        if not flushingLastLineToStdoutFile:
            self.statusBar().showMessage(self.tr('Failed to flush standard output log to file.'))
        self.stdoutFile.close()
        writingLastLineToStderrBuffer = self.stderrFile.write(b'\n')
        if writingLastLineToStderrBuffer == -1:
            self.statusBar().showMessage(self.tr('Failed to write standard error log to buffer.'))
        flushingLastLineToStderrFile = self.stderrFile.flush()
        if not flushingLastLineToStderrFile:
            self.statusBar().showMessage(self.tr('Failed to flush standard error log to file.'))
        self.stderrFile.close()
        event.accept()