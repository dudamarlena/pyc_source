# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bbicon\bbicon.py
# Compiled at: 2011-01-22 06:18:45
import PyQt4.Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import sys, re, textwrap, logging, yaml, bbicon_qrc
from yaml.error import YAMLError
states = [
 'success', 'warn', 'fail', 'exception', 'offline', 'error']

class Build(QObject):
    log = logging.getLogger('Build')

    def __init__(self, id, url):
        QObject.__init__(self)
        assert url.isValid(), "Build %s has invalid url '%s'" % (id, url)
        self.id = id
        self.url = url
        self.prev_state = None
        self.state = None
        self.tray = QSystemTrayIcon()
        self.set_status('offline')
        self.tray.setVisible(True)
        return

    def __repr__(self):
        return '<%s instance %s %s>' % (type(self), self.id, self.url)

    def set_status(self, new_state, error=None):
        if new_state == 'success':
            title = 'Build ok.'
            text = 'Build %(id)s at %(url)s has completed sucessfully.'
            icon_type = QSystemTrayIcon.Information
        elif new_state == 'warn':
            title = 'Build has warnings!'
            text = 'A build %(id)s at %(url)s has completed with warnings.'
            icon_type = QSystemTrayIcon.Warning
        elif new_state == 'fail':
            title = 'Build failed!'
            text = 'A build %(id)s at %(url)s has failed.'
            icon_type = QSystemTrayIcon.Warning
        elif new_state == 'exception':
            title = 'Build failed with exception!'
            text = 'A build %(id)s at %(url)s has failed with an exception.'
            icon_type = QSystemTrayIcon.Warning
        elif new_state == 'offline':
            title = 'BuildBot is offline'
            text = 'Unable to reach the BuildBot at %(url)s.'
            icon_type = QSystemTrayIcon.Warning
        elif error:
            new_state = 'error'
            title = 'Error checking %s' % self.id
            text = error
            icon_type = QSystemTrayIcon.Critical
        else:
            title = 'Internal error'
            text = 'Build %(id)s at %(url)s has unknown build state ' + str(new_state)
            icon_type = QSystemTrayIcon.Critical
            new_state = 'error'
        if new_state != self.state:
            text = text % {'url': self.url.toString(), 'id': self.id}
            if new_state == 'error':
                self.log.warning('Builder %s went from %s to %s: %s' % (self.id, self.state, new_state, text))
            else:
                self.log.info('Builder %s went from %s to %s: %s' % (self.id, self.state, new_state, text))
            if 'offline' not in [self.state, new_state]:
                self.tray.showMessage(title, text, icon_type)
            icon = QIcon(':/buildbot-%s.%s' % (new_state, 'png' if new_state == 'error' else 'gif'))
            self.tray.setIcon(icon)
            self.tray.setToolTip(text)
            self.prev_state = self.state
            self.state = new_state


