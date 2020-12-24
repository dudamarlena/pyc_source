# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/software/codegra.fs/env/lib/python3.7/site-packages/codegra_fs/gui.py
# Compiled at: 2019-02-14 08:40:52
# Size of source mod 2**32: 15539 bytes
import os, abc, sys, json, time, typing as t, logging, codegra_fs
import codegra_fs.cgfs as cgfs
import codegra_fs.constants as constants
from appdirs import AppDirs
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QStyle, QDialog, QWidget, QCheckBox, QGroupBox, QLineEdit, QSplitter, QFileDialog, QFormLayout, QHBoxLayout, QMessageBox, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QTreeWidget, QVBoxLayout, QApplication, QInputDialog, QRadioButton, QDesktopWidget, QPlainTextEdit
try:
    import fuse
except:
    pass

PREVIOUS_VALUES_PATH = ''

class ValueObject:

    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError


class CGFSRadioSelect(QHBoxLayout, ValueObject):

    def __init__(self, options, default):
        super().__init__()
        self._CGFSRadioSelect__buttons = []
        for option in options:
            but = QRadioButton(option)
            self._CGFSRadioSelect__buttons.append((but, option))
            self.addWidget(but)
            if option == default:
                but.setChecked(True)

    @property
    def value(self):
        for but, val in self._CGFSRadioSelect__buttons:
            if but.isChecked():
                return val


class DirectoryButton(QHBoxLayout, ValueObject):

    def __init__(self, window, default):
        super().__init__()
        self._DirectoryButton__label = QLineEdit(window)

        def on_click():
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            options |= QFileDialog.DontResolveSymlinks
            value = QFileDialog.getExistingDirectory(window, 'Mount directory', '~', options)
            self._DirectoryButton__label.setText(value)

        self._DirectoryButton__button = QPushButton('Browse')
        self._DirectoryButton__button.clicked.connect(on_click)
        if default is not None:
            self._DirectoryButton__label.setText(default)
        self.addWidget(self._DirectoryButton__label)
        self.addWidget(self._DirectoryButton__button)

    @property
    def value(self) -> str:
        return self._DirectoryButton__label.text()


class StringInput(QLineEdit, ValueObject):

    def __init__(self, is_password=False, default=None):
        super().__init__()
        if is_password:
            self.setEchoMode(QLineEdit.Password)
        if default is not None:
            self.setText(default)

    @property
    def value(self) -> str:
        return self.text()


class CheckBoxInput(QCheckBox, ValueObject):

    def __init__(self, default=False):
        super().__init__()
        self.tooltip = 'Hello'
        if default is not None:
            self.setChecked(default)

    @property
    def value(self) -> str:
        return self.isChecked()


class CGFSFormLayout(QFormLayout):

    def add_help_row(self, a, b, help_text):
        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        if isinstance(a, str):
            a = QLabel(a)
        layout.addWidget(a)
        help_button = QToolButton()
        help_button.setIcon(QApplication.style().standardIcon(QStyle.SP_TitleBarContextHelpButton))
        layout.addWidget(help_button)
        help_button.setStyleSheet('margin-left: 5px;')
        help_label = QLabel(help_text)
        help_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        help_label.hide()
        help_button.clicked.connect(lambda : help_label.setVisible(not help_label.isVisible()))
        help_label.setStyleSheet('border: 1px solid gray; padding: 5px;')
        if isinstance(b, QWidget):
            wrap = QWidget()
            l = QHBoxLayout(wrap)
            l.addWidget(b)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(0)
            b = wrap
        self.addRow(wrapper, b)
        self.addRow(help_label)


class CGFSLoggingWindow(QPlainTextEdit):
    signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.setReadOnly(True)
        fixed_font = QFont('monospace')
        fixed_font.setStyleHint(QFont.TypeWriter)
        self.setFont(fixed_font)
        outer_self = self

        class QTextEditLogger(logging.Handler):

            def __init__(self):
                super().__init__()

            def emit(self, record):
                msg = self.format(record)
                outer_self.signal.emit(msg)

        self.log_handler = QTextEditLogger

        def connector(msg):
            self.appendPlainText(msg)

        self.signal.connect(connector)

    def set_logging_level(self, level) -> None:
        logging.basicConfig(level=(logging.DEBUG),
          format='%(asctime)-10s - %(module)-8s - %(levelname)-8s | %(message)s',
          datefmt='%Y-%m-%d %H:%M:%S',
          handlers=[
         self.log_handler()])
        logging.disable(level)


