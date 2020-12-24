# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/application/taurusapplication.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides the base
:class:`taurus.qt.qtgui.application.TaurusApplication` class."""
from builtins import str
import os, sys, logging, optparse, threading
from taurus.external.qt import Qt
from taurus.core.util.log import LogExceptHook, Logger
__all__ = [
 'TaurusApplication']
__docformat__ = 'restructuredtext'

class STD(Logger):
    FlushWaterMark = 1000

    def __init__(self, name='', parent=None, format=None, std=None, pure_text=True):
        """The STD Logger constructor

        :param name: (str) the logger name (default is empty string)
        :param parent: (Logger) the parent logger or None if no parent exists
                       (default is None)
        :param format: (str) the log message format or None to use the default
                       log format (default is None)
        :param std: std to forward write
        :param pure_text: if True, writes the 'message' parameter of the log
                          message in a separate line preserving the
                          indentation
        """
        Logger.__init__(self, name=name, parent=parent, format=format)
        self.buffer = ''
        self.log_obj.propagate = False
        self.std = std

    @property
    def errors(self):
        return self.std.errors

    def addLogHandler(self, handler):
        """When called, set to use a private handler and DON'T send messages
        to parent loggers (basically will act as an independent logging system
        by itself)

        :param handler: new handler"""
        Logger.addLogHandler(self, handler)
        self.log_obj.propagate = not len(self.log_handlers)

    def write(self, msg):
        try:
            try:
                self.buffer += msg
                msgl = len(msg)
                if msgl > 0 and (msg[(-1)] == '\n' or msg.index('\n') >= 0 or msgl >= self.FlushWaterMark):
                    self.flush()
            except ValueError:
                pass

        finally:
            if self.std is not None:
                try:
                    self.std.write(msg)
                except:
                    pass

        return

    def flush(self):
        try:
            buff = self.buffer
            if buff is None or len(buff) == 0:
                return
            if buff[(-1)] == '\n':
                buff = buff[:-1]
            if self.log_handlers:
                self.log(Logger.Console, '\n' + buff)
            self.buffer = ''
        finally:
            if self.std is not None:
                try:
                    self.std.flush()
                except:
                    pass

        return


class TaurusApplication(Qt.QApplication, Logger):
    """A QApplication that performs some taurus-specific initializations
    and (optionally but deprecated) also parses the command line for taurus
    options.

    The optional keyword parameters:
        - app_name: (str) application name
        - app_version: (str) application version
        - org_name: (str) organization name
        - org_domain: (str) organization domain
        - cmd_line_parser (None [or DEPRECATED :class:`optparse.OptionParser`])

    If cmd_line_parser is explicitly set to None (recommended), no parsing will
    be done at all. If a  :class:`optparse.OptionParser` instance is passed as
    cmd_line_parser (deprecated), it will be used for parsing the command line
    arguments. If it is not explicitly passed (not recommended), a default
    parser will be assumed with the default taurus options.

    Simple example::

        import sys
        from taurus.qt.qtgui.application import TaurusApplication
        import taurus.qt.qtgui.display

        app = TaurusApplication(cmd_line_parser=None)

        w = taurus.qt.qtgui.display.TaurusLabel()
        w.model = 'sys/tg_test/1/double_scalar'
        w.show()

        sys.exit(app.exec_())

    """

    def __init__(self, *args, **kwargs):
        """The constructor. Parameters are the same as QApplication plus a
        keyword parameter: 'cmd_line_parser' which should be None or an
        instance of :class:`optparse.OptionParser`. If cmd_line_parser is None
        no command line parsing will be done ()
        """
        self._lock = threading.Lock()
        if len(args) == 0:
            args = (
             getattr(sys, 'argv', []),)
        app_name = kwargs.pop('app_name', None)
        app_version = kwargs.pop('app_version', None)
        org_name = kwargs.pop('org_name', None)
        org_domain = kwargs.pop('org_domain', None)
        parser = kwargs.pop('cmd_line_parser', optparse.OptionParser())
        try:
            Qt.QCoreApplication.setAttribute(Qt.Qt.AA_X11InitThreads)
        except AttributeError:
            pass

        try:
            Qt.QApplication.__init__(self, *args, **kwargs)
        except TypeError:
            Qt.QApplication.__init__(self, *args)

        Logger.__init__(self)
        self._out = None
        self._err = None
        if app_name is not None:
            self.setApplicationName(app_name)
        if app_version is not None:
            self.setApplicationVersion(app_version)
        if org_name is not None:
            self.setOrganizationName(org_name)
        if org_domain is not None:
            self.setOrganizationDomain(org_domain)
        if parser is None:
            p, opt, args = (None, None, None)
        else:
            if parser.version is None and app_version:
                v = app_version
                if app_name:
                    v = app_name + ' ' + app_version
                parser.version = v
                parser._add_version_option()
            import taurus.core.util.argparse
            p, opt, args = taurus.core.util.argparse.init_taurus_args(parser=parser, args=args[0][1:])
        self._cmd_line_parser = p
        self._cmd_line_options = opt
        self._cmd_line_args = args
        self.__registerQtLogger()
        self.__registerExtensions()
        self.__redirect_std()
        return

    def __registerQtLogger(self):
        import taurus.qt.qtcore.util
        taurus.qt.qtcore.util.initTaurusQtLogger()

    def __registerExtensions(self):
        """Registers taurus Qt extensions"""
        try:
            import sardana.taurus.qt.qtcore.tango.sardana
            sardana.taurus.qt.qtcore.tango.sardana.registerExtensions()
        except:
            self.debug('Failed to load sardana extensions', exc_info=1)

        try:
            import taurus.core.tango.img
            taurus.core.tango.img.registerExtensions()
        except:
            self.debug('Failed to load image extensions', exc_info=1)

    def __redirect_std(self):
        """Internal method to redirect stdout and stderr to log messages"""
        Logger.addLevelName(Logger.Critical + 10, 'CONSOLE')
        if sys.displayhook == sys.__displayhook__:
            self._out = STD(name='OUT', std=sys.stdout)
            sys.stdout = self._out
            self._err = STD(name='ERR', std=sys.stderr)
            sys.stderr = self._err

    def __buildLogFileName(self, prefix=None, name=None):
        if prefix is None:
            prefix = os.path.expanduser('~/tmp')
        appName = str(self.applicationName())
        if not appName:
            appName = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        dirName = os.path.join(prefix, appName)
        if not os.path.isdir(dirName):
            os.makedirs(dirName)
        if name is None:
            name = appName + '.log'
        fileName = os.path.join(dirName, name)
        return fileName

    def get_command_line_parser(self):
        """Returns the :class:`optparse.OptionParser` used to parse the
        command line parameters.

        :return: the parser used in the command line
        :rtype: :class:`optparse.OptionParser`"""
        return self._cmd_line_parser

    def get_command_line_options(self):
        """Returns the :class:`optparse.Option` that resulted from parsing the
        command line parameters.

        :return: the command line options
        :rtype: :class:`optparse.Option`"""
        return self._cmd_line_options

    def get_command_line_args(self):
        """Returns the list of arguments that resulted from parsing the
        command line parameters.

        :return: the command line arguments
        :rtype: list of strings"""
        return self._cmd_line_args

    def setTaurusStyle(self, styleName):
        """Sets taurus application style to the given style name

        :param styleName: the new style name to be applied
        :type styleName: str"""
        import taurus.qt.qtgui.style
        taurus.qt.qtgui.style.setTaurusStyle(styleName)

    def basicConfig(self, log_file_name=None, maxBytes=10000000.0, backupCount=5, with_gui_exc_handler=True):
        hook_to = None
        if with_gui_exc_handler:
            import taurus.qt.qtgui.dialog
            hook_to = taurus.qt.qtgui.dialog.TaurusExceptHookMessageBox()
        sys.excepthook = LogExceptHook(hook_to=hook_to)
        try:
            if log_file_name is None:
                log_file_name = self.__buildLogFileName()
            f_h = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=maxBytes, backupCount=backupCount)
            Logger.addRootLogHandler(f_h)
            if self._out is not None:
                self._out.std = sys.__stdout__
                self._out.addLogHandler(f_h)
            if self._out is not None:
                self._err.std = sys.__stderr__
                self._err.addLogHandler(f_h)
            self.info('Logs will be saved in %s', log_file_name)
        except:
            self.warning("'%s' could not be created. Logs will not be stored", log_file_name)
            self.debug('Error description', exc_info=1)

        return

    @staticmethod
    def exec_(*args, **kwargs):
        try:
            ret = Qt.QApplication.exec_(*args, **kwargs)
        except TypeError:
            ret = Qt.QApplication.exec_(*args)

        from taurus.core.util.log import _DEPRECATION_COUNT
        from taurus import info
        info('\n*********************\n%s', _DEPRECATION_COUNT.pretty())
        return ret