# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/SafeRun.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 16717 bytes
WINDOWS_BATCH_KEYWORDS = [
 'ECHO', 'ASSOC', 'ATTRIB ', 'BREAK ', 'BCDEDIT', 'CACLS', 'CALL', 'CD', 'CHCP', 'CHDIR', 'CHKDSK', 'CHKNTFS', 'CLS', 'CMD', 'COLOR', 'COMP', 'COMPACT', 'CONVERT', 'COPY', 'DATE', 'DEL', 'DIR', 'DISKCOMP', 'DISKCOPY', 'DISKPART', 'DOSKEY', 'DRIVERQUERY', 'ECHO', 'ENDLOCAL', 'ERASE', 'EXIT', 'FC', 'FIND', 'FINDSTR', 'FOR', 'FORMAT', 'FSUTIL', 'FTYPE', 'GOTO', 'GPRESULT', 'GRAFTABL', 'HELP', 'ICACLS', 'IF', 'LABEL', 'MD', 'MKDIR', 'MKLINK', 'MODE', 'MORE', 'MOVE', 'OPENFILES', 'PATH', 'PAUSE', 'POPD', 'PRINT', 'PROMPT', 'PUSHD', 'RD', 'RECOVER', 'REM', 'REN', 'RENAME', 'REPLACE', 'RMDIR', 'ROBOCOPY', 'SET', 'SETLOCAL', 'SC', 'SCHTASKS', 'SHIFT', 'SHUTDOWN', 'SORT', 'START', 'SUBST', 'SYSTEMINFO', 'TASKLIST', 'TASKKILL', 'TIME', 'TITLE', 'TREE', 'TYPE', 'VER', 'VERIFY', 'VOL', 'XCOPY', 'WMIC']
LINUX_BACH_KEYWORDS = [
 'SOURCE', 'UNALIAS', 'ULIMIT', 'TYPESET', 'TYPE', 'READARRAY', 'READ', 'MAPFILE', 'LOGOUT', 'LOCAL', 'LET', 'ENABLE', 'DECLARE', 'COMMAND', 'CALLER', 'BUILTIN', 'BIND', 'ALIAS', 'ECHO']
import subprocess, signal, select
try:
    from signal import SIGPIPE, SIG_DFL
except:
    pass

from threading import Thread
import sys, os, logging, shlex
from string import Template
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from HdlLib.Utilities.Timer import *
from HdlLib.Utilities.Misc import cd
import HdlLib.Utilities
if sys.platform.startswith('win'):
    OS = 'win'
else:
    OS = 'lin'

def SetParam(Line, Vars={}):
    """
        Try to set parameter from line (format: "Variable = Value").
        return False if failure, True if success. 
        """
    Line = Template(Line)
    Vars.update(os.environ)
    Line = Line.safe_substitute(Vars)
    SplittedLine = Line.split('=', 1)
    if len(SplittedLine) != 2:
        return
    else:
        if len(SplittedLine[0].split()) > 1:
            return
        SplittedLine = [x.strip('\n').strip('\r').strip() for x in SplittedLine]
        Key = SplittedLine[0]
        if SplittedLine[1].count('"') > 2:
            try:
                Vars[Key] = eval(SplittedLine[1])
            except:
                logging.error("Unable to compute expression '{0}'.".format(SplittedLine[1]))
                return

        else:
            SplittedLine = [' '.join(shlex.split(x, comments=True)) for x in SplittedLine]
            Vars[Key] = SplittedLine[1].strip('"').strip('\n').strip('\r').strip()
        try:
            Vars[Key] = eval(Vars[Key])
        except:
            pass

        logging.debug("New variable '{0}'='{1}'".format(Key, Vars[Key]))
        return True


