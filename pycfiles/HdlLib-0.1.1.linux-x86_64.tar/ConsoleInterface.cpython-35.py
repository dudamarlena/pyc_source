# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/ConsoleInterface.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 8305 bytes
import os, sys, datetime, traceback, logging
sys.path.append(os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), '../HdlLib.Utilities'))))
from HdlLib.Utilities.ExtensionSilence import ExtensionSilence
from HdlLib.Utilities import ColoredLogging
import struct
try:
    if not sys.platform.startswith('win'):
        import fcntl, termios
except:
    pass

import argparse
if sys.maxsize == 2147483647.0:
    ARCHI = '32'
else:
    ARCHI = '64'
LM = None

def TestEnv(ToolName):
    try:
        if ToolName is None:
            logging.info('Environment variables found.')
            return True
        if 'ADACSYS_TOOL' in os.environ:
            if os.environ['ADACSYS_TOOL'] == ToolName:
                logging.info('{0} environment variables found. AVA-Test GUI can start.'.format(ToolName))
                return True
            else:
                logging.error("Wrong environment variable.\n'ADACSYS_TOOL' environment variable is not set.")
                return False
        else:
            logging.error("Command called for wrong ADACSYS tool.\n'ADACSYS_TOOL' environment variable is set to '{0}'. This tool is {1}.\n\nSet this variable to '{1}' to get it run.".format(os.environ['ADACSYS_TOOL'], ToolName))
            return False
    except:
        logging.error(traceback.format_exc(10))
        return False


def GetTerminalSize(fd=1):
    """
        Returns height and width of current terminal. First tries to get
        size via termios.TIOCGWINSZ, then from environment. Defaults to 25
        lines x 80 columns if both methods fail.

        fd: file descriptor (default: 1=stdout)
        """
    if sys.platform.startswith('win'):
        return (25, 80)
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            os.close(fd)
        except:
            try:
                os.close(fd)
                hw = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                hw = (25, 80)

        return hw


def ArgIsFile(FilePath):
    """
        Test validity of file path passed as argument
        """
    if os.path.isfile(FilePath):
        return os.path.abspath(os.path.normpath(os.path.expanduser(FilePath)))
    raise argparse.ArgumentTypeError("'{0}' does not exist or is not a file.".format(FilePath))


def ParseOptions(LaunchFunc, Version):
    """
        Parse argument options and do corresponding actions.
        """
    Parser = argparse.ArgumentParser(description='GUI for AVA-Test tool.', epilog='')
    Parser.set_defaults(func=LaunchFunc)
    Args = Parser.parse_args()
    return Args


def ConfigLogging(Version, ModuleName, UseLogFile=True):
    """
        Configure logging mode.
        """
    LogDir = os.path.expanduser(os.path.join('~/', ModuleName + '_logs'))
    if not os.path.isdir(LogDir):
        os.makedirs(LogDir)
    if 'LOGGING_LEVEL' in os.environ:
        LogLevel = os.environ['LOGGING_LEVEL'].upper()
        if LogLevel == 'DEBUG':
            UseLogFile = False
            LoggingMode = logging.DEBUG
        else:
            if LogLevel == 'INFO':
                UseLogFile = False
                LoggingMode = logging.INFO
            else:
                if LogLevel == 'ERROR':
                    UseLogFile = False
                    LoggingMode = logging.ERROR
                else:
                    print("'{0}' log level not supported. 'LOGGING_LEVEL' env must be [DEBUG, INFO, ERROR]".format(LogLevel))
                    LoggingMode = logging.INFO
    else:
        LoggingMode = logging.INFO
    if 'SYNTHESYS_LOG_FILE' in os.environ:
        LogFilePath = os.environ['SYNTHESYS_LOG_FILE']
        ColoredLogging.SetActive(False)
        LogFile = os.path.abspath(os.path.normpath(LogFilePath))
        logging.basicConfig(filename=LogFile, format='%(asctime)s | %(levelname)s: %(message)s', level=LoggingMode, filemode='w+')
    else:
        ColoredLogging.SetActive(True)
        logging.basicConfig(filename=None, format='%(levelname)s: %(message)s', level=LoggingMode)


def TimeStamp(Format='%Y-%m-%d_%Hh%Mm%Ss'):
    return datetime.datetime.now().strftime(Format)


def Start(NAME, MODULE, DESCRIPTION, DATETIME, VERSION, GUI):
    """
        Initialize command line parameters/option parsing and banner display.
        """
    F = lambda arg: GUI.Start()
    Args = ParseOptions(F, VERSION)
    try:
        Args.func(Args)
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupt: Leave {0}.'.format(MODULE))

    return True