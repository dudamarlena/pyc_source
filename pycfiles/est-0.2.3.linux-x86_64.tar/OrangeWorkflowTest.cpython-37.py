# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/test/OrangeWorkflowTest.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 12054 bytes
__authors__ = [
 'H. Payno', 'Orange']
__license__ = 'MIT'
__date__ = '03/03/2017'
import os, sys, gc, re, logging, pickle, pkg_resources
from silx.gui.qt import QApplication
from AnyQt.QtGui import QFont
from AnyQt.QtCore import Qt, QDir
import AnyQt.importhooks
if AnyQt.USED_API == 'pyqt5':
    AnyQt.importhooks.install_backport_hook('pyqt4')
from Orange import canvas
from est.gui.qtapplicationmanager import QApplicationManager
from Orange.canvas.application.canvasmain import CanvasMainWindow
from Orange.canvas.application.outputview import TextStream
from Orange.canvas.config import cache_dir
from Orange.canvas import config
from Orange.canvas.registry.base import WidgetRegistry
from Orange.canvas.registry import qt
from Orange.canvas.registry import set_global_registry
from Orange.canvas.scheme import SchemeNode, SchemeLink
from Orange.canvas.registry import cache
from unittest import TestCase
log = logging.getLogger(__name__)
app = QApplicationManager()

