# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/Misc.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 4709 bytes
import contextlib, sys, os, re, logging, platform, fileinput, glob, types, shutil
from HdlLib.Utilities import RemoteOperations
if sys.maxsize > 4294967296:
    ARCHI = '64'
else:
    ARCHI = '32'
if sys.platform.startswith('win'):
    OS = 'win'
    OS_CLASS = 'windows'
    OS_FULL_NAME = platform.platform()
else:
    OS = 'lin'
    OS_CLASS = 'linux'
    OS_FULL_NAME = '_'.join(platform.linux_distribution() + (ARCHI,))

class SyntheSysError(Exception):

    def __init__(self, Message='SyntheSys Error'):
        self.Message = Message

    def __str__(self):
        return repr(self.Message)


def GetSysInfo():
    global ARCHI
    global OS
    global OS_CLASS
    global OS_FULL_NAME
    return (
     ARCHI, OS, OS_CLASS, OS_FULL_NAME)


class DummyFile(object):

    def write(self, x):
        pass


@contextlib.contextmanager
def Silence(FD):
    SavedFD = FD
    FD = DummyFile()
    yield
    FD = SavedFD


class cd:
    __doc__ = '\n\tContext manager for changing the current working directory\n\t'

    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def ReplaceTextInFile(FileName, OldText, NewText):
    Found = False
    if not os.path.exists(FileName):
        raise NameError('File <{0}> cannot be found'.format(FileName))
    else:
        for line in fileinput.input(FileName, inplace=True):
            if line.count(OldText):
                Found = True
                line = line.replace(OldText, NewText)
            sys.stdout.write(line)

    return Found


def IterFiles(SearchPaths=[], Name='*.ini'):
    """
        Generator that yield each configuration files found in specified directories.
        """
    for SearchPath in SearchPaths:
        for Root, Dirs, Files in os.walk(SearchPath, topdown=True):
            Template = os.path.join(Root, Name)
            MatchedFiles = glob.glob(Template)
            for FileName in MatchedFiles:
                yield os.path.join(Root, FileName)


def ListModules(ModName):
    try:
        Module = __import__(ModName, globals(), locals(), [ModName.split('.')[(-1)]])
    except ImportError:
        return

    print(ModName)
    for Name in dir(Module):
        if type(getattr(Module, Name)) == types.ModuleType:
            ListModules('.'.join([ModName, Name]))


def IndentationLevel(Line, TabSize=4):
    """
        return the indentation level of specified line.
        """
    LineX = Line.expandtabs(TabSize)
    if LineX.isspace():
        return 0
    else:
        return int((len(LineX) - len(LineX.lstrip())) / TabSize)


def NaturalSort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def CleanTempFiles(Path, Host=None):
    """
        Test environment variable 'SYNTHESYS_KEEP_ALL' and remove specified folder if value is 'true'.
        """
    if 'SYNTHESYS_KEEP_ALL' in os.environ:
        if os.environ['SYNTHESYS_KEEP_ALL'].lower() == 'true':
            logging.info("The 'SYNTHESYS_KEEP_ALL' environment variable is set. Do not remove the '{0}' folder.".format(OutputPath))
        else:
            if Host is None:
                shutil.rmtree(Path)
            else:
                R = RemoteOperations()
                R.RemoteRun(Command='rm -rf {Path}'.format(Path=Path), abort_on_prompts='True', warn_only=True)
    else:
        if Host is None:
            shutil.rmtree(Path)
        else:
            R = RemoteOperations()
            R.RemoteRun(Command='rm -rf {Path}'.format(Path=Path), abort_on_prompts='True', warn_only=True)