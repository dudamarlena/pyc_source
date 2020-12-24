# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/scripts/launch_gui.py
# Compiled at: 2019-12-10 09:01:45
# Size of source mod 2**32: 32543 bytes
import datetime, os, re, psutil, shutil, sys, textwrap, numpy, circus, pkg_resources
try:
    from PyQt5 import uic
    from PyQt5.QtCore import Qt, QUrl, QProcess
    from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QDialog, QPushButton, QLineEdit, QWidget, QMessageBox
    from PyQt5.QtGui import QTextCursor, QDesktopServices, QFont, QIcon
except ImportError:
    try:
        from PySide import uic
        from PySide.QtCore import Qt, QUrl, QProcess
        from PySide.QtGui import QApplication, QFileDialog, QCheckBox, QPushButton, QLineEdit, QDialog, QWidget, QTextCursor, QMessageBox, QDesktopServices, QFont, QIcon
    except ImportError:
        from PyQt4 import uic
        from PyQt4.QtCore import Qt, QUrl, QProcess
        from PyQt4.QtGui import QApplication, QFileDialog, QCheckBox, QPushButton, QLineEdit, QWidget, QTextCursor, QMessageBox, QDesktopServices, QFont, QDialog, QIcon

from circus.shared.messages import print_error, print_info, print_and_log, get_colored_header, init_logging
from circus.files import __supported_data_files__, list_all_file_format
if sys.platform == 'win32':
    import ctypes

    class WinProcInfo(ctypes.Structure):
        _fields_ = [
         (
          'hProcess', ctypes.wintypes.HANDLE),
         (
          'hThread', ctypes.wintypes.HANDLE),
         (
          'dwProcessID', ctypes.wintypes.DWORD),
         (
          'dwThreadID', ctypes.wintypes.DWORD)]


    LPWinProcInfo = ctypes.POINTER(WinProcInfo)