class OrangeWorflowTest(TestCase):
    __doc__ = 'Define a specific TestCase reltive to OrangeWorkflow'

    def addWidget(self, widgetID):
        """Create an instanciation of the widgetID

        :return SchemeNode: the node created
        """
        assert type(widgetID) is str
        assert self.widget_registry.has_widget(widgetID)
        widget_desc = self.widget_registry.widget(widgetID)
        myItem = SchemeNode(widget_desc)
        self.canvas_window.current_document().scheme().add_node(myItem)
        return myItem

    def link(self, schemeNode1, outNode1, schemeNode2, inputNode2):
        """Create a link between the node on the given input and output

        :param SchemeNode schemeNode1: the node emitting the output signal
        :param outNode1: the output chanel to be linked
        :param SchemeNode schemeNode2: the node receiving the input signal
        :param inputNode2: the input chanel to be linked
        :return: the link created between the two nodes
        """
        assert type(schemeNode1) is SchemeNode
        assert type(schemeNode2) is SchemeNode
        assert type(outNode1) is str
        assert type(inputNode2) is str
        link = SchemeLink(schemeNode1, outNode1, schemeNode2, inputNode2)
        self.canvas_window.current_document().scheme().add_link(link)
        return link

    def getWidgetForNode(self, node):
        """

        :param SchemeNode node: the node for which we want the corresponding
            widget
        :return: the widget instanciated for the given node
        """
        assert type(node) is SchemeNode
        return self.canvas_window.current_document().scheme().widget_for_node(node)

    @classmethod
    def setUpClass(cls):
        cls.init(cls)
        TestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.canvas_window.deleteLater()
        while app.hasPendingEvents():
            app.processEvents()
            cls.processOrangeEvents(cls)

        app.flush()
        del cls.canvas_window
        gc.collect()
        TestCase.tearDownClass()

    def tearDown(self):
        while app.hasPendingEvents():
            app.processEvents()
            TestCase.tearDown(self)

    @staticmethod
    def fix_osx_10_9_private_font():
        if sys.platform == 'darwin':
            import platform
            try:
                version = platform.mac_ver()[0]
                version = float(version[:version.rfind('.')])
                if version >= 10.11:
                    QFont.insertSubstitution('.SF NS Text', 'Helvetica Neue')
                else:
                    if version >= 10.1:
                        QFont.insertSubstitution('.Helvetica Neue DeskInterface', 'Helvetica Neue')
                    else:
                        if version >= 10.9:
                            QFont.insertSubstitution('.Lucida Grande UI', 'Lucida Grande')
            except AttributeError:
                pass

    @staticmethod
    def fix_win_pythonw_std_stream():
        """
        On windows when running without a console (using pythonw.exe) the
        std[err|out] file descriptors are invalid and start throwing exceptions
        when their buffer is flushed (`http://bugs.python.org/issue706263`_)

        """
        if sys.platform == 'win32':
            if os.path.basename(sys.executable) == 'pythonw.exe':
                if sys.stdout is None:
                    sys.stdout = open(os.devnull, 'w')
                if sys.stderr is None:
                    sys.stderr = open(os.devnull, 'w')

    def processOrangeEvents(self):
        self.canvas_window.current_document().scheme().signal_manager.process_queued()

    def processOrangeEventsStack(self):
        node_update_front = self.canvas_window.current_document().scheme().signal_manager.node_update_front()
        if node_update_front:
            self.processOrangeEvents()
            self.processOrangeEventsStack()

    def init(self):
        OrangeWorflowTest.fix_win_pythonw_std_stream()
        OrangeWorflowTest.fix_osx_10_9_private_font()
        rootlogger = logging.getLogger(canvas.__name__)
        stream_hander = logging.StreamHandler()
        rootlogger.addHandler(stream_hander)
        log.info("Starting 'Orange Canvas' application.")
        log.debug('Starting CanvasApplicaiton ')
        config.init()
        file_handler = logging.FileHandler(filename=(os.path.join(config.log_dir(), 'canvas.log')),
          mode='w')
        rootlogger.addHandler(file_handler)
        open_requests = []

        def onrequest(url):
            log.info('Received an file open request %s', url)
            open_requests.append(url)

        app.fileOpenRequest.connect(onrequest)
        stylesheet = 'orange'
        stylesheet_string = None
        if stylesheet != 'none':
            if os.path.isfile(stylesheet):
                with open(stylesheet, 'r') as (f):
                    stylesheet_string = f.read()
            else:
                if not os.path.splitext(stylesheet)[1]:
                    stylesheet = os.path.extsep.join([stylesheet, 'qss'])
                else:
                    pkg_name = canvas.__name__
                    resource = 'styles/' + stylesheet
                    if pkg_resources.resource_exists(pkg_name, resource):
                        stylesheet_string = pkg_resources.resource_string(pkg_name, resource).decode()
                        base = pkg_resources.resource_filename(pkg_name, 'styles')
                        pattern = re.compile('^\\s@([a-zA-Z0-9_]+?)\\s*:\\s*([a-zA-Z0-9_/]+?);\\s*$',
                          flags=(re.MULTILINE))
                        matches = pattern.findall(stylesheet_string)
                        for prefix, search_path in matches:
                            QDir.addSearchPath(prefix, os.path.join(base, search_path))
                            log.info('Adding search path %r for prefix, %r', search_path, prefix)

                        stylesheet_string = pattern.sub('', stylesheet_string)
                    else:
                        log.info('%r style sheet not found.', stylesheet)
        dirpath = os.path.abspath(os.path.dirname(canvas.__file__))
        QDir.addSearchPath('canvas_icons', os.path.join(dirpath, 'icons'))
        self.canvas_window = CanvasMainWindow()
        self.canvas_window.setWindowIcon(config.application_icon())
        if stylesheet_string is not None:
            self.canvas_window.setStyleSheet(stylesheet_string)
        reg_cache = None
        widget_discovery = qt.QtWidgetDiscovery(cached_descriptions=reg_cache)
        self.widget_registry = qt.QtWidgetRegistry()
        widget_discovery.found_category.connect(self.widget_registry.register_category)
        widget_discovery.found_widget.connect(self.widget_registry.register_widget)
        cache_filename = os.path.join(cache_dir(), 'widget-registry.pck')
        entry_points = []
        for entry_point in config.widgets_entry_points():
            if entry_point.name != 'Orange Widgets':
                entry_points.append(entry_point)

        widget_discovery.run(entry_points)
        cache.save_registry_cache(widget_discovery.cached_descriptions)
        with open(cache_filename, 'wb') as (f):
            pickle.dump(WidgetRegistry(self.widget_registry), f)
        set_global_registry(self.widget_registry)
        self.canvas_window.set_widget_registry(self.widget_registry)
        self.canvas_window.show()
        app.processEvents()
        log.info('discovery ended')
        log_view = self.canvas_window.log_view()
        stdout = TextStream()
        stdout.stream.connect(log_view.write)
        if sys.stdout:
            stdout.stream.connect(sys.stdout.write)
            stdout.flushed.connect(sys.stdout.flush)
        stderr = TextStream()
        error_writer = log_view.formated(color=(Qt.red))
        stderr.stream.connect(error_writer.write)
        if sys.stderr:
            stderr.stream.connect(sys.stderr.write)
            stderr.flushed.connect(sys.stderr.flush)
        log.info('End initialization')