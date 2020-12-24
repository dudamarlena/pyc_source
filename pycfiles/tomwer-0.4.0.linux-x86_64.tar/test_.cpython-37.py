# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/test_.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 6062 bytes
"""Launch unittests of the library"""
__authors__ = [
 'V. Valls']
__license__ = 'MIT'
__date__ = '12/01/2018'
import sys, argparse, logging, unittest, os
from tomwer.test.utils import skip_gui_test

class StreamHandlerUnittestReady(logging.StreamHandler):
    __doc__ = 'The unittest class TestResult redefine sys.stdout/err to capture\n    stdout/err from tests and to display them only when a test fail.\n\n    This class allow to use unittest stdout-capture by using the last sys.stdout\n    and not a cached one.\n    '

    def emit(self, record):
        self.stream = sys.stderr
        super(StreamHandlerUnittestReady, self).emit(record)

    def flush(self):
        pass


def createBasicHandler():
    """Create the handler using the basic configuration"""
    hdlr = StreamHandlerUnittestReady()
    fs = logging.BASIC_FORMAT
    dfs = None
    fmt = logging.Formatter(fs, dfs)
    hdlr.setFormatter(fmt)
    return hdlr


for h in logging.root.handlers:
    logging.root.removeHandler(h)

logging.root.addHandler(createBasicHandler())
logging.captureWarnings(True)
_logger = logging.getLogger(__name__)

class TextTestResultWithSkipList(unittest.TextTestResult):
    __doc__ = 'Override default TextTestResult to display list of skipped tests at the\n    end\n    '

    def printErrors(self):
        unittest.TextTestResult.printErrors(self)
        self.printErrorList('SKIPPED', self.skipped)


def main(argv):
    """
    Main function to launch the unittests as an application

    :param argv: Command line arguments
    :returns: exit status
    """
    from silx.test import utils
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', default=0, action='count',
      dest='verbose',
      help='Increase verbosity. Option -v prints additional INFO messages. Use -vv for full verbosity, including debug messages and test help strings.')
    parser.add_argument('--qt-binding', dest='qt_binding', default=None, help="Force using a Qt binding: 'PyQt5' or 'PySide2'")
    parser.add_argument('--web', dest='web_log', default=False, help="Force unit test to export his log to graylog'",
      action='store_true')
    utils.test_options.add_parser_argument(parser)
    options = parser.parse_args(argv[1:])
    test_verbosity = 1
    use_buffer = True
    if options.verbose == 1:
        logging.root.setLevel(logging.INFO)
        _logger.info('Set log level: INFO')
        test_verbosity = 2
        use_buffer = False
    else:
        if options.verbose > 1:
            logging.root.setLevel(logging.DEBUG)
            _logger.info('Set log level: DEBUG')
            test_verbosity = 2
            use_buffer = False
        else:
            os.environ['_TOMWER_NO_GUI_UNIT_TESTS'] = str(not options.gui)
            if options.qt_binding and options.gui is True:
                binding = options.qt_binding.lower()
                if binding == 'pyqt4':
                    _logger.info('Force using PyQt4')
                    import PyQt4.QtCore
            elif binding == 'pyqt5':
                _logger.info('Force using PyQt5')
                import PyQt5.QtCore
            else:
                if binding == 'pyside':
                    _logger.info('Force using PySide')
                    import PySide.QtCore
                else:
                    if binding == 'pyside2':
                        _logger.info('Force using PySide2')
                        import PySide2.QtCore
                    else:
                        previous_web_log_value = os.environ.get('ORANGE_WEB_LOG')
                        os.environ['ORANGE_WEB_LOG'] = str(options.web_log)
                        utils.test_options.configure(options)
                        runnerArgs = {}
                        runnerArgs['verbosity'] = test_verbosity
                        runnerArgs['buffer'] = use_buffer
                        runner = (unittest.TextTestRunner)(**runnerArgs)
                        runner.resultclass = TextTestResultWithSkipList
                        unittest.installHandler()
                        import tomwer.test
                        test_suite = unittest.TestSuite()
                        test_suite.addTest(tomwer.test.suite())
                        if options.gui is True:
                            import orangecontrib.tomwer.test
                            test_suite.addTest(orangecontrib.tomwer.test.suite())
                        result = runner.run(test_suite)
                        if previous_web_log_value is None:
                            del os.environ['ORANGE_WEB_LOG']
                        else:
                            os.environ['ORANGE_WEB_LOG'] = previous_web_log_value
                    if result.wasSuccessful():
                        exit_status = 0
                    else:
                        exit_status = 1
        return exit_status