def strip_ansi_codes(s):
    return re.sub('\\x1b\\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)


def to_str(b):
    """
    Helper function to convert a byte string (or a QByteArray) to a string --
    for Python 3, this specifies an encoding to not end up with "b'...'".
    """
    if sys.version_info[0] == 3:
        return str(b, encoding='ascii', errors='ignore')
    return str(b)


def overwrite_text(cursor, text):
    text_length = len(text)
    cursor.clearSelection()
    current_position = cursor.position()
    cursor.movePosition((QTextCursor.Right), mode=(QTextCursor.MoveAnchor),
      n=text_length)
    cursor.movePosition((QTextCursor.Left), mode=(QTextCursor.KeepAnchor),
      n=(cursor.position() - current_position))
    cursor.insertText(text)


class LaunchGUI(QDialog):

    def __init__(self, app):
        super(LaunchGUI, self).__init__()
        self.app = app
        self.init_gui_layout()

    def init_gui_layout(self):
        gui_fname = pkg_resources.resource_filename('circus', os.path.join('qt_GUI', 'qt_launcher.ui'))
        self.ui = uic.loadUi(gui_fname)
        self.task_comboboxes = [cb for cb in self.ui.grp_tasks.children() if isinstance(cb, QCheckBox)]
        logo = pkg_resources.resource_filename('circus', os.path.join('icons', 'icon.png'))
        self.ui.setWindowIcon(QIcon(logo))
        try:
            import cudamat as cmt
            cmt.init()
            self.HAVE_CUDA = True
        except Exception:
            self.HAVE_CUDA = False

        self.params = None
        self.ui.btn_run.clicked.connect(self.run)
        self.ui.btn_plots.clicked.connect(self.open_plot_folder)
        self.ui.btn_phy.clicked.connect(self.help_phy)
        self.ui.btn_matlab.clicked.connect(self.help_matlab)
        self.ui.btn_help_cpus.clicked.connect(self.help_cpus)
        self.ui.btn_help_gpus.clicked.connect(self.help_gpus)
        self.ui.btn_help_file_format.clicked.connect(self.help_file_format)
        self.ui.tabWidget.currentChanged.connect(self.changing_tab)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.ui.btn_file.clicked.connect(self.update_data_file)
        self.ui.btn_about.clicked.connect(self.show_about)
        self.ui.rb_gui_matlab.clicked.connect(self.update_gui_command)
        self.ui.rb_gui_python.clicked.connect(self.update_gui_command)
        self.ui.btn_output.clicked.connect(self.update_output_file)
        self.ui.btn_hostfile.clicked.connect(self.update_host_file)
        self.ui.btn_log.clicked.connect(self.open_log_file)
        self.ui.cb_batch.toggled.connect(self.update_batch_mode)
        self.ui.cb_preview.toggled.connect(self.update_preview_mode)
        self.ui.cb_results.toggled.connect(self.update_results_mode)
        self.ui.cb_benchmarking.toggled.connect(self.update_benchmarking)
        self.ui.cb_merging.toggled.connect(self.update_extension)
        self.ui.cb_converting.toggled.connect(self.update_extension)
        self.ui.cb_deconverting.toggled.connect(self.update_extension)
        self.update_benchmarking()
        self.update_extension()
        for cb in self.task_comboboxes:
            cb.toggled.connect(self.store_tasks)
            cb.toggled.connect(self.update_command)

        self.ui.edit_file.textChanged.connect(self.update_command)
        self.ui.edit_output.textChanged.connect(self.update_command)
        self.ui.edit_hostfile.textChanged.connect(self.update_command)
        self.ui.edit_extension.textChanged.connect(self.update_command)
        self.ui.gui_extension.textChanged.connect(self.update_gui_command)
        self.ui.param_editor.textChanged.connect(self.save_params)
        self.ui.spin_cpus.valueChanged.connect(self.update_command)
        if not self.HAVE_CUDA:
            self.ui.spin_gpus.setEnabled(False)
        self.ui.spin_gpus.valueChanged.connect(self.update_command)
        self.store_tasks()
        self.process = None
        self.ui.closeEvent = self.closeEvent
        self.last_log_file = None
        try:
            import sklearn
        except ImportError:
            self.ui.cb_validating.setEnabled(False)

        self.ui.show()

    def store_tasks(self):
        self.stored_tasks = [cb.isChecked() for cb in self.task_comboboxes]
        if not numpy.any(self.stored_tasks):
            self.ui.btn_run.setEnabled(False)
        else:
            if str(self.ui.edit_file.text()) != '':
                self.ui.btn_run.setEnabled(True)
                self.ui.btn_plots.setEnabled(True)

    def restore_tasks(self):
        for cb, prev_state in zip(self.task_comboboxes, self.stored_tasks):
            cb.setEnabled(True)
            cb.setChecked(prev_state)

    def update_batch_mode(self):
        batch_mode = self.ui.cb_batch.isChecked()
        self.ui.spin_cpus.setEnabled(not batch_mode)
        self.ui.spin_gpus.setEnabled(not batch_mode)
        self.ui.edit_hostfile.setEnabled(not batch_mode)
        self.ui.btn_hostfile.setEnabled(not batch_mode)
        self.update_tasks()
        self.update_extension()
        self.update_benchmarking()
        if batch_mode:
            self.ui.spin_cpus.setEnabled(not batch_mode)
            self.ui.spin_gpus.setEnabled(not batch_mode)
            self.ui.edit_hostfile.setEnabled(not batch_mode)
            self.ui.btn_hostfile.setEnabled(not batch_mode)
            self.update_tasks()
            self.update_extension()
            self.update_benchmarking()
            self.update_command()
            self.ui.cb_preview.setChecked(False)
            self.ui.cb_results.setChecked(False)
            self.ui.lbl_file.setText('Command file')
        else:
            self.last_mode = None
            self.ui.lbl_file.setText('Data file')
        self.update_command()

    def changing_tab(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.update_command()
        else:
            if self.ui.tabWidget.currentIndex() == 2:
                self.update_gui_command()

    def update_preview_mode(self):
        preview_mode = self.ui.cb_preview.isChecked()
        self.update_tasks()
        if preview_mode:
            self.ui.cb_batch.setChecked(False)
            self.ui.cb_results.setChecked(False)
        self.update_command()

    def update_results_mode(self):
        results_mode = self.ui.cb_results.isChecked()
        self.ui.spin_cpus.setEnabled(not results_mode)
        self.ui.spin_gpus.setEnabled(not results_mode)
        self.ui.edit_hostfile.setEnabled(not results_mode)
        self.ui.btn_hostfile.setEnabled(not results_mode)
        self.update_tasks()
        self.update_extension()
        self.update_benchmarking()
        self.update_command()
        if results_mode:
            self.ui.cb_batch.setChecked(False)
            self.ui.cb_preview.setChecked(False)

    def update_result_tab(self):
        if str(self.ui.edit_file.text()) != '':
            f_next, _ = os.path.splitext(str(self.ui.edit_file.text()))
            ft = os.path.basename(os.path.normpath(f_next))
            f_results = os.path.join(f_next, ft + '.result.hdf5')
            if os.path.exists(f_results):
                self.ui.selection_gui.setEnabled(True)
                self.ui.extension_gui.setEnabled(True)
        else:
            self.ui.selection_gui.setEnabled(False)
            self.ui.extension_gui.setEnabled(False)

    def update_extension(self):
        batch_mode = self.ui.cb_batch.isChecked()
        if not batch_mode:
            if self.ui.cb_merging.isChecked() or self.ui.cb_converting.isChecked() or self.ui.cb_deconverting.isChecked():
                self.ui.edit_extension.setEnabled(True)
        else:
            self.ui.edit_extension.setEnabled(False)

    def update_benchmarking(self):
        batch_mode = self.ui.cb_batch.isChecked()
        enable = not batch_mode and self.ui.cb_benchmarking.isChecked()
        self.ui.edit_output.setEnabled(enable)
        self.ui.btn_output.setEnabled(enable)
        self.ui.cmb_type.setEnabled(enable)
        self.update_command()

    def update_tasks(self):
        batch_mode = self.ui.cb_batch.isChecked()
        preview_mode = self.ui.cb_preview.isChecked()
        results_mode = self.ui.cb_results.isChecked()
        if batch_mode or results_mode:
            self.restore_tasks()
            for cb in self.task_comboboxes:
                cb.setEnabled(False)

        else:
            if preview_mode:
                prev_stored_tasks = self.stored_tasks
                for cb in self.task_comboboxes:
                    cb.setEnabled(False)
                    cb.setChecked(False)

                self.ui.cb_filtering.setChecked(True)
                self.ui.cb_whitening.setChecked(True)
                self.stored_tasks = prev_stored_tasks
            else:
                self.restore_tasks()
        self.update_command()

    def update_data_file(self):
        if self.ui.cb_batch.isChecked():
            title = 'Select file with list of commands'
        else:
            title = 'Select data file'
        fname = QFileDialog.getOpenFileName(self, title, self.ui.edit_file.text())
        if isinstance(fname, tuple):
            fname, _ = fname
        elif fname:
            self.ui.edit_file.setText(fname)
        elif str(self.ui.edit_file.text()) != '':
            self.ui.btn_run.setEnabled(True)
            f_next, _ = os.path.splitext(str(self.ui.edit_file.text()))
            self.params = f_next + '.params'
            self.last_log_file = f_next + '.log'
            if os.path.exists(self.params):
                self.ui.btn_plots.setEnabled(True)
                self.update_params()
        else:
            self.ui.btn_run.setEnabled(False)
        if self.ui.tabWidget.currentIndex() == 0:
            self.update_command()
        else:
            if self.ui.tabWidget.currentIndex() == 2:
                self.update_gui_command()
            self.update_result_tab()
            if self.params is not None:
                if not os.path.exists(self.params):
                    self.create_params_file(self.params)

    def update_params(self):
        f = open(self.params, 'r')
        lines = f.readlines()
        f.close()
        text = ''.join(lines)
        self.ui.param_editor.setPlainText(text)

    def save_params(self):
        all_text = self.ui.param_editor.toPlainText()
        myfile = open(self.params, 'w')
        myfile.write(all_text)
        myfile.close()

    def update_host_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select MPI host file', self.ui.edit_hostfile.text())
        if isinstance(fname, tuple):
            fname, _ = fname
        if fname:
            self.ui.edit_hostfile.setText(fname)

    def update_output_file(self):
        fname = QFileDialog.getSaveFileName(self, 'Output file name', self.ui.edit_output.text())
        if isinstance(fname, tuple):
            fname, _ = fname
        if fname:
            self.ui.edit_output.setText(fname)

    def open_log_file(self):
        assert self.last_log_file is not None
        QDesktopServices.openUrl(QUrl(self.last_log_file))

    def gui_command_line_args(self):
        if self.ui.rb_gui_matlab.isChecked():
            args = [
             'circus-gui-matlab']
        else:
            if self.ui.rb_gui_python.isChecked():
                args = [
                 'circus-gui-python']
        fname = str(self.ui.edit_file.text()).strip()
        if fname:
            args.append(fname)
        extension = str(self.ui.gui_extension.text()).strip()
        if extension:
            args.extend(['--extension', extension])
        return args

    def command_line_args(self):
        batch_mode = self.ui.cb_batch.isChecked()
        preview_mode = self.ui.cb_preview.isChecked()
        results_mode = self.ui.cb_results.isChecked()
        args = [
         'spyking-circus']
        fname = str(self.ui.edit_file.text()).strip()
        if fname:
            args.append(fname)
        if batch_mode:
            args.append('--batch')
        else:
            if preview_mode:
                args.append('--preview')
                if self.ui.spin_cpus.value() > 1:
                    args.extend(['--cpu', str(self.ui.spin_cpus.value())])
                if self.ui.spin_gpus.value() > 0:
                    args.extend(['--gpu', str(self.ui.spin_gpus.value())])
            else:
                if results_mode:
                    args.append('--result')
                else:
                    tasks = []
                    for cb in self.task_comboboxes:
                        if cb.isChecked():
                            label = str(cb.text()).lower()
                            tasks.append(label)

                    if len(tasks) > 0:
                        args.extend(['--method', ','.join(tasks)])
                    else:
                        if self.ui.spin_cpus.value() > 1:
                            args.extend(['--cpu', str(self.ui.spin_cpus.value())])
                        if self.ui.spin_gpus.value() > 0:
                            args.extend(['--gpu', str(self.ui.spin_gpus.value())])
                        hostfile = str(self.ui.edit_hostfile.text()).strip()
                        if hostfile:
                            args.extend(['--hostfile', hostfile])
                        if 'merging' in tasks or 'converting' in tasks:
                            extension = str(self.ui.edit_extension.text()).strip()
                            if extension:
                                args.extend(['--extension', extension])
                    if 'benchmarking' in tasks:
                        args.extend(['--output', str(self.ui.edit_output.text())])
                        args.extend(['--type', str(self.ui.cmb_type.currentText())])
                    return args

    def update_gui_command(self):
        args = ' '.join(self.gui_command_line_args())
        self.ui.edit_command.setPlainText(args)

    def update_command(self, text=None):
        args = ' '.join(self.command_line_args())
        self.ui.edit_command.setPlainText(args)

    def run(self):
        if self.ui.cb_batch.isChecked():
            self.last_log_file = None
        else:
            if self.params is None:
                self.create_params_file(self.params)
                return
                if not os.path.exists(self.params):
                    self.create_params_file(self.params)
                    return
            elif self.ui.tabWidget.currentIndex() == 0:
                args = self.command_line_args()
            else:
                if self.ui.tabWidget.currentIndex() == 2:
                    args = self.gui_command_line_args()
            self.update_result_tab()
            self.ui.edit_stdout.clear()
            format = self.ui.edit_stdout.currentCharFormat()
            format.setFontWeight(QFont.Normal)
            format.setForeground(Qt.blue)
            self.ui.edit_stdout.setCurrentCharFormat(format)
            time_str = datetime.datetime.now().ctime()
            start_msg = '                       Starting spyking circus at {time_str}.\n\n                       Command line call:\n                       {call}\n                    '.format(time_str=time_str, call=(' '.join(args)))
            self.ui.edit_stdout.appendPlainText(textwrap.dedent(start_msg))
            format.setForeground(Qt.black)
            self.ui.edit_stdout.setCurrentCharFormat(format)
            self.ui.edit_stdout.appendPlainText('\n')
            self.process = QProcess(self)
            self.process.readyReadStandardOutput.connect(self.append_output)
            self.process.readyReadStandardError.connect(self.append_error)
            self.process.started.connect(self.process_started)
            self.process.finished.connect(self.process_finished)
            self.process.error.connect(self.process_errored)
            self._interrupted = False
            self.process.start(args[0], args[1:])

    def restore_gui(self):
        for widget, previous_state in self._previous_state:
            widget.setEnabled(previous_state)

        self.app.restoreOverrideCursor()

    def process_started(self):
        all_children = [obj for obj in self.ui.findChildren(QWidget) if isinstance(obj, (QCheckBox, QPushButton, QLineEdit))]
        self._previous_state = [(obj, obj.isEnabled()) for obj in all_children]
        for obj in all_children:
            obj.setEnabled(False)

        self.ui.btn_stop.setEnabled(True)
        self.ui.edit_stdout.setTextInteractionFlags(Qt.NoTextInteraction)
        self.app.setOverrideCursor(Qt.WaitCursor)

    def process_finished(self, exit_code):
        format = self.ui.edit_stdout.currentCharFormat()
        format.setFontWeight(QFont.Bold)
        if exit_code == 0:
            if self._interrupted:
                color = Qt.red
                msg = 'Process interrupted by user'
            else:
                color = Qt.green
                msg = 'Process exited normally'
        else:
            color = Qt.red
            msg = 'Process exited with exit code %d' % exit_code
        format.setForeground(color)
        self.ui.edit_stdout.setCurrentCharFormat(format)
        self.ui.edit_stdout.appendPlainText(msg)
        self.restore_gui()
        self.ui.edit_stdout.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.process = None
        self.ui.btn_log.setEnabled(self.last_log_file is not None and os.path.isfile(self.last_log_file))

    def process_errored(self):
        try:
            exit_code = self.process.exitCode()
        except Exception:
            exit_code = 0

        format = self.ui.edit_stdout.currentCharFormat()
        format.setFontWeight(QFont.Bold)
        format.setForeground(Qt.red)
        self.ui.edit_stdout.setCurrentCharFormat(format)
        self.ui.edit_stdout.appendPlainText('Process exited with exit code' % exit_code)
        self.restore_gui()
        self.ui.edit_stdout.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.process = None

    def add_output_lines(self, lines):
        """
        Add the output line by line to the text area, jumping back to the
        beginning of the line when we encounter a carriage return (to
        correctly display progress bars)
        """
        cursor = self.ui.edit_stdout.textCursor()
        cursor.clearSelection()
        splitted_lines = lines.split('\n')
        for idx, line in enumerate(splitted_lines):
            if '\r' in line:
                chunks = line.split('\r')
                overwrite_text(cursor, chunks[0])
                for chunk in chunks[1:]:
                    cursor.movePosition(QTextCursor.StartOfLine)
                    overwrite_text(cursor, chunk)

            else:
                overwrite_text(cursor, line)
            if not '\n' in lines or idx == 0 or idx != len(splitted_lines) - 1:
                cursor.movePosition(QTextCursor.EndOfLine)
                cursor.insertText('\n')

        self.ui.edit_stdout.setTextCursor(cursor)

    def append_output--- This code section failed: ---

 L. 548         0  LOAD_FAST                'self'
                2  LOAD_ATTR                process
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 549        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 550        14  LOAD_GLOBAL              strip_ansi_codes
               16  LOAD_GLOBAL              to_str
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                process
               22  LOAD_METHOD              readAllStandardOutput
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'lines'

 L. 551        32  LOAD_FAST                'self'
               34  LOAD_METHOD              add_output_lines
               36  LOAD_FAST                'lines'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_TOP          

 L. 553        42  LOAD_STR                 'Export already made! Do you want to erase everything? (y)es / (n)o'
               44  LOAD_FAST                'lines'
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE   138  'to 138'

 L. 554        50  LOAD_GLOBAL              QMessageBox
               52  CALL_FUNCTION_0       0  '0 positional arguments'
               54  STORE_FAST               'msg'

 L. 555        56  LOAD_FAST                'msg'
               58  LOAD_METHOD              setIcon
               60  LOAD_GLOBAL              QMessageBox
               62  LOAD_ATTR                Question
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          

 L. 556        68  LOAD_FAST                'msg'
               70  LOAD_METHOD              setWindowTitle
               72  LOAD_STR                 'Erase everything?'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_TOP          

 L. 557        78  LOAD_FAST                'msg'
               80  LOAD_METHOD              setText
               82  LOAD_STR                 'Export already made! Do you want to erase everything?'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_TOP          

 L. 558        88  LOAD_FAST                'msg'
               90  LOAD_METHOD              setStandardButtons
               92  LOAD_GLOBAL              QMessageBox
               94  LOAD_ATTR                Yes
               96  LOAD_GLOBAL              QMessageBox
               98  LOAD_ATTR                No
              100  BINARY_OR        
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_TOP          

 L. 559       106  LOAD_FAST                'msg'
              108  LOAD_METHOD              exec_
              110  CALL_METHOD_0         0  '0 positional arguments'
              112  STORE_FAST               'answer'

 L. 560       114  LOAD_FAST                'answer'
              116  LOAD_GLOBAL              QMessageBox
              118  LOAD_ATTR                Yes
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   130  'to 130'

 L. 561       124  LOAD_STR                 'y'
              126  STORE_FAST               'answer_string'
              128  JUMP_FORWARD        500  'to 500'
            130_0  COME_FROM           122  '122'

 L. 563       130  LOAD_STR                 'n'
              132  STORE_FAST               'answer_string'
          134_136  JUMP_FORWARD        500  'to 500'
            138_0  COME_FROM            48  '48'

 L. 564       138  LOAD_STR                 'Do you want SpyKING CIRCUS to export PCs? (a)ll / (s)ome / (n)o'
              140  LOAD_FAST                'lines'
              142  COMPARE_OP               in
          144_146  POP_JUMP_IF_FALSE   300  'to 300'

 L. 565       148  LOAD_GLOBAL              QMessageBox
              150  CALL_FUNCTION_0       0  '0 positional arguments'
              152  STORE_FAST               'msg'

 L. 566       154  LOAD_FAST                'msg'
              156  LOAD_METHOD              setIcon
              158  LOAD_GLOBAL              QMessageBox
              160  LOAD_ATTR                Question
              162  CALL_METHOD_1         1  '1 positional argument'
              164  POP_TOP          

 L. 567       166  LOAD_FAST                'msg'
              168  LOAD_METHOD              setWindowTitle
              170  LOAD_STR                 'Export PCs?'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_TOP          

 L. 568       176  LOAD_FAST                'msg'
              178  LOAD_METHOD              setText
              180  LOAD_STR                 'Do you want SpyKING CIRCUS to export PCs?'
              182  CALL_METHOD_1         1  '1 positional argument'
              184  POP_TOP          

 L. 569       186  LOAD_FAST                'msg'
              188  LOAD_METHOD              addButton
              190  LOAD_STR                 'No'
              192  LOAD_GLOBAL              QMessageBox
              194  LOAD_ATTR                NoRole
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  STORE_FAST               'no_button'

 L. 570       200  LOAD_FAST                'msg'
              202  LOAD_METHOD              addButton
              204  LOAD_STR                 'Some'
              206  LOAD_GLOBAL              QMessageBox
              208  LOAD_ATTR                YesRole
              210  CALL_METHOD_2         2  '2 positional arguments'
              212  STORE_FAST               'some_button'

 L. 571       214  LOAD_FAST                'msg'
              216  LOAD_METHOD              addButton
              218  LOAD_STR                 'All'
              220  LOAD_GLOBAL              QMessageBox
              222  LOAD_ATTR                YesRole
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  STORE_FAST               'all_button'

 L. 572       228  LOAD_FAST                'msg'
              230  LOAD_METHOD              exec_
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  POP_TOP          

 L. 573       236  LOAD_FAST                'msg'
              238  LOAD_METHOD              clickedButton
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  LOAD_FAST                'no_button'
              244  COMPARE_OP               ==
              246  POP_JUMP_IF_FALSE   254  'to 254'

 L. 574       248  LOAD_STR                 'n'
              250  STORE_FAST               'answer_string'
              252  JUMP_FORWARD        298  'to 298'
            254_0  COME_FROM           246  '246'

 L. 575       254  LOAD_FAST                'msg'
              256  LOAD_METHOD              clickedButton
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  LOAD_FAST                'some_button'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   274  'to 274'

 L. 576       268  LOAD_STR                 's'
              270  STORE_FAST               'answer_string'
              272  JUMP_FORWARD        298  'to 298'
            274_0  COME_FROM           264  '264'

 L. 577       274  LOAD_FAST                'msg'
              276  LOAD_METHOD              clickedButton
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  LOAD_FAST                'all_button'
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   294  'to 294'

 L. 578       288  LOAD_STR                 'a'
              290  STORE_FAST               'answer_string'
              292  JUMP_FORWARD        298  'to 298'
            294_0  COME_FROM           284  '284'

 L. 580       294  LOAD_STR                 'n'
              296  STORE_FAST               'answer_string'
            298_0  COME_FROM           292  '292'
            298_1  COME_FROM           272  '272'
            298_2  COME_FROM           252  '252'
              298  JUMP_FORWARD        500  'to 500'
            300_0  COME_FROM           144  '144'

 L. 581       300  LOAD_STR                 'Do you want to delete these files? [Y/n]'
              302  LOAD_FAST                'lines'
              304  COMPARE_OP               in
          306_308  POP_JUMP_IF_FALSE   398  'to 398'

 L. 582       310  LOAD_GLOBAL              QMessageBox
              312  CALL_FUNCTION_0       0  '0 positional arguments'
              314  STORE_FAST               'msg'

 L. 583       316  LOAD_FAST                'msg'
              318  LOAD_METHOD              setIcon
              320  LOAD_GLOBAL              QMessageBox
              322  LOAD_ATTR                Question
              324  CALL_METHOD_1         1  '1 positional argument'
              326  POP_TOP          

 L. 584       328  LOAD_FAST                'msg'
              330  LOAD_METHOD              setWindowTitle
              332  LOAD_STR                 'Delete everything?'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          

 L. 585       338  LOAD_FAST                'msg'
              340  LOAD_METHOD              setText
              342  LOAD_STR                 'Files already deconverted! Do you want to delete everything?'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  POP_TOP          

 L. 586       348  LOAD_FAST                'msg'
              350  LOAD_METHOD              setStandardButtons
              352  LOAD_GLOBAL              QMessageBox
              354  LOAD_ATTR                Yes
              356  LOAD_GLOBAL              QMessageBox
              358  LOAD_ATTR                No
              360  BINARY_OR        
              362  CALL_METHOD_1         1  '1 positional argument'
              364  POP_TOP          

 L. 587       366  LOAD_FAST                'msg'
              368  LOAD_METHOD              exec_
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  STORE_FAST               'answer'

 L. 588       374  LOAD_FAST                'answer'
              376  LOAD_GLOBAL              QMessageBox
              378  LOAD_ATTR                Yes
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   392  'to 392'

 L. 589       386  LOAD_STR                 'y'
              388  STORE_FAST               'answer_string'
              390  JUMP_FORWARD        396  'to 396'
            392_0  COME_FROM           382  '382'

 L. 591       392  LOAD_STR                 'n'
              394  STORE_FAST               'answer_string'
            396_0  COME_FROM           390  '390'
              396  JUMP_FORWARD        500  'to 500'
            398_0  COME_FROM           306  '306'

 L. 592       398  LOAD_STR                 'You should re-export the data because of a fix in 0.6'
              400  LOAD_FAST                'lines'
              402  COMPARE_OP               in
          404_406  POP_JUMP_IF_FALSE   496  'to 496'

 L. 593       408  LOAD_GLOBAL              QMessageBox
              410  CALL_FUNCTION_0       0  '0 positional arguments'
              412  STORE_FAST               'msg'

 L. 594       414  LOAD_FAST                'msg'
              416  LOAD_METHOD              setIcon
              418  LOAD_GLOBAL              QMessageBox
              420  LOAD_ATTR                Question
              422  CALL_METHOD_1         1  '1 positional argument'
              424  POP_TOP          

 L. 595       426  LOAD_FAST                'msg'
              428  LOAD_METHOD              setWindowTitle
              430  LOAD_STR                 'You should re-export the data because of a fix in 0.6'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  POP_TOP          

 L. 596       436  LOAD_FAST                'msg'
              438  LOAD_METHOD              setText
              440  LOAD_STR                 'Continue anyway (results may not be fully correct)?'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          

 L. 597       446  LOAD_FAST                'msg'
              448  LOAD_METHOD              setStandardButtons
              450  LOAD_GLOBAL              QMessageBox
              452  LOAD_ATTR                Yes
              454  LOAD_GLOBAL              QMessageBox
              456  LOAD_ATTR                No
              458  BINARY_OR        
              460  CALL_METHOD_1         1  '1 positional argument'
              462  POP_TOP          

 L. 598       464  LOAD_FAST                'msg'
              466  LOAD_METHOD              exec_
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  STORE_FAST               'answer'

 L. 599       472  LOAD_FAST                'answer'
              474  LOAD_GLOBAL              QMessageBox
              476  LOAD_ATTR                Yes
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   490  'to 490'

 L. 600       484  LOAD_STR                 'y'
              486  STORE_FAST               'answer_string'
              488  JUMP_FORWARD        494  'to 494'
            490_0  COME_FROM           480  '480'

 L. 602       490  LOAD_STR                 'n'
            492_0  COME_FROM           128  '128'
              492  STORE_FAST               'answer_string'
            494_0  COME_FROM           488  '488'
              494  JUMP_FORWARD        500  'to 500'
            496_0  COME_FROM           404  '404'

 L. 604       496  LOAD_STR                 ''
              498  STORE_FAST               'answer_string'
            500_0  COME_FROM           494  '494'
            500_1  COME_FROM           396  '396'
            500_2  COME_FROM           298  '298'
            500_3  COME_FROM           134  '134'

 L. 606       500  LOAD_FAST                'answer_string'
          502_504  POP_JUMP_IF_FALSE   546  'to 546'

 L. 607       506  LOAD_FAST                'answer_string'
              508  LOAD_STR                 '\n'
              510  BINARY_ADD       
              512  STORE_FAST               'to_write'

 L. 608       514  LOAD_FAST                'to_write'
              516  LOAD_METHOD              encode
              518  LOAD_STR                 'utf-8'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  STORE_FAST               'to_write'

 L. 609       524  LOAD_FAST                'self'
              526  LOAD_ATTR                process
              528  LOAD_METHOD              write
              530  LOAD_FAST                'to_write'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  POP_TOP          

 L. 610       536  LOAD_FAST                'self'
              538  LOAD_METHOD              add_output_lines
              540  LOAD_FAST                'to_write'
              542  CALL_METHOD_1         1  '1 positional argument'
              544  POP_TOP          
            546_0  COME_FROM           502  '502'

Parse error at or near `COME_FROM' instruction at offset 492_0

    def append_error(self):
        if self.process is None:
            return
        lines = strip_ansi_codes(to_str(self.process.readAllStandardError()))
        self.add_output_lines(lines)

    def stop(self, force=False):
        if self.process is not None:
            if not force:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Confirm process termination')
                msg.setText('This will terminate the running process. Are you sure you want to do this?')
                msg.setInformativeText('Interrupting the process may leave partly created files that cannot be used for further analysis.')
                msg.addButton('Stop process', QMessageBox.YesRole)
                cancel_button = msg.addButton('Cancel', QMessageBox.NoRole)
                msg.setDefaultButton(cancel_button)
                msg.exec_()
                if msg.clickedButton() == cancel_button:
                    return
            else:
                self._interrupted = True
                pid = int(self.process.pid())
                if sys.platform == 'win32' and pid != 0:
                    lp = ctypes.cast(pid, LPWinProcInfo)
                    pid = lp.contents.dwProcessID
            if pid != 0:
                process = psutil.Process(pid)
                children = process.children(recursive=True)
                for proc in children:
                    proc.terminate()

                gone, alive = psutil.wait_procs(children, timeout=3)
                for proc in alive:
                    proc.kill()

                self.process.terminate()
                self.process = None

    def create_params_file(self, fname):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Parameter file %r not found, do you want SpyKING CIRCUS to create it for you?' % fname)
        msg.setWindowTitle('Generate parameter file?')
        msg.setInformativeText("This will create a parameter file from a template file and open it in your system's standard text editor. Fill properly before launching the code. See the documentation for details")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        answer = msg.exec_()
        if answer == QMessageBox.Yes:
            user_path = os.path.join(os.path.expanduser('~'), 'spyking-circus')
            if os.path.exists(user_path + 'config.params'):
                config_file = os.path.abspath(user_path + 'config.params')
            else:
                config_file = os.path.abspath(pkg_resources.resource_filename('circus', 'config.params'))
            shutil.copyfile(config_file, fname)
            self.params = fname
            self.last_log_file = fname.replace('.params', '.log')
            self.update_params()

    def show_about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('SpyKING CIRCUS v%s' % circus.__version__)
        msg.setWindowTitle('About')
        msg.setInformativeText('Documentation can be found at\nhttp://spyking-circus.rtfd.org\n\nOpen a browser to see the online help?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        answer = msg.exec_()
        if answer == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl('http://spyking-circus.rtfd.org'))

    def help_cpus(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Setting the number of CPUs')
        msg.setWindowTitle('Number of CPUs')
        msg.setInformativeText('SpyKING CIRCUS can use several CPUs either locally or on multiple machines using MPI (see documentation) \n\nYou have %d local CPUs available' % psutil.cpu_count())
        msg.setStandardButtons(QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Close)
        answer = msg.exec_()

    def help_gpus(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Setting the number of GPUs')
        msg.setWindowTitle('Number of GPUs')
        if not self.HAVE_CUDA:
            info = 'No GPUs are detected on your system'
        else:
            gpu_id = 0
            is_available = True
            while is_available:
                try:
                    cmt.cuda_set_device(gpu_id)
                    is_available = True
                except Exception:
                    is_available = False

            info = '%d GPU is detected on your system' % (gpu_id + 1)
        msg.setInformativeText('SpyKING CIRCUS can use several GPUs\neither locally or on multiple machine\nusing MPI (see documentation)\n\n%s' % info)
        msg.setStandardButtons(QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Close)
        answer = msg.exec_()

    def help_file_format(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Supported file formats')
        msg.setWindowTitle('File formats')
        msg.setInformativeText('\n'.join(list_all_file_format()))
        msg.setStandardButtons(QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Close)
        answer = msg.exec_()

    def open_plot_folder(self):
        f_next, _ = os.path.splitext(str(self.ui.edit_file.text()))
        plot_folder = os.path.join(f_next, 'plots')
        QDesktopServices.openUrl(QUrl(plot_folder))

    def help_phy(self):
        QDesktopServices.openUrl(QUrl('https://github.com/kwikteam/phy-contrib'))

    def help_matlab(self):
        QDesktopServices.openUrl(QUrl('http://ch.mathworks.com/products/matlab/'))

    def closeEvent(self, event):
        if self.process is not None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Confirm process interruption')
            msg.setText('Closing the window will terminate the running process. Do you really want to exit?')
            msg.setInformativeText('Interrupting the process may leave partly created files that cannot be used for further analysis.')
            close_button = msg.addButton('Stop and close', QMessageBox.YesRole)
            cancel_button = msg.addButton('Cancel', QMessageBox.NoRole)
            msg.setDefaultButton(cancel_button)
            msg.exec_()
            if msg.clickedButton() == close_button:
                self.stop(force=True)
                super(LaunchGUI, self).closeEvent(event)
            else:
                event.ignore()


def main():
    app = QApplication([])
    gui = LaunchGUI(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()