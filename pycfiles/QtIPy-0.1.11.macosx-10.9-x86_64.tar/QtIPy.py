# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/qtipy/QtIPy.py
# Compiled at: 2014-05-14 23:17:18
from __future__ import unicode_literals
import sys, logging
frozen = getattr(sys, b'frozen', None)
if frozen:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import os, re
from .qt import *
from . import utils
from .translate import tr
from datetime import datetime, timedelta
import traceback
VERSION_STRING = b'0.0.1'
from pyqtconfig import ConfigManager
import os, sys, time
try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, NotebookNode
from IPython.nbconvert.exporters import export as IPyexport
from IPython.nbconvert.exporters.export import exporter_map as IPyexporter_map
from IPython.utils.ipstruct import Struct
from runipy.notebook_runner import NotebookRunner
_w = None
MODE_MANUAL = 0
MODE_WATCH_FILES = 1
MODE_WATCH_FOLDER = 2
MODE_TIMER = 3

class NotebookNotFound(Exception):
    pass


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Logger(logging.Handler):

    def __init__(self, parent, widget, out=None, color=None):
        super(Logger, self).__init__()
        self.m = parent
        self.widget = widget
        self.out = None
        self.color = color
        return

    def emit(self, record):
        msg = self.format(record)
        color = {logging.CRITICAL: QColor(164, 0, 0, 50), 
           logging.ERROR: QColor(239, 41, 41, 50), 
           logging.WARNING: QColor(252, 233, 79, 50), 
           logging.INFO: QColor(0, 0, 0, 255), 
           logging.DEBUG: QColor(114, 159, 207, 50), 
           logging.NOTSET: QColor(0, 0, 0, 255)}[record.levelno]
        rows = self.widget._current_rows
        if rows:
            rows = rows[-50:]
        rows.append(b'<pre style="color:%s;">%s</pre>' % (color.name(), msg.replace(b'\n', b'<br />')))
        self.widget._current_rows = rows
        self.widget.setHtml(b'<html><body>' + (b'\n\n\n').join(rows) + b'</body></html>')

    def write(self, m):
        pass