class CGFSUi(QWidget):

    def __init__(self):
        super().__init__()
        self.want_stop = True
        self.setWindowTitle('CodeGra.fs')
        self._CGFSUi__fields = {}
        layout = QVBoxLayout()
        err = codegra_fs.utils.get_fuse_install_message()
        if err:
            msg, url = err
            if url:
                msg += '\nYou can download it <a href="{}">here</a>.'.format(url)
            error_label = QLabel(msg)
            error_label.setTextFormat(Qt.RichText)
            error_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            error_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            error_label.setOpenExternalLinks(True)
            layout.addWidget(error_label)
        else:
            start_form = self._CGFSUi__create_start_form()
            run_dialog = self._CGFSUi__create_run_dialog()
            run_dialog.hide()
            layout.addWidget(start_form)
            layout.addWidget(run_dialog)
        self.setLayout(layout)
        width = 800
        height = 800
        top = 40
        left = 40
        self.setGeometry(left, top, width, height)
        self._CGFSUi__run_thread = None
        self.show()

    def __check_options(self) -> t.List[str]:
        err = []
        f = self._CGFSUi__fields
        if not f['username'].value:
            err.append('The username cannot be empty')
        if not f['password'].value:
            err.append('The password cannot be empty')
        if not f['url'].value:
            err.append('The url cannot be empty')
        mp = f['mountpoint'].value
        if not mp and os.path.isdir(mp) or os.listdir(mp):
            err.append('The mount directory should be an empty existing folder')
        return err

    def __start_cgfs(self) -> None:
        self.want_stop = False
        errs = self._CGFSUi__check_options()
        if errs:
            self._CGFSUi__errs_field.setText('\n'.join(('- {}'.format(e) for e in errs)))
            self._CGFSUi__errs_field.setVisible(True)
            return
        else:
            self._CGFSUi__errs_field.setVisible(False)
            if self._CGFSUi__fields['verbosity'].value == 'quiet':
                level = logging.INFO
            else:
                if self._CGFSUi__fields['verbosity'].value == 'verbose':
                    level = logging.NOTSET
                else:
                    level = logging.DEBUG
        self._CGFSUi__log_window.clear()
        self._CGFSUi__log_window.set_logging_level(level)

        class RunThread(QThread):

            def __init__(self, fields, outer):
                super().__init__()
                self._RunThread__fields = fields
                self.outer = outer

            def run(self) -> None:
                global PREVIOUS_VALUES_PATH
                f = self._RunThread__fields
                with open(PREVIOUS_VALUES_PATH, 'w') as (file):
                    json.dump({k:v.value for k, v in f.items() if k != 'password' if k != 'password'}, file)
                mountpoint = f['mountpoint'].value
                if sys.platform.startswith('win32'):
                    mountpoint = os.path.join(mountpoint, 'codegrade')
                try:
                    cgfs.create_and_mount_fs(username=(f['username'].value),
                      password=(f['password'].value),
                      url=(f['url'].value),
                      fixed=(f['fixed'].value),
                      assigned_only=(f['assigned_only'].value),
                      latest_only=(not f['all_submissions'].value),
                      mountpoint=mountpoint,
                      rubric_append_only=True)
                except:
                    pass

        self._CGFSUi__run_thread = RunThread(self._CGFSUi__fields, self)
        self._CGFSUi__run_thread.finished.connect(self.on_cgfs_stopped)
        self._CGFSUi__run_thread.start()
        self._CGFSUi__form_wrapper.setVisible(False)
        self._CGFSUi__run_wrapper.setVisible(True)

    def stop_cgfs(self) -> None:
        self.want_stop = True
        if self._CGFSUi__run_thread and self._CGFSUi__run_thread.isRunning():
            self._CGFSUi__log_window.appendPlainText('')
            self._CGFSUi__log_window.appendPlainText('Stopping and unmounting FS, this can take some time (especially on MacOS)')
            if cgfs.fuse_ptr is not None:
                fuse._libfuse.fuse_exit(cgfs.fuse_ptr)
                try:
                    os.listdir(self._CGFSUi__fields['mountpoint'].value)
                except BaseException:
                    pass

            self._CGFSUi__stop_button.setEnabled(False)
        else:
            self.on_cgfs_stopped()
        cgfs.fuse_ptr = None

    def on_cgfs_stopped(self) -> None:
        if not self.want_stop:
            logging.critical('========================')
            logging.critical('      FS crashed!')
            logging.critical('========================')
            return
        self._CGFSUi__run_thread = None
        self._CGFSUi__stop_button.setEnabled(True)
        self._CGFSUi__form_wrapper.setVisible(True)
        self._CGFSUi__run_wrapper.setVisible(False)
        self.want_stop = False

    def __create_run_dialog(self) -> QWidget:
        stop_button = QPushButton('Stop!')
        stop_button.clicked.connect(self.stop_cgfs)
        self._CGFSUi__stop_button = stop_button
        wrapper = QWidget()
        res = QVBoxLayout(wrapper)
        self._CGFSUi__log_window = CGFSLoggingWindow()
        res.addWidget(self._CGFSUi__log_window)
        res.addWidget(stop_button)
        self._CGFSUi__run_wrapper = wrapper
        return wrapper

    def __create_start_form(self) -> QWidget:
        try:
            with open(PREVIOUS_VALUES_PATH, 'r') as (f):
                prev_values = json.load(f)
        except:
            prev_values = {}

        form = CGFSFormLayout()
        fields = {'username':StringInput(default=prev_values.get('username')), 
         'password':StringInput(is_password=True), 
         'url':StringInput(default=os.getenv('CGAPI_BASE_URL', prev_values.get('url'))), 
         'fixed':CheckBoxInput(prev_values.get('fixed')), 
         'assigned_only':CheckBoxInput(prev_values.get('assigned_only')), 
         'mountpoint':DirectoryButton(self, prev_values.get('mountpoint')), 
         'all_submissions':CheckBoxInput(prev_values.get('all_submissions')), 
         'verbosity':CGFSRadioSelect([
          'verbose', 'normal', 'quiet'], prev_values.get('verbosity', 'normal'))}
        form.add_help_row('Username *', fields['username'], 'Your CodeGra.de username')
        form.add_help_row('Password *', fields['password'], constants.password_help)
        form.add_help_row('URL *', fields['url'], constants.url_help)
        form.add_help_row('Fixed mode', fields['fixed'], constants.fixed_mode_help)
        form.add_help_row('Assigned only', fields['assigned_only'], constants.assigned_only_help)
        form.add_help_row('All submissions', fields['all_submissions'], constants.all_submissions_help)
        form.add_help_row('Verbosity *', fields['verbosity'], "Amount of log output displayed. Set to 'verbose' when reporting bugs.")
        form.add_help_row('Mount directory *', fields['mountpoint'], constants.mountpoint_help)
        form.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        form.addRow(QLabel('* indicates a required field'))
        self._CGFSUi__errs_field = QLabel()
        self._CGFSUi__errs_field.setVisible(False)
        self._CGFSUi__errs_field.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._CGFSUi__errs_field.setStyleSheet('border: 1px solid red; background: white; padding: 5px;')
        start_button = QPushButton('Mount!')
        start_button.clicked.connect(self._CGFSUi__start_cgfs)
        wrapper = QWidget()
        self._CGFSUi__fields = fields
        self._CGFSUi__form_wrapper = wrapper
        res = QVBoxLayout(wrapper)
        if codegra_fs.utils.newer_version_available():
            version_label = QLabel('A new version of CodeGra.fs is available.\nYou can download it at <a href="https://codegra.de/codegra_fs/latest" >https://codegra.de/codegra_fs/latest</a>')
            version_label.setTextFormat(Qt.RichText)
            version_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            version_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            version_label.setOpenExternalLinks(True)
            version_label.setStyleSheet('border: 1px solid gray; padding: 5px;')
            res.addWidget(version_label)
            res.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))
        res.addLayout(form)
        res.addWidget(self._CGFSUi__errs_field)
        res.addWidget(start_button)
        return wrapper


def main() -> None:
    global PREVIOUS_VALUES_PATH
    appdir = AppDirs('CodeGra_fs', 'CodeGrade')
    PREVIOUS_VALUES_PATH = os.path.join(appdir.user_data_dir, 'prev_values.json')
    if not os.path.isdir(appdir.user_data_dir):
        os.makedirs((appdir.user_data_dir), exist_ok=True)
    app = QApplication(sys.argv)
    window = CGFSUi()
    try:
        app.exec_()
    finally:
        window.stop_cgfs()


if __name__ == '__main__':
    main()