def SafeRun(CaseInsensitive, CommandFiles, Quiet=False, NoLogFile=False):
    """
        Safe command execution dedicated to testbench et QA 
        Argument: 
                CommandFiles: list of path to command files 
        """
    ASafeCheckOS()
    LocalParam = {}
    returnCode = 0
    CURRENTPATH = os.path.abspath('./')
    if len(CommandFiles) > 0 and isinstance(CommandFiles[0], list):
        CommandFiles = CommandFiles[0]
    for CommandFile in CommandFiles:
        logging.debug("Command file: '{0}'".format(CommandFile))
        if not os.path.isfile(CommandFile):
            logging.error("No such command file '{0}'.".format(os.path.abspath(CommandFile)))
            return 1
        with open(CommandFile) as (CmdFile):
            for Line in CmdFile.readlines():
                if SetParam(Line, LocalParam):
                    LocalParam.update(LocalParam)
                else:
                    RawCmd = Line.strip('\n').strip('\r').strip()
                    Cmd = Template(RawCmd)
                    Cmd = Cmd.safe_substitute(LocalParam)
                    if len(Cmd) > 1 and Cmd[0] != '#':
                        logging.debug('----------------')
                        returnCode, log = Execute(Cmd=Cmd, LogDirectory=CURRENTPATH, CaseInsensitive=CaseInsensitive, Quiet=Quiet, NoLogFile=NoLogFile)
                    else:
                        returnCode, log = (0, 'Comment')
                        continue
                    logging.debug('returnCode = ' + str(returnCode))
                    if returnCode != 0:
                        logging.error('RUN FAILED')
                        FilesBaseName = os.path.join(CURRENTPATH, os.path.basename(Cmd.split()[0]))
                        if NoLogFile is False:
                            logging.error("Read log files for more details: \n   > '{0}'\n   > '{1}'".format(FilesBaseName + '.log', FilesBaseName + '.errorlog'))
                        return returnCode

    logging.debug('Run succeeded.')
    return returnCode


def ASafeCheckOS():
    """
        Check os compatibility
        """
    if os.name == 'nt':
        pass
    else:
        if os.name == 'posix':
            pass
        else:
            sys.exit('OS not supported by this program.')


def Execute(Cmd, LogDirectory='./', CaseInsensitive=False, Quiet=False, NoLogFile=False):
    """
        Move to command file directory, then execute listed commands.
        """
    logging.debug("Execute command : '" + Cmd + "'")
    for fileName in os.listdir(LogDirectory):
        if fileName.endswith('.log') or fileName.endswith('.errorlog'):
            os.remove(os.path.join(LogDirectory, fileName))

    CmdArgList = shlex.split(Cmd, posix=False, comments=True)
    HdlLib.Utilities.Executable = os.path.expanduser(os.path.normpath(CmdArgList[0])).replace('\\', '/')
    LogFileName = os.path.join(LogDirectory, os.path.basename(HdlLib.Utilities.Executable) + '.log')
    logErrorFileName = os.path.join(LogDirectory, os.path.basename(HdlLib.Utilities.Executable) + '.errorlog')
    if OS == 'lin':
        PATHLIST = os.environ['PATH'].split(':')
    else:
        if OS == 'win':
            PATHLIST = os.environ['Path'].split(';')
            logging.debug("'Path' env var content = '{0}'".format(PATHLIST))
        else:
            PATHLIST = []
        FoundExec = False
        if not os.path.isfile(HdlLib.Utilities.Executable):
            if OS == 'win':
                for Path in PATHLIST:
                    if not os.path.isdir(Path):
                        pass
                    else:
                        if CaseInsensitive:
                            ExecName = HdlLib.Utilities.Executable.lower()
                        else:
                            ExecName = HdlLib.Utilities.Executable
                        for Exe in [ExecName, ExecName + '.exe']:
                            if Exe in [x.lower() for x in os.listdir(Path)]:
                                FoundExec = True
                                break

                        if FoundExec:
                            break

            else:
                for Path in PATHLIST:
                    if not os.path.isdir(Path):
                        pass
                    elif HdlLib.Utilities.Executable in os.listdir(Path):
                        FoundExec = True
                        break

        else:
            FoundExec = True
            HdlLib.Utilities.Executable = os.path.abspath(HdlLib.Utilities.Executable)
            CmdArgList[0] = HdlLib.Utilities.Executable
    if NoLogFile is False:
        LogFile = open(LogFileName, 'a+')
        ErrorLogFile = open(logErrorFileName, 'a+')
    FoundExec or logging.debug("Executable '{0}' not in $PATH.".format(HdlLib.Utilities.Executable))
    if OS == 'win':
        if HdlLib.Utilities.Executable.upper() not in WINDOWS_BATCH_KEYWORDS:
            errorLogString = "Unable to launch command '{0}': Executable '{1}' not found.".format(Cmd, HdlLib.Utilities.Executable)
            logging.error(errorLogString)
            LogFile.write(errorLogString)
            ErrorLogFile.write(errorLogString)
            return (
             1, errorLogString)
        logging.debug("Command use Windows batch keyword '{0}'".format(HdlLib.Utilities.Executable.upper()))
    else:
        if OS == 'lin':
            if HdlLib.Utilities.Executable.upper() not in LINUX_BACH_KEYWORDS:
                errorLogString = "Unable to launch command '{0}': Executable '{1}' not found.".format(Cmd, HdlLib.Utilities.Executable)
                logging.error(errorLogString)
                LogFile.write(errorLogString)
                ErrorLogFile.write(errorLogString)
                return (
                 1, errorLogString)
            logging.debug("Command use Linux bash keyword '{0}'".format(HdlLib.Utilities.Executable.upper()))
            FoundBash = False
            for Path in PATHLIST:
                if not os.path.isdir(Path):
                    pass
                elif 'bash' in os.listdir(Path):
                    FoundBash = True
                    NewCmd = Cmd.replace(HdlLib.Utilities.Executable, '')
                    HdlLib.Utilities.Executable = os.path.join(Path, 'bash') + ' -c "' + HdlLib.Utilities.Executable
                    NewCmd = HdlLib.Utilities.Executable + ' ' + NewCmd.strip() + '"'
                    logging.debug('NewCmd:' + NewCmd)
                    CmdArgList = shlex.split(NewCmd, comments=True)

            if not FoundBash:
                errorLogString = "Unable to launch command '{0}': bash keyword '{1}' cannot be executed without a bash command (which was not found in PATH environment variable).".format(Cmd, HdlLib.Utilities.Executable)
                logging.error(errorLogString)
                LogFile.write("Unable to launch command '{0}': bash keyword '{1}' cannot be executed without a bash command (which was not found in PATH environment variable).")
                ErrorLogFile.write("Unable to launch command '{0}': bash keyword '{1}' cannot be executed without a bash command (which was not found in PATH environment variable).")
                return (
                 1, errorLogString)
            logging.debug("Launch command: '{0}'".format(' '.join(CmdArgList)))
            if NoLogFile is False:
                LogFile.flush()
                ErrorLogFile.flush()
            with Timer() as (t):
                with SubprocessLogger(ExecName=HdlLib.Utilities.Executable):
                    if OS == 'win':
                        HdlLib.Utilities.CurrentProcess = subprocess.Popen(CmdArgList, shell=True, stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:
                        HdlLib.Utilities.CurrentProcess = subprocess.Popen(CmdArgList, shell=False, stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=lambda : signal.signal(SIGPIPE, SIG_DFL))
                    if NoLogFile is False:
                        if OS == 'win':
                            PollSubprocess_Win(HdlLib.Utilities.CurrentProcess, LogFile, ErrorLogFile, Quiet=Quiet)
                        else:
                            PollSubprocess(HdlLib.Utilities.CurrentProcess, LogFile, ErrorLogFile, Quiet=Quiet)
                    else:
                        if OS == 'win':
                            PollSubprocess_Win(HdlLib.Utilities.CurrentProcess, LogFile, ErrorLogFile, Quiet=Quiet)
                        else:
                            PollSubprocess(HdlLib.Utilities.CurrentProcess, None, None, Quiet=Quiet)
                    HdlLib.Utilities.CurrentProcess.wait()
            returncode = HdlLib.Utilities.CurrentProcess.returncode
            logging.debug('Execution time in (secs): %.3f' % t.elapsed_secs)
            if NoLogFile is False:
                if returncode != 0:
                    LogFile.seek(0, os.SEEK_SET)
                    LogString = LogFile.read()
                LogFile.close()
                ErrorLogFile.close()
                if returncode == 0:
                    os.remove(LogFileName)
                    os.remove(logErrorFileName)
                    return (0, '')
                else:
                    return (
                     returncode, LogString)
        else:
            return (
             returncode, None)


def PollSubprocess(CurrentProcess, LogFile, ErrorLogFile, Quiet=False):
    """
        Poll stdout and stderr of a given subprocess.
        """
    if LogFile:
        LogFile.seek(0, os.SEEK_END)
    if ErrorLogFile:
        ErrorLogFile.seek(0, os.SEEK_END)
    poll = select.poll()
    poll.register(CurrentProcess.stdout, select.POLLIN | select.POLLHUP)
    poll.register(CurrentProcess.stderr, select.POLLIN | select.POLLHUP)
    pollc = 2
    events = poll.poll()
    while pollc > 0 and len(events) > 0:
        for event in events:
            rfd, event = event
            if event & select.POLLIN:
                if rfd == CurrentProcess.stdout.fileno():
                    Line = CurrentProcess.stdout.readline().decode('utf-8')
                    if len(Line) > 0:
                        if LogFile:
                            LogFile.write(Line)
                        if not Quiet:
                            sys.stdout.write(Line)
                if rfd == CurrentProcess.stderr.fileno():
                    Line = CurrentProcess.stderr.readline().decode('utf-8')
                    if len(Line) > 0:
                        if LogFile:
                            LogFile.write(Line)
                        if ErrorLogFile:
                            ErrorLogFile.write(Line)
                        if not Quiet:
                            sys.stderr.write(Line)
                        if event & select.POLLHUP:
                            poll.unregister(rfd)
                            pollc = pollc - 1
                        if pollc > 0:
                            events = poll.poll()


def PollSubprocess_Win(CurrentProcess, LogFile, ErrorLogFile, Quiet=False):
    """
        Poll stdout and stderr of a given subprocess.
        """

    def LogStream(Stream, Type):
        while 1:
            Out = Stream.readline()
            if Out:
                Line = (Out.rstrip() + '\n').decode('utf-8')
                if Type == 'stderr':
                    if LogFile:
                        LogFile.write(Line)
                    if ErrorLogFile:
                        ErrorLogFile.write(Line)
                    if not Quiet:
                        sys.stderr.write(Line)
                elif Type == 'stdout':
                    if LogFile:
                        LogFile.write(Line)
                    if not Quiet:
                        sys.stdout.write(Line)
                    else:
                        break

    stdout_thread = Thread(target=LogStream, args=(
     CurrentProcess.stdout, 'stdout'))
    stderr_thread = Thread(target=LogStream, args=(
     CurrentProcess.stderr, 'stderr'))
    stdout_thread.start()
    stderr_thread.start()
    while stdout_thread.isAlive() and stderr_thread.isAlive():
        pass

    Thread.join(stdout_thread)
    Thread.join(stderr_thread)


class SubprocessLogger:
    __doc__ = '\n\tChange logging format for subprocess call.\n\t'
    OriFormatter = '%(message)s'
    RootHandler = None

    def __init__(self, ExecName='Subprocess'):
        self.ExecName = ExecName

    def __enter__(self):
        self.RootHandler = logging.getLogger().handlers[0]
        self.OriFormatter = self.RootHandler.formatter
        self.RootHandler.setFormatter(logging.Formatter('[{0}] > %(message)s'.format(self.ExecName)))

    def __exit__(self, type, value, traceback):
        self.RootHandler.setFormatter(self.OriFormatter)