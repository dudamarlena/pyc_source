# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/externals/pysideuic/driver.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 3990 bytes
import sys, logging
from pysideuic import compileUi

class Driver(object):
    __doc__ = ' This encapsulates access to the pyuic functionality so that it can be\n    called by code that is Python v2/v3 specific.\n    '
    LOGGER_NAME = 'PySide.uic'

    def __init__(self, opts, ui_file):
        """ Initialise the object.  opts is the parsed options.  ui_file is the
        name of the .ui file.
        """
        if opts.debug:
            logger = logging.getLogger(self.LOGGER_NAME)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        self._opts = opts
        self._ui_file = ui_file

    def invoke(self):
        """ Invoke the action as specified by the parsed options.  Returns 0 if
        there was no error.
        """
        if self._opts.preview:
            return self._preview()
        else:
            self._generate()
            return 0

    def _preview(self):
        """ Preview the .ui file.  Return the exit status to be passed back to
        the parent process.
        """
        from PySide import QtUiTools
        from PySide import QtGui
        app = QtGui.QApplication([self._ui_file])
        widget = QtUiTools.QUiLoader().load(self._ui_file)
        widget.show()
        return app.exec_()

    def _generate(self):
        """ Generate the Python code. """
        if sys.hexversion >= 50331648:
            if self._opts.output == '-':
                from io import TextIOWrapper
                pyfile = TextIOWrapper((sys.stdout.buffer), encoding='utf8')
            else:
                pyfile = open((self._opts.output), 'wt', encoding='utf8')
        else:
            if self._opts.output == '-':
                pyfile = sys.stdout
            else:
                pyfile = open(self._opts.output, 'wt')
        compileUi(self._ui_file, pyfile, self._opts.execute, self._opts.indent, self._opts.from_imports)

    def on_IOError(self, e):
        """ Handle an IOError exception. """
        sys.stderr.write('Error: %s: "%s"\n' % (e.strerror, e.filename))

    def on_SyntaxError(self, e):
        """ Handle a SyntaxError exception. """
        sys.stderr.write('Error in input file: %s\n' % e)

    def on_NoSuchWidgetError(self, e):
        """ Handle a NoSuchWidgetError exception. """
        if e.args[0].startswith('Q3'):
            sys.stderr.write('Error: Q3Support widgets are not supported by PySide.\n')
        else:
            sys.stderr.write(str(e) + '\n')

    def on_Exception(self, e):
        """ Handle a generic exception. """
        if logging.getLogger(self.LOGGER_NAME).level == logging.DEBUG:
            import traceback
            (traceback.print_exception)(*sys.exc_info())
        else:
            from PySide import QtCore
            sys.stderr.write('An unexpected error occurred.\nCheck that you are using the latest version of PySide and report the error to\nhttp://bugs.openbossa.org, including the ui file used to trigger the error.\n')