class BuildBotIcon(QObject):
    regex = re.compile('(%s)' % ('|').join(states[:4]))
    log = logging.getLogger('BuildBotIcon')

    def __init__(self, settings):
        QObject.__init__(self)
        self.cxt_menu = QMenu()
        self.cxt_menu.addAction('About...', self.on_about)
        self.cxt_menu.addAction('About Qt...', lambda : QMessageBox.aboutQt(None))
        self.cxt_menu.addAction('Quit', qApp.quit)
        self.timer = QTimer(self)
        self.timer.setObjectName('timer')
        self.timer.setInterval(settings.interval * 1000)
        self.network = QNetworkAccessManager(self)
        self.network.setObjectName('network')
        self.sounds = settings.sounds
        self.builds = dict((id, self._setup_build(id, url)) for (id, url) in settings.builds.items())
        self.outstanding_requests = 0
        self.offline_errors = [
         QNetworkReply.ConnectionRefusedError,
         QNetworkReply.HostNotFoundError,
         QNetworkReply.TimeoutError]
        if hasattr(QNetworkReply, 'TemporaryNetworkFailureError'):
            self.offline_errors.append(QNetworkReply.TemporaryNetworkFailureError)
        QMetaObject.connectSlotsByName(self)

    def start(self):
        self.timer.start()
        self.on_timer_timeout()

    def _setup_build(self, id, url):
        b = Build(id, url)
        b.tray.activated.connect(self.on_activated)
        b.tray.setContextMenu(self.cxt_menu)
        return b

    def on_activated(self, reason):
        actions = {QSystemTrayIcon.Context: lambda : self.cxt_menu.show(), 
           QSystemTrayIcon.Trigger: lambda : self.cxt_menu.show()}
        actions.get(reason, lambda : None)()

    def on_about(self):
        text = textwrap.dedent('            BuildBotIcon v0.3.2 - a BuildBot monitoring utility\n\n            http://bitbucket.org/marcusl/buildboticon\n\n            Copyright 2010-2011 Marcus Lindblom\n            Licensed under GPLv3\n\n            Using Qt %s, PyQt %s and\n            Python %s' % (
         PyQt4.Qt.QT_VERSION_STR, PyQt4.Qt.PYQT_VERSION_STR,
         sys.version))
        self.about = QMessageBox()
        self.about.setWindowTitle('About BuildBotIcon...')
        self.about.setText(text)
        self.about.setIconPixmap(QPixmap(':/buildbot-bignut.png'))
        self.about.show()

    def on_timer_timeout(self):
        self.log.debug("Checking builds' statuses...")
        self.outstanding_requests = 0
        for b in self.builds.values():
            req = QNetworkRequest(b.url)
            req.setOriginatingObject(b)
            self.network.get(req)
            self.outstanding_requests += 1

    def on_network_finished(self, reply):
        self.log.debug('Request to %s finished' % reply.request().url().toString())
        b = reply.request().originatingObject()
        error = None
        state = None
        if reply.error() in self.offline_errors:
            state = 'offline'
        elif reply.error():
            error = 'Network error %i reading %s: %s' % (
             reply.error(), b.url.toString(), reply.errorString())
        else:
            match = self.regex.search(QString.fromUtf8(reply.readAll()))
            if not match:
                error = 'Reply did not match any expected content'
            else:
                state = match.group(0)
        b.set_status(state, error)
        self.outstanding_requests -= 1
        if not self.outstanding_requests:
            self._maybePlaySound()
        return

    def _maybePlaySound(self):
        new_states = set(b.state for b in self.builds.values() if b.state != b.prev_state if b.prev_state not in ('offline',
                                                                                                                  None))
        for state in reversed(states):
            if state in new_states:
                sound = self.sounds.get(state)
                if sound:
                    sound.play()
                    return


class SettingsError(Exception):
    pass


class Settings(object):
    """Settings for BuildbotIcon
    
       interval - integer of seconds between polls
       builds - list of tuples (id, url) for builds to check
       sounds - dict of state -> QSound for playing sounds 
    """

    def __init__(self, file=None):
        self.interval = 30
        self.builds = {}
        self.sounds = {}

    def configure(self, argv):
        if len(argv) <= 1:
            QMessageBox.information(None, 'No config file specified', 'Usage: bbicon.py <path-to-settings.yaml>', buttons=QMessageBox.Close)
            return False
        else:
            try:
                with open(argv[1], 'r') as (file):
                    self._load(file)
                return True
            except (YAMLError, SettingsError, IOError), e:
                QMessageBox.warning(None, '%s loading config file' % type(e).__name__, str(e), buttons=QMessageBox.Close)
                return False

            return

    def _load(self, file):
        """load settings from yaml file
        
            @param file: a file-like object providing a yaml document
        
            @throws: YAMLError on syntax error in file
            @throws: SettingsError on bad configuration
        """
        settings = yaml.safe_load(file)
        for i in settings:
            if 'builds' == i:
                for (id, url) in settings['builds'].items():
                    qurl = QUrl(url)
                    if not qurl.isValid():
                        raise SettingsError("Invalid url '%s' for build '%s'" % (url, id))
                    self.builds[id] = qurl

            elif 'interval' == i:
                self.interval = int(settings['interval'])
            elif 'sounds' == i:
                for (state, file) in settings['sounds'].items():
                    if state not in states:
                        raise SettingsError("Invalid state '%s' in sounds" % state)
                    self.sounds[state] = QSound(file)

            else:
                raise SettingsError('Unknown settings item: %s' % i)