class GenericDialog(QDialog):
    """
    A generic dialog wrapper that handles most common dialog setup/shutdown functions.
    
    Support for config, etc. to be added for auto-handling widgets and config load/save. 
    """

    def __init__(self, parent, buttons=[
 b'ok', b'cancel'], **kwargs):
        super(GenericDialog, self).__init__(parent, **kwargs)
        self.sizer = QVBoxLayout()
        self.layout = QVBoxLayout()
        QButtons = {b'ok': QDialogButtonBox.Ok, 
           b'cancel': QDialogButtonBox.Cancel}
        Qbtn = 0
        for k in buttons:
            Qbtn = Qbtn | QButtons[k]

        self.buttonBox = QDialogButtonBox(Qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def finalise(self):
        self.sizer.addLayout(self.layout)
        self.sizer.addWidget(self.buttonBox)
        self.setLayout(self.sizer)


class AutomatonDialog(GenericDialog):
    mode_options = {b'Manual': MODE_MANUAL, 
       b'Watch files': MODE_WATCH_FILES, 
       b'Watch folder': MODE_WATCH_FOLDER, 
       b'Timer': MODE_TIMER}

    def __init__(self, parent, **kwargs):
        super(AutomatonDialog, self).__init__(parent, **kwargs)
        self.setWindowTitle(b'Edit Automaton')
        self.config = ConfigManager()
        gb = QGroupBox(b'IPython notebook(s) (*.ipynb)')
        grid = QGridLayout()
        notebook_path_le = QLineEdit()
        self.config.add_handler(b'notebook_paths', notebook_path_le, mapper=(lambda x: x.split(b';'), lambda x: (b';').join(x)))
        grid.addWidget(notebook_path_le, 0, 0, 1, 2)
        notebook_path_btn = QToolButton()
        notebook_path_btn.setIcon(QIcon(os.path.join(utils.scriptdir, b'icons', b'document-attribute-i.png')))
        notebook_path_btn.clicked.connect(lambda : self.onNotebookBrowse(notebook_path_le))
        grid.addWidget(notebook_path_btn, 0, 2, 1, 1)
        gb.setLayout(grid)
        self.layout.addWidget(gb)
        gb = QGroupBox(b'Automaton mode')
        grid = QGridLayout()
        mode_cb = QComboBox()
        mode_cb.addItems(self.mode_options.keys())
        mode_cb.currentIndexChanged.connect(self.onChangeMode)
        self.config.add_handler(b'mode', mode_cb, mapper=self.mode_options)
        grid.addWidget(QLabel(b'Mode'), 0, 0)
        grid.addWidget(mode_cb, 0, 1)
        grid.addWidget(QLabel(b'Hold trigger'), 1, 0)
        fwatcher_hold_sb = QSpinBox()
        fwatcher_hold_sb.setRange(0, 60)
        fwatcher_hold_sb.setSuffix(b' secs')
        self.config.add_handler(b'trigger_hold', fwatcher_hold_sb)
        grid.addWidget(fwatcher_hold_sb, 1, 1)
        gb.setLayout(grid)
        self.layout.addWidget(gb)
        self.watchfile_gb = QGroupBox(b'Watch files')
        grid = QGridLayout()
        watched_path_le = QLineEdit()
        grid.addWidget(watched_path_le, 0, 0, 1, 2)
        self.config.add_handler(b'watched_files', watched_path_le, mapper=(lambda x: x.split(b';'), lambda x: (b';').join(x)))
        watched_path_btn = QToolButton()
        watched_path_btn.setIcon(QIcon(os.path.join(utils.scriptdir, b'icons', b'document-copy.png')))
        watched_path_btn.setStatusTip(b'Add file(s)')
        watched_path_btn.clicked.connect(lambda : self.onFilesBrowse(watched_path_le))
        grid.addWidget(watched_path_btn, 0, 2, 1, 1)
        grid.addWidget(QLabel(b'Watch window'), 1, 0)
        watch_window_sb = QSpinBox()
        watch_window_sb.setRange(0, 60)
        watch_window_sb.setSuffix(b' secs')
        self.config.add_handler(b'watch_window', watch_window_sb)
        grid.addWidget(watch_window_sb, 1, 1)
        self.watchfile_gb.setLayout(grid)
        self.layout.addWidget(self.watchfile_gb)
        self.watchfolder_gb = QGroupBox(b'Watch folder')
        grid = QGridLayout()
        watched_path_le = QLineEdit()
        grid.addWidget(watched_path_le, 0, 0, 1, 3)
        self.config.add_handler(b'watched_folder', watched_path_le)
        watched_path_btn = QToolButton()
        watched_path_btn.setIcon(QIcon(os.path.join(utils.scriptdir, b'icons', b'folder-horizontal-open.png')))
        watched_path_btn.setStatusTip(b'Add folder')
        watched_path_btn.clicked.connect(lambda : self.onFolderBrowse(watched_path_le))
        grid.addWidget(watched_path_btn, 0, 3, 1, 1)
        grid.addWidget(QLabel(b'Iterate files in folder'), 3, 0)
        loop_folder_sb = QCheckBox()
        self.config.add_handler(b'iterate_watched_folder', loop_folder_sb)
        grid.addWidget(loop_folder_sb, 3, 1)
        loop_wildcard_le = QLineEdit()
        self.config.add_handler(b'iterate_wildcard', loop_wildcard_le)
        grid.addWidget(loop_wildcard_le, 3, 2)
        self.watchfolder_gb.setLayout(grid)
        self.layout.addWidget(self.watchfolder_gb)
        self.timer_gb = QGroupBox(b'Timer')
        grid = QGridLayout()
        grid.addWidget(QLabel(b'Run every'), 0, 0)
        watch_timer_sb = QSpinBox()
        watch_timer_sb.setRange(0, 60)
        watch_timer_sb.setSuffix(b' secs')
        self.config.add_handler(b'timer_seconds', watch_timer_sb)
        grid.addWidget(watch_timer_sb, 0, 1)
        self.timer_gb.setLayout(grid)
        self.layout.addWidget(self.timer_gb)
        self.manual_gb = QGroupBox(b'Manual')
        grid = QGridLayout()
        grid.addWidget(QLabel(b'No configuration'), 0, 0)
        self.manual_gb.setLayout(grid)
        self.layout.addWidget(self.manual_gb)
        gb = QGroupBox(b'Output')
        grid = QGridLayout()
        output_path_le = QLineEdit()
        self.config.add_handler(b'output_path', output_path_le)
        grid.addWidget(output_path_le, 0, 0, 1, 2)
        notebook_path_btn = QToolButton()
        notebook_path_btn.setIcon(QIcon(os.path.join(utils.scriptdir, b'icons', b'folder-horizontal-open.png')))
        notebook_path_btn.clicked.connect(lambda : self.onFolderBrowse(notebook_path_le))
        grid.addWidget(notebook_path_btn, 0, 2, 1, 1)
        export_cb = QComboBox()
        export_cb.addItems(IPyexporter_map.keys())
        self.config.add_handler(b'output_format', export_cb)
        grid.addWidget(QLabel(b'Notebook output format'), 1, 0)
        grid.addWidget(export_cb, 1, 1)
        gb.setLayout(grid)
        self.layout.addWidget(gb)
        self.layout.addStretch()
        self.finalise()
        self.onChangeMode(mode_cb.currentIndex())

    def onNotebookBrowse(self, t):
        global _w
        filenames, _ = QFileDialog.getOpenFileNames(_w, b'Load IPython notebook(s)', b'', b'IPython Notebooks (*.ipynb);;All files (*.*)')
        if filenames:
            self.config.set(b'notebook_paths', filenames)

    def onFolderBrowse(self, t):
        filename = QFileDialog.getExistingDirectory(_w, b'Select folder to watch')
        if filename:
            self.config.set(b'watched_folder', filename)

    def onFilesBrowse(self, t):
        filenames, _ = QFileDialog.getOpenFileNames(_w, b'Select file(s) to watch')
        if filenames:
            self.config.set(b'watched_files', filenames)

    def onChangeMode(self, i):
        for m, gb in {MODE_MANUAL: self.manual_gb, MODE_WATCH_FILES: self.watchfile_gb, MODE_WATCH_FOLDER: self.watchfolder_gb, MODE_TIMER: self.timer_gb}.items():
            if m == list(self.mode_options.items())[i][1]:
                gb.show()
            else:
                gb.hide()

    def sizeHint(self):
        return QSize(400, 200)


class AutomatonListDelegate(QAbstractItemDelegate):

    def paint(self, painter, option, index):
        ic = QIcon(index.data(Qt.DecorationRole))
        automaton = index.data(Qt.UserRole)
        f = QFont()
        f.setPointSize(10)
        painter.setFont(f)
        if automaton.is_running:
            painter.setPen(QPalette().text().color())
            painter.fillRect(option.rect, QBrush(QColor(0, 255, 0, 50)))
        elif automaton.latest_run[b'success'] == False:
            painter.setPen(QPalette().text().color())
            painter.fillRect(option.rect, QBrush(QColor(255, 0, 0, 50)))
        elif option.state & QStyle.State_Selected:
            painter.setPen(QPalette().highlightedText().color())
            painter.fillRect(option.rect, QBrush(QPalette().highlight().color()))
        else:
            painter.setPen(QPalette().text().color())
        r = QRect(5, 4, 12, 12)
        r.translate(option.rect.x(), option.rect.y())
        icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'document-attribute-i-sm.png'))
        painter.drawPixmap(r, icn.pixmap(QSize(12, 12)))
        r = QRect(5, 36, 12, 12)
        r.translate(option.rect.x(), option.rect.y())
        icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'disk-sm.png'))
        painter.drawPixmap(r, icn.pixmap(QSize(12, 12)))
        pen = QPen()
        if automaton.config.get(b'is_active'):
            pen.setColor(QColor(b'black'))
        else:
            pen.setColor(QColor(b'#aaaaaa'))
        painter.setPen(pen)
        r = QRect(20, 4, option.rect.width() - 40, 20)
        r.translate(option.rect.x(), option.rect.y())
        painter.drawText(r, Qt.AlignLeft, (b';').join(automaton.config.get(b'notebook_paths')))
        r = QRect(20, 36, option.rect.width() - 40, 20)
        r.translate(option.rect.x(), option.rect.y())
        painter.drawText(r, Qt.AlignLeft, automaton.config.get(b'output_path'))
        r = QRect(20, 20, option.rect.width() - 40, 20)
        r.translate(option.rect.x(), option.rect.y())
        if automaton.config.get(b'mode') == MODE_WATCH_FILES:
            painter.drawText(r, Qt.AlignLeft, (b';').join(automaton.config.get(b'watched_files')))
            icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'document-copy-sm.png'))
        elif automaton.config.get(b'mode') == MODE_WATCH_FOLDER:
            painter.drawText(r, Qt.AlignLeft, automaton.config.get(b'watched_folder'))
            icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'folder-horizontal-open-sm.png'))
        elif automaton.config.get(b'mode') == MODE_TIMER:
            painter.drawText(r, Qt.AlignLeft, b'%s seconds(s)' % automaton.config.get(b'timer_seconds'))
            icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'clock-select-sm.png'))
        elif automaton.config.get(b'mode') == MODE_MANUAL:
            icn = QIcon(os.path.join(utils.scriptdir, b'icons', b'hand-finger-sm.png'))
        r = QRect(5, 20, 12, 12)
        r.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(r, icn.pixmap(QSize(12, 12)))
        if automaton.latest_run[b'timestamp']:
            r = QRect(5, 52, option.rect.width() - 10, 20)
            r.translate(option.rect.x(), option.rect.y())
            painter.drawText(r, Qt.AlignLeft, b'Latest run: %s' % automaton.latest_run[b'timestamp'].strftime(b'%Y-%m-%d %H:%M:%S'))

    def sizeHint(self, option, index):
        return QSize(200, 70)


class Automaton(QStandardItem):

    def __init__(self, *args, **kwargs):
        super(Automaton, self).__init__(*args, **kwargs)
        self.setData(self, Qt.UserRole)
        self.watcher = QFileSystemWatcher()
        self.timer = QTimer()
        self.watch_window = {}
        self.latest_run = {}
        self.is_running = False
        self.config = ConfigManager()
        self.config.set_defaults({b'mode': MODE_WATCH_FOLDER, 
           b'is_active': True, 
           b'trigger_hold': 1, 
           b'notebook_paths': b'', 
           b'output_path': b'{home}/{notebook_filename}_{datetime}_', 
           b'output_format': b'html', 
           b'watched_files': [], b'watched_folder': b'', 
           b'watch_window': 15, 
           b'iterate_watched_folder': True, 
           b'iterate_wildcard': b'.csv', 
           b'timer_seconds': 60})
        self.runner = None
        self.lock = None
        self.latest_run = {b'timestamp': None, 
           b'success': None}
        self.watcher.fileChanged.connect(self.file_trigger_accumulator)
        self.watcher.directoryChanged.connect(self.trigger)
        self.timer.timeout.connect(self.trigger)
        return

    def startup(self):
        if self.config.get(b'is_active') == False:
            return False
        if self.config.get(b'mode') == MODE_TIMER:
            self.timer.setInterval(self.config.get(b'timer_seconds') * 1000)
            self.timer.start()
        elif self.config.get(b'mode') == MODE_WATCH_FILES:
            current_paths = self.watcher.files() + self.watcher.directories()
            if current_paths:
                self.watcher.removePaths(current_paths)
            self.watch_window = {}
            self.watcher.addPaths(self.config.get(b'watched_files'))
        elif self.config.get(b'mode') == MODE_WATCH_FOLDER:
            current_paths = self.watcher.files() + self.watcher.directories()
            if current_paths:
                self.watcher.removePaths(current_paths)
            self.watcher.addPath(self.config.get(b'watched_folder'))

    def shutdown(self):
        if self.config.get(b'mode') == MODE_TIMER:
            self.timer.stop()
        elif self.config.get(b'mode') == MODE_WATCH_FILES or self.config.get(b'mode') == MODE_WATCH_FOLDER:
            current_paths = self.watcher.files() + self.watcher.directories()
            if current_paths:
                self.watcher.removePaths(current_paths)
            self.watch_window = {}

    def load_notebook(self, filename):
        try:
            with open(filename) as (f):
                nb = reads(f.read(), b'json')
        except:
            return

        return nb
        return

    def file_trigger_accumulator(self, f):
        current_time = datetime.now()
        self.watch_window[f] = current_time
        self.watch_window = {k:v for k, v in self.watch_window.items() if current_time - timedelta(seconds=self.config.get(b'watch_window')) < v}
        if set(self.watch_window.keys()) == set(self.watcher.files() + self.watcher.directories()):
            self.trigger()

    def trigger(self, e=None):
        if self.config.get(b'is_active') == False:
            return False
        else:
            if self.lock is None:
                self.is_running = True
                self.update()
                self.lock = QTimer.singleShot(self.config.get(b'trigger_hold') * 1000, self.run)
                self.shutdown()
            return

    def run(self, vars={}):
        default_vars = {b'home': os.path.expanduser(b'~'), b'version': VERSION_STRING}
        default_vars_and_config = dict(list(default_vars.items()) + list(self.config.config.items()))
        if self.runner == None:
            self.runner = NotebookRunner(None, pylab=True, mpl_inline=True)
        if self.config.get(b'mode') == MODE_WATCH_FOLDER and self.config.get(b'iterate_watched_folder'):
            for dirpath, dirnames, filenames in os.walk(self.config.get(b'watched_folder')):
                break

            filenames = [ f for f in filenames if self.config.get(b'iterate_wildcard') in f ]
            logging.info(b'Watched folder contains %d files; looping' % len(filenames))
        else:
            filenames = [
             None]
        self.latest_run[b'timestamp'] = datetime.now()
        try:
            try:
                for f in filenames:
                    now = datetime.now()
                    current_vars = {b'datetime': now.strftime(b'%Y-%m-%d %H.%M.%S'), 
                       b'date': now.date().strftime(b'%Y-%m-%d'), 
                       b'time': now.time().strftime(b'%H.%M.%S'), 
                       b'filename': f}
                    vars = dict(list(default_vars_and_config.items()) + list(current_vars.items()))
                    for nb_path in self.config.get(b'notebook_paths'):
                        nb = self.load_notebook(nb_path)
                        if nb:
                            vars[b'notebook_path'] = nb_path
                            vars[b'notebook_filename'] = os.path.basename(nb_path)
                            vars[b'output_path'] = self.config.get(b'output_path').format(**vars)
                            parent_folder = os.path.dirname(vars[b'output_path'])
                            if parent_folder:
                                try:
                                    utils.mkdir_p(parent_folder)
                                except:
                                    self.latest_run[b'success'] = False
                                    raise

                            self.run_notebook(nb, vars)
                        else:
                            raise NotebookNotFound(nb_path)

            except:
                self.latest_run[b'success'] = False
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                logging.error(b'%s\n%s\n%s' % (exctype, value, traceback.format_exc()))

        finally:
            self.is_running = False
            self.lock = None
            self.update()
            self.startup()

        return

    def run_notebook(self, nb, vars={}):
        if len(nb[b'worksheets']) == 0:
            nb[b'worksheets'] = [
             NotebookNode({b'cells': [], b'metadata': {}})]
        start = nb[b'worksheets'][0][b'cells']
        start.insert(0, Struct(**{b'cell_type': b'code', 
           b'language': b'python', 
           b'outputs': [], b'collapsed': False, 
           b'prompt_number': -1, 
           b'input': b'qtipy=%s' % vars, 
           b'metadata': {}}))
        self.runner.nb = nb
        try:
            try:
                self.runner.run_notebook()
            except:
                self.latest_run[b'success'] = False
                raise
            else:
                self.latest_run[b'success'] = True

        finally:
            ext = dict(html=b'html', slides=b'slides', latex=b'latex', markdown=b'md', python=b'py', rst=b'rst')
            output, resources = IPyexport(IPyexporter_map[self.config.get(b'output_format')], self.runner.nb)
            output_path = vars[b'output_path'] + b'notebook.%s' % ext[self.config.get(b'output_format')]
            logging.info(b'Exporting updated notebook to %s' % output_path)
            with open(output_path, b'w') as (f):
                f.write(output)

    def update(self):
        _w.viewer.update(self.index())


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.menuBars = {b'file': self.menuBar().addMenu(tr(b'&File')), 
           b'edit': self.menuBar().addMenu(tr(b'&Edit')), 
           b'control': self.menuBar().addMenu(tr(b'&Control'))}
        t = self.addToolBar(b'File')
        t.setIconSize(QSize(16, 16))
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'folder-horizontal-open.png')), tr(b'Load automatons'), self)
        action.setShortcut(QKeySequence.Open)
        action.setStatusTip(b'Load automatons')
        action.triggered.connect(self.load_automatons)
        t.addAction(action)
        self.menuBars[b'file'].addAction(action)
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'disk.png')), tr(b'Save automatons'), self)
        action.setShortcut(QKeySequence.Save)
        action.setStatusTip(b'Save automatons')
        action.triggered.connect(self.save_automatons)
        t.addAction(action)
        self.menuBars[b'file'].addAction(action)
        t = self.addToolBar(b'Edit')
        t.setIconSize(QSize(16, 16))
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'plus-circle.png')), tr(b'Add automaton'), self)
        action.setShortcut(QKeySequence.New)
        action.setStatusTip(b'Add new automaton')
        action.triggered.connect(self.add_new_automaton)
        t.addAction(action)
        self.menuBars[b'edit'].addAction(action)
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'property.png')), tr(b'Edit automaton'), self)
        action.setStatusTip(b'Edit automaton')
        action.triggered.connect(self.edit_automaton)
        t.addAction(action)
        self.menuBars[b'edit'].addAction(action)
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'cross.png')), tr(b'Delete automaton'), self)
        action.setShortcut(QKeySequence.Delete)
        action.setStatusTip(b'Delete automaton')
        action.triggered.connect(self.delete_automaton)
        t.addAction(action)
        self.menuBars[b'edit'].addAction(action)
        t = self.addToolBar(b'Control')
        t.setIconSize(QSize(16, 16))
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'control.png')), tr(b'Enable'), self)
        action.setShortcut(tr(b'Ctrl+E'))
        action.setStatusTip(b'Enable automaton')
        action.triggered.connect(self.enable_automaton)
        t.addAction(action)
        self.menuBars[b'control'].addAction(action)
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'control-pause.png')), tr(b'Pause'), self)
        action.setShortcut(tr(b'Ctrl+W'))
        action.setStatusTip(b'Pause automaton')
        action.triggered.connect(self.pause_automaton)
        t.addAction(action)
        self.menuBars[b'control'].addAction(action)
        t = self.addToolBar(b'Manual')
        t.setIconSize(QSize(16, 16))
        btn = QToolButton(self)
        action = QAction(QIcon(os.path.join(utils.scriptdir, b'icons', b'play.png')), tr(b'Run now'), self)
        action.setShortcut(tr(b'Ctrl+R'))
        btn.setText(tr(b'Run now'))
        btn.setStatusTip(b'Run now...')
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setDefaultAction(action)
        action.triggered.connect(self.run_automaton)
        t.addWidget(btn)
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.South)
        self.viewer = QListView()
        self.viewer.setItemDelegate(AutomatonListDelegate(self.viewer))
        self.automatons = QStandardItemModel(self.viewer)
        self.viewer.setModel(self.automatons)
        self.log = QTextEdit()
        self.log._current_rows = []
        self.log.setReadOnly(True)
        logHandler = Logger(self, self.log)
        logging.getLogger().addHandler(logHandler)
        logging.info(b'Welcome to QtIPy')
        self.tabs.addTab(self.viewer, b'Automatons')
        self.tabs.addTab(self.log, b'Log')
        self.setCentralWidget(self.tabs)
        self.setWindowTitle(b'QtIPy: The data automator')
        self.statusBar().showMessage(tr(b'Ready'))
        self.setMinimumSize(QSize(400, 500))
        self.show()

    def add_new_automaton(self):
        """
        Define a new automaton and add to the list
        
        Show a dialog with options to:
        - define the notebook file to use (.pylnb)
        - define the file, folder or other to watch
        - define the output folder/file pattern
        - set config settings
        """
        automaton = Automaton()
        self.automatons.appendRow(automaton)
        lastitem = self.automatons.item(self.automatons.rowCount() - 1)
        self.viewer.setCurrentIndex(lastitem.index())
        self.edit_automaton()

    def edit_automaton(self):
        """
        
        
        """
        try:
            automaton = self.automatons.itemFromIndex(self.viewer.selectionModel().currentIndex())
        except:
            return

        automaton.shutdown()
        dlg = AutomatonDialog(self)
        dlg.config.set_many(automaton.config.config)
        if dlg.exec_():
            automaton.config.set_many(dlg.config.config)
            if automaton.config.get(b'is_active'):
                automaton.startup()
            automaton.update()

    def delete_automaton(self):
        """
        """
        _btn = QMessageBox.question(self, b'Confirm delete', b'Are you sure you want to delete this automaton?')
        if _btn == QMessageBox.Yes:
            automaton = self.automatons.itemFromIndex(self.viewer.selectionModel().currentIndex())
            automaton.shutdown()
            automaton_idx = self.viewer.selectionModel().selectedIndexes()[0]
            self.automatons.removeRows(automaton_idx.row(), 1, QModelIndex())

    def enable_automaton(self):
        """
        """
        try:
            automaton = self.automatons.itemFromIndex(self.viewer.selectionModel().currentIndex())
        except:
            return

        automaton.config.set(b'is_active', True)
        automaton.startup()
        automaton.update()

    def pause_automaton(self):
        """
        """
        try:
            automaton = self.automatons.itemFromIndex(self.viewer.selectionModel().currentIndex())
        except:
            return

        automaton.config.set(b'is_active', False)
        automaton.shutdown()
        automaton.update()

    def run_automaton(self):
        """
        """
        try:
            automaton = self.automatons.itemFromIndex(self.viewer.selectionModel().currentIndex())
        except:
            return

        automaton.trigger(None)
        return

    def load_automatons(self):
        """
        """
        filename, _ = QFileDialog.getOpenFileName(_w, b'Load QtIPy Automatons', b'', b'QtIPy Automaton File (*.qifx);;All files (*.*)')
        if filename:
            self.automatons.clear()
            tree = et.parse(filename)
            automatons = tree.getroot()
            for automatonx in automatons.findall(b'Automaton'):
                automaton = Automaton()
                automaton.config.setXMLConfig(automatonx)
                self.automatons.appendRow(automaton)
                automaton.startup()

    def save_automatons(self):
        """
        """
        filename, _ = QFileDialog.getSaveFileName(_w, b'Save QtIPy Automatons', b'', b'QtIPy Automaton File (*.qifx);;All files (*.*)')
        if filename:
            root = et.Element(b'QtIPy')
            root.set(b'xmlns:mpwfml', b'http://martinfitzpatrick.name/schema/QtIPy/2013a')
            for i in range(0, self.automatons.rowCount()):
                a = self.automatons.item(i)
                automaton = et.SubElement(root, b'Automaton')
                automaton = a.config.getXMLConfig(automaton)

            tree = et.ElementTree(root)
            tree.write(filename)

    def sizeHint(self):
        return QSize(400, 500)


def main():
    global _w
    app = QApplication(sys.argv)
    app.setStyle(b'fusion')
    app.setOrganizationName(b'QtIPy')
    app.setOrganizationDomain(b'martinfitzpatrick.name')
    app.setApplicationName(b'QtIPy')
    locale = QLocale.system().name()
    _w = MainWindow()
    logging.info(b'Ready.')
    app.exec_()
    logging.info(b'Exiting.')
    sys.exit()


if __name__ == b'__main__':
    main()