# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/shell.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 4448 bytes
import atexit, os
import pocsuite3.lib.core as readline
from pocsuite3.lib.core.data import logger
from pocsuite3.lib.core.data import paths
from pocsuite3.lib.core.enums import AUTOCOMPLETE_TYPE
from pocsuite3.lib.core.enums import OS
from pocsuite3.lib.core.settings import MAX_HISTORY_LENGTH
try:
    import rlcompleter

    class CompleterNG(rlcompleter.Completer):

        def global_matches(self, text):
            """
            Compute matches when text is a simple name.
            Return a list of all names currently defined in self.namespace
            that match.
            """
            matches = []
            n = len(text)
            for ns in (self.namespace,):
                for word in ns:
                    if word[:n] == text:
                        matches.append(word)

            return matches


except Exception:
    readline._readline = None

def readline_available():
    """
    Check if the readline is available. By default
    it is not in Python default installation on Windows
    """
    return readline._readline is not None


def clear_history():
    if not readline_available():
        return
    readline.clear_history()


def save_history(completion=None):
    if not readline_available():
        return
    elif completion == AUTOCOMPLETE_TYPE.SQL:
        history_path = paths.SQL_SHELL_HISTORY
    else:
        if completion == AUTOCOMPLETE_TYPE.OS:
            history_path = paths.OS_SHELL_HISTORY
        else:
            if completion == AUTOCOMPLETE_TYPE.API:
                history_path = paths.API_SHELL_HISTORY
            else:
                if completion == AUTOCOMPLETE_TYPE.CONSOLE:
                    history_path = paths.POCSUITE_CONSOLE_HISTORY
                else:
                    history_path = paths.POCSUITE_SHELL_HISTORY
    try:
        with open(history_path, 'w+'):
            pass
    except Exception:
        pass

    readline.set_history_length(MAX_HISTORY_LENGTH)
    try:
        readline.write_history_file(history_path)
    except IOError as msg:
        try:
            warn_msg = "there was a problem writing the history file '{0}' ({1})".format(history_path, msg)
            logger.warn(warn_msg)
        finally:
            msg = None
            del msg


def load_history(completion=None):
    if not readline_available():
        return
    else:
        clear_history()
        if completion == AUTOCOMPLETE_TYPE.SQL:
            history_path = paths.SQL_SHELL_HISTORY
        else:
            if completion == AUTOCOMPLETE_TYPE.OS:
                history_path = paths.OS_SHELL_HISTORY
            else:
                if completion == AUTOCOMPLETE_TYPE.API:
                    history_path = paths.API_SHELL_HISTORY
                else:
                    if completion == AUTOCOMPLETE_TYPE.CONSOLE:
                        history_path = paths.POCSUITE_CONSOLE_HISTORY
                    else:
                        history_path = paths.POCSUITE_SHELL_HISTORY
    if os.path.exists(history_path):
        try:
            readline.read_history_file(history_path)
        except IOError as msg:
            try:
                warn_msg = "there was a problem loading the history file '{0}' ({1})".format(history_path, msg)
                logger.warn(warn_msg)
            finally:
                msg = None
                del msg


def auto_completion(completion=None, os=None, commands=None, console=None):
    if not readline_available():
        return
    elif completion == AUTOCOMPLETE_TYPE.OS:
        if os == OS.WINDOWS:
            completer = CompleterNG({'copy':None, 
             'del':None,  'dir':None,  'echo':None, 
             'md':None,  'mem':None,  'move':None, 
             'net':None,  'netstat -na':None,  'ver':None, 
             'xcopy':None,  'whoami':None})
        else:
            completer = CompleterNG({'cp':None, 
             'rm':None,  'ls':None,  'echo':None, 
             'mkdir':None,  'free':None,  'mv':None, 
             'ifconfig':None,  'netstat -natu':None,  'pwd':None, 
             'uname':None,  'id':None,  'whoami':None})
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
    else:
        if commands:
            completer = CompleterNG(dict(((_, None) for _ in commands)))
            readline.set_completer_delims(' ')
            readline.set_completer(completer.complete)
            readline.parse_and_bind('tab: complete')
        else:
            if console:
                readline.set_completer_delims(' ')
                readline.set_completer(console)
                readline.parse_and_bind('tab: complete')
    load_history(completion)
    atexit.register(save_history